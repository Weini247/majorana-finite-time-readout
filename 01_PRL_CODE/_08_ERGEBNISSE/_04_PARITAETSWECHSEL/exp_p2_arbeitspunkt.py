"""EXP-P2: Verschiebt sich der fehlerminimale Arbeitspunkt omega unter Paritätswechsel? (Etappe 6, Q-6C)

Spezifikation: 02_FORSCHUNGSDOKUMENTATION/_03_EXPERIMENTE/EXP-P2_Arbeitspunkt_Paritaetswechsel.md (vorab registriert).
Referenz omega = 11.99 aus EXP-P1 (gleiche Lebensdauern, gleiches Protokoll); hier nur die Nachbarpunkte 11.97 und 12.01.
Aufruf aus 01_PRL_CODE:  python -B -u -m _08_ERGEBNISSE._04_PARITAETSWECHSEL.exp_p2_arbeitspunkt [--probe]
"""
from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import asdict

from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest
from _08_ERGEBNISSE._02_ENDLICHE_MESSZEIT.exp_e1_endliche_messzeit import CUTOFF, ETA, _modell
from _08_ERGEBNISSE._04_PARITAETSWECHSEL.exp_p1_paritaetswechsel import (BUDGET, DT, BIN, E2, EINHEITEN_PRO_US, NTRAJ,
                                                                         T_WERTE, _arbeitspunkt, punkt)

OMEGAS = (11.97, 12.01)
LEBENSDAUERN_US = (15.0, 5.0)
SEED_BASIS = 7000


def main() -> int:
    ap_ = argparse.ArgumentParser()
    ap_.add_argument("--probe", action="store_true")
    args = ap_.parse_args()
    if args.probe:
        praefix, omegas, lebensdauern, T_werte, ntraj = "PROBE-P2", (11.97,), (0.2,), (100.0, 200.0, 400.0), 100
    else:
        praefix, omegas, lebensdauern, T_werte, ntraj = "EXP-P2", OMEGAS, LEBENSDAUERN_US, T_WERTE, NTRAJ
    lauf_id = neue_lauf_id(praefix)
    roh, aus = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id, PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True); aus.mkdir(parents=True, exist_ok=True)
    m = _modell()
    aps = {w: _arbeitspunkt(w) for w in omegas}
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": praefix, "quelle_e2": E2, "budget": BUDGET,
                            "omegas": list(omegas), "lebensdauern_us": list(lebensdauern),
                            "einheiten_pro_us": EINHEITEN_PRO_US, "T_werte": T_werte, "dt": DT, "bin": BIN,
                            "ntraj": ntraj, "eta": ETA, "seed_basis": SEED_BASIS, "cutoff": CUTOFF[BUDGET],
                            "arbeitspunkte": {str(w): {"I0": a["I0"], "theta": a["theta"]} for w, a in aps.items()},
                            "modell": asdict(m)})
    alle, gueltigkeit = [], {}
    for i, w in enumerate(omegas):
        for j, ld in enumerate(lebensdauern):
            t0 = time.time()
            zeilen, g = punkt(m, aps[w], ld, SEED_BASIS + 1000 * i + 100 * j, T_werte, ntraj, omega=w)
            alle += [{"omega": w, **z} for z in zeilen]
            gueltigkeit[f"{w}|{ld}"] = g
            with (aus / "exp_p2.csv").open("w", newline="", encoding="utf-8") as h:   # Zwischenstand nach jedem Punkt
                wtr = csv.DictWriter(h, fieldnames=list(alle[0].keys())); wtr.writeheader(); wtr.writerows(alle)
            (aus / "gueltigkeit.json").write_text(json.dumps(gueltigkeit, indent=2), encoding="utf-8")
            print(f"omega {w}, lebensdauer {ld} us: {time.time() - t0:.0f} s, T*={g['T_stern']}, llr={g['llr_mittel']}",
                  flush=True)
    print("Ausgabe:", aus)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
