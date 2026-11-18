"""Abbildungen für die README aus den committeten Ergebnis-CSVs (keine Simulation).

Aufruf aus 01_PRL_CODE:  python -B -m _09_ABBILDUNGEN.abbildungen_readme
Ausgabe: <Repo>/abbildungen/*.png
"""
from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "11_Processed_Outputs"
ZIEL = REPO / "abbildungen"

E2 = OUT / "EXP-E2_20261109T205736Z" / "gauss_scan_n0.3.csv"
E2K = OUT / "EXP-E2K_20261110T000043Z" / "ergebnis.json"
E3 = OUT / "EXP-E3_20261117T194320Z" / "exp_e3.csv"
E4 = OUT / "EXP-E4_20261111T002220Z" / "exp_e4_n0.3.csv"

NS_PRO_EINHEIT = 1.0 / (2 * math.pi * 0.2)  # 1/λ0 mit λ0 = h·0.2 GHz ⇒ ≈ 0.796 ns
OMEGA_STAT = 11.99

# neutrale, in hell und dunkel lesbare Farben
FARBEN = {"gauss": "#7f7f7f", "mf": "#1f77b4", "bc": "#2ca02c", "bayes": "#d62728"}

plt.rcParams.update({
    "figure.dpi": 100, "savefig.dpi": 170, "font.size": 10,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.3,
    "savefig.facecolor": "white", "savefig.bbox": "tight",
})


def lies_csv(pfad: Path) -> list[dict[str, float | str]]:
    with pfad.open(newline="", encoding="utf-8") as f:
        zeilen = list(csv.DictReader(f))
    out = []
    for z in zeilen:
        d = {}
        for k, v in z.items():
            try:
                d[k] = float(v)
            except ValueError:
                d[k] = v
        out.append(d)
    return out


def abbildung_fehlerrate_ueber_omega() -> Path:
    zeilen = lies_csv(E3)
    fig, achsen = plt.subplots(1, 2, figsize=(9, 3.6), sharey=False)
    for ax, T in zip(achsen, (2500.0, 5000.0)):
        z = sorted((r for r in zeilen if r["T"] == T), key=lambda r: r["omega"])
        om = [r["omega"] for r in z]
        ax.plot(om, [r["P_G"] for r in z], "--", color=FARBEN["gauss"], label="Gaussian benchmark")
        for schluessel, name, versatz, marker in (("mf", "Matched filter", -0.0025, "o"),
                                                    ("bc", "Boxcar", 0.0, "s"),
                                                    ("bayes", "Bayesian filter", 0.0025, "D")):
            p = [r[f"{schluessel}_p"] for r in z]
            fehler = [[r[f"{schluessel}_p"] - r[f"{schluessel}_lo"] for r in z],
                      [r[f"{schluessel}_hi"] - r[f"{schluessel}_p"] for r in z]]
            ax.errorbar([o + versatz for o in om], p, yerr=fehler, fmt=marker, ms=4, capsize=2,
                        color=FARBEN[schluessel], label=name)
        ax.axvline(OMEGA_STAT, color="black", lw=0.8, alpha=0.5)
        ax.set_title(f"T = {T * NS_PRO_EINHEIT / 1000:.1f} µs")
        ax.set_xlabel(r"Drive frequency $\omega$ ($\lambda_0$)")
        ax.set_xticks(om)
    achsen[0].set_ylabel("Single-shot error rate")
    for ax in achsen:
        ax.text(OMEGA_STAT + 0.001, 0.97, r"$\omega_\mathrm{stat}$", transform=ax.get_xaxis_transform(),
                ha="left", va="top", fontsize=9)
    achsen[1].legend(frameon=False, fontsize=8, loc="center right")
    fig.suptitle("Error rate vs. drive frequency (trajectories, 2000 test records/point, Wilson 95 %)",
                 fontsize=10)
    pfad = ZIEL / "fehlerrate_ueber_omega.png"
    fig.savefig(pfad)
    plt.close(fig)
    return pfad


