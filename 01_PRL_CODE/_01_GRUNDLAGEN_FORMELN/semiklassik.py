"""Semiklassische Faktorisierung (Benjadi & Egger 2026, Eqs. 16-20, 26-27)."""
from __future__ import annotations

import math

from _01_GRUNDLAGEN_FORMELN.abgeleitete_groessen import AbgeleiteteGroessen, chi_stark, chi_schwach
from _05_INFRASTRUKTUR.konfiguration.config import AntriebsParameter, ModellParameter


def tau_z_thermisch(g: AbgeleiteteGroessen, temperatur: float) -> float:
    """Eq. (17): <tau_z>_ss = -tanh(omega_z / T); T = 0 -> -1."""
    if temperatur == 0.0:
        return -1.0
    return -math.tanh(g.omega_z / temperatur)


def a_semiklassisch_stark(m: ModellParameter, d: AntriebsParameter, g: AbgeleiteteGroessen) -> complex:
    """Eq. (18): <a>_ss = -i sqrt(kappa_in I0) / (-i kappa/2 + Delta_0 - chi_z <tau_z>)."""
    tz = tau_z_thermisch(g, m.temperatur)
    return -1j * math.sqrt(m.kappa_in * d.I0) / (-0.5j * m.kappa + g.Delta_0 - chi_stark(g) * tz)


def amplitude_semiklassisch_stark(m: ModellParameter, g: AbgeleiteteGroessen) -> complex:
    """Eq. (20): A = -i sqrt(kappa_in kappa_out) / (Delta_0 - i kappa/2 - chi_z <tau_z>)."""
    tz = tau_z_thermisch(g, m.temperatur)
    return -1j * math.sqrt(m.kappa_in * m.kappa_out) / (g.Delta_0 - 0.5j * m.kappa - chi_stark(g) * tz)


def amplitude_semiklassisch_schwach(m: ModellParameter, g: AbgeleiteteGroessen) -> complex:
    """Eq. (26), mit chi_z aus Eq. (22) (Vorzeichen +chi_z <tau_z> wie im Paper)."""
    tz = tau_z_thermisch(g, m.temperatur)
    chi = chi_schwach(g, m.omega0)
    return -1j * math.sqrt(m.kappa_in * m.kappa_out) / (g.Delta_0 - 0.5j * m.kappa + chi * tz)
