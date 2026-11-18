"""EXP-R1: Reproduktionsvergleich Benjadi & Egger (2026) Fig. 3(a), 3(c), 3(e), 3(g).

Schreibt Rohdaten + Manifest nach 10_Raw_Outputs/<lauf_id>/ und Abbildungen + Kennzahlen nach
11_Processed_Outputs/<lauf_id>/. Aufruf aus 01_PRL_CODE:
    python -B -m _08_ERGEBNISSE.reproduktion_fig3
"""
from __future__ import annotations

import csv
import math
import os
from dataclasses import asdict

os.environ.setdefault("MPLBACKEND", "Agg")
import matplotlib.pyplot as plt
import numpy as np

from _01_GRUNDLAGEN_FORMELN import semiklassik as sk
from _01_GRUNDLAGEN_FORMELN.abgeleitete_groessen import abgeleitete_groessen
from _01_GRUNDLAGEN_FORMELN.einheiten import ghz_nach_lambda0
from _02_AUSFUEHRUNG.fall_ausfuehrung import rechne_fall
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_schwach, modell_stark
from _05_INFRASTRUKTUR.konfiguration.config import AntriebsParameter
from _05_INFRASTRUKTUR.referenzdaten.zenodo_benjadi_egger import ZITATION, lade_referenzdatei
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT, neue_lauf_id, schreibe_manifest

KONVENTION = "gewoehnlich"        # D-1.1, Begründung: semiklassische Phase fig3a (siehe Befund F-1.1)
I0_LINEAR = 1.0e-6
CUTOFF = 12


def _semikl(modell, x_ghz, formel):
    return np.array([formel(modell, abgeleitete_groessen(modell, AntriebsParameter(ghz_nach_lambda0(x), 1.0), 1))
                     for x in x_ghz])


def _exakt_amplitude(modell, x_ghz):
    return np.array([rechne_fall(buendel(modell, ghz_nach_lambda0(x), I0_LINEAR, CUTOFF)).A_ref for x in x_ghz])


def _fig3c_eigene(modell, x_werte, variante: str):
    """Fehlermaße vs. Delta_z. x interpretiert als Delta_z in GHz (Variante *_ghz) oder in lambda0."""
    zeilen = []
    for x in x_werte:
        dz = ghz_nach_lambda0(x) if variante.endswith("ghz") else x
        if variante.startswith("omega"):
            omega = 12.0 - dz                                   # 2 omega_z = 12 fest
            b = buendel(modell, omega, I0_LINEAR, CUTOFF)
        else:                                                   # omega = omega0 fest, omega_z über epsilon
            omega_z = 0.5 * (modell.omega0 + dz)
            eps = math.sqrt(max(omega_z ** 2 - 36.0, 0.0))
            from dataclasses import replace
            b = buendel(replace(modell, epsilon=eps), modell.omega0, I0_LINEAR, CUTOFF)
        r = rechne_fall(b)
        zeilen.append((x, r.eps_a_tau_z, r.eps_a_tau_z_gegen_semikl, r.eps_A, r.eps_phi))
    return np.array(zeilen)


