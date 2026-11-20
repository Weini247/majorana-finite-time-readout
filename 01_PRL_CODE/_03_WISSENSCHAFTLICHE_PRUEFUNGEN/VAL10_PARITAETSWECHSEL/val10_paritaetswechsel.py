"""VAL10 — Paritätswechsel während der Messung: Modell, Integrator und Wonham-Filter (Etappe 6, ADR-0006).

Prüft V6-0 bis V6-3 und die Kalibrierung des Filters aus ETAPPE_6_PLAN.md §5.
Referenzen:
  * V6-0: Rabi-Eigenbasis des Doppelpunkts H_d = eps sigma_z + Re(t_z) sigma_x + Im(t_z) sigma_y (L01 Eqs. 2-4,
    Laborbasis); bei eps = 0, phi = 0 ist t_z = t0 ± t1 reell positiv, beide Paritäten haben dieselbe Basis (U = 1).
  * V6-1: gamma_qp = 0 muss den Etappe-3-Code bitgenau reproduzieren.
  * V6-2: Ensemblemittel der Records = gekoppelte Mastergleichung (erweiterter Raum, mesolve), abseits der
    Resonanz (Lehre aus F-3.4).
  * V6-3: Telegrafenprozess: Anteil mit gekippter Parität = 1/2 (1 - exp(-2 gamma t)).
  * Kalibrierung: Für den exakten Bayes-Filter ist die Posterior-Konfidenz sigma(|LLR|) im Mittel gleich der
    Trefferquote. Negativkontrolle: der Filter ohne Wechsel (gamma = 0) ist auf denselben Daten überkonfident.
Testfall: L01 stark, n* = 0.3 (Cutoff 8), omega = 12.03 (I0, theta aus EXP-E2), eta = 0.5. Prüfrate
gamma_qp = 1/200 (unphysikalisch groß, damit Wechsel in T = 400 häufig sind).
"""
from __future__ import annotations

import cmath
import csv
import unittest

import numpy as np

from _02_AUSFUEHRUNG.homodyn_trajektorien import log_likelihood_quotient, messkanal_rwa, trajektorien
from _02_AUSFUEHRUNG.paritaetswechsel import (log_likelihood_quotient_mit_wechsel, mittelwert_record_mit_wechsel,
                                             trajektorien_mit_wechsel)
from _03_WISSENSCHAFTLICHE_PRUEFUNGEN.referenzfaelle import buendel
from _05_INFRASTRUKTUR.runtime.provenienz import PROJEKT_ROOT
from _08_ERGEBNISSE._02_ENDLICHE_MESSZEIT.exp_e1_endliche_messzeit import CUTOFF, ETA, _modell

OMEGA, BUDGET = 12.03, 0.3
GAMMA = 1.0 / 200.0
DT, BIN, T, NTRAJ = 0.2, 2, 400.0, 400
FENSTER = ((0, 250), (250, 500), (500, 1000))       # Schritte à 0.2 = Bins à 0.4 / 2
Z_MAX = 4.0                                         # wie VAL9
BASIS_MIN = 1.0 - 1e-12                             # V6-0, T1
BASIS_KONTROLLE_MAX = 1.0 - 1e-4                    # V6-0 Negativkontrolle phi = 0.1
IDENTISCH_MAX = 1e-10                               # V6-1, T2


def _kanaele():
    with (PROJEKT_ROOT / "11_Processed_Outputs" / "EXP-E2_20261109T205736Z" / f"gauss_scan_n{BUDGET}.csv").open(
            encoding="utf-8") as h:
        ap = next({k: float(v) for k, v in z.items()} for z in csv.DictReader(h) if abs(float(z["omega"]) - OMEGA) < 1e-9)
    m = _modell()
    return {z: messkanal_rwa(buendel(m, OMEGA, ap["I0"], CUTOFF[BUDGET], paritaet=z), eta=ETA, theta=ap["theta"])[0]
            for z in (1, -1)}


def _rabi_basis(eps: float, t0: float, t1: float, phi: float, z: int) -> np.ndarray:
    t_z = t0 + z * t1 * cmath.exp(1j * phi)
    H = np.array([[eps, np.conj(t_z)], [t_z, -eps]])
    w, v = np.linalg.eigh(H)
    return v[:, ::-1]                                   # Spalte 0 = obere Energie (Konventionen §2)


def _ueberlapp(eps: float, phi: float) -> float:
    m = _modell()
    vp, vm = _rabi_basis(eps, m.t0, m.t1, phi, 1), _rabi_basis(eps, m.t0, m.t1, phi, -1)
    return float(min(abs(np.vdot(vp[:, i], vm[:, i])) for i in range(2)))


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


