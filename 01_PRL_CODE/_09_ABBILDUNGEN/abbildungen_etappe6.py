"""Abbildung Etappe 6: Fehlerrate über Messzeit je Paritätslebensdauer und Decoder (EXP-P1, omega = 11.99).

Aufruf aus 01_PRL_CODE:  python -B -m _09_ABBILDUNGEN.abbildungen_etappe6
"""
from __future__ import annotations

import csv
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT

LAUF = "EXP-P1_20261118T152412Z"
NAMEN = {"mf_nom": "MF (nominal)", "mf_gamma": "MF (with Γ)", "bc": "Boxcar", "bayes": "Bayes (Wonham)"}
TITEL = {"inf": "no parity switching", "1000.0": "τ = 1 ms", "100.0": "τ = 100 µs", "15.0": "τ = 15 µs", "5.0": "τ = 5 µs"}


def main() -> int:
    daten = defaultdict(lambda: defaultdict(list))
    with (PROJEKT_ROOT / "11_Processed_Outputs" / LAUF / "exp_p1.csv").open(encoding="utf-8") as h:
        for z in csv.DictReader(h):
            daten[z["lebensdauer_us"]][z["decoder"]].append(
                (float(z["T_us"]), float(z["p_test"]), float(z["lo"]), float(z["hi"])))
    fig, achsen = plt.subplots(1, 5, figsize=(17, 3.6), sharey=True)
    for ax, ld in zip(achsen, TITEL):
        for dec, name in NAMEN.items():
            pts = sorted(daten[ld][dec])
            x = [p[0] for p in pts]; y = [p[1] for p in pts]
            ax.errorbar(x, y, yerr=[[p[1] - p[2] for p in pts], [p[3] - p[1] for p in pts]],
                        marker="o", ms=3, capsize=2, lw=1.2, label=name)
        ax.set_yscale("log"); ax.set_title(TITEL[ld]); ax.set_xlabel("measurement time T (µs)")
        ax.grid(alpha=0.3, which="both")
    achsen[0].set_ylabel("error rate (test, 95 % Wilson)")
    achsen[0].legend(fontsize=8, loc="lower left")
    fig.suptitle("Parity readout under quasiparticle poisoning, ω = 11.99 (EXP-P1)", y=1.02)
    ziel = PROJEKT_ROOT / "abbildungen" / "paritaetswechsel_messzeit.png"
    fig.savefig(ziel, dpi=150, bbox_inches="tight")
    print(ziel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
