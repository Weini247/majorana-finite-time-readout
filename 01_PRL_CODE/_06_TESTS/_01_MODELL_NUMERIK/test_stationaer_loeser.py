import unittest

from _01_GRUNDLAGEN_FORMELN.operatoren_rwa import baue_rwa_modell
from _02_AUSFUEHRUNG.stationaer_loeser import StationaerLoeserFehler, loese_stationaer
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark


class StationaerLoeserVertrag(unittest.TestCase):
    def setUp(self) -> None:
        self.m = modell_stark("gewoehnlich")

    def _loese(self, methode: str, cutoff: int = 12, I0: float = 1e-3, max_fock: float = 1e-10):
        ops = baue_rwa_modell(buendel(self.m, omega=11.99, I0=I0, cutoff=cutoff))
        return loese_stationaer(ops, methode, kappa=self.m.kappa, gamma_min=self.m.gamma, max_fock=max_fock)

    def test_direkter_loeser_liefert_physikalischen_zustand(self) -> None:
        erg = self._loese("qutip_direkt")
        self.assertLess(erg.residuum, 1e-9)
        self.assertLess(erg.spur_fehler, 1e-10)
        self.assertGreater(erg.min_eigenwert, -1e-10)

    def test_eigener_sparse_loeser_stimmt_mit_qutip_ueberein(self) -> None:
        a = self._loese("qutip_direkt").rho.full()
        b = self._loese("sparse_spurzeile").rho.full()
        self.assertLess(float(abs(a - b).max()), 1e-10)

    def test_zu_kleiner_cutoff_wird_nicht_still_akzeptiert(self) -> None:
        with self.assertRaises(StationaerLoeserFehler) as kontext:
            self._loese("qutip_direkt", cutoff=3, I0=0.3)
        self.assertIn("Cutoff", kontext.exception.grund)
        self.assertIn("oberste_fock_population", kontext.exception.diagnostik)

    def test_unbekannte_methode_wird_abgelehnt(self) -> None:
        ops = baue_rwa_modell(buendel(self.m, omega=11.99, I0=1e-3, cutoff=4))
        with self.assertRaises(ValueError):
            loese_stationaer(ops, "zauberei", kappa=self.m.kappa, gamma_min=self.m.gamma)


if __name__ == "__main__":
    unittest.main()
