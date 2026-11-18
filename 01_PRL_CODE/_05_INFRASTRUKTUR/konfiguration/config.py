"""Parameterbündel einer stationären Ausleserechnung (Benjadi & Egger 2026, Eqs. 2-15).

Alle Energien, Raten und Frequenzen in Einheiten von lambda0 (hbar = k_B = 1).
Die Temperatur wird als T/lambda0 gespeichert; die Umrechnung aus Kelvin hängt von der
lambda0-Konvention ab und liegt in _01_GRUNDLAGEN_FORMELN.einheiten.

Frozen dataclasses mit früher Prüfung: keine stillen Defaults für
Studienwerte, jede Größe endlich, Raten nicht negativ.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from numbers import Integral, Real

ERLAUBTE_LOESER = frozenset({"qutip_direkt", "sparse_spurzeile", "propagation"})


def _reell_endlich(name: str, wert: object) -> float:
    if isinstance(wert, bool) or not isinstance(wert, Real):
        raise TypeError(f"{name} muss eine reelle Zahl sein")
    zahl = float(wert)
    if not isfinite(zahl):
        raise ValueError(f"{name} muss endlich sein")
    return zahl


def _nicht_negativ(name: str, wert: object) -> float:
    zahl = _reell_endlich(name, wert)
    if zahl < 0.0:
        raise ValueError(f"{name} darf nicht negativ sein")
    return zahl


def _positiv(name: str, wert: object) -> float:
    zahl = _reell_endlich(name, wert)
    if zahl <= 0.0:
        raise ValueError(f"{name} muss positiv sein")
    return zahl


def _ganz_positiv(name: str, wert: object) -> int:
    if isinstance(wert, bool) or not isinstance(wert, Integral):
        raise TypeError(f"{name} muss eine ganze Zahl sein")
    zahl = int(wert)
    if zahl <= 0:
        raise ValueError(f"{name} muss positiv sein")
    return zahl


@dataclass(frozen=True)
class ModellParameter:
    """Box-Doppelpunkt-Resonator (L01 Eqs. 2-13). t_z = t0 + z t1 exp(i phi), t0, t1 >= 0."""
    t0: float
    t1: float
    phi: float
    epsilon: float
    omega0: float
    lam: float
    kappa_in: float
    kappa_out: float
    gamma: float
    gamma_phi: float
    temperatur: float          # T / lambda0

    def __post_init__(self) -> None:
        _nicht_negativ("t0", self.t0)
        _nicht_negativ("t1", self.t1)
        _reell_endlich("phi", self.phi)
        _reell_endlich("epsilon", self.epsilon)
        _positiv("omega0", self.omega0)
        _reell_endlich("lam", self.lam)
        _nicht_negativ("kappa_in", self.kappa_in)
        _nicht_negativ("kappa_out", self.kappa_out)
        _nicht_negativ("gamma", self.gamma)
        _nicht_negativ("gamma_phi", self.gamma_phi)
        _nicht_negativ("temperatur", self.temperatur)
        if self.kappa_in + self.kappa_out <= 0.0:
            raise ValueError("kappa = kappa_in + kappa_out muss positiv sein (eindeutiger Steady State)")

    @property
    def kappa(self) -> float:
        return self.kappa_in + self.kappa_out


@dataclass(frozen=True)
class AntriebsParameter:
    """Kohärenter Antrieb (L01 Eq. 9): Frequenz omega, Eingangsintensität I0 = |<b_in>|^2."""
    omega: float
    I0: float

    def __post_init__(self) -> None:
        _positiv("omega", self.omega)
        _nicht_negativ("I0", self.I0)


@dataclass(frozen=True)
class NumerikParameter:
    cutoff: int = 12
    loeser: str = "qutip_direkt"
    max_oberste_fock_population: float = 1.0e-10

    def __post_init__(self) -> None:
        if _ganz_positiv("cutoff", self.cutoff) < 2:
            raise ValueError("cutoff muss mindestens 2 sein")
        if self.loeser not in ERLAUBTE_LOESER:
            raise ValueError(f"unbekannter Löser {self.loeser}; erlaubt: {sorted(ERLAUBTE_LOESER)}")
        _positiv("max_oberste_fock_population", self.max_oberste_fock_population)


@dataclass(frozen=True)
class ParameterBuendel:
    modell: ModellParameter
    antrieb: AntriebsParameter
    paritaet: int
    numerik: NumerikParameter = field(default_factory=NumerikParameter)

    def __post_init__(self) -> None:
        if self.paritaet not in (-1, 1):
            raise ValueError("paritaet muss +1 oder -1 sein")
