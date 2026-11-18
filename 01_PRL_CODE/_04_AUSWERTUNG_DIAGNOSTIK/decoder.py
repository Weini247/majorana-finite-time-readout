"""Decoder für Zwei-Hypothesen-Records (Parität z = +1 / -1) und Fehlerstatistik.

Ergebnisblind-Vertrag: Gewichte stammen nur aus dem Modell (Mittelwert-Records),
Schwellen nur aus Kalibrierrecords; Testrecords werden ausschließlich bewertet.
Fehlermaß: P_err = 1/2 [P(-|+) + P(+|-)] (gleiche Priors).
"""
from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.special import erfc
from scipy.stats import norm


def boxcar(dY_bins: np.ndarray, n_bins: int) -> np.ndarray:
    """Integrierter Record bis Bin n_bins."""
    return dY_bins[:, :n_bins].sum(axis=1)


def matched_filter(dY_bins: np.ndarray, gewichte: np.ndarray, n_bins: int) -> np.ndarray:
    """sum_k w_k dY_k mit w = mu_+ - mu_- (Modell), bis Bin n_bins."""
    return dY_bins[:, :n_bins] @ gewichte[:n_bins]


@dataclass(frozen=True)
class Schwelle:
    wert: float
    plus_oben: bool          # True: Score > wert -> z = +1


def kalibriere_schwelle(score_plus: np.ndarray, score_minus: np.ndarray) -> Schwelle:
    """Empirisch fehlerminimierende Schwelle auf Kalibrierdaten (Gleichstand: Mittelpunkt)."""
    plus_oben = bool(np.mean(score_plus) >= np.mean(score_minus))
    kandidaten = np.sort(np.concatenate([score_plus, score_minus]))
    mitten = 0.5 * (kandidaten[1:] + kandidaten[:-1])
    if mitten.size == 0:
        return Schwelle(float(kandidaten[0]), plus_oben)
    sp, sm = np.sort(score_plus), np.sort(score_minus)
    if plus_oben:
        fehler = 0.5 * (np.searchsorted(sp, mitten, side="right") / sp.size
                        + (sm.size - np.searchsorted(sm, mitten, side="right")) / sm.size)
    else:
        fehler = 0.5 * ((sp.size - np.searchsorted(sp, mitten, side="right")) / sp.size
                        + np.searchsorted(sm, mitten, side="right") / sm.size)
    besten = np.flatnonzero(fehler == fehler.min())
    return Schwelle(float(np.median(mitten[besten])), plus_oben)


@dataclass(frozen=True)
class Fehlerrate:
    p_err: float
    ci_unten: float
    ci_oben: float
    n_plus: int
    n_minus: int


def _wilson(k: int, n: int, z: float) -> tuple[float, float]:
    if n == 0:
        return 0.0, 1.0
    p = k / n
    nenner = 1 + z * z / n
    mitte = (p + z * z / (2 * n)) / nenner
    breite = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / nenner
    return max(0.0, mitte - breite), min(1.0, mitte + breite)


def bewerte(score_plus: np.ndarray, score_minus: np.ndarray, s: Schwelle, konfidenz: float = 0.95) -> Fehlerrate:
    """P_err mit 95-%-Intervall: Wilson je Klasse, kombiniert als Mittel der Grenzen (konservativ)."""
    if s.plus_oben:
        k_plus = int(np.sum(score_plus <= s.wert)); k_minus = int(np.sum(score_minus > s.wert))
    else:
        k_plus = int(np.sum(score_plus >= s.wert)); k_minus = int(np.sum(score_minus < s.wert))
    z = norm.ppf(0.5 + konfidenz / 2)
    lp, up = _wilson(k_plus, score_plus.size, z)
    lm, um = _wilson(k_minus, score_minus.size, z)
    p = 0.5 * (k_plus / score_plus.size + k_minus / score_minus.size)
    return Fehlerrate(p_err=p, ci_unten=0.5 * (lp + lm), ci_oben=0.5 * (up + um),
                      n_plus=int(score_plus.size), n_minus=int(score_minus.size))


def gauss_vorhersage(mu_plus: np.ndarray, mu_minus: np.ndarray, dt_bin: float) -> np.ndarray:
    """Gauß-Benchmark (deterministische Mittelwerte + weißes Rauschen, Einheitsvarianz pro Zeit):
    SNR^2(T) = int_0^T (mu_+ - mu_-)^2 dt,  P_err(T) = 1/2 erfc(SNR / (2 sqrt 2)), kumulativ über Bins."""
    snr2 = np.cumsum((mu_plus - mu_minus) ** 2) * dt_bin
    return 0.5 * erfc(np.sqrt(snr2) / (2.0 * math.sqrt(2.0)))
