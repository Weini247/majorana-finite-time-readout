"""Pilot für EXP-E3 (nur Design: Binbreite des Bayes-Filters, Laufzeit, Effektgröße) — kein Ergebnisclaim.

Punkt: n̄* = 0.3, ω_stat, T = 2500 (EXP-E2K-Punkt mit Gauß-Abweichung). Decoder: Matched Filter, Boxcar
(Schwelle auf Kalibrierdaten), Bayes-LLR mit Schwelle 0 bei Binbreiten 0.2 / 0.4 / 1.0.
Aufruf aus 01_PRL_CODE:  python -B -u -m _08_ERGEBNISSE._03_BAYES_ROBUSTHEIT.pilot_e3_bayes
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import log_likelihood_quotient, messkanal_rwa, mittelwert_record, trajektorien
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel
from _04_AUSWERTUNG_DIAGNOSTIK import decoder
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest
from _08_ERGEBNISSE._02_ENDLICHE_MESSZEIT.exp_e1_endliche_messzeit import CUTOFF, ETA, _modell
from _08_ERGEBNISSE._02_ENDLICHE_MESSZEIT.exp_e2_kontrollpunkt import _arbeitspunkt

E2 = "EXP-E2_20261109T205736Z"
BUDGET, T, DT, NTRAJ, PROZ = 0.3, 2500.0, 0.2, 2000, 6


def main() -> int:
    lauf_id = neue_lauf_id("PILOT-E3")
    roh, aus = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id, PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True); aus.mkdir(parents=True, exist_ok=True)
    m = _modell(); ap = _arbeitspunkt(PROJEKT_ROOT / "11_Processed_Outputs" / E2, BUDGET)
    nc = CUTOFF[BUDGET]
    k = {z: messkanal_rwa(buendel(m, ap["omega"], ap["I0"], nc, paritaet=z), eta=ETA, theta=ap["theta"])[0] for z in (1, -1)}
    t0 = time.time()
    kal = {z: trajektorien(k[z], T=T, dt=DT, ntraj=NTRAJ, seed=500 + z, bin_schritte=1, block=200, prozesse=PROZ).dY_bins for z in (1, -1)}
    test = {z: trajektorien(k[z], T=T, dt=DT, ntraj=NTRAJ, seed=600 + z, bin_schritte=1, block=200, prozesse=PROZ).dY_bins for z in (1, -1)}
    erg = {"punkt": {"omega": ap["omega"], "I0": ap["I0"], "theta": ap["theta"], "T": T, "P_G_scan": ap[f"P_G_T{int(T)}"]},
           "t_simulation_s": round(time.time() - t0, 1)}
    # Matched Filter / Boxcar auf Binbreite 1.0
    zeiten = np.arange(0.0, T + 1e-9, 0.5)
    mu = {z: mittelwert_record(k[z], zeiten) for z in (1, -1)}
    zus = lambda r, b: r.reshape(r.shape[0], -1, b).sum(axis=2)
    nb = int(T)
    w = np.interp(np.arange(nb) + 0.5, zeiten, mu[1] - mu[-1])
    for name, f in (("mf", lambda r: decoder.matched_filter(zus(r, 5), w, nb)), ("bc", lambda r: decoder.boxcar(r, r.shape[1]))):
        s = decoder.kalibriere_schwelle(f(kal[1]), f(kal[-1]))
        erg[name] = asdict(decoder.bewerte(f(test[1]), f(test[-1]), s))
    for b in (5, 2, 1):
        t1 = time.time()
        llr = {z: log_likelihood_quotient(k[1], k[-1], zus(test[z], b), DT * b, block=200, prozesse=PROZ)[:, 0] for z in (1, -1)}
        erg[f"bayes_bin{DT * b:.1f}"] = {**asdict(decoder.bewerte(llr[1], llr[-1], decoder.Schwelle(0.0, True))),
                                         "t_s": round(time.time() - t1, 1)}
        print(json.dumps(erg, indent=1), flush=True)
        (aus / "ergebnis.json").write_text(json.dumps(erg, indent=2), encoding="utf-8")
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": "PILOT-E3", "quelle_e2": E2, "budget": BUDGET, "T": T,
                            "dt": DT, "ntraj": NTRAJ, "eta": ETA, "cutoff": nc, "modell": asdict(m)})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