def abbildung_fehlerrate_ueber_messzeit() -> Path:
    gauss = lies_csv(E2)
    Ts = (400, 1000, 2500, 5000, 10000)
    fig, ax = plt.subplots(figsize=(6, 3.8))
    for omega, stil in ((11.95, ":"), (11.97, "-."), (OMEGA_STAT, "-")):
        zeile = min(gauss, key=lambda r: abs(r["omega"] - omega))
        ax.plot([T * NS_PRO_EINHEIT / 1000 for T in Ts], [zeile[f"P_G_T{T}"] for T in Ts], stil,
                color=FARBEN["gauss"] if omega != OMEGA_STAT else "black",
                label=f"Gaussian, ω = {omega:.2f}")
    # Trajektorien-Kontrollpunkte bei ω_stat
    e2k = [p for p in json.loads(E2K.read_text(encoding="utf-8"))
           if p["budget"] == 0.3 and abs(p["omega"] - OMEGA_STAT) < 1e-9]
    if e2k:
        x = [p["T"] * NS_PRO_EINHEIT / 1000 for p in e2k]
        y = [p["mf"]["p_err"] for p in e2k]
        yerr = [[p["mf"]["p_err"] - p["mf"]["ci_unten"] for p in e2k],
                [p["mf"]["ci_oben"] - p["mf"]["p_err"] for p in e2k]]
        ax.errorbar(x, y, yerr=yerr, fmt="o", ms=4, capsize=2, color=FARBEN["mf"],
                    label="Matched filter, trajectories (EXP-E2K)")
    e3 = [r for r in lies_csv(E3) if abs(r["omega"] - OMEGA_STAT) < 1e-9]
    x = [r["T"] * NS_PRO_EINHEIT / 1000 * 1.04 for r in e3]
    ax.errorbar(x, [r["bayes_p"] for r in e3],
                yerr=[[r["bayes_p"] - r["bayes_lo"] for r in e3], [r["bayes_hi"] - r["bayes_p"] for r in e3]],
                fmt="D", ms=4, capsize=2, color=FARBEN["bayes"], label="Bayesian filter, trajectories (EXP-E3)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ticks = [0.3, 0.5, 1, 2, 4, 8]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{t:g}" for t in ticks])
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_xlabel("Measurement time T (µs)")
    ax.set_ylabel("Single-shot error rate")
    ax.set_title(r"Error rate vs. measurement time ($\bar n^* = 0.3$, $\eta = 0.5$)", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    pfad = ZIEL / "fehlerrate_ueber_messzeit.png"
    fig.savefig(pfad)
    plt.close(fig)
    return pfad


def abbildung_robustheit() -> Path:
    zeilen = [r for r in lies_csv(E4) if r["T"] == 2500.0]
    nach_omega: dict[float, dict[str, float]] = defaultdict(dict)
    for r in zeilen:
        nach_omega[r["omega"]][r["abweichung"]] = r["P_fest"]
    om = sorted(o for o in nach_omega if 11.90 <= o <= 12.08)
    nominal = [nach_omega[o]["nominal"] for o in om]
    schlimmst = [max(nach_omega[o].values()) for o in om]
    mittel = [sum(nach_omega[o].values()) / len(nach_omega[o]) for o in om]
    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(om, nominal, "-", color="black", label="Nominal parameters")
    ax.plot(om, mittel, "--", color=FARBEN["mf"], label="Mean over miscalibrations")
    ax.plot(om, schlimmst, "-", color=FARBEN["bayes"], label="Worst case over miscalibrations")
    for kurve, farbe in ((nominal, "black"), (mittel, FARBEN["mf"]), (schlimmst, FARBEN["bayes"])):
        i = min(range(len(om)), key=lambda k: kurve[k])
        ax.plot(om[i], kurve[i], "o", color=farbe, ms=5)
    ax.axvline(OMEGA_STAT, color="black", lw=0.8, alpha=0.5)
    ax.set_xlabel(r"Drive frequency $\omega$ ($\lambda_0$), calibrated on the nominal model")
    ax.set_ylabel("Error rate (Gaussian benchmark)")
    ax.set_title(r"Robustness: $\varphi\pm0.1/0.2$, $t_1\times0.95/1.05$, $\kappa\times0.8/1.2$"
                 f"  (T = {2500 * NS_PRO_EINHEIT / 1000:.1f} µs)", fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    pfad = ZIEL / "robustheit.png"
    fig.savefig(pfad)
    plt.close(fig)
    return pfad


def main() -> None:
    ZIEL.mkdir(exist_ok=True)
    for f in (abbildung_fehlerrate_ueber_omega, abbildung_fehlerrate_ueber_messzeit, abbildung_robustheit):
        print(f().relative_to(REPO))


if __name__ == "__main__":
    main()
