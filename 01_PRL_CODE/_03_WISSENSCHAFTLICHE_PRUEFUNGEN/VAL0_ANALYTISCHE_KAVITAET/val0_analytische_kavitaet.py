"""VAL0 — getriebene, gedämpfte Kavität ohne Kopplung (g = 0) und Thermalzustand ohne Antrieb.

Referenz (Lehrbuch, z. B. Walls & Milburn, Quantum Optics; Clerk et al. RMP 82, 1155 (2010)):
  <a>_ss = sqrt(kappa_in I0) / (i Delta_0 + kappa/2)           (kohärenter Zustand bei N_th = 0)
  <tau_z> = -tanh(omega_z / T),  <a^dag a> = N_th               (ohne Antrieb, ohne Kopplung)
"""
from __future__ import annotations

import math
import unittest
from dataclasses import replace

import numpy as np

from _02_AUSFUEHRUNG.fall_ausfuehrung import rechne_fall
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark

LOESER_REL_MAX = 1.0e-9       # T2
CUTOFF = 14


class Val0AnalytischeKavitaet(unittest.TestCase):
    def test_leere_kavitaet_ergibt_kohaerenten_zustand(self) -> None:
        m = replace(modell_stark("gewoehnlich", temperatur_k=0.0), lam=0.0)
        for omega in (11.8, 11.99, 12.2):
            with self.subTest(omega=omega):
                I0 = 2e-3
                r = rechne_fall(buendel(m, omega=omega, I0=I0, cutoff=CUTOFF))
                erwartet = math.sqrt(m.kappa_in * I0) / (1j * (m.omega0 - omega) + m.kappa / 2)
                self.assertLess(abs(r.exakt.a - erwartet) / abs(erwartet), LOESER_REL_MAX)
                self.assertLess(abs(r.exakt.n_res - abs(erwartet) ** 2), LOESER_REL_MAX)
                # ohne Kopplung ist die Semiklassik exakt
                self.assertLess(r.eps_A, LOESER_REL_MAX)
                self.assertLess(r.eps_a_tau_z, LOESER_REL_MAX)

    def test_thermalzustand_ohne_antrieb(self) -> None:
        m = replace(modell_stark("gewoehnlich", temperatur_k=0.1), lam=0.0)    # N_th ~ 0.46
        r = rechne_fall(buendel(m, omega=11.99, I0=1e-12, cutoff=32))
        g = r.groessen
        self.assertLess(abs(r.exakt.tau_z + math.tanh(g.omega_z / m.temperatur)), 1e-8)
        self.assertLess(abs(r.exakt.n_res - g.N_th) / g.N_th, 1e-6)


if __name__ == "__main__":
    unittest.main()
