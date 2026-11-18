"""VAL1 — Jaynes-Cummings-Kavität bei schwachem Antrieb und T = 0: lineare Antwort.

Referenz: Standardergebnis der cavity-/circuit-QED für die Transmission einer an ein dissipatives
Zweiniveausystem gekoppelten Kavität im Grenzfall schwachen Antriebs, z. B.
A. Blais, A. L. Grimsmo, S. M. Girvin, A. Wallraff, Rev. Mod. Phys. 93, 025005 (2021), Abschnitt zur
Vakuum-Rabi-Aufspaltung (Gleichungsnummer vor Zitation prüfen):
  <a>_ss = sqrt(kappa_in I0) / ( i Delta_0 + kappa/2 + g^2 / (i Delta_z + Gamma) ),  Gamma = Gamma_phi + gamma/2.
Bei T = 0 ist das Qubit im Grundzustand, die Faktorisierung <a tau_z> = -<a> gilt in erster Ordnung in
sqrt(I0); daher stimmt hier auch Benjadi & Egger Eq. (18) mit <tau_z> = -1 exakt überein.

Diese Prüfung ist wichtig für die Reproduktion: Abweichungen der Semiklassik in L01 Fig. 3 können bei
T -> 0 und I0 -> 0 nicht aus dem Modell selbst stammen.
"""
from __future__ import annotations

import math
import unittest

import numpy as np

from _02_AUSFUEHRUNG.fall_ausfuehrung import rechne_fall
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark

I0_LINEAR = 1.0e-8
REL_MAX = 1.0e-6         # T3: Nichtlinearität ~ I0 * n_sat^-1, Cutoff und Löser deutlich kleiner
ORDNUNG_TOLERANZ = 0.1   # erwartete Steigung 1 von eps_A gegen I0


class Val1JaynesCummingsLineareAntwort(unittest.TestCase):
    def setUp(self) -> None:
        self.m = modell_stark("gewoehnlich", temperatur_k=0.0)

    def test_vakuum_rabi_transmission_bei_schwachem_antrieb(self) -> None:
        for omega in (11.80, 11.94, 11.99, 12.04, 12.20):
            with self.subTest(omega=omega):
                r = rechne_fall(buendel(self.m, omega=omega, I0=I0_LINEAR, cutoff=6))
                g = r.groessen
                gamma_qubit = self.m.gamma_phi + 0.5 * self.m.gamma
                referenz = math.sqrt(self.m.kappa_in * I0_LINEAR) / (
                    1j * g.Delta_0 + self.m.kappa / 2 + g.g_z ** 2 / (1j * g.Delta_z + gamma_qubit))
                self.assertLess(abs(r.exakt.a - referenz) / abs(referenz), REL_MAX)
                self.assertLess(r.eps_A, REL_MAX)

    def test_semiklassischer_fehler_waechst_linear_mit_antrieb(self) -> None:
        werte = []
        for I0 in (1e-7, 1e-6, 1e-5):
            werte.append(rechne_fall(buendel(self.m, omega=11.99, I0=I0, cutoff=8)).eps_A)
        steigungen = np.diff(np.log10(werte))
        for s in steigungen:
            self.assertLess(abs(s - 1.0), ORDNUNG_TOLERANZ)


if __name__ == "__main__":
    unittest.main()
