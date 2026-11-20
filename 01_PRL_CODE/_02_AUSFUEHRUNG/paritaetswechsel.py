"""Homodynmessung mit Paritätswechsel während der Messung (Etappe 6, ADR-0006).

Modell: rho = rho_+ ⊕ rho_-; jeder Block folgt dem RWA-Lindblad-Modell seiner Parität (gleicher Messkanal),
dazu Telegrafenprozess mit Rate gamma_qp je Richtung:
  d rho_±/dt = L_± rho_± + gamma_qp (rho_∓ - rho_±)      (U = 1, nur für epsilon = 0, phi = 0; V6-0)
Trajektorien: wahrer Paritätsverlauf als Poisson-Prozess (eigener Zufallsstrom), bedingter Zustand mit dem
Rouchon-Ralph-Schritt des aktuellen Sektors (exakte Entfaltung, weil U = 1 und die Rate zustandsunabhängig ist).
Bayes-Filter: je Anfangsparität ein gekoppelter Filter (Wonham-artig). Für gamma_qp = 0 identisch mit
homodyn_trajektorien (V6-1).
Dieses Modul kennt keine Auswertung.
"""
from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import numpy as np
import qutip as qt

from _02_AUSFUEHRUNG.homodyn_trajektorien import (
    _BLAS_VARIABLEN, Messkanal, TrajektorienFehler, _rr_schritt, _sparse_superoperatoren,
)


@dataclass(frozen=True)
class WechselErgebnis:
    zeiten_bins: np.ndarray        # Endzeit jedes Bins
    dY_bins: np.ndarray            # (ntraj, nbins)
    paritaet_bins: np.ndarray      # (ntraj, nbins) int8: wahre Parität am Ende jedes Bins (Diagnose, nie für Decoder)
    start: int
    gamma_qp: float
    dt: float
    seed: int


def _pruefe_kanaele(kanal_plus: Messkanal, kanal_minus: Messkanal) -> None:
    if np.max(np.abs(kanal_plus.beobachtet.full() - kanal_minus.beobachtet.full())) > 1e-14:
        raise ValueError("beide Paritäten müssen denselben Messkanal (eta, theta, kappa_out) haben")
    if kanal_plus.H.dims != kanal_minus.H.dims:
        raise ValueError("beide Paritäten müssen denselben Hilbertraum haben")


def _wechsel_rng(quelle) -> np.random.Generator:
    """Eigener Strom für die Paritätswechsel; der Rauschstrom bleibt wie in homodyn_trajektorien (V6-1)."""
    ss = quelle if isinstance(quelle, np.random.SeedSequence) else np.random.SeedSequence(quelle)
    return np.random.default_rng(np.random.SeedSequence(entropy=ss.entropy, spawn_key=tuple(ss.spawn_key) + (2 ** 20,)))


def _simuliere_block_wechsel(ops, x_vec, d, rho0_vec, start, p_wechsel, n, n_schritte, dt, bin_schritte,
                             pruefintervall, rng_quelle):
    rng = np.random.default_rng(rng_quelle)
    rng_w = _wechsel_rng(rng_quelle) if p_wechsel > 0 else None
    spur_idx = np.arange(d) * (d + 1)
    W = np.repeat(rho0_vec[:, None], n, axis=1)
    z = np.full(n, start, dtype=np.int8)
    nbins = n_schritte // bin_schritte
    dY_bins = np.zeros((n, nbins))
    par_bins = np.zeros((n, nbins), dtype=np.int8)
    wurzel_dt = math.sqrt(dt)
    for schritt in range(n_schritte):
        erw = np.real(x_vec @ W)
        dY = erw * dt + rng.standard_normal(n) * wurzel_dt
        plus = z == 1
        if plus.all():
            W = _rr_schritt(ops[1], W, dY)
        elif not plus.any():
            W = _rr_schritt(ops[-1], W, dY)
        else:
            ip, im = np.flatnonzero(plus), np.flatnonzero(~plus)
            neu = np.empty_like(W)
            neu[:, ip] = _rr_schritt(ops[1], W[:, ip], dY[ip])
            neu[:, im] = _rr_schritt(ops[-1], W[:, im], dY[im])
            W = neu
        spur = np.real(W[spur_idx].sum(axis=0))
        W /= spur[None, :]
        if rng_w is not None:
            kippt = rng_w.random(n) < p_wechsel
            z[kippt] = -z[kippt]
        k = schritt // bin_schritte
        dY_bins[:, k] += dY
        par_bins[:, k] = z
        if schritt % pruefintervall == 0:
            rho = W.T.reshape(n, d, d)
            herm = np.max(np.abs(rho - np.conj(np.transpose(rho, (0, 2, 1)))))
            if not np.isfinite(herm) or herm > 1e-8 or np.any(spur <= 0):
                raise TrajektorienFehler(f"Schritt {schritt}: Hermitizitätsfehler {herm:.2e} oder Spur <= 0")
    return dY_bins, par_bins, W


