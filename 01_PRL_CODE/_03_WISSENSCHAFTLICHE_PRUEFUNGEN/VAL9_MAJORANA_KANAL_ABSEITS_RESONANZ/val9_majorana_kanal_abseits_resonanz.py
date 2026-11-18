"""VAL9 — Konsistenz von Integrator und Bayes-Filter im Majorana-Kanal abseits der Resonanz (Etappe 3, F-3.4).

Anlass: EXP-E3 (Lauf EXP-E3_20261110T214052Z) war ungültig, weil der linearisierte Schritt
A = 1 - (iH + 1/2 sum L^dag L) dt bei ||H|| dt ~ 0.4-0.8 abseits von omega_stat die Dynamik verfälschte
(Trajektorienmittel bis 12 sigma neben mesolve, LLR für beide Paritäten positiv). VAL7/VAL8 laufen nur im
dispersiven Grenzfall bzw. am Resonanzpunkt und haben das nicht erfasst.

Referenzen:
  * Ensemblemittel der bedingten Records = unbedingte Mastergleichung (Wiseman & Milburn 2010, Kap. 4):
    E[dY]/dt = <c + c^dag>(t) aus mesolve.
  * Ein konsistenter Filter darf von der Binbreite nur schwach abhängen; Referenz ist die feine Binbreite.
Testfall: L01 starke Kopplung, n* = 0.3 (Cutoff 8), omega = 12.03 (I0, theta aus EXP-E2), eta = 0.5.
"""
from __future__ import annotations

import csv
import unittest

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import log_likelihood_quotient, messkanal_rwa, mittelwert_record, trajektorien
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT
from _08_ERGEBNISSE.exp_e1_endliche_messzeit import CUTOFF, ETA, _modell

OMEGA, BUDGET = 12.03, 0.3
DT, T, NTRAJ = 0.2, 400.0, 400
FENSTER = ((0, 250), (250, 500), (500, 1000))      # Bins à 0.4: [0,100), [100,200), [200,400)
Z_MAX = 4.0                                        # |emp - mu| / sem je Fenster (T4-artig, 6 Fenster)
LLR_REL_MAX = 0.35                                 # |mean LLR(0.4) - mean LLR(0.2)| / std LLR(0.2)


def _kanaele():
    with (PROJEKT_ROOT / "11_Processed_Outputs" / "EXP-E2_20261109T205736Z" / f"gauss_scan_n{BUDGET}.csv").open(
            encoding="utf-8") as h:
        ap = next({k: float(v) for k, v in z.items()} for z in csv.DictReader(h) if abs(float(z["omega"]) - OMEGA) < 1e-9)
    m = _modell()
    return {z: messkanal_rwa(buendel(m, OMEGA, ap["I0"], CUTOFF[BUDGET], paritaet=z), eta=ETA, theta=ap["theta"])[0]
            for z in (1, -1)}


class Val9MajoranaKanalAbseitsResonanz(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.k = _kanaele()
        cls.rec = {z: trajektorien(cls.k[z], T=T, dt=DT, ntraj=NTRAJ, seed=90 + z, bin_schritte=1, block=200,
                                   prozesse=2).dY_bins for z in (1, -1)}

    def test_trajektorienmittel_gleicht_der_mastergleichung(self) -> None:
        tb = np.arange(int(round(T / DT)) + 1) * DT
        for z in (1, -1):
            mu = mittelwert_record(self.k[z], tb)
            mu_bin = 0.5 * (mu[1:] + mu[:-1]) * DT
            for a, b in FENSTER:
                summe = self.rec[z][:, a:b].sum(axis=1)
                abw = (summe.mean() - mu_bin[a:b].sum()) / (summe.std(ddof=1) / np.sqrt(NTRAJ))
                self.assertLess(abs(abw), Z_MAX, f"z={z}, Bins {a}-{b}: {abw:.1f} sigma")

    def test_bayes_filter_haengt_kaum_von_der_binbreite_ab_und_trennt_die_paritaeten(self) -> None:
        for z in (1, -1):
            fein = log_likelihood_quotient(self.k[1], self.k[-1], self.rec[z], DT, block=200, prozesse=2)[:, 0]
            grob_rec = self.rec[z].reshape(NTRAJ, -1, 2).sum(axis=2)
            grob = log_likelihood_quotient(self.k[1], self.k[-1], grob_rec, 2 * DT, block=200, prozesse=2)[:, 0]
            self.assertLess(abs(grob.mean() - fein.mean()) / fein.std(), LLR_REL_MAX, (z, grob.mean(), fein.mean()))
            self.assertGreater(z * fein.mean(), 0.0)          # mittlerer LLR zeigt zur wahren Parität
            self.assertGreater(z * grob.mean(), 0.0)


if __name__ == "__main__":
    unittest.main()
