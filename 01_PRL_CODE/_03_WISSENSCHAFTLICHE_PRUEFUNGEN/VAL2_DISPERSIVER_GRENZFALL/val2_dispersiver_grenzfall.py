"""VAL2 — dispersiver Grenzfall: Kavitätsverschiebung -g^2/Delta.

Referenz: A. Blais, R.-S. Huang, A. Wallraff, S. M. Girvin, R. J. Schoelkopf,
Phys. Rev. A 69, 062320 (2004), dispersive Transformation (Gleichungsnummer vor Zitation prüfen):
  H_disp = (omega_r + chi sigma_z) a^dag a + ...,  chi = g^2 / Delta,  Delta = omega_q - omega_r.
Im Grundzustand (sigma_z = -1) liegt die Kavitätsresonanz bei omega_r - g^2/Delta.
Hier: omega_q = 2 omega_z, omega_r = omega0. Die Abweichung muss wie (g/Delta)^2 relativ skalieren.

Abgrenzung zu Benjadi & Egger Eq. (22): Dort enthält chi_z zusätzlich gegenrotierende Beiträge
(Faktor 4 omega_z / (2 omega_z + omega0)); das RWA-Modell kann Eq. (22) daher nur bis O(Delta/omega) treffen.
"""
from __future__ import annotations

import unittest
from dataclasses import replace

import numpy as np
from scipy.optimize import minimize_scalar

from _02_AUSFUEHRUNG.fall_ausfuehrung import rechne_fall
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel, modell_stark

I0_LINEAR = 1e-8
STEIGUNG_TOLERANZ = 0.25     # erwartete Steigung 2 der relativen Abweichung in log(g/Delta)


def _resonanz(m, omega_grob: float) -> float:
    def negativ_betrag(omega: float) -> float:
        return -abs(rechne_fall(buendel(m, omega=omega, I0=I0_LINEAR, cutoff=6)).A_ref)
    erg = minimize_scalar(negativ_betrag, bracket=(omega_grob - 0.02, omega_grob, omega_grob + 0.02),
                          options={"xtol": 1e-12})
    return float(erg.x)


class Val2DispersiverGrenzfall(unittest.TestCase):
    def test_kavitaetsverschiebung_folgt_g_quadrat_durch_delta(self) -> None:
        basis = replace(modell_stark("gewoehnlich", temperatur_k=0.0), gamma_phi=0.002, gamma=0.001, lam=0.1)
        relative_fehler, verhaeltnisse = [], []
        for delta in (0.4, 0.8, 1.6):
            m = replace(basis, omega0=12.0 - delta)              # 2 omega_z = 12
            g_z = -0.1 * 6.0 / 12.0
            erwartet = m.omega0 - g_z ** 2 / delta
            gefunden = _resonanz(m, erwartet)
            verschiebung_erwartet = g_z ** 2 / delta
            relative_fehler.append(abs((m.omega0 - gefunden) - verschiebung_erwartet) / verschiebung_erwartet)
            verhaeltnisse.append(abs(g_z) / delta)
        steigung = np.polyfit(np.log(verhaeltnisse), np.log(relative_fehler), 1)[0]
        self.assertLess(max(relative_fehler), 0.05)
        self.assertLess(abs(steigung - 2.0), STEIGUNG_TOLERANZ)


if __name__ == "__main__":
    unittest.main()
