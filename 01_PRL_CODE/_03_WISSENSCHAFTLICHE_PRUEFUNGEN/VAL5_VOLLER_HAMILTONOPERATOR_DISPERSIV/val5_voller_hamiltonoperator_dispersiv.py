"""VAL5 — Richtung der dispersiven Kavitätsverschiebung im vollen Modell (Benjadi & Egger Eq. 5, ohne RWA).

Exakte Diagonalisierung von
  H = omega_z tau_z + omega0 a^dag a + lam/2 (a + a^dag)(1 - eps/omega_z tau_z - |t_z|/omega_z tau_x)
und Vergleich der Kavitätsanregung im Qubit-Grundzustand mit der Schrieffer-Wolff-Störungstheorie
  omega_cav|g> = omega0 - g_z^2 (1/Delta + 1/Sigma),  Delta = 2 omega_z - omega0,  Sigma = 2 omega_z + omega0
(z. B. Zueco, Reuther, Kohler, Hänggi, PRA 80, 033846 (2009) für Korrekturen jenseits der RWA; Blais et al.
PRA 69, 062320 (2004) für den RWA-Anteil — Gleichungsnummern vor Zitation prüfen).

Hintergrund: Die in fig3e veröffentlichten Kurven folgen Eq. (26) mit chi_z aus Eq. (22) und liegen bei
omega0 + |chi|; die exakte Diagonalisierung ergibt omega0 - |chi|. Dieser Test sichert die eigene Seite des
Widerspruchs ab (Befund F-1.2, Status HYPOTHESIS bis zur Klärung mit den Autoren).
"""
from __future__ import annotations

import math
import unittest

import numpy as np
import qutip as qt

CUTOFF = 30
SW_REL_MAX = 0.05          # Abweichung höherer Ordnung (g/Delta)^2 bei g/Delta ~ 0.09


def _kavitaet_grundzustand(omega_z: float, omega0: float, lam: float, eps: float, t: float) -> float:
    a = qt.tensor(qt.destroy(CUTOFF), qt.qeye(2))
    tz = qt.tensor(qt.qeye(CUTOFF), qt.sigmaz())
    tx = qt.tensor(qt.qeye(CUTOFF), qt.sigmax())
    H = omega_z * tz + omega0 * a.dag() * a + 0.5 * lam * (a + a.dag()) * (1 - eps / omega_z * tz - t / omega_z * tx)
    E, V = H.eigenstates()

    def energie(n: int) -> float:
        ziel = qt.tensor(qt.basis(CUTOFF, n), qt.basis(2, 1))     # basis(2,1): sigmaz = -1 (unten)
        return float(E[int(np.argmax([abs(ziel.overlap(v)) ** 2 for v in V]))])
    return energie(1) - energie(0)


class Val5VollerHamiltonoperatorDispersiv(unittest.TestCase):
    def test_kavitaet_wird_vom_hoeher_liegenden_qubit_nach_unten_gedrueckt(self) -> None:
        for eps, omega0, lam in ((6.0, 16.0, 0.25), (0.0, 11.0, 0.1), (0.0, 13.0, 0.1)):
            with self.subTest(eps=eps, omega0=omega0):
                t = 6.0
                omega_z = math.sqrt(eps ** 2 + t ** 2)
                g_z = -lam * t / (2 * omega_z)
                delta, sigma = 2 * omega_z - omega0, 2 * omega_z + omega0
                chi_sw = g_z ** 2 * (1 / delta + 1 / sigma)
                gefunden = _kavitaet_grundzustand(omega_z, omega0, lam, eps, t)
                verschiebung = gefunden - omega0
                self.assertEqual(np.sign(verschiebung), -np.sign(delta))
                self.assertLess(abs(verschiebung + chi_sw) / abs(chi_sw), SW_REL_MAX)


if __name__ == "__main__":
    unittest.main()
