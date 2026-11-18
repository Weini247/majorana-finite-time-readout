"""VAL3 — Löserunabhängigkeit (QuTiP direkt / eigene Sparse-Lösung / Zeitpropagation) und Cutoff-Konvergenz
am Resonanzpunkt von Benjadi & Egger Fig. 3 (starke Kopplung, T = 30 mK, gewöhnliche Frequenzkonvention).
"""
from __future__ import annotations

import unittest

from _02_AUSFUEHRUNG.fall_ausfuehrung import rechne_fall
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark

METHODEN_REL_MAX = 1.0e-8     # T2
PROPAGATION_REL_MAX = 1.0e-6  # Zeitintegration: rtol 1e-10 über viele Relaxationszeiten
CUTOFF_REL_MAX = 1.0e-6       # T3


class Val3LoeserunabhaengigkeitCutoff(unittest.TestCase):
    def setUp(self) -> None:
        self.m = modell_stark("gewoehnlich")

    def test_drei_methoden_liefern_dieselbe_amplitude(self) -> None:
        for I0 in (1e-4, 1e-2):
            with self.subTest(I0=I0):
                ref = rechne_fall(buendel(self.m, 11.99, I0, cutoff=16, loeser="qutip_direkt")).A_ref
                sparse = rechne_fall(buendel(self.m, 11.99, I0, cutoff=16, loeser="sparse_spurzeile")).A_ref
                self.assertLess(abs(sparse - ref) / abs(ref), METHODEN_REL_MAX)
        prop = rechne_fall(buendel(self.m, 11.99, 1e-2, cutoff=16, loeser="propagation")).A_ref
        ref = rechne_fall(buendel(self.m, 11.99, 1e-2, cutoff=16)).A_ref
        self.assertLess(abs(prop - ref) / abs(ref), PROPAGATION_REL_MAX)

    def test_cutoff_konvergenz(self) -> None:
        for I0, nc in ((1e-2, 16), (0.1, 30)):
            with self.subTest(I0=I0):
                a = rechne_fall(buendel(self.m, 11.99, I0, cutoff=nc))
                b = rechne_fall(buendel(self.m, 11.99, I0, cutoff=2 * nc))
                self.assertLess(abs(a.A_ref - b.A_ref) / abs(b.A_ref), CUTOFF_REL_MAX)
                self.assertLess(abs(a.eps_a_tau_z - b.eps_a_tau_z), CUTOFF_REL_MAX)


if __name__ == "__main__":
    unittest.main()