def _block_aufgabe_wechsel(args):
    return _simuliere_block_wechsel(*args)


def _verteile(funktion, aufgaben, prozesse):
    if prozesse > 1 and len(aufgaben) > 1:
        alt = {v: os.environ.get(v) for v in _BLAS_VARIABLEN}
        os.environ.update({v: "1" for v in _BLAS_VARIABLEN})
        try:
            with ProcessPoolExecutor(max_workers=prozesse) as pool:
                return list(pool.map(funktion, aufgaben))
        finally:
            for v, w in alt.items():
                if w is None:
                    os.environ.pop(v, None)
                else:
                    os.environ[v] = w
    return [funktion(a) for a in aufgaben]


def trajektorien_mit_wechsel(kanal_plus: Messkanal, kanal_minus: Messkanal, *, gamma_qp: float, start: int,
                             T: float, dt: float, ntraj: int, seed: int, bin_schritte: int = 10,
                             pruefintervall: int = 200, block: int | None = None, prozesse: int = 1) -> WechselErgebnis:
    """Bedingte Homodyn-Trajektorien mit Paritätswechsel; Startparität start, Startzustand rho0 des Startsektors.

    Seeds und Blockaufteilung wie homodyn_trajektorien.trajektorien: für gamma_qp = 0 identische Records (V6-1).
    """
    if start not in (1, -1):
        raise ValueError("start muss +1 oder -1 sein")
    if gamma_qp < 0:
        raise ValueError("gamma_qp muss >= 0 sein")
    _pruefe_kanaele(kanal_plus, kanal_minus)
    n_schritte = int(round(T / dt))
    if abs(n_schritte * dt - T) > 1e-9 * max(T, 1.0):
        raise ValueError("T muss ein ganzzahliges Vielfaches von dt sein")
    if n_schritte % bin_schritte:
        raise ValueError("Schrittzahl muss durch bin_schritte teilbar sein")
    ops_p, x_vec, d = _sparse_superoperatoren(kanal_plus, dt)
    ops_m, _, _ = _sparse_superoperatoren(kanal_minus, dt)
    ops = {1: ops_p, -1: ops_m}
    rho0_vec = (kanal_plus if start == 1 else kanal_minus).rho0.full().ravel()
    p_wechsel = -math.expm1(-gamma_qp * dt)
    if block is None or block >= ntraj:
        groessen, quellen = [ntraj], [seed]
    else:
        groessen = [block] * (ntraj // block) + ([ntraj % block] if ntraj % block else [])
        quellen = np.random.SeedSequence(seed).spawn(len(groessen))
    aufgaben = [(ops, x_vec, d, rho0_vec, start, p_wechsel, n, n_schritte, dt, bin_schritte, pruefintervall, q)
                for n, q in zip(groessen, quellen)]
    teile = _verteile(_block_aufgabe_wechsel, aufgaben, prozesse)
    dY_bins = np.concatenate([t[0] for t in teile], axis=0)
    par_bins = np.concatenate([t[1] for t in teile], axis=0)
    rho = np.concatenate([t[2].T.reshape(-1, d, d) for t in teile], axis=0)
    eig_min = float(np.min(np.linalg.eigvalsh(0.5 * (rho + np.conj(np.transpose(rho, (0, 2, 1)))))))
    if eig_min < -1e-8:
        raise TrajektorienFehler(f"bedingter Zustand nicht positiv: lambda_min = {eig_min:.2e}")
    zeiten = dt * bin_schritte * np.arange(1, n_schritte // bin_schritte + 1)
    return WechselErgebnis(zeiten_bins=zeiten, dY_bins=dY_bins, paritaet_bins=par_bins, start=start,
                           gamma_qp=gamma_qp, dt=dt, seed=seed)


def gekoppelte_mastergleichung(kanal_plus: Messkanal, kanal_minus: Messkanal, gamma_qp: float, start: int):
    """Erweiterter Raum (Parität ⊗ System): H, c_ops, rho0 und x = 1 ⊗ (c + c^dag) für qutip.mesolve."""
    _pruefe_kanaele(kanal_plus, kanal_minus)
    P = {1: qt.fock_dm(2, 0), -1: qt.fock_dm(2, 1)}
    k = {1: kanal_plus, -1: kanal_minus}
    eins = qt.qeye(kanal_plus.H.dims[0])
    H = sum(qt.tensor(P[z], k[z].H) for z in (1, -1))
    c_ops = [qt.tensor(P[z], L) for z in (1, -1) for L in list(k[z].unbeobachtet) + [k[z].beobachtet]]
    if gamma_qp > 0:
        c_ops.append(math.sqrt(gamma_qp) * qt.tensor(qt.sigmax(), eins))
    rho0 = qt.tensor(P[start], k[start].rho0)
    x = qt.tensor(qt.qeye(2), kanal_plus.beobachtet + kanal_plus.beobachtet.dag())
    return H, c_ops, rho0, x


def mittelwert_record_mit_wechsel(kanal_plus: Messkanal, kanal_minus: Messkanal, gamma_qp: float, start: int,
                                  zeiten: np.ndarray) -> np.ndarray:
    """mu(t) = E[dY]/dt bei Startparität start, aus der gekoppelten Mastergleichung."""
    H, c_ops, rho0, x = gekoppelte_mastergleichung(kanal_plus, kanal_minus, gamma_qp, start)
    opts = {"atol": 1e-10, "rtol": 1e-8, "nsteps": 10 ** 6}
    res = qt.mesolve(H, rho0, zeiten, c_ops=c_ops, e_ops=[x], options=opts)
    return np.real(np.asarray(res.expect[0]))


def _llr_block_wechsel(S, x_vec, d, rho0, p_wechsel, dY_bins, dt_bin, checkpunkte):
    """Zwei gekoppelte Filter (Hypothese Anfangsparität h = ±1), je mit Blöcken W[h][z]."""
    n, nbins = dY_bins.shape
    spur_idx = np.arange(d) * (d + 1)
    W = {h: {h: np.repeat(rho0[h][:, None], n, axis=1), -h: None} for h in (1, -1)}
    llr = np.zeros(n)
    aus = np.zeros((n, len(checkpunkte)))
    ziel = {k: i for i, k in enumerate(checkpunkte)}
    for k in range(nbins):
        dY = dY_bins[:, k]
        erw = {}
        for h in (1, -1):
            gesamt = W[h][h] if W[h][-h] is None else W[h][h] + W[h][-h]
            erw[h] = np.real(x_vec @ gesamt)
        llr += (erw[1] - erw[-1]) * dY - 0.5 * (erw[1] ** 2 - erw[-1] ** 2) * dt_bin
        for h in (1, -1):
            for z in (1, -1):
                if W[h][z] is not None:
                    W[h][z] = _rr_schritt(S[z], W[h][z], dY)
            if p_wechsel > 0:
                a, b = W[h][1], W[h][-1]
                a = np.zeros_like(b) if a is None else a
                b = np.zeros_like(a) if b is None else b
                W[h][1], W[h][-1] = (1 - p_wechsel) * a + p_wechsel * b, (1 - p_wechsel) * b + p_wechsel * a
            spur = sum(np.real(W[h][z][spur_idx].sum(axis=0)) for z in (1, -1) if W[h][z] is not None)
            if np.any(~np.isfinite(spur)) or np.any(spur <= 0):
                raise TrajektorienFehler(f"Filter h={h}, Bin {k}: Spur <= 0")
            for z in (1, -1):
                if W[h][z] is not None:
                    W[h][z] /= spur[None, :]
        if k + 1 in ziel:
            aus[:, ziel[k + 1]] = llr
    return aus


def _llr_aufgabe_wechsel(args):
    return _llr_block_wechsel(*args)


def log_likelihood_quotient_mit_wechsel(kanal_plus: Messkanal, kanal_minus: Messkanal, gamma_qp: float,
                                        dY_bins: np.ndarray, dt_bin: float, *, checkpunkte: list[int] | None = None,
                                        block: int = 200, prozesse: int = 1) -> np.ndarray:
    """ln[P(Record | Anfangsparität +1) / P(Record | Anfangsparität -1)] mit Paritätswechsel (Wonham-artig).

    Für gamma_qp = 0 identisch mit homodyn_trajektorien.log_likelihood_quotient (V6-1).
    Rückgabe: (n_records, len(checkpunkte)), checkpunkte = Anzahl Bins (Standard: alle).
    """
    _pruefe_kanaele(kanal_plus, kanal_minus)
    if gamma_qp < 0:
        raise ValueError("gamma_qp muss >= 0 sein")
    n, nbins = dY_bins.shape
    checkpunkte = [nbins] if checkpunkte is None else list(checkpunkte)
    if not all(0 < k <= nbins for k in checkpunkte):
        raise ValueError("Checkpunkte außerhalb des Records")
    S_p, x_vec, d = _sparse_superoperatoren(kanal_plus, dt_bin)
    S_m, _, _ = _sparse_superoperatoren(kanal_minus, dt_bin)
    S = {1: S_p, -1: S_m}
    rho0 = {1: kanal_plus.rho0.full().ravel(), -1: kanal_minus.rho0.full().ravel()}
    p_wechsel = -math.expm1(-gamma_qp * dt_bin)
    aufgaben = [(S, x_vec, d, rho0, p_wechsel, dY_bins[i:i + block], dt_bin, checkpunkte) for i in range(0, n, block)]
    return np.concatenate(_verteile(_llr_aufgabe_wechsel, aufgaben, prozesse), axis=0)
