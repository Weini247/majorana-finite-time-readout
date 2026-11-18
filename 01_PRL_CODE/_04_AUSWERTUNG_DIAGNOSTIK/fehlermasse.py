"""Exakte Erwartungswerte, Ausleseamplitude und Fehlermaße (Benjadi & Egger 2026, Eqs. 35, 43-45).

A_ref = sqrt(kappa_out / I0) <a>_ss  (Eq. 35, Konvention wie Eq. 20; die Zenodo-Daten fig3a
zeigen arg A -> -pi/2 unterhalb der Resonanz, konsistent mit Eq. 20).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import qutip as qt

from _01_GRUNDLAGEN_FORMELN.operatoren_rwa import Modelloperatoren


@dataclass(frozen=True)
class ExakteErwartungswerte:
    a: complex
    tau_z: float
    a_tau_z: complex
    n_res: float


def erwartungswerte(ops: Modelloperatoren, rho: qt.Qobj) -> ExakteErwartungswerte:
    return ExakteErwartungswerte(
        a=complex(qt.expect(ops.a, rho)),
        tau_z=float(np.real(qt.expect(ops.tau_z, rho))),
        a_tau_z=complex(qt.expect(ops.a_tau_z, rho)),
        n_res=float(np.real(qt.expect(ops.n_res, rho))),
    )


def amplitude_exakt(w: ExakteErwartungswerte, kappa_out: float, I0: float) -> complex:
    if I0 <= 0:
        raise ValueError("I0 muss positiv sein, um A zu definieren")
    return math.sqrt(kappa_out / I0) * w.a


def fehler_faktorisierung(w: ExakteErwartungswerte) -> float:
    """Eq. (43), Lesart A1-6a: alle Größen aus dem exakten Steady State."""
    return abs(w.a_tau_z - w.a * w.tau_z) / abs(w.a)


def fehler_faktorisierung_gegen_semiklassik(w: ExakteErwartungswerte, a_sc: complex, tau_z_sc: float) -> float:
    """Eq. (43), Lesart A1-6b: exaktes <a tau_z> gegen semiklassisches Produkt, normiert auf |<a>_sc|."""
    return abs(w.a_tau_z - a_sc * tau_z_sc) / abs(a_sc)


def fehler_amplitude(A_sc: complex, A_ref: complex) -> float:
    """Eq. (44)."""
    return abs(A_sc - A_ref) / (abs(A_sc) + abs(A_ref))


def fehler_phase(A_sc: complex, A_ref: complex) -> float:
    """Eq. (45): |arg A_sc - arg A_ref| / pi, arg in (-pi, pi] wie numpy.angle."""
    return abs(float(np.angle(A_sc)) - float(np.angle(A_ref))) / math.pi
