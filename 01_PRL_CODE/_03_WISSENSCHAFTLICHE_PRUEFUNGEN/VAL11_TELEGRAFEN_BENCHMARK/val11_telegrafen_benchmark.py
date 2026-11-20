"""VAL11 — Paritätswechsel im dispersiven Grenzfall gegen einen klassischen Telegrafen-Benchmark (Etappe 6, V6-4/V6-6).

Testfall: Resonator allein, H_± = ±chi a^dag a + i E (a^dag - a), Vakuum als Start, Homodyn bei theta = pi/2.
Die Parität ±1 wechselt als Telegrafenprozess (ADR-0006, U = 1: der Resonatorzustand bleibt beim Wechsel erhalten).
Referenz (unabhängig vom Quantencode): Bei linearer Dynamik bleibt der Resonator kohärent, alpha folgt
  d alpha/dt = -(i s(t) chi + kappa/2) alpha + E,     s(t) = Paritätsverlauf,
und der Record ist bei gegebenem Verlauf exakt dY = mu(alpha) dt + dW mit mu = 2 sqrt(eta kappa) Im(alpha)
(Wiseman & Milburn 2010, Kap. 4; vgl. referenzfaelle_dispersiv.alpha_analytisch). Wegen alpha_- = conj(alpha_+)
ist mu antisymmetrisch, der Boxcar-Decoder hat die Schwelle 0, und seine Fehlerrate ist
  P = E_s[ Phi(-m[s] / sqrt(T)) ],   m[s] = sum_k mu(alpha_k) dt   (linker Punkt wie im Integrator).
Der Erwartungswert über Verläufe wird klassisch per Monte Carlo berechnet (Wechsel nach jedem Schritt mit
Wahrscheinlichkeit 1 - exp(-gamma dt), wie im Integrator).
V6-6: Der Wonham-Filter ist auf denselben Testdaten nicht schlechter als der Boxcar-Decoder.
"""
from __future__ import annotations

import math
import unittest

import numpy as np
import qutip as qt
from scipy.special import ndtr

from _02_AUSFUEHRUNG.homodyn_trajektorien import Messkanal
from _02_AUSFUEHRUNG.paritaetswechsel import log_likelihood_quotient_mit_wechsel, trajektorien_mit_wechsel

CHI, KAPPA, E, ETA, CUTOFF = 0.1, 0.2, 0.14, 0.5, 15         # |alpha_ss| = 1, chi = kappa/2
DT, T, BIN = 0.2, 20.0, 1
GAMMA = 1.0 / 20.0
NTRAJ = 2000                                                  # je Startparität
N_MC = 200_000                                                # klassische Verläufe
Z_MAX = 4.0


def _kanal(s: int) -> Messkanal:
    a = qt.destroy(CUTOFF)
    H = s * CHI * a.dag() * a + 1j * E * (a.dag() - a)
    unbeob = (math.sqrt((1.0 - ETA) * KAPPA) * a,)
    c = math.sqrt(ETA * KAPPA) * np.exp(-1j * math.pi / 2) * a
    return Messkanal(H=H, unbeobachtet=unbeob, beobachtet=c, rho0=qt.fock_dm(CUTOFF, 0))


def boxcar_vorhersage(gamma: float, start: int, seed: int = 11) -> float:
    """Klassischer Telegrafen-Benchmark: Fehlerrate des Boxcar-Decoders (Schwelle 0) bei Startparität start."""
    rng = np.random.default_rng(seed)
    n = int(round(T / DT))
    p = -math.expm1(-gamma * DT)
    s = np.full(N_MC, start, dtype=float)
    alpha = np.zeros(N_MC, dtype=complex)
    m = np.zeros(N_MC)
    lam = {1: 1j * CHI + KAPPA / 2, -1: -1j * CHI + KAPPA / 2}
    ss = {k: E / v for k, v in lam.items()}
    fak = {k: np.exp(-v * DT) for k, v in lam.items()}
    for _ in range(n):
        m += 2.0 * math.sqrt(ETA * KAPPA) * alpha.imag * DT
        plus = s > 0
        alpha = np.where(plus, ss[1] + (alpha - ss[1]) * fak[1], ss[-1] + (alpha - ss[-1]) * fak[-1])
        if p > 0:
            s = np.where(rng.random(N_MC) < p, -s, s)
    # Fehler: Vorzeichen des Boxcar-Scores entgegen der Startparität; mu > 0 gehört zu s = -1 (Im alpha_- > 0)
    return float(np.mean(ndtr(start * m / math.sqrt(T))))


def _wilson_z(k: int, n: int, p: float) -> float:
    return (k / n - p) / math.sqrt(p * (1 - p) / n)


class Val11TelegrafenBenchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.k = {1: _kanal(1), -1: _kanal(-1)}
        cls.daten = {}
        for gamma in (0.0, GAMMA):
            cls.daten[gamma] = {z: trajektorien_mit_wechsel(cls.k[1], cls.k[-1], gamma_qp=gamma, start=z, T=T, dt=DT,
                                                            ntraj=NTRAJ, seed=1100 + 10 * int(gamma > 0) + z,
                                                            bin_schritte=BIN, block=500, prozesse=2).dY_bins
                                for z in (1, -1)}

    def _boxcar_fehler(self, gamma: float, z: int) -> int:
        score = self.daten[gamma][z].sum(axis=1)
        return int(np.sum(z * score > 0))            # z = +1 hat mu < 0: Fehler bei positivem Score

    def test_boxcar_ohne_wechsel_gleicht_der_analytischen_gauss_vorhersage(self) -> None:
        for z in (1, -1):
            p = boxcar_vorhersage(0.0, z)
            self.assertLess(abs(_wilson_z(self._boxcar_fehler(0.0, z), NTRAJ, p)), Z_MAX, (z, p))

    def test_boxcar_mit_wechsel_gleicht_dem_klassischen_telegrafen_benchmark(self) -> None:
        for z in (1, -1):
            p, p_ohne = boxcar_vorhersage(GAMMA, z), boxcar_vorhersage(0.0, z)
            k = self._boxcar_fehler(GAMMA, z)
            self.assertLess(abs(_wilson_z(k, NTRAJ, p)), Z_MAX, (z, k / NTRAJ, p))
            self.assertGreater(abs(_wilson_z(k, NTRAJ, p_ohne)), Z_MAX, (z, k / NTRAJ, p_ohne))   # Trennschärfe

    def test_wonham_filter_ist_nicht_schlechter_als_der_boxcar_decoder(self) -> None:
        for z in (1, -1):
            dY = self.daten[GAMMA][z]
            llr = log_likelihood_quotient_mit_wechsel(self.k[1], self.k[-1], GAMMA, dY, DT * BIN, block=500,
                                                      prozesse=2)[:, 0]
            bayes_falsch = z * llr < 0
            box_falsch = z * dY.sum(axis=1) > 0
            diff = bayes_falsch.astype(float) - box_falsch.astype(float)       # gepaarter Vergleich
            self.assertLess(diff.mean() / (diff.std(ddof=1) / math.sqrt(NTRAJ)), Z_MAX, z)


if __name__ == "__main__":
    unittest.main()
