import math
import unittest
from dataclasses import replace

from _01_GRUNDLAGEN_FORMELN.einheiten import temperatur_in_lambda0
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import modell_stark
from _05_INFRASTRUKTUR.konfiguration.config import (AntriebsParameter, NumerikParameter, ParameterBuendel)


class ParameterpruefungVertrag(unittest.TestCase):
    def test_negative_raten_werden_abgelehnt(self) -> None:
        with self.assertRaises(ValueError):
            replace(modell_stark("gewoehnlich"), gamma=-0.1)

    def test_nicht_endliche_werte_werden_abgelehnt(self) -> None:
        with self.assertRaises(ValueError):
            replace(modell_stark("gewoehnlich"), epsilon=math.inf)

    def test_bool_ist_keine_zahl(self) -> None:
        with self.assertRaises(TypeError):
            replace(modell_stark("gewoehnlich"), t0=True)

    def test_verschwindende_resonatordaempfung_wird_abgelehnt(self) -> None:
        with self.assertRaises(ValueError):
            replace(modell_stark("gewoehnlich"), kappa_in=0.0, kappa_out=0.0)

    def test_paritaet_nur_plus_minus_eins(self) -> None:
        with self.assertRaises(ValueError):
            ParameterBuendel(modell=modell_stark("gewoehnlich"), antrieb=AntriebsParameter(12.0, 1e-3), paritaet=0)

    def test_unbekannter_loeser_wird_abgelehnt(self) -> None:
        with self.assertRaises(ValueError):
            NumerikParameter(loeser="beliebig")


class EinheitenVertrag(unittest.TestCase):
    def test_temperaturumrechnung_beider_konventionen(self) -> None:
        gewoehnlich = temperatur_in_lambda0(0.030, "gewoehnlich")
        kreis = temperatur_in_lambda0(0.030, "kreisfrequenz")
        self.assertAlmostEqual(gewoehnlich, 20.83661912 * 0.030 / 0.2, places=10)
        self.assertAlmostEqual(kreis / gewoehnlich, 2 * math.pi, places=12)

    def test_unbekannte_konvention_wird_abgelehnt(self) -> None:
        with self.assertRaises(ValueError):
            temperatur_in_lambda0(0.03, "beliebig")


if __name__ == "__main__":
    unittest.main()
