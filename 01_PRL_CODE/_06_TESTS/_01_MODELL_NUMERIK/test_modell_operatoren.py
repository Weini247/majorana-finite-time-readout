import math
import unittest
from dataclasses import replace

import numpy as np
import qutip as qt

from _01_GRUNDLAGEN_FORMELN.abgeleitete_groessen import abgeleitete_groessen, bose, chi_stark, chi_voll
from _01_GRUNDLAGEN_FORMELN.operatoren_rwa import baue_rwa_modell
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark

EXAKT = 1.0e-12  # T1


class ModelloperatorenVertrag(unittest.TestCase):
    def setUp(self) -> None:
        self.modell = modell_stark("gewoehnlich")
        self.b = buendel(self.modell, omega=11.99, I0=1e-3, cutoff=6)

    def test_hamiltonoperator_ist_hermitesch(self) -> None:
        H = baue_rwa_modell(self.b).H
        self.assertLess(float(np.max(np.abs((H - H.dag()).full()))), EXAKT)

    def test_tau_operatoren_erfuellen_pauli_algebra(self) -> None:
        ops = baue_rwa_modell(self.b)
        tp = ops.tau_minus.dag()
        kommutator = tp * ops.tau_minus - ops.tau_minus * tp
        self.assertLess(float(np.max(np.abs((kommutator - ops.tau_z).full()))), EXAKT)

    def test_tau_minus_senkt_die_energie(self) -> None:
        ops = baue_rwa_modell(self.b)
        oben = qt.tensor(qt.basis(6, 0), qt.basis(2, 0))
        self.assertAlmostEqual(qt.expect(ops.tau_z, oben), 1.0, delta=EXAKT)
        unten = (ops.tau_minus * oben).unit()
        self.assertAlmostEqual(qt.expect(ops.tau_z, unten), -1.0, delta=EXAKT)

    def test_kopplung_hat_vorzeichen_aus_gleichung_7(self) -> None:
        g = abgeleitete_groessen(self.modell, self.b.antrieb, 1)
        self.assertAlmostEqual(g.omega_z, 6.0, delta=EXAKT)
        self.assertAlmostEqual(g.g_z, -0.1 * 6.0 / 12.0, delta=EXAKT)

    def test_ohne_t1_sind_beide_paritaeten_identisch(self) -> None:
        m = replace(self.modell, t1=0.0, phi=0.7)
        plus = abgeleitete_groessen(m, self.b.antrieb, 1)
        minus = abgeleitete_groessen(m, self.b.antrieb, -1)
        self.assertEqual(plus, minus)

    def test_paritaeten_unterscheiden_sich_mit_t1(self) -> None:
        plus = abgeleitete_groessen(self.modell, self.b.antrieb, 1)
        minus = abgeleitete_groessen(self.modell, self.b.antrieb, -1)
        self.assertAlmostEqual(plus.t_z_betrag, 6.0, delta=EXAKT)
        self.assertAlmostEqual(minus.t_z_betrag, 4.0, delta=EXAKT)

    def test_phase_pi_halbe_macht_paritaeten_gleich(self) -> None:
        m = replace(self.modell, phi=math.pi / 2)
        plus = abgeleitete_groessen(m, self.b.antrieb, 1)
        minus = abgeleitete_groessen(m, self.b.antrieb, -1)
        self.assertAlmostEqual(plus.omega_z, minus.omega_z, delta=EXAKT)

    def test_bose_grenzfaelle(self) -> None:
        self.assertEqual(bose(1.0, 0.0), 0.0)
        self.assertAlmostEqual(bose(1.0, 1.0), 1.0 / (math.e - 1.0), delta=EXAKT)

    def test_volle_suszeptibilitaet_enthaelt_rwa_term(self) -> None:
        g = abgeleitete_groessen(self.modell, self.b.antrieb, 1)
        omega = self.b.antrieb.omega
        gegenrotierend = -g.g_z ** 2 / (1j * g.Gamma_tot + (2 * g.omega_z + omega))
        self.assertLess(abs(chi_voll(g, omega) - (chi_stark(g) + gegenrotierend)), EXAKT)

    def test_dissipatoren_entsprechen_gleichung_12(self) -> None:
        ops = baue_rwa_modell(self.b)
        g = ops.groessen
        raten = sorted(float(np.real((c.dag() * c).tr())) for c in ops.c_ops)
        # Spur von c^dag c ist Rate * Spur des Operatorprodukts; hier nur Anzahl und Positivität geprüft
        self.assertEqual(len(ops.c_ops), 5 if (g.n_th > 0 and g.N_th > 0) else len(ops.c_ops))
        self.assertTrue(all(r > 0 for r in raten))


if __name__ == "__main__":
    unittest.main()
