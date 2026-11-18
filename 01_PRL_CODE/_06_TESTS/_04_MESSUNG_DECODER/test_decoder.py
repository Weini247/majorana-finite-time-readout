import math
import unittest

import numpy as np
from scipy.special import erfc

from _04_AUSWERTUNG_DIAGNOSTIK import decoder


class DecoderVertrag(unittest.TestCase):
    def test_schwelle_trennt_perfekt_getrennte_klassen(self) -> None:
        s = decoder.kalibriere_schwelle(np.array([3.0, 4.0, 5.0]), np.array([-1.0, 0.0, 1.0]))
        self.assertTrue(s.plus_oben)
        self.assertGreater(s.wert, 1.0)
        self.assertLess(s.wert, 3.0)
        fr = decoder.bewerte(np.array([3.0, 4.0]), np.array([0.0, 1.0]), s)
        self.assertEqual(fr.p_err, 0.0)

    def test_schwelle_erkennt_vertauschte_richtung(self) -> None:
        s = decoder.kalibriere_schwelle(np.array([-3.0, -4.0]), np.array([2.0, 3.0]))
        self.assertFalse(s.plus_oben)

    def test_fehlerrate_gaussscher_scores_entspricht_erfc(self) -> None:
        rng = np.random.default_rng(5)
        d = 1.5
        plus = rng.normal(+d / 2, 1.0, 200_000)
        minus = rng.normal(-d / 2, 1.0, 200_000)
        fr = decoder.bewerte(plus, minus, decoder.Schwelle(0.0, True))
        erwartet = 0.5 * erfc(d / (2 * math.sqrt(2)))
        self.assertLess(fr.ci_unten, erwartet)
        self.assertGreater(fr.ci_oben, erwartet)

    def test_gauss_vorhersage_ohne_trennung_ist_raten(self) -> None:
        mu = np.ones(50)
        self.assertAlmostEqual(float(decoder.gauss_vorhersage(mu, mu, 0.1)[-1]), 0.5, places=12)

    def test_gauss_vorhersage_faellt_monoton(self) -> None:
        p = decoder.gauss_vorhersage(np.full(100, 0.3), np.zeros(100), 0.5)
        self.assertTrue(np.all(np.diff(p) <= 0))

    def test_wilson_intervall_umschliesst_schaetzwert(self) -> None:
        fr = decoder.bewerte(np.array([1.0] * 90 + [-1.0] * 10), np.array([-1.0] * 95 + [1.0] * 5),
                             decoder.Schwelle(0.0, True))
        self.assertAlmostEqual(fr.p_err, 0.075)
        self.assertLess(fr.ci_unten, fr.p_err)
        self.assertGreater(fr.ci_oben, fr.p_err)


if __name__ == "__main__":
    unittest.main()
