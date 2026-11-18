"""VAL4 — Benjadi & Egger, Phys. Rev. B (2026), arXiv:2603.06482v2, Fig. 3; Daten Zenodo 10.5281/zenodo.20623730.

Geprüft wird nur, was als REPRODUCED geführt wird (EXP-R1, Akzeptanzregel 1 % des Kurvenmaßstabs):
  * fig3a Spalten 2/4 = |A_sc|^2, arg A_sc nach Eq. (20), starke Kopplung
  * fig3e Spalten 2/4 = |A_sc|^2, arg A_sc nach Eq. (26) mit chi_z aus Eq. (22), schwache Kopplung
  * Konventionsdiskriminierung: lambda0 = h * 0.2 GHz ('gewoehnlich'); 'kreisfrequenz' verletzt die Regel deutlich
Die exakten Spalten (3/5) und fig3c sind NICHT reproduziert (Status BLOCKED, siehe 07_BEFUNDE.md F-1.3).
"""
from __future__ import annotations

import unittest

import numpy as np

from _01_GRUNDLAGEN_FORMELN import semiklassik as sk
from _01_GRUNDLAGEN_FORMELN.abgeleitete_groessen import abgeleitete_groessen
from _01_GRUNDLAGEN_FORMELN.einheiten import ghz_nach_lambda0
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import modell_schwach, modell_stark
from _05_INFRASTRUKTUR.konfiguration.config import AntriebsParameter
from _05_INFRASTRUKTUR.referenzdaten.zenodo_benjadi_egger import lade_referenzdatei

REPRODUKTION_REL_SKALA = 1.0e-2     # T3, EXP-R1 §4 primär
MEDIAN_REL_MAX = 2.0e-2             # EXP-R1 §4 sekundär
NEGATIVKONTROLLE_FAKTOR = 3.0       # EXP-R1 §5: zweitbeste Variante muss um Faktor >= 3 schlechter sein


def _vergleich(modell, name: str, formel) -> tuple[float, float, float]:
    ref = lade_referenzdatei(name).daten
    A = np.array([formel(modell, abgeleitete_groessen(modell, AntriebsParameter(ghz_nach_lambda0(x), 1.0), 1))
                  for x in ref[:, 0]])
    betrag = np.abs(np.abs(A) ** 2 - ref[:, 1]) / np.abs(ref[:, 1]).max()
    phase = np.abs(np.angle(A) - ref[:, 3]) / np.abs(ref[:, 3]).max()
    median_rel = float(np.median(np.abs(np.abs(A) ** 2 - ref[:, 1]) / np.abs(ref[:, 1])))
    return float(betrag.max()), float(phase.max()), median_rel


class Val4BenjadiEggerFig3(unittest.TestCase):
    def test_semiklassische_amplitude_starke_kopplung_fig3a(self) -> None:
        b, p, med = _vergleich(modell_stark("gewoehnlich"), "fig3a.dat", sk.amplitude_semiklassisch_stark)
        self.assertLess(b, REPRODUKTION_REL_SKALA)
        self.assertLess(p, REPRODUKTION_REL_SKALA)
        self.assertLess(med, MEDIAN_REL_MAX)

    def test_semiklassische_amplitude_schwache_kopplung_fig3e(self) -> None:
        b, p, med = _vergleich(modell_schwach("gewoehnlich"), "fig3e.dat", sk.amplitude_semiklassisch_schwach)
        self.assertLess(b, REPRODUKTION_REL_SKALA)
        self.assertLess(p, REPRODUKTION_REL_SKALA)
        self.assertLess(med, MEDIAN_REL_MAX)

    def test_kreisfrequenz_konvention_wird_von_den_daten_verworfen(self) -> None:
        gut = max(_vergleich(modell_stark("gewoehnlich"), "fig3a.dat", sk.amplitude_semiklassisch_stark)[:2])
        schlecht = max(_vergleich(modell_stark("kreisfrequenz"), "fig3a.dat", sk.amplitude_semiklassisch_stark)[:2])
        self.assertGreater(schlecht, REPRODUKTION_REL_SKALA)
        self.assertGreater(schlecht / gut, NEGATIVKONTROLLE_FAKTOR)


if __name__ == "__main__":
    unittest.main()
