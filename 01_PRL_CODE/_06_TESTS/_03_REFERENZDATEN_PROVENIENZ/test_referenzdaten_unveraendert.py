import unittest

from _05_INFRASTRUKTUR.referenzdaten.zenodo_benjadi_egger import ERWARTETE_MD5, lade_referenzdatei

ERWARTETE_FORMEN = {"fig3a.dat": (200, 5), "fig3c.dat": (101, 4), "fig3e.dat": (400, 5), "fig3g.dat": (81, 4)}


class ReferenzdatenVertrag(unittest.TestCase):
    def test_alle_zenodo_dateien_entsprechen_der_md5_aus_der_api(self) -> None:
        for name in ERWARTETE_MD5:
            with self.subTest(datei=name):
                self.assertEqual(lade_referenzdatei(name).md5, ERWARTETE_MD5[name])

    def test_formen_der_reproduktionsdateien(self) -> None:
        for name, form in ERWARTETE_FORMEN.items():
            with self.subTest(datei=name):
                self.assertEqual(lade_referenzdatei(name).daten.shape, form)


if __name__ == "__main__":
    unittest.main()
