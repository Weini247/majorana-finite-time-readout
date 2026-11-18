"""Abgeleitete Größen des Box-Doppelpunkt-Modells (Benjadi & Egger 2026, arXiv:2603.06482v2).

Gleichungsnummern beziehen sich auf arXiv v2.
"""
from __future__ import annotations

import cmath
import math
from dataclasses import dataclass

from _05_INFRASTRUKTUR.konfiguration.config import AntriebsParameter, ModellParameter


def bose(energie: float, temperatur: float) -> float:
    """Bose-Besetzung 1/(exp(E/T)-1); T = 0 ergibt 0 (E > 0)."""
    if energie <= 0.0:
        raise ValueError("Energie muss positiv sein")
    if temperatur == 0.0:
        return 0.0
    x = energie / temperatur
    if x > 700.0:
        return 0.0
    return 1.0 / math.expm1(x)


@dataclass(frozen=True)
class AbgeleiteteGroessen:
    t_z_betrag: float
    omega_z: float          # Eq. (4); Rabi-Aufspaltung ist 2*omega_z
    g_z: float              # Eq. (7), mit Vorzeichen
    n_th: float             # Eq. (13), Doppelpunkt bei 2*omega_z
    N_th: float             # Eq. (13), Resonator bei omega0
    gamma_tilde: float      # Eq. (15)
    Gamma_tot: float        # Eq. (15)
    Delta_z: float          # Eq. (11)
    Delta_0: float          # Eq. (11)


def abgeleitete_groessen(m: ModellParameter, a: AntriebsParameter, paritaet: int) -> AbgeleiteteGroessen:
    t_z = m.t0 + paritaet * m.t1 * cmath.exp(1j * m.phi)       # Eq. (2), Eichung: Phase in t1
    t_abs = abs(t_z)
    omega_z = math.sqrt(m.epsilon ** 2 + t_abs ** 2)            # Eq. (4)
    if omega_z == 0.0:
        raise ValueError("omega_z = 0: entarteter Doppelpunkt, Modell nicht definiert")
    g_z = -m.lam * t_abs / (2.0 * omega_z)                       # Eq. (7)
    n_th = bose(2.0 * omega_z, m.temperatur)
    N_th = bose(m.omega0, m.temperatur)
    gamma_tilde = (2.0 * n_th + 1.0) * m.gamma
    return AbgeleiteteGroessen(
        t_z_betrag=t_abs, omega_z=omega_z, g_z=g_z, n_th=n_th, N_th=N_th,
        gamma_tilde=gamma_tilde, Gamma_tot=m.gamma_phi + 0.5 * gamma_tilde,
        Delta_z=2.0 * omega_z - a.omega, Delta_0=m.omega0 - a.omega,
    )


def chi_stark(g: AbgeleiteteGroessen) -> complex:
    """Eq. (19): chi_z = -g_z^2 / (Delta_z - i Gamma_tot)."""
    return -g.g_z ** 2 / (g.Delta_z - 1j * g.Gamma_tot)


def chi_schwach(g: AbgeleiteteGroessen, omega0: float) -> float:
    """Eq. (22): chi_z = -g_z^2 / (omega_z - omega0^2/(4 omega_z))."""
    return -g.g_z ** 2 / (g.omega_z - omega0 ** 2 / (4.0 * g.omega_z))


def chi_voll(g: AbgeleiteteGroessen, omega: float) -> complex:
    """Eq. (40): volle Suszeptibilität inkl. gegenrotierendem Term."""
    return g.g_z ** 2 * (1.0 / (1j * g.Gamma_tot - (2.0 * g.omega_z - omega))
                         - 1.0 / (1j * g.Gamma_tot + (2.0 * g.omega_z + omega)))
