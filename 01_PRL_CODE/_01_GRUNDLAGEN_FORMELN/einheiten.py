"""Einheiten: lambda0 = 0.2 GHz (Benjadi & Egger 2026, Fig.-3-Caption).

Ob "GHz" eine gewöhnliche Frequenz (h * 0.2 GHz) oder eine Kreisfrequenz
(hbar * 0.2 Grad/s) bezeichnet, ist im Paper nicht spezifiziert (offene Frage Q-3).
Beide Konventionen sind hier explizit; Rechnungen tragen die Konvention im Manifest.
"""
from __future__ import annotations

import math

LAMBDA0_GHZ = 0.2
KB_UEBER_H_GHZ_PRO_K = 20.83661912          # k_B / h in GHz/K (CODATA 2018, exakt aus SI-Definitionen)
KONVENTIONEN = ("gewoehnlich", "kreisfrequenz")


def temperatur_in_lambda0(temperatur_kelvin: float, konvention: str) -> float:
    """k_B T / lambda0 für lambda0 = h*0.2 GHz ('gewoehnlich') oder hbar*0.2 Grad/s ('kreisfrequenz')."""
    if konvention not in KONVENTIONEN:
        raise ValueError(f"unbekannte Konvention {konvention}")
    if temperatur_kelvin < 0:
        raise ValueError("Temperatur darf nicht negativ sein")
    kbt_ghz = KB_UEBER_H_GHZ_PRO_K * temperatur_kelvin          # k_B T / h in GHz
    if konvention == "gewoehnlich":
        return kbt_ghz / LAMBDA0_GHZ
    return 2.0 * math.pi * kbt_ghz / LAMBDA0_GHZ                 # k_B T / hbar in Grad/s, geteilt durch 0.2


def lambda0_nach_ghz(wert_lambda0: float) -> float:
    """Achsenwert in 'GHz' wie in den Zenodo-Dateien (numerisch: 0.2 * Wert)."""
    return LAMBDA0_GHZ * wert_lambda0


def ghz_nach_lambda0(wert_ghz: float) -> float:
    return wert_ghz / LAMBDA0_GHZ
