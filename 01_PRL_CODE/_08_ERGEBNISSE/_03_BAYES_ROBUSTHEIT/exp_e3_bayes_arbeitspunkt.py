"""EXP-E3: Arbeitspunktwahl unter echter Messstatistik (Bayes-Filter, Matched Filter, Boxcar) bei n̄* = 0.3.

Spezifikation: 02_FORSCHUNGSDOKUMENTATION/_03_EXPERIMENTE/EXP-E3_Bayes_Arbeitspunkt.md (vorab registriert).
Aufruf aus 01_PRL_CODE:  python -B -u -m _08_ERGEBNISSE._03_BAYES_ROBUSTHEIT.exp_e3_bayes_arbeitspunkt
"""
from __future__ import annotations

import csv
import json
import time
from dataclasses import asdict

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import log_likelihood_quotient, messkanal_rwa, mittelwert_record, trajektorien
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel
from _04_AUSWERTUNG_DIAGNOSTIK import decoder
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest
from _08_ERGEBNISSE._02_ENDLICHE_MESSZEIT.exp_e1_endliche_messzeit import CUTOFF, ETA, _modell

E2 = "EXP-E2_20261109T205736Z"
BUDGET = 0.3
OMEGAS = (11.95, 11.97, 11.99, 12.01, 12.03)
T_WERTE = (2500.0, 5000.0)
DT, BIN, NTRAJ, PROZ = 0.2, 2, 2000, 6          # Binbreite 0.4 (Pilot: konvergiert gegenüber 0.2)


def _zeile(omega):
    with (PROJEKT_ROOT / "11_Processed_Outputs" / E2 / f"gauss_scan_n{BUDGET}.csv").open(encoding="utf-8") as h:
        for z in csv.DictReader(h):
            if abs(float(z["omega"]) - omega) < 1e-9:
                return {k: float(v) for k, v in z.items()}
    raise KeyError(omega)


def punkt(m, omega, seed):
    ap = _zeile(omega)
    nc = CUTOFF[BUDGET]
    k = {z: messkanal_rwa(buendel(m, omega, ap["I0"], nc, paritaet=z), eta=ETA, theta=ap["theta"])[0] for z in (1, -1)}
    T_max, dtb = max(T_WERTE), DT * BIN
    kal = {z: trajektorien(k[z], T=T_max, dt=DT, ntraj=NTRAJ, seed=seed + 1 + z, bin_schritte=BIN, block=200, prozesse=PROZ).dY_bins
           for z in (1, -1)}
    test = {z: trajektorien(k[z], T=T_max, dt=DT, ntraj=NTRAJ, seed=seed + 11 + z, bin_schritte=BIN, block=200, prozesse=PROZ).dY_bins
            for z in (1, -1)}
    zeiten = np.arange(0.0, T_max + 1e-9, 0.5)
    mu = {z: mittelwert_record(k[z], zeiten) for z in (1, -1)}
    nb_max = int(round(T_max / dtb))
    w = np.interp((np.arange(nb_max) + 0.5) * dtb, zeiten, mu[1] - mu[-1])
    checks = [int(round(T / dtb)) for T in T_WERTE]
    llr = {z: log_likelihood_quotient(k[1], k[-1], test[z], dtb, checkpunkte=checks, block=200, prozesse=PROZ) for z in (1, -1)}
    out = []
    for i, T in enumerate(T_WERTE):
        n = checks[i]
        r = {"omega": omega, "T": T, "I0": ap["I0"], "theta": ap["theta"], "D_ss": ap["D_ss"], "P_G": ap[f"P_G_T{int(T)}"]}
        for name, f in (("mf", lambda x: decoder.matched_filter(x, w, n)), ("bc", lambda x: decoder.boxcar(x, n))):
            s = decoder.kalibriere_schwelle(f(kal[1]), f(kal[-1]))
            fr = decoder.bewerte(f(test[1]), f(test[-1]), s)
            r.update({f"{name}_p": fr.p_err, f"{name}_lo": fr.ci_unten, f"{name}_hi": fr.ci_oben})
        fr = decoder.bewerte(llr[1][:, i], llr[-1][:, i], decoder.Schwelle(0.0, True))
        r.update({"bayes_p": fr.p_err, "bayes_lo": fr.ci_unten, "bayes_hi": fr.ci_oben})
        out.append(r)
    return out


def main() -> int:
    lauf_id = neue_lauf_id("EXP-E3")
    roh, aus = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id, PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True); aus.mkdir(parents=True, exist_ok=True)
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": "EXP-E3", "quelle_e2": E2, "budget": BUDGET, "omegas": OMEGAS,
                            "T_werte": T_WERTE, "dt": DT, "bin": BIN, "ntraj": NTRAJ, "eta": ETA,
                            "cutoff": CUTOFF[BUDGET], "modell": asdict(_modell())})
    m = _modell(); zeilen = []
    for j, omega in enumerate(OMEGAS):
        t0 = time.time()
        zeilen += punkt(m, omega, seed=5000 + 100 * j)
        with (aus / "exp_e3.csv").open("w", newline="", encoding="utf-8") as h:     # Zwischenstand nach jedem ω, vor jeder Ausgabe
            wtr = csv.DictWriter(h, fieldnames=list(zeilen[0].keys())); wtr.writeheader(); wtr.writerows(zeilen)
        print(f"omega = {omega}: {time.time() - t0:.0f} s", json.dumps(zeilen[-len(T_WERTE):]), flush=True)   # nur ASCII (cp1252-Konsole)
    print("Ausgabe:", aus)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
