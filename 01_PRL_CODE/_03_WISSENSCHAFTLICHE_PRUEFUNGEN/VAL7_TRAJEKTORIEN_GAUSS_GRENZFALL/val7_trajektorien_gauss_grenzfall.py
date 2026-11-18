"""VAL7 — Bedingte Homodyn-Trajektorien: Ensemble-Mittel, Gauß-Grenzfall der Diskriminierung, eta = 0.

Referenzen:
  * Ensemble-Mittel der Records = unbedingte Mastergleichung (Wiseman & Milburn, Quantum Measurement and
    Control, CUP 2010, Kap. 4).
  * Gauß-Grenzfall einer QND-Messung ohne Zerfall: J. Gambetta et al., PRA 76, 012325 (2007), Eq. (6),
    F = erf(sqrt(tau SNR / 2)) für Boxcar; allgemein für zeitabhängige Mittelwerte der Matched Filter mit
    P_err = 1/2 erfc(SNR/(2 sqrt 2)), SNR^2 = int (mu_+ - mu_-)^2 dt (Neyman-Pearson, gleiche Varianz).
Testfall: dispersiver Pointer-Fall (referenzfaelle_dispersiv), Qubit statisch.
"""
from __future__ import annotations

import math
import unittest

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import mittelwert_record, trajektorien
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle_dispersiv import alpha_analytisch, dispersiver_kanal
from _04_AUSWERTUNG_DIAGNOSTIK import decoder

CHI, KAPPA, E = 0.05, 0.1, 0.004
T, DT, BIN = 120.0, 0.1, 10
NTRAJ = 3000
SIGMA_GRENZE = 4.5            # T4: |Mittel - Erwartung| <= 4.5 Standardfehler (viele Bins gleichzeitig)


def _theta() -> float:
    d = alpha_analytisch(np.array([1e9]), chi=CHI, kappa=KAPPA, E=E, sigma=1)[0] \
        - alpha_analytisch(np.array([1e9]), chi=CHI, kappa=KAPPA, E=E, sigma=-1)[0]
    return float(np.angle(d))


def _bins_mittel(kanal) -> np.ndarray:
    t = np.linspace(0.0, T, int(T / DT) + 1)
    mu = mittelwert_record(kanal, t)
    pro_schritt = 0.5 * (mu[1:] + mu[:-1]) * DT
    return pro_schritt.reshape(-1, BIN).sum(axis=1)


class Val7TrajektorienGaussGrenzfall(unittest.TestCase):
    def test_ensemble_mittel_entspricht_mastergleichung(self) -> None:
        kanal = dispersiver_kanal(chi=CHI, kappa=KAPPA, E=0.02, eta=0.7, theta=0.4, sigma=1, cutoff=5)
        erg = trajektorien(kanal, T=T, dt=DT, ntraj=NTRAJ, seed=11, bin_schritte=BIN)
        erwartet = _bins_mittel(kanal)
        standardfehler = math.sqrt(DT * BIN / NTRAJ)
        abw = np.abs(erg.dY_bins.mean(axis=0) - erwartet) / standardfehler
        self.assertLess(float(abw.max()), SIGMA_GRENZE)

    def test_matched_filter_erreicht_gauss_vorhersage(self) -> None:
        theta = _theta()
        mu, kal, test = {}, {}, {}
        for s, seed in ((1, 21), (-1, 22)):
            kanal = dispersiver_kanal(chi=CHI, kappa=KAPPA, E=E, eta=1.0, theta=theta, sigma=s, cutoff=4)
            mu[s] = _bins_mittel(kanal) / (DT * BIN)
            kal[s] = trajektorien(kanal, T=T, dt=DT, ntraj=NTRAJ, seed=seed, bin_schritte=BIN).dY_bins
            test[s] = trajektorien(kanal, T=T, dt=DT, ntraj=NTRAJ, seed=seed + 100, bin_schritte=BIN).dY_bins
        w = mu[1] - mu[-1]
        n = w.size
        vorhersage = decoder.gauss_vorhersage(mu[1], mu[-1], DT * BIN)[-1]
        schwelle = decoder.kalibriere_schwelle(decoder.matched_filter(kal[1], w, n), decoder.matched_filter(kal[-1], w, n))
        fr = decoder.bewerte(decoder.matched_filter(test[1], w, n), decoder.matched_filter(test[-1], w, n), schwelle)
        self.assertGreater(vorhersage, 0.05)          # Test nur sinnvoll bei messbarer Fehlerrate
        self.assertLess(fr.ci_unten, vorhersage)
        self.assertGreater(fr.ci_oben, vorhersage)

    def test_ohne_detektion_bleibt_nur_raten(self) -> None:
        theta = _theta()
        scores = {}
        for s, seed in ((1, 31), (-1, 32)):
            kanal = dispersiver_kanal(chi=CHI, kappa=KAPPA, E=0.02, eta=0.0, theta=theta, sigma=s, cutoff=5)
            scores[s] = decoder.boxcar(trajektorien(kanal, T=T, dt=DT, ntraj=2000, seed=seed, bin_schritte=BIN).dY_bins, 120)
        schwelle = decoder.Schwelle(0.0, True)
        fr = decoder.bewerte(scores[1], scores[-1], schwelle)
        self.assertLess(fr.ci_unten, 0.5)
        self.assertGreater(fr.ci_oben, 0.5)


if __name__ == "__main__":
    unittest.main()
