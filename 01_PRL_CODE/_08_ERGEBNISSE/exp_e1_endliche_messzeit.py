"""EXP-E1: stationär gewählter vs. endlichzeit-optimaler Arbeitspunkt (Spezifikation im Experimentordner).

Aufruf aus 01_PRL_CODE:  python -B -m _08_ERGEBNISSE.exp_e1_endliche_messzeit [--nur-gauss]
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
from dataclasses import asdict, replace

os.environ.setdefault("MPLBACKEND", "Agg")
import matplotlib.pyplot as plt
import numpy as np
import qutip as qt
from scipy.optimize import brentq

from _02_AUSFUEHRUNG.homodyn_trajektorien import messkanal_rwa, mittelwert_record, trajektorien
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark
from _04_AUSWERTUNG_DIAGNOSTIK import decoder
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest

ETA = 0.5
OMEGAS = np.round(np.arange(11.80, 12.2001, 0.01), 4)
BUDGETS = (0.01, 0.3)
T_WERTE = (25.0, 50.0, 100.0, 200.0, 400.0)
T_MAX = max(T_WERTE)
DT_MW = 0.5                    # Zeitgitter Mittelwert-Records
CUTOFF = {0.01: 5, 0.3: 8}
NTRAJ = 2000
DT_TRAJ = 0.2
BIN = 5


def _modell():
    return modell_stark("gewoehnlich")


def _steady_a(m, omega, I0, z, nc):
    b = buendel(m, omega, I0, nc, paritaet=z)
    kanal, ops = messkanal_rwa(b, eta=ETA, theta=0.0)
    rho = qt.steadystate(kanal.H, list(kanal.unbeobachtet) + [kanal.beobachtet], method="direct")
    return complex(qt.expect(ops.a, rho))


def _n_max(m, omega, I0, nc, zeiten):
    werte = []
    for z in (1, -1):
        kanal, ops = messkanal_rwa(buendel(m, omega, I0, nc, paritaet=z), eta=ETA, theta=0.0)
        res = qt.mesolve(kanal.H, kanal.rho0, zeiten, c_ops=list(kanal.unbeobachtet) + [kanal.beobachtet],
                         e_ops=[ops.n_res], options={"atol": 1e-10, "rtol": 1e-8, "nsteps": 10 ** 6})
        werte.append(float(np.max(np.real(res.expect[0]))))
    return max(werte)


def kalibriere_I0(m, omega, budget, nc, zeiten) -> float:
    n_th = _n_max(m, omega, 0.0 + 1e-14, nc, zeiten)       # thermischer Untergrund (I0 -> 0)
    ziel = budget + n_th
    f = lambda logI: _n_max(m, omega, 10 ** logI, nc, zeiten) - ziel
    return 10 ** brentq(f, -8, 1, xtol=1e-4)


def gauss_scan(m, budget):
    nc = CUTOFF[budget]
    zeiten = np.arange(0.0, T_MAX + 1e-9, DT_MW)
    zeilen, mus = [], {}
    for omega in OMEGAS:
        I0 = kalibriere_I0(m, float(omega), budget, nc, zeiten)
        a_p = _steady_a(m, float(omega), I0, 1, nc)
        a_m = _steady_a(m, float(omega), I0, -1, nc)
        theta = float(np.angle(a_p - a_m))
        mu = {}
        for z in (1, -1):
            kanal, _ = messkanal_rwa(buendel(m, float(omega), I0, nc, paritaet=z), eta=ETA, theta=theta)
            mu[z] = mittelwert_record(kanal, zeiten)
        d_ss = (2 * math.sqrt(ETA * m.kappa_out) * abs(a_p - a_m)) ** 2
        diff = 0.5 * ((mu[1] - mu[-1])[1:] + (mu[1] - mu[-1])[:-1])
        snr2 = np.concatenate([[0.0], np.cumsum(diff ** 2) * DT_MW])
        p_g = {T: 0.5 * math.erfc(math.sqrt(snr2[int(round(T / DT_MW))]) / (2 * math.sqrt(2))) for T in T_WERTE}
        zeilen.append({"omega": float(omega), "I0": I0, "theta": theta, "D_ss": d_ss,
                       **{f"P_G_T{int(T)}": p for T, p in p_g.items()}})
        mus[float(omega)] = (mu[1], mu[-1], I0, theta)
    return zeilen, mus, zeiten


def trajektorien_vergleich(m, budget, omega, I0, theta, T, mu_p, mu_m, zeiten, seed, dt=DT_TRAJ):
    nc = CUTOFF[budget]
    n_bins = int(round(T / (dt * BIN)))
    # Gewichte: Mittelwert-Records auf Bin-Mitten interpoliert
    mitten = (np.arange(n_bins) + 0.5) * dt * BIN
    w = np.interp(mitten, zeiten, mu_p - mu_m)
    scores = {}
    for z, s_off in ((1, 0), (-1, 1)):
        kanal, ops = messkanal_rwa(buendel(m, omega, I0, nc, paritaet=z), eta=ETA, theta=theta)
        kal = trajektorien(kanal, T=T, dt=dt, ntraj=NTRAJ, seed=seed + 10 * s_off, bin_schritte=BIN).dY_bins
        test = trajektorien(kanal, T=T, dt=dt, ntraj=NTRAJ, seed=seed + 10 * s_off + 5, bin_schritte=BIN).dY_bins
        scores[z] = {"mf_kal": decoder.matched_filter(kal, w, n_bins), "mf_test": decoder.matched_filter(test, w, n_bins),
                     "bc_kal": decoder.boxcar(kal, n_bins), "bc_test": decoder.boxcar(test, n_bins)}
    out = {}
    for name in ("mf", "bc"):
        s = decoder.kalibriere_schwelle(scores[1][f"{name}_kal"], scores[-1][f"{name}_kal"])
        fr = decoder.bewerte(scores[1][f"{name}_test"], scores[-1][f"{name}_test"], s)
        out[name] = asdict(fr)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--nur-gauss", action="store_true")
    parser.add_argument("--experiment", default="EXP-E1")
    parser.add_argument("--t-werte", type=float, nargs="+", default=None)
    args = parser.parse_args()
    global T_WERTE, T_MAX
    if args.t_werte:
        T_WERTE = tuple(args.t_werte); T_MAX = max(T_WERTE)
    lauf_id = neue_lauf_id(args.experiment)
    roh, aus = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id, PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True); aus.mkdir(parents=True, exist_ok=True)
    m = _modell()
    ergebnis = {}
    fig, axes = plt.subplots(len(BUDGETS), 2, figsize=(11, 4 * len(BUDGETS)))
    for k, budget in enumerate(BUDGETS):
        zeilen, mus, zeiten = gauss_scan(m, budget)
        with (aus / f"gauss_scan_n{budget}.csv").open("w", newline="", encoding="utf-8") as h:
            wtr = csv.DictWriter(h, fieldnames=list(zeilen[0].keys())); wtr.writeheader(); wtr.writerows(zeilen)
        om = np.array([z["omega"] for z in zeilen]); dss = np.array([z["D_ss"] for z in zeilen])
        omega_stat = float(om[np.argmax(dss)])
        regret = {}
        for T in T_WERTE:
            p = np.array([z[f"P_G_T{int(T)}"] for z in zeilen])
            omega_T = float(om[np.argmin(p)])
            regret[T] = {"omega_T": omega_T, "P_G_stat": float(p[np.argmax(dss)]), "P_G_opt": float(p.min()),
                         "regret": float(p[np.argmax(dss)] - p.min())}
            axes[k, 1].plot(om, p, label=f"T={int(T)}")
        axes[k, 0].plot(om, dss / dss.max(), "k"); axes[k, 0].axvline(omega_stat, color="r", ls="--")
        axes[k, 0].set_title(f"n*={budget}: stationäre Trennrate (normiert)"); axes[k, 0].set_xlabel(r"$\omega/\lambda_0$")
        axes[k, 1].axvline(omega_stat, color="r", ls="--"); axes[k, 1].set_yscale("log")
        axes[k, 1].set_title(f"n*={budget}: Gauß-Benchmark $P_G(T)$, η={ETA}"); axes[k, 1].legend(fontsize=7)
        axes[k, 1].set_xlabel(r"$\omega/\lambda_0$")
        ergebnis[str(budget)] = {"omega_stat": omega_stat, "regret_gauss": {str(int(T)): v for T, v in regret.items()}}
        if not args.nur_gauss:
            T_star = max(T_WERTE, key=lambda T: regret[T]["regret"])
            traj = {}
            for label, omega in (("stat", omega_stat), ("opt", regret[T_star]["omega_T"])):
                mu_p, mu_m, I0, theta = mus[omega]
                traj[label] = {"omega": omega, "T": T_star,
                               "P_G": float([z for z in zeilen if z["omega"] == omega][0][f"P_G_T{int(T_star)}"]),
                               **trajektorien_vergleich(m, budget, omega, I0, theta, T_star, mu_p, mu_m, zeiten, seed=1000 + k)}
            ergebnis[str(budget)]["trajektorien"] = traj
        print(json.dumps(ergebnis[str(budget)], indent=1))
    fig.tight_layout(); fig.savefig(aus / "exp_e1_scan.png", dpi=150); plt.close(fig)
    (aus / "ergebnis.json").write_text(json.dumps(ergebnis, indent=2), encoding="utf-8")
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": args.experiment, "eta": ETA, "omegas": OMEGAS.tolist(),
                            "budgets": BUDGETS, "T_werte": T_WERTE, "cutoff": {str(k): v for k, v in CUTOFF.items()},
                            "ntraj": NTRAJ, "dt_traj": DT_TRAJ, "modell": asdict(_modell()), "nur_gauss": args.nur_gauss})
    print("Ausgabe:", aus)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
