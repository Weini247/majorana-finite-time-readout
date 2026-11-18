"""EXP-E2 Stufe 1b: Trajektorien-Kontrollpunkte für die Gültigkeit des Gauß-Benchmarks bei langem T.

Vorab registriert in 02_FORSCHUNGSDOKUMENTATION/_03_EXPERIMENTE/EXP-E2_Mikrosekunden_Messzeit.md
(Abschnitt „Kontrollpunkte"). Arbeitspunkte (ω_stat, I0, θ) werden unverändert aus dem EXP-E2-Lauf übernommen.

Aufruf aus 01_PRL_CODE:  python -B -u -m _08_ERGEBNISSE.exp_e2_kontrollpunkt --e2-lauf EXP-E2_<zeitstempel>
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import asdict

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import messkanal_rwa, mittelwert_record, trajektorien
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel
from _04_AUSWERTUNG_DIAGNOSTIK import decoder
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest
from _08_ERGEBNISSE.exp_e1_endliche_messzeit import CUTOFF, DT_MW, ETA, _modell

NTRAJ = 2000
BIN_ZEIT = 5.0                       # Binbreite in λ0^-1 (unabhängig von dt)
# (Budget, T, dt) — Reihenfolge = Priorität; dt-Halbierung bei T = 1000.
# n̄* = 0.3 (Cutoff 8, d = 16) kostet ~10x mehr pro Zeitschritt als n̄* = 0.01 (d = 10, Superoperator-Pfad),
# daher dort T = 2500 statt 10^4 (Laufzeitmessung 2026-11-10: d = 16, T = 100 ≈ 330 s unter Last).
KONTROLLPUNKTE = ((0.01, 10000.0, 0.2), (0.3, 2500.0, 0.2), (0.3, 1000.0, 0.2), (0.3, 1000.0, 0.1))


def _arbeitspunkt(e2_dir, budget):
    with (e2_dir / f"gauss_scan_n{budget}.csv").open(encoding="utf-8") as h:
        zeilen = [{k: float(v) for k, v in z.items()} for z in csv.DictReader(h)]
    z = max(zeilen, key=lambda r: r["D_ss"])
    return z


def kontrollpunkt(m, budget, T, dt, ap, seed):
    nc = CUTOFF[budget]
    omega, I0, theta = ap["omega"], ap["I0"], ap["theta"]
    zeiten = np.arange(0.0, T + 1e-9, DT_MW)
    mu = {}
    for z in (1, -1):
        kanal, _ = messkanal_rwa(buendel(m, omega, I0, nc, paritaet=z), eta=ETA, theta=theta)
        mu[z] = mittelwert_record(kanal, zeiten)
    bin_schritte = int(round(BIN_ZEIT / dt))
    n_bins = int(round(T / BIN_ZEIT))
    mitten = (np.arange(n_bins) + 0.5) * BIN_ZEIT
    mu_p_bin, mu_m_bin = np.interp(mitten, zeiten, mu[1]), np.interp(mitten, zeiten, mu[-1])
    w = mu_p_bin - mu_m_bin
    p_gauss_bin = float(decoder.gauss_vorhersage(mu_p_bin, mu_m_bin, BIN_ZEIT)[-1])
    scores = {}
    for z, s_off in ((1, 0), (-1, 1)):
        kanal, _ = messkanal_rwa(buendel(m, omega, I0, nc, paritaet=z), eta=ETA, theta=theta)
        kal = trajektorien(kanal, T=T, dt=dt, ntraj=NTRAJ, seed=seed + 10 * s_off, bin_schritte=bin_schritte).dY_bins
        test = trajektorien(kanal, T=T, dt=dt, ntraj=NTRAJ, seed=seed + 10 * s_off + 5, bin_schritte=bin_schritte).dY_bins
        scores[z] = {"mf_kal": decoder.matched_filter(kal, w, n_bins), "mf_test": decoder.matched_filter(test, w, n_bins),
                     "bc_kal": decoder.boxcar(kal, n_bins), "bc_test": decoder.boxcar(test, n_bins)}
        del kal, test
    out = {"budget": budget, "T": T, "dt": dt, "omega": omega, "I0": I0, "theta": theta, "cutoff": nc,
           "P_G_scan": ap.get(f"P_G_T{int(T)}"), "P_G_bin": p_gauss_bin}
    for name in ("mf", "bc"):
        s = decoder.kalibriere_schwelle(scores[1][f"{name}_kal"], scores[-1][f"{name}_kal"])
        fr = decoder.bewerte(scores[1][f"{name}_test"], scores[-1][f"{name}_test"], s)
        out[name] = asdict(fr)
    out["gauss_im_wilson_mf"] = bool(out["mf"]["ci_unten"] <= p_gauss_bin <= out["mf"]["ci_oben"])
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--e2-lauf", required=True)
    args = parser.parse_args()
    e2_dir = PROJEKT_ROOT / "11_Processed_Outputs" / args.e2_lauf
    lauf_id = neue_lauf_id("EXP-E2K")
    roh, aus = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id, PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True); aus.mkdir(parents=True, exist_ok=True)
    m = _modell()
    ergebnisse = []
    for i, (budget, T, dt) in enumerate(KONTROLLPUNKTE):
        t0 = time.time()
        r = kontrollpunkt(m, budget, T, dt, _arbeitspunkt(e2_dir, budget), seed=2000 + 100 * i)
        r["rechenzeit_s"] = round(time.time() - t0, 1)
        ergebnisse.append(r)
        print(json.dumps(r, indent=1), flush=True)
        (aus / "ergebnis.json").write_text(json.dumps(ergebnisse, indent=2), encoding="utf-8")   # Zwischenstand
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": "EXP-E2K", "quelle_e2": args.e2_lauf, "eta": ETA,
                            "kontrollpunkte": KONTROLLPUNKTE, "ntraj": NTRAJ, "bin_zeit": BIN_ZEIT,
                            "cutoff": {str(k): v for k, v in CUTOFF.items()}, "modell": asdict(_modell())})
    print("Ausgabe:", aus)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
