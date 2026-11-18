"""Referenzparameter aus Benjadi & Egger (2026), Fig.-3-Caption, in Einheiten lambda0."""
from __future__ import annotations

from dataclasses import replace

from _01_GRUNDLAGEN_FORMELN.einheiten import temperatur_in_lambda0
from _05_INFRASTRUKTUR.konfiguration.config import (AntriebsParameter, ModellParameter, NumerikParameter,
                                                    ParameterBuendel)

TEMPERATUR_FIG3_K = 0.030
KAPPA_FIG3 = 0.04


def modell_stark(konvention: str, *, kappa_in_anteil: float = 0.5, temperatur_k: float = TEMPERATUR_FIG3_K) -> ModellParameter:
    """Fig. 3(a-d): starke Kopplung."""
    return ModellParameter(t0=5.0, t1=1.0, phi=0.0, epsilon=0.0, omega0=11.99, lam=0.1,
                           kappa_in=kappa_in_anteil * KAPPA_FIG3, kappa_out=(1 - kappa_in_anteil) * KAPPA_FIG3,
                           gamma=0.003, gamma_phi=0.1,
                           temperatur=temperatur_in_lambda0(temperatur_k, konvention))


def modell_schwach(konvention: str, *, kappa_in_anteil: float = 0.5, temperatur_k: float = TEMPERATUR_FIG3_K) -> ModellParameter:
    """Fig. 3(e-h): schwache Kopplung."""
    return ModellParameter(t0=5.0, t1=1.0, phi=0.0, epsilon=6.0, omega0=16.0, lam=0.25,
                           kappa_in=kappa_in_anteil * KAPPA_FIG3, kappa_out=(1 - kappa_in_anteil) * KAPPA_FIG3,
                           gamma=0.015, gamma_phi=0.05,
                           temperatur=temperatur_in_lambda0(temperatur_k, konvention))


def buendel(modell: ModellParameter, omega: float, I0: float, cutoff: int = 8,
            loeser: str = "qutip_direkt", paritaet: int = 1) -> ParameterBuendel:
    return ParameterBuendel(modell=modell, antrieb=AntriebsParameter(omega=omega, I0=I0), paritaet=paritaet,
                            numerik=NumerikParameter(cutoff=cutoff, loeser=loeser))


__all__ = ["modell_stark", "modell_schwach", "buendel", "replace"]
