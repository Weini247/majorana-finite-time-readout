import math
import unittest

import numpy as np
import qutip as qt

from _02_AUSFUEHRUNG.homodyn_trajektorien import messkanal_rwa, trajektorien, trajektorien_referenz
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark


class MesskanalVertrag(unittest.TestCase):
    def setUp(self) -> None:
        self.m = modell_stark("gewoehnlich")
        self.b = buendel(self.m, omega=11.99, I0=1e-3, cutoff=4)

    def test_kein_doppelzaehlen_des_resonatorzerfalls(self) -> None:
        kanal, ops = messkanal_rwa(self.b, eta=0.5, theta=0.3)
        summe = sum((L.dag() * L for L in kanal.unbeobachtet), 0 * ops.n_res) + kanal.beobachtet.dag() * kanal.beobachtet
        referenz = sum((L.dag() * L for L in ops.c_ops), 0 * ops.n_res)
        self.assertLess((summe - referenz).norm(), 1e-12)

    def test_effizienz_ausserhalb_null_eins_wird_abgelehnt(self) -> None:
        with self.assertRaises(ValueError):
            messkanal_rwa(self.b, eta=1.2, theta=0.0)

    def test_startzustand_ist_thermisch_und_normiert(self) -> None:
        kanal, ops = messkanal_rwa(self.b, eta=1.0, theta=0.0)
        self.assertAlmostEqual(kanal.rho0.tr(), 1.0, places=12)
        tz = qt.expect(ops.tau_z, kanal.rho0)
        self.assertAlmostEqual(tz, -math.tanh(ops.groessen.omega_z / self.m.temperatur), places=10)

    def test_trajektorien_sind_mit_gleichem_seed_reproduzierbar(self) -> None:
        kanal, _ = messkanal_rwa(self.b, eta=1.0, theta=0.0)
        a = trajektorien(kanal, T=2.0, dt=0.1, ntraj=5, seed=7, bin_schritte=5).dY_bins
        b = trajektorien(kanal, T=2.0, dt=0.1, ntraj=5, seed=7, bin_schritte=5).dY_bins
        self.assertTrue(np.array_equal(a, b))

    def test_duenner_integrator_gleicht_dem_referenzintegrator(self) -> None:
        # V3-1: gleiche Zufallszahlen (block=None) => gleiche Records und Endzustände bis auf Rundung
        for cutoff in (4, 6):                       # d = 8 (alter Superoperator-Pfad) und d = 12 (alter Bündel-Pfad)
            kanal, ops = messkanal_rwa(buendel(self.m, omega=11.99, I0=1e-2, cutoff=cutoff), eta=0.5, theta=0.4)
            neu = trajektorien(kanal, T=20.0, dt=0.1, ntraj=40, seed=3, bin_schritte=5, beobachtbar_ende=ops.tau_z)
            alt = trajektorien_referenz(kanal, T=20.0, dt=0.1, ntraj=40, seed=3, bin_schritte=5, beobachtbar_ende=ops.tau_z)
            self.assertLess(np.max(np.abs(neu.dY_bins - alt.dY_bins)), 1e-10)
            self.assertLess(np.max(np.abs(neu.tau_z_end - alt.tau_z_end)), 1e-10)

    def test_blockergebnis_haengt_nicht_von_der_prozesszahl_ab(self) -> None:
        kanal, _ = messkanal_rwa(self.b, eta=1.0, theta=0.0)
        a = trajektorien(kanal, T=2.0, dt=0.1, ntraj=25, seed=9, bin_schritte=5, block=10, prozesse=1).dY_bins
        b = trajektorien(kanal, T=2.0, dt=0.1, ntraj=25, seed=9, bin_schritte=5, block=10, prozesse=2).dY_bins
        self.assertEqual(a.shape, (25, 4))
        self.assertTrue(np.array_equal(a, b))

    def test_ungueltige_zeitaufteilung_wird_abgelehnt(self) -> None:
        kanal, _ = messkanal_rwa(self.b, eta=1.0, theta=0.0)
        with self.assertRaises(ValueError):
            trajektorien(kanal, T=1.05, dt=0.1, ntraj=2, seed=1, bin_schritte=5)


if __name__ == "__main__":
    unittest.main()
