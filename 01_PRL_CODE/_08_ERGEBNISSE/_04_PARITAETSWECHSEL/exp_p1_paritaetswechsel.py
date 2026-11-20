"""EXP-P1: Optimale Messzeit und Decoder unter Paritätswechsel am Arbeitspunkt omega_stat = 11.99 (Etappe 6).

Spezifikation: 02_FORSCHUNGSDOKUMENTATION/_03_EXPERIMENTE/EXP-P1_Paritaetswechsel_Messzeit.md (vorab registriert).
Aufruf aus 01_PRL_CODE:  python -B -u -m _08_ERGEBNISSE._04_PARITAETSWECHSEL.exp_p1_paritaetswechsel [--probe]
--probe: kleiner Funktionstest (wenige Records, kurzes T), schreibt nach 10_Raw_Outputs/11_Processed_Outputs mit Präfix PROBE-P1.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import asdict

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import messkanal_rwa
from _02_AUSFUEHRUNG.paritaetswechsel import (log_likelihood_quotient_mit_wechsel, mittelwert_record_mit_wechsel,
                                             trajektorien_mit_wechsel)
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel
from _04_AUSWERTUNG_DIAGNOSTIK import decoder
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest
from _08_ERGEBNISSE._02_ENDLICHE_MESSZEIT.exp_e1_endliche_messzeit import CUTOFF, ETA, _modell

E2 = "EXP-E2_20261109T205736Z"
BUDGET, OMEGA = 0.3, 11.99
EINHEITEN_PRO_US = 1000.0 * 2 * math.pi * 0.2          # 1 µs in 1/lambda0 (lambda0 = h 0.2 GHz) = 1256.6
LEBENSDAUERN_US = (math.inf, 1000.0, 100.0, 15.0, 5.0)
T_WERTE = (500.0, 1000.0, 2500.0, 5000.0, 7500.0, 10000.0)
DT, BIN, NTRAJ, PROZ, BLOCK = 0.2, 2, 2000, 6, 200
SEED_BASIS = 6000
DECODER = ("mf_nom", "mf_gamma", "bc", "bayes")


def _arbeitspunkt(omega=OMEGA):
    with (PROJEKT_ROOT / "11_Processed_Outputs" / E2 / f"gauss_scan_n{BUDGET}.csv").open(encoding="utf-8") as h:
        for z in csv.DictReader(h):
            if abs(float(z["omega"]) - omega) < 1e-9:
                return {k: float(v) for k, v in z.items()}
    raise KeyError(omega)


def _gewichte(k, gamma, T_max, dtb):
    zeiten = np.arange(0.0, T_max + 1e-9, 0.5)
    mu = {z: mittelwert_record_mit_wechsel(k[1], k[-1], gamma, z, zeiten) for z in (1, -1)}
    mitten = (np.arange(int(round(T_max / dtb))) + 0.5) * dtb
    return np.interp(mitten, zeiten, mu[1] - mu[-1])


def _scores(dY, w_nom, w_gam, checks):
    """Lineare Decoder-Scores je Checkpunkt: dict decoder -> (n, len(checks))."""
    starts = [0] + list(checks[:-1])                   # Segmentsummen statt voller kumulierter Kopien (Speicher)
    aus = {}
    for name, w in (("mf_nom", w_nom), ("mf_gamma", w_gam), ("bc", None)):
        x = dY[:, :checks[-1]] if w is None else dY[:, :checks[-1]] * w[None, :checks[-1]]
        aus[name] = np.cumsum(np.add.reduceat(x, starts, axis=1), axis=1)
    return aus


def punkt(m, ap, lebensdauer_us, seed, T_werte, ntraj, omega=OMEGA):
    gamma = 0.0 if math.isinf(lebensdauer_us) else 1.0 / (lebensdauer_us * EINHEITEN_PRO_US)
    nc = CUTOFF[BUDGET]
    k = {z: messkanal_rwa(buendel(m, omega, ap["I0"], nc, paritaet=z), eta=ETA, theta=ap["theta"])[0] for z in (1, -1)}
    T_max, dtb = max(T_werte), DT * BIN
    checks = [int(round(T / dtb)) for T in T_werte]
    w_nom = _gewichte(k, 0.0, T_max, dtb)
    w_gam = w_nom if gamma == 0.0 else _gewichte(k, gamma, T_max, dtb)

    def satz(seed_satz):
        """Records je Startparität -> lineare Scores, LLR, Paritätsdiagnose (dY wird danach verworfen)."""
        aus = {}
        for z in (1, -1):
            r = trajektorien_mit_wechsel(k[1], k[-1], gamma_qp=gamma, start=z, T=T_max, dt=DT, ntraj=ntraj,
                                         seed=seed_satz + z, bin_schritte=BIN, block=BLOCK, prozesse=PROZ)
            sc = _scores(r.dY_bins, w_nom, w_gam, checks)
            sc["bayes"] = log_likelihood_quotient_mit_wechsel(k[1], k[-1], gamma, r.dY_bins, dtb, checkpunkte=checks,
                                                              block=BLOCK, prozesse=PROZ)
            gekippt = np.stack([np.any(r.paritaet_bins[:, :n] != z, axis=1) for n in checks], axis=1)
            aus[z] = (sc, gekippt, r.paritaet_bins[:, -1] != z)
            del r
        return aus

    kal, test = satz(seed + 1), satz(seed + 11)
    zeilen = []
    tstern = {}
    for name in DECODER:
        kal_fehler, schwellen = [], []
        for i in range(len(T_werte)):
            if name == "bayes":
                s = decoder.Schwelle(0.0, True)
            else:
                s = decoder.kalibriere_schwelle(kal[1][0][name][:, i], kal[-1][0][name][:, i])
            schwellen.append(s)
            kal_fehler.append(decoder.bewerte(kal[1][0][name][:, i], kal[-1][0][name][:, i], s).p_err)
        i_best = int(np.argmin(kal_fehler))              # bei Gleichstand das kürzere T (erstes Minimum)
        tstern[name] = T_werte[i_best]
        for i, T in enumerate(T_werte):
            fr = decoder.bewerte(test[1][0][name][:, i], test[-1][0][name][:, i], schwellen[i])
            # Diagnose: Fehler getrennt nach Trajektorien mit/ohne Wechsel bis T
            diag = {}
            for teil, maske_fn in (("ohne", lambda g: ~g), ("mit", lambda g: g)):
                falsch, anzahl = 0, 0
                for z in (1, -1):
                    sc = test[z][0][name][:, i]
                    maske = maske_fn(test[z][1][:, i])
                    vorhersage_plus = (sc > schwellen[i].wert) if schwellen[i].plus_oben else (sc < schwellen[i].wert)
                    richtig = vorhersage_plus if z == 1 else ~vorhersage_plus
                    falsch += int(np.sum(~richtig & maske)); anzahl += int(np.sum(maske))
                diag[f"p_{teil}_wechsel"] = falsch / anzahl if anzahl else float("nan")
                diag[f"n_{teil}_wechsel"] = anzahl
            zeilen.append({"lebensdauer_us": lebensdauer_us, "gamma_qp": gamma, "T": T, "T_us": T / EINHEITEN_PRO_US,
                           "decoder": name, "p_test": fr.p_err, "lo": fr.ci_unten, "hi": fr.ci_oben,
                           "p_kal": kal_fehler[i], "T_stern": tstern[name], **diag})
    # Gültigkeit: LLR-Mittel zur wahren Parität; Anteil gekippter Testtrajektorien bei T_max
    llr_mittel = {z: float(np.mean(test[z][0]["bayes"][:, -1])) for z in (1, -1)}
    gekippt_ende = float(np.mean(np.concatenate([test[z][2] for z in (1, -1)])))
    erwartet = 0.5 * (1 - math.exp(-2 * gamma * T_max))
    gepaart = []
    for i in range(len(T_werte)):
        d = []
        for z in (1, -1):
            b_falsch = z * test[z][0]["bayes"][:, i] < 0
            s = decoder.kalibriere_schwelle(kal[1][0]["bc"][:, i], kal[-1][0]["bc"][:, i])
            sc = test[z][0]["bc"][:, i]
            vp = (sc > s.wert) if s.plus_oben else (sc < s.wert)
            bc_falsch = ~vp if z == 1 else vp
            d.append(b_falsch.astype(float) - bc_falsch.astype(float))
        d = np.concatenate(d)
        gepaart.append(float(d.mean() / (d.std(ddof=1) / math.sqrt(d.size))) if d.std() > 0 else 0.0)
    gueltig = {"llr_mittel": llr_mittel, "llr_zur_wahren_paritaet": bool(llr_mittel[1] > 0 > llr_mittel[-1]),
               "gekippt_ende": gekippt_ende, "gekippt_erwartet": erwartet,
               "gekippt_z": (gekippt_ende - erwartet) / math.sqrt(max(erwartet * (1 - erwartet), 1e-12) / (2 * ntraj)),
               "bayes_minus_boxcar_z": gepaart, "T_stern": tstern}
    return zeilen, gueltig


def main() -> int:
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("--probe", action="store_true")
    args = ap_.parse_args()
    if args.probe:
        praefix, lebensdauern, T_werte, ntraj = "PROBE-P1", (math.inf, 0.2), (100.0, 200.0, 400.0), 100
    else:
        praefix, lebensdauern, T_werte, ntraj = "EXP-P1", LEBENSDAUERN_US, T_WERTE, NTRAJ
    lauf_id = neue_lauf_id(praefix)
    roh, aus = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id, PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True); aus.mkdir(parents=True, exist_ok=True)
    ap = _arbeitspunkt()
    m = _modell()
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": praefix, "quelle_e2": E2, "budget": BUDGET, "omega": OMEGA,
                            "lebensdauern_us": [str(x) for x in lebensdauern], "einheiten_pro_us": EINHEITEN_PRO_US,
                            "T_werte": T_werte, "dt": DT, "bin": BIN, "ntraj": ntraj, "eta": ETA, "seed_basis": SEED_BASIS,
                            "cutoff": CUTOFF[BUDGET], "I0": ap["I0"], "theta": ap["theta"], "modell": asdict(m)})
    alle, gueltigkeit = [], {}
    for j, ld in enumerate(lebensdauern):
        t0 = time.time()
        zeilen, g = punkt(m, ap, ld, SEED_BASIS + 100 * j, T_werte, ntraj)
        alle += zeilen
        gueltigkeit[str(ld)] = g
        with (aus / "exp_p1.csv").open("w", newline="", encoding="utf-8") as h:       # Zwischenstand nach jedem Punkt
            wtr = csv.DictWriter(h, fieldnames=list(alle[0].keys())); wtr.writeheader(); wtr.writerows(alle)
        (aus / "gueltigkeit.json").write_text(json.dumps(gueltigkeit, indent=2), encoding="utf-8")
        print(f"lebensdauer {ld} us: {time.time() - t0:.0f} s, T*={g['T_stern']}, llr={g['llr_mittel']}", flush=True)
    print("Ausgabe:", aus)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
