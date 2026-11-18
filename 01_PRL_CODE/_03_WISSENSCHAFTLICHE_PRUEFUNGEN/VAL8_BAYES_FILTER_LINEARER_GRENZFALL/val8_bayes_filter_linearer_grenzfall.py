"""VAL8 — Bayes-Decoder (Log-Likelihood-Quotient aus zwei bedingten Zuständen) im linearen Grenzfall.

Referenzen:
  * Wiseman & Milburn, Quantum Measurement and Control (CUP 2010), Kap. 4/5: Likelihood eines Homodyn-Records
    aus dem bedingten Zustand, dl = (<x>_+ - <x>_-) dY - 1/2 (<x>_+^2 - <x>_-^2) dt.
  * Linearer Pointer (Qubit statisch, kein Zerfall): Der bedingte Resonatorzustand bleibt kohärent mit
    deterministischer Amplitude, <x>_c = mu(t). Der LLR ist dann exakt linear im Record — der Matched Filter
    plus Konstante (Gambetta et al., PRA 76, 012325 (2007)); Fehlerrate = Gauß-Vorhersage.
Testfall: VAL7-Kanal (referenzfaelle_dispersiv).
"""
from __future__ import annotations

import unittest

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import log_likelihood_quotient, mittelwert_record, trajektorien
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle_dispersiv import dispersiver_kanal
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.VAL7_TRAJEKTORIEN_GAUSS_GRENZFALL.val7_trajektorien_gauss_grenzfall import (
    CHI, DT, E, KAPPA, T, _theta)
from _04_AUSWERTUNG_DIAGNOSTIK import decoder

NTRAJ = 3000
LINEAR_REL_MAX = 1e-3          # LLR vs. lineare Formel bei Binbreite 0.5 und 0.2, relativ zur LLR-Streuung
# 2026-11-11 (F-3.4): Mit dem exakten kohärenten Propagator entfällt der Fehler erster Ordnung in der Binbreite
# (vorher 0.015 / 0.0059 bei 0.5 / 0.2, jetzt ~1e-4). Die frühere Ordnungsprüfung (Verhältnis 1.8-3.2) prüfte
# diesen Diskretisierungsfehler und ist ersetzt durch die strengere absolute Schranke bei beiden Binbreiten.


def _kanaele(eta=1.0):
    th = _theta()
    return {s: dispersiver_kanal(chi=CHI, kappa=KAPPA, E=E, eta=eta, theta=th, sigma=s, cutoff=4) for s in (1, -1)}


class Val8BayesFilterLinearerGrenzfall(unittest.TestCase):
    def test_llr_gleicht_dem_linearen_matched_filter_bei_beiden_binbreiten(self) -> None:
        k = _kanaele()
        abw = {}
        for b in (5, 2):
            dtb = DT * b
            rec = trajektorien(k[1], T=T, dt=DT, ntraj=200, seed=5, bin_schritte=b).dY_bins
            llr = log_likelihood_quotient(k[1], k[-1], rec, dtb)[:, 0]
            tb = np.arange(rec.shape[1] + 1) * dtb
            mp, mm = (mittelwert_record(k[s], tb)[:-1] for s in (1, -1))
            linear = rec @ (mp - mm) - 0.5 * np.sum(mp ** 2 - mm ** 2) * dtb
            abw[b] = float(np.max(np.abs(llr - linear)) / np.std(linear))
        self.assertLess(abw[2], LINEAR_REL_MAX, abw)
        self.assertLess(abw[5], LINEAR_REL_MAX, abw)

    def test_bayes_decoder_ohne_kalibrierung_erreicht_gauss_vorhersage(self) -> None:
        k = _kanaele()
        b = 2
        test = {s: trajektorien(k[s], T=T, dt=DT, ntraj=NTRAJ, seed=seed, bin_schritte=b, block=250, prozesse=6).dY_bins
                for s, seed in ((1, 41), (-1, 42))}
        llr = {s: log_likelihood_quotient(k[1], k[-1], test[s], DT * b, block=250, prozesse=6)[:, 0] for s in (1, -1)}
        tb = np.linspace(0.0, T, int(round(T / DT)) + 1)
        mp, mm = (mittelwert_record(k[s], tb) for s in (1, -1))
        vorhersage = decoder.gauss_vorhersage(mp[1:], mm[1:], DT)[-1]
        fr = decoder.bewerte(llr[1], llr[-1], decoder.Schwelle(0.0, True))     # Schwelle 0 = gleiche Priors
        self.assertGreater(vorhersage, 0.05)
        self.assertLess(fr.ci_unten, vorhersage)
        self.assertGreater(fr.ci_oben, vorhersage)

    def test_ohne_detektion_ist_der_llr_null(self) -> None:
        k = _kanaele(eta=0.0)
        rec = trajektorien(k[1], T=20.0, dt=DT, ntraj=20, seed=1, bin_schritte=2).dY_bins
        self.assertLess(float(np.max(np.abs(log_likelihood_quotient(k[1], k[-1], rec, DT * 2)))), 1e-14)


if __name__ == "__main__":
    unittest.main()