class Val10Paritaetswechsel(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.k = _kanaele()
        cls.r = {z: trajektorien_mit_wechsel(cls.k[1], cls.k[-1], gamma_qp=GAMMA, start=z, T=T, dt=DT, ntraj=NTRAJ,
                                             seed=100 + z, bin_schritte=BIN, block=200, prozesse=2) for z in (1, -1)}

    def test_rabi_basen_beider_paritaeten_stimmen_bei_den_l01_parametern_ueberein(self) -> None:
        m = _modell()
        self.assertEqual((m.epsilon, m.phi), (0.0, 0.0))
        self.assertGreater(_ueberlapp(0.0, 0.0), BASIS_MIN)
        self.assertLess(_ueberlapp(0.0, 0.1), BASIS_KONTROLLE_MAX)       # Negativkontrolle: U != 1

    def test_ohne_wechsel_identisch_mit_dem_bisherigen_integrator_und_filter(self) -> None:
        for z in (1, -1):
            alt = trajektorien(self.k[z], T=40.0, dt=DT, ntraj=60, seed=7 + z, bin_schritte=BIN, block=25)
            neu = trajektorien_mit_wechsel(self.k[1], self.k[-1], gamma_qp=0.0, start=z, T=40.0, dt=DT, ntraj=60,
                                           seed=7 + z, bin_schritte=BIN, block=25)
            self.assertLessEqual(np.max(np.abs(alt.dY_bins - neu.dY_bins)), IDENTISCH_MAX)
            self.assertTrue(np.all(neu.paritaet_bins == z))
            l_alt = log_likelihood_quotient(self.k[1], self.k[-1], alt.dY_bins, DT * BIN, checkpunkte=[50, 100], block=25)
            l_neu = log_likelihood_quotient_mit_wechsel(self.k[1], self.k[-1], 0.0, alt.dY_bins, DT * BIN,
                                                        checkpunkte=[50, 100], block=25)
            self.assertLessEqual(np.max(np.abs(l_alt - l_neu)), IDENTISCH_MAX)

    def test_trajektorienmittel_gleicht_der_gekoppelten_mastergleichung(self) -> None:
        tb = np.arange(int(round(T / DT)) + 1) * DT
        for z in (1, -1):
            # Konsistenzprüfung wie VAL9 (fängt grobe Integratorfehler). Trennschärfe gegen das Modell ohne Wechsel
            # ist hier gering (gemessen 0.9 sigma, 2026-11-18): der Wechsel ändert den Mittelwert-Record bei
            # 400 Trajektorien kaum messbar. Trennscharf für die Wechsel sind V6-3 und die Filterkalibrierung.
            mu = mittelwert_record_mit_wechsel(self.k[1], self.k[-1], GAMMA, z, tb)
            schritt = (0.5 * (mu[1:] + mu[:-1]) * DT).reshape(-1, BIN).sum(axis=1)
            for a, b in FENSTER:
                summe = self.r[z].dY_bins[:, a // BIN:b // BIN].sum(axis=1)
                sem = summe.std(ddof=1) / np.sqrt(NTRAJ)
                abw = (summe.mean() - schritt[a // BIN:b // BIN].sum()) / sem
                self.assertLess(abs(abw), Z_MAX, f"z={z}, Schritte {a}-{b}: {abw:.1f} sigma")

    def test_anteil_gekippter_trajektorien_folgt_dem_telegrafenprozess(self) -> None:
        zeiten = self.r[1].zeiten_bins
        for z in (1, -1):
            for t in (100.0, 200.0, 400.0):
                k = int(np.argmin(np.abs(zeiten - t)))
                p = 0.5 * (1.0 - np.exp(-2.0 * GAMMA * zeiten[k]))
                emp = float(np.mean(self.r[z].paritaet_bins[:, k] != z))
                self.assertLess(abs(emp - p) / np.sqrt(p * (1 - p) / NTRAJ), Z_MAX, (z, t, emp, p))

    def test_wonham_filter_ist_kalibriert_und_der_filter_ohne_wechsel_ueberkonfident(self) -> None:
        def kalibrierung(gamma):
            abw = []
            for z in (1, -1):
                l = log_likelihood_quotient_mit_wechsel(self.k[1], self.k[-1], gamma, self.r[z].dY_bins, DT * BIN,
                                                        block=200, prozesse=2)[:, 0]
                treffer = (z * l > 0).astype(float)
                abw.append(treffer - _sigmoid(np.abs(l)))
                if gamma > 0:
                    self.assertGreater(z * l.mean(), 0.0)             # E_z[z LLR] = KL >= 0 für den exakten Filter
            abw = np.concatenate(abw)
            return abw.mean() / (abw.std(ddof=1) / np.sqrt(abw.size))
        z_mit, z_ohne = kalibrierung(GAMMA), kalibrierung(0.0)
        self.assertLess(abs(z_mit), Z_MAX, f"Wonham-Filter: Kalibrierung {z_mit:.1f} sigma")
        self.assertLess(z_ohne, -Z_MAX, f"Filter ohne Wechsel: nur {z_ohne:.1f} sigma überkonfident")


if __name__ == "__main__":
    unittest.main()
