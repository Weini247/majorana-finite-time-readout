"""Hamiltonoperator und Sprungoperatoren im rotierenden Rahmen (Benjadi & Egger 2026).

Eq. (10):  H_sc = Delta_z/2 tau_z + Delta_0 a^dag a + g_z (a tau_+ + a^dag tau_-) + i sqrt(kappa_in I0) (a^dag - a)
Eq. (12):  Gamma_phi/2 D[tau_z] + gamma{(n_th+1) D[tau_-] + n_th D[tau_+]} + kappa{(N_th+1) D[a] + N_th D[a^dag]}

Tensorordnung: Resonator (Fock, cutoff) ⊗ Doppelpunkt (Rabi-Basis, Index 0 = obere Energie, tau_z=+1).
Dieses Modul kennt keine Löser.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import qutip as qt

from _01_GRUNDLAGEN_FORMELN.abgeleitete_groessen import AbgeleiteteGroessen, abgeleitete_groessen
from _05_INFRASTRUKTUR.konfiguration.config import ParameterBuendel


@dataclass(frozen=True)
class Modelloperatoren:
    H: qt.Qobj
    c_ops: tuple[qt.Qobj, ...]
    c_ops_doppelpunkt: tuple[qt.Qobj, ...]
    a: qt.Qobj
    tau_z: qt.Qobj
    tau_minus: qt.Qobj
    n_res: qt.Qobj
    a_tau_z: qt.Qobj
    projektor_oberster_fock: qt.Qobj
    groessen: AbgeleiteteGroessen


def baue_rwa_modell(b: ParameterBuendel) -> Modelloperatoren:
    m, d, n = b.modell, b.antrieb, b.numerik.cutoff
    g = abgeleitete_groessen(m, d, b.paritaet)

    a = qt.tensor(qt.destroy(n), qt.qeye(2))
    tau_z = qt.tensor(qt.qeye(n), qt.sigmaz())         # QuTiP sigmaz: |0> -> +1 (obere Energie)
    tau_minus = qt.tensor(qt.qeye(n), qt.basis(2, 1) * qt.basis(2, 0).dag())   # |unten><oben| senkt Energie
    tau_plus = tau_minus.dag()
    n_res = a.dag() * a

    H = (0.5 * g.Delta_z * tau_z + g.Delta_0 * n_res
         + g.g_z * (a * tau_plus + a.dag() * tau_minus)
         + 1j * math.sqrt(m.kappa_in * d.I0) * (a.dag() - a))

    c_ops: list[qt.Qobj] = []
    if m.gamma_phi > 0:
        c_ops.append(math.sqrt(m.gamma_phi / 2.0) * tau_z)
    if m.gamma > 0:
        c_ops.append(math.sqrt(m.gamma * (g.n_th + 1.0)) * tau_minus)
        if g.n_th > 0:
            c_ops.append(math.sqrt(m.gamma * g.n_th) * tau_plus)
    c_ops_doppelpunkt = tuple(c_ops)
    c_ops.append(math.sqrt(m.kappa * (g.N_th + 1.0)) * a)
    if g.N_th > 0:
        c_ops.append(math.sqrt(m.kappa * g.N_th) * a.dag())

    projektor = qt.tensor(qt.fock_dm(n, n - 1), qt.qeye(2))
    return Modelloperatoren(H=H, c_ops=tuple(c_ops), c_ops_doppelpunkt=c_ops_doppelpunkt, a=a, tau_z=tau_z, tau_minus=tau_minus,
                            n_res=n_res, a_tau_z=a * tau_z, projektor_oberster_fock=projektor, groessen=g)
