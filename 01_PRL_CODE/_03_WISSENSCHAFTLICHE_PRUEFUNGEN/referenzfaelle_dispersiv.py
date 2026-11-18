"""Dispersiver QND-Referenzfall (Pointerzustände ohne Qubitdynamik) für die Messkanalprüfungen VAL6/VAL7.

H = (Delta_0 + chi sigma_z) a^dag a + i E (a^dag - a),  sigma_z statisch (keine Qubit-Dissipation)
Hypothesen: Qubit in |oben> (sigma_z = +1) bzw. |unten> (sigma_z = -1), Resonator im Vakuum.
"""
from __future__ import annotations

import math

import numpy as np
import qutip as qt

from _02_AUSFUEHRUNG.homodyn_trajektorien import Messkanal


def dispersiver_kanal(*, chi: float, kappa: float, E: float, eta: float, theta: float, sigma: int,
                      delta0: float = 0.0, cutoff: int = 15) -> Messkanal:
    a = qt.tensor(qt.destroy(cutoff), qt.qeye(2))
    sz = qt.tensor(qt.qeye(cutoff), qt.sigmaz())
    H = (delta0 * a.dag() * a + chi * sz * a.dag() * a + 1j * E * (a.dag() - a))
    unbeob = [math.sqrt((1.0 - eta) * kappa) * a] if eta < 1.0 else []
    c = math.sqrt(eta * kappa) * np.exp(-1j * theta) * a
    qubit = qt.basis(2, 0) if sigma > 0 else qt.basis(2, 1)
    rho0 = qt.ket2dm(qt.tensor(qt.basis(cutoff, 0), qubit))
    return Messkanal(H=H, unbeobachtet=tuple(unbeob), beobachtet=c, rho0=rho0)


def alpha_analytisch(t: np.ndarray, *, chi: float, kappa: float, E: float, sigma: int, delta0: float = 0.0) -> np.ndarray:
    """Kohärente Amplitude: d alpha/dt = -(i(Delta_0 + sigma chi) + kappa/2) alpha + E."""
    lam = 1j * (delta0 + sigma * chi) + kappa / 2
    return E / lam * (1 - np.exp(-lam * t))
