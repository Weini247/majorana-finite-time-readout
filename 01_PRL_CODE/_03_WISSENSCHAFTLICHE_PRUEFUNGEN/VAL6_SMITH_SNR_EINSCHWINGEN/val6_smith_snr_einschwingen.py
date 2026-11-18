"""VAL6 — Einschwingen des Signal-Rausch-Verhältnisses einer dispersiven Messung bei kappa = 2 chi.

Referenz: T. B. Smith, M. C. Cassidy, D. J. Reilly, S. D. Bartlett, A. L. Grimsmo,
"Dispersive readout of Majorana qubits", PRX Quantum 1, 020313 (2020), arXiv:2009.00027, Eq. (29)
(Heterodyn, eta = 1, Boxcar-Integration):
  SNR_het(tau) = 2|eps| sqrt(tau/chi) [1 - (1 - e^{-chi tau} cos(chi tau)) / (chi tau)]
(Smith zitiert dafür Didier et al. 2015 und Blais et al. 2021.)

Geprüft wird die eigene Kette Mittelwert-Record (mesolve) -> Boxcar-SNR auf der stationär optimalen
Quadratur, Homodyn mit allen Photonen beobachtet: SNR_hom = sqrt(2) SNR_het (Heterodyn halbiert SNR^2).
Antrieb: Smith's eps entspricht hier E (i E (a^dag - a)).
"""
from __future__ import annotations

import math
import unittest

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import mittelwert_record
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle_dispersiv import alpha_analytisch, dispersiver_kanal

REL_MAX = 1.0e-4          # T3: mesolve atol/rtol 1e-10/1e-8, Trapezintegration auf feinem Gitter


def smith_eq29(tau: np.ndarray, eps: float, chi: float) -> np.ndarray:
    return 2 * abs(eps) * np.sqrt(tau / chi) * (1 - (1 - np.exp(-chi * tau) * np.cos(chi * tau)) / (chi * tau))


class Val6SmithSnrEinschwingen(unittest.TestCase):
    def test_boxcar_snr_entspricht_smith_gleichung_29(self) -> None:
        chi, E = 0.05, 0.01
        kappa = 2 * chi
        # stationär optimale Quadratur: Richtung von alpha_+ - alpha_-
        d_ss = alpha_analytisch(np.array([1e9]), chi=chi, kappa=kappa, E=E, sigma=1)[0] \
            - alpha_analytisch(np.array([1e9]), chi=chi, kappa=kappa, E=E, sigma=-1)[0]
        theta = float(np.angle(d_ss))
        t = np.linspace(0.0, 200.0, 4001)
        mu = {}
        for s in (1, -1):
            mu[s] = mittelwert_record(dispersiver_kanal(chi=chi, kappa=kappa, E=E, eta=1.0, theta=theta, sigma=s), t)
        diff = mu[1] - mu[-1]
        integral = np.concatenate([[0.0], np.cumsum(0.5 * (diff[1:] + diff[:-1]) * np.diff(t))])
        auswahl = t >= 5.0
        snr_hom = integral[auswahl] / np.sqrt(t[auswahl])
        snr_het_smith = smith_eq29(t[auswahl], E, chi)
        rel = np.abs(snr_hom / math.sqrt(2.0) - snr_het_smith) / snr_het_smith
        self.assertLess(float(rel.max()), REL_MAX)

    def test_mittelwert_record_entspricht_kohaerenter_amplitude(self) -> None:
        chi, kappa, E, eta, theta = 0.03, 0.04, 0.008, 0.5, 0.3
        t = np.linspace(0.0, 150.0, 301)
        for s in (1, -1):
            mu = mittelwert_record(dispersiver_kanal(chi=chi, kappa=kappa, E=E, eta=eta, theta=theta, sigma=s), t)
            alpha = alpha_analytisch(t, chi=chi, kappa=kappa, E=E, sigma=s)
            erwartet = math.sqrt(eta * kappa) * 2 * np.real(np.exp(-1j * theta) * alpha)
            self.assertLess(float(np.max(np.abs(mu - erwartet))), 1e-7)


if __name__ == "__main__":
    unittest.main()