def main() -> int:
    lauf_id = neue_lauf_id("EXP-R1")
    roh = PROJEKT_ROOT / "10_Raw_Outputs" / lauf_id
    aus = PROJEKT_ROOT / "11_Processed_Outputs" / lauf_id
    roh.mkdir(parents=True, exist_ok=True)
    aus.mkdir(parents=True, exist_ok=True)
    stark, schwach = modell_stark(KONVENTION), modell_schwach(KONVENTION)
    kennzahlen: list[dict] = []
    eingaben = {}

    # --- Fig. 3(a) und 3(e): |A|^2 und arg A
    for name, modell, formel in (("fig3a.dat", stark, sk.amplitude_semiklassisch_stark),
                                 ("fig3e.dat", schwach, sk.amplitude_semiklassisch_schwach)):
        ref = lade_referenzdatei(name)
        eingaben[name] = ref.sha256
        x = ref.daten[:, 0]
        A_sc = _semikl(modell, x, formel)
        A_ex = _exakt_amplitude(modell, x)
        np.savez(roh / f"{name[:-4]}_eigene.npz", x_ghz=x, A_semikl=A_sc, A_exakt_rwa=A_ex)
        for spalte, eigene, label in ((1, np.abs(A_sc) ** 2, "|A_sc|^2"), (3, np.angle(A_sc), "arg A_sc"),
                                      (2, np.abs(A_ex) ** 2, "|A_ex|^2 (RWA, lineare Antwort)"),
                                      (4, np.angle(A_ex), "arg A_ex (RWA, lineare Antwort)")):
            r = ref.daten[:, spalte]
            abw = np.abs(eigene - r)
            kennzahlen.append({"datei": name, "spalte": spalte + 1, "groesse": label,
                               "max_abs_abw": float(abw.max()), "skala": float(np.abs(r).max()),
                               "max_abw_rel_skala": float(abw.max() / np.abs(r).max())})
        fig, ax = plt.subplots(2, 2, figsize=(10, 6), sharex=True)
        ax[0, 0].plot(x, ref.daten[:, 1], "k-", label="Ref. semikl.")
        ax[0, 0].plot(x, np.abs(A_sc) ** 2, "r--", label="eigene semikl.")
        ax[0, 0].plot(x, ref.daten[:, 2], "b-", label="Ref. exakt")
        ax[0, 0].plot(x, np.abs(A_ex) ** 2, "c--", label="eigene exakt (RWA)")
        ax[0, 0].set_ylabel(r"$|A_\omega|^2$"); ax[0, 0].legend(fontsize=7)
        ax[0, 1].plot(x, ref.daten[:, 3], "k-"); ax[0, 1].plot(x, np.angle(A_sc), "r--")
        ax[0, 1].plot(x, ref.daten[:, 4], "b-"); ax[0, 1].plot(x, np.angle(A_ex), "c--")
        ax[0, 1].set_ylabel(r"arg $A_\omega$")
        ax[1, 0].semilogy(x, np.abs(np.abs(A_sc) ** 2 - ref.daten[:, 1]) + 1e-16, "r", label="semikl.")
        ax[1, 0].semilogy(x, np.abs(np.abs(A_ex) ** 2 - ref.daten[:, 2]) + 1e-16, "c", label="exakt")
        ax[1, 0].set_ylabel("Residuum |A|^2"); ax[1, 0].legend(fontsize=7); ax[1, 0].set_xlabel(r"$\omega$ [GHz]")
        ax[1, 1].semilogy(x, np.abs(np.angle(A_sc) - ref.daten[:, 3]) + 1e-16, "r")
        ax[1, 1].semilogy(x, np.abs(np.angle(A_ex) - ref.daten[:, 4]) + 1e-16, "c")
        ax[1, 1].set_ylabel("Residuum arg"); ax[1, 1].set_xlabel(r"$\omega$ [GHz]")
        fig.suptitle(f"EXP-R1 {name}: Referenz Benjadi & Egger (Zenodo, CC-BY-4.0) vs. eigene Rechnung")
        fig.tight_layout(); fig.savefig(aus / f"{name[:-4]}_vergleich.png", dpi=150); plt.close(fig)

    # --- Fig. 3(c): Fehlermaße, vier Interpretationsvarianten
    ref = lade_referenzdatei("fig3c.dat")
    eingaben["fig3c.dat"] = ref.sha256
    fig, axes = plt.subplots(1, 3, figsize=(13, 4), sharey=True)
    for variante in ("omega_lambda0", "omega_ghz", "epsilon_lambda0", "epsilon_ghz"):
        eigene = _fig3c_eigene(stark, ref.daten[:, 0], variante)
        np.save(roh / f"fig3c_eigene_{variante}.npy", eigene)
        for k, (spalte_eigen, name_mass) in enumerate(((1, "eps_a_tau_z"), (3, "eps_A"), (4, "eps_phi"))):
            axes[k].semilogy(ref.daten[:, 0], eigene[:, spalte_eigen] + 1e-16, "--", label=variante)
            r = ref.daten[:, k + 1]
            kennzahlen.append({"datei": "fig3c.dat", "spalte": k + 2, "groesse": f"{name_mass} [{variante}]",
                               "max_abs_abw": float(np.abs(eigene[:, spalte_eigen] - r).max()),
                               "skala": float(r.max()),
                               "max_abw_rel_skala": float(np.abs(eigene[:, spalte_eigen] - r).max() / r.max())})
    for k in range(3):
        axes[k].semilogy(ref.daten[:, 0], ref.daten[:, k + 1], "k-", lw=2, label=f"Ref. Spalte {k + 2}")
        axes[k].set_xlabel("x (Spalte 1)"); axes[k].legend(fontsize=6)
    fig.suptitle("EXP-R1 fig3c: Referenz vs. eigene Fehlermaße (RWA, lineare Antwort)")
    fig.tight_layout(); fig.savefig(aus / "fig3c_vergleich.png", dpi=150); plt.close(fig)

    with (aus / "kennzahlen.csv").open("w", newline="", encoding="utf-8") as handle:
        w = csv.DictWriter(handle, fieldnames=list(kennzahlen[0].keys()))
        w.writeheader(); w.writerows(kennzahlen)
    schreibe_manifest(roh, {"lauf_id": lauf_id, "experiment": "EXP-R1", "konvention_lambda0": KONVENTION,
                            "I0": I0_LINEAR, "cutoff": CUTOFF, "modell_stark": asdict(stark),
                            "modell_schwach": asdict(schwach), "eingaben_sha256": eingaben,
                            "referenzdaten": ZITATION})
    for z in kennzahlen:
        print(f"{z['datei']:10s} Sp.{z['spalte']} {z['groesse']:40s} max|Abw|/Skala = {z['max_abw_rel_skala']:.2e}")
    print("Ausgabe:", aus)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
