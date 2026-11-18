"""Homodynmessung am Ausgangsport: Mittelwert-Records (mesolve) und bedingte Trajektorien (ADR-0005).

Konvention (Itô, Wiseman-Milburn):
  d rho_c = L rho_c dt + H[c] rho_c dW,   c = sqrt(eta kappa_out) e^{-i theta} a
  dY      = <c + c^dag>_c dt + dW,         dW^2 = dt
Der Integrator ist über Trajektorien vektorisiert und nutzt das positivitätserhaltende Schema nach
P. Rouchon, J. F. Ralph, PRA 91, 012118 (2015):
  M = A + c dY,   A = exp[-(i H + 1/2 sum_k L_k^dag L_k + 1/2 c^dag c) dt]
  rho' = (M rho M^dag + sum_k L_k rho L_k^dag dt) / Tr(...)
mit den unbeobachteten Kanälen L_k (inkl. (1-eta) kappa_out D[a] und kappa_in D[a]).
A ist der exakte nicht-hermitesche Propagator (Etappe 3, F-3.4): die Linearisierung 1 - (...) dt war bei
||H|| dt ~ 0.4-0.8 abseits der Resonanz zu grob (EXP-E3 FAILED). Sprungterme bleiben erster Ordnung.
Dieses Modul kennt keine Auswertung (Decoder liegen in _04_AUSWERTUNG_DIAGNOSTIK).
"""
from __future__ import annotations

import math
import os
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import numpy as np
import qutip as qt
import scipy.linalg as sla
import scipy.sparse as sp

from _01_GRUNDLAGEN_FORMELN.operatoren_rwa import Modelloperatoren, baue_rwa_modell
from _05_INFRASTRUKTUR.konfiguration.config import ParameterBuendel


SUPEROPERATOR_MAX_DIM = 10          # nur trajektorien_referenz
_BLAS_VARIABLEN = ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS")


def _propagator_ohne_spruenge(H, summe, dt):
    """A = exp[-(i H + 1/2 sum L^dag L) dt]; exakt fuer den sprungfreien Teil (F-3.4)."""
    return sla.expm(-(1j * H + 0.5 * summe) * dt)


class TrajektorienFehler(RuntimeError):
    """Numerisch ungültige Trajektorie (Spur, Hermitizität, Positivität) — nie still weiterrechnen."""


@dataclass(frozen=True)
class Messkanal:
    H: qt.Qobj
    unbeobachtet: tuple[qt.Qobj, ...]     # alle Lindblad-Operatoren außer dem beobachteten Anteil
    beobachtet: qt.Qobj                    # c = sqrt(eta kappa_out) e^{-i theta} a
    rho0: qt.Qobj


def thermischer_startzustand(ops: Modelloperatoren, temperatur: float) -> qt.Qobj:
    """Resonator thermisch (N_th), Doppelpunkt thermisch (<tau_z> = -tanh(omega_z/T)), unkorreliert (ADR-0005)."""
    n = ops.a.dims[0][0]
    g = ops.groessen
    p_oben = 0.0 if temperatur == 0.0 else g.n_th / (2.0 * g.n_th + 1.0)
    dot = qt.Qobj(np.diag([p_oben, 1.0 - p_oben]))
    return qt.tensor(qt.thermal_dm(n, g.N_th), dot)


def messkanal_rwa(b: ParameterBuendel, *, eta: float, theta: float) -> tuple[Messkanal, Modelloperatoren]:
    """Messkanal für das RWA-Modell: kappa (N_th+1) D[a] = [kappa(N_th+1) - eta kappa_out] D[a] + eta kappa_out D[a]."""
    if not 0.0 <= eta <= 1.0:
        raise ValueError("eta muss in [0, 1] liegen")
    m = b.modell
    ops = baue_rwa_modell(b)
    g = ops.groessen
    zerfall = m.kappa * (g.N_th + 1.0)
    unbeob = zerfall - eta * m.kappa_out
    rest = list(ops.c_ops_doppelpunkt)
    if unbeob > 0:
        rest.append(math.sqrt(unbeob) * ops.a)
    if g.N_th > 0:
        rest.append(math.sqrt(m.kappa * g.N_th) * ops.a.dag())
    c = math.sqrt(eta * m.kappa_out) * np.exp(-1j * theta) * ops.a
    return Messkanal(H=ops.H, unbeobachtet=tuple(rest), beobachtet=c,
                     rho0=thermischer_startzustand(ops, m.temperatur)), ops


def mittelwert_record(kanal: Messkanal, zeiten: np.ndarray) -> np.ndarray:
    """mu(t) = <c + c^dag>(t) aus der unbedingten Mastergleichung (exakter Ensemble-Mittelwert von dY/dt)."""
    c_ops = list(kanal.unbeobachtet) + [kanal.beobachtet]
    x = kanal.beobachtet + kanal.beobachtet.dag()
    opts = {"atol": 1e-10, "rtol": 1e-8, "nsteps": 10 ** 6}
    res = qt.mesolve(kanal.H, kanal.rho0, zeiten, c_ops=c_ops, e_ops=[x], options=opts)
    return np.real(np.asarray(res.expect[0]))


@dataclass(frozen=True)
class TrajektorienErgebnis:
    zeiten_bins: np.ndarray        # Endzeit jedes Bins
    dY_bins: np.ndarray            # (ntraj, nbins): Recordinkremente summiert pro Bin
    tau_z_end: np.ndarray | None   # optional <O>_c am Ende (diagnostisch)
    dt: float
    seed: int


def _sparse_superoperatoren(kanal: Messkanal, dt: float):
    """Rouchon-Ralph-Schritt als dünnbesetzte Superoperatoren (zeilenweise Vektorisierung, s. trajektorien_referenz)."""
    H = kanal.H.full(); c = kanal.beobachtet.full(); Ls = [L.full() for L in kanal.unbeobachtet]
    d = H.shape[0]
    summe = sum((L.conj().T @ L for L in Ls), np.zeros((d, d), complex)) + c.conj().T @ c
    A = _propagator_ohne_spruenge(H, summe, dt)

    def kr(X, Y):
        S = sp.kron(sp.csr_matrix(X), sp.csr_matrix(Y), format="csr")
        S.eliminate_zeros()
        return S.tocsr()

    eins = np.eye(d, dtype=complex)
    # Faktorisiert, damit das dichte exakte A dünn bleibt: vec(M rho M^dag) = (I ⊗ M*) (M ⊗ I) vec(rho), M = A + dY c
    sprung = sum((kr(L, L.conj()) for L in Ls), sp.csr_matrix((d * d, d * d), dtype=complex)) * dt
    ops = (kr(A, eins), kr(c, eins), kr(eins, A.conj()), kr(eins, c.conj()), sp.csr_matrix(sprung))
    x_vec = (c + c.conj().T).T.ravel()
    return ops, x_vec, d


def _rr_schritt(ops, W, dY):
    """Ein Rouchon-Ralph-Schritt für alle Spalten W[:, j] = vec(rho_j) (unnormiert)."""
    AL, CL, AR, CR, J = ops
    B = AL @ W + (CL @ W) * dY[None, :]
    return AR @ B + (CR @ B) * dY[None, :] + J @ W


def _simuliere_block(ops, x_vec, d, rho0_vec, n, n_schritte, dt, bin_schritte, pruefintervall, rng_quelle):
    """Ein Block unabhängiger Trajektorien; Spaltenlayout W[:, j] = vec(rho_j) hält die Arrays im Cache."""
    rng = np.random.default_rng(rng_quelle)
    spur_idx = np.arange(d) * (d + 1)
    W = np.repeat(rho0_vec[:, None], n, axis=1)
    dY_bins = np.zeros((n, n_schritte // bin_schritte))
    wurzel_dt = math.sqrt(dt)
    for schritt in range(n_schritte):
        erw = np.real(x_vec @ W)
        dY = erw * dt + rng.standard_normal(n) * wurzel_dt
        W = _rr_schritt(ops, W, dY)
        spur = np.real(W[spur_idx].sum(axis=0))
        W /= spur[None, :]
        dY_bins[:, schritt // bin_schritte] += dY
        if schritt % pruefintervall == 0:
            rho = W.T.reshape(n, d, d)
            herm = np.max(np.abs(rho - np.conj(np.transpose(rho, (0, 2, 1)))))
            if not np.isfinite(herm) or herm > 1e-8 or np.any(spur <= 0):
                raise TrajektorienFehler(f"Schritt {schritt}: Hermitizitätsfehler {herm:.2e} oder Spur <= 0")
    return dY_bins, W


def _block_aufgabe(args):
    return _simuliere_block(*args)


def trajektorien(kanal: Messkanal, *, T: float, dt: float, ntraj: int, seed: int, bin_schritte: int = 10,
                 beobachtbar_ende: qt.Qobj | None = None, pruefintervall: int = 200,
                 block: int | None = None, prozesse: int = 1) -> TrajektorienErgebnis:
    """Bedingte Homodyn-Trajektorien (dünnbesetzter Superoperator, Etappe 3, V3-1).

    block=None: ein Block mit np.random.default_rng(seed) — identische Zufallszahlen und Records wie
    trajektorien_referenz (Regression V3-1). block=k: Blöcke zu k Trajektorien mit unabhängigen, aus
    SeedSequence(seed) abgeleiteten Strömen (reproduzierbar, aber andere Zufallszahlen); prozesse > 1
    verteilt die Blöcke auf Prozesse (Ergebnis unabhängig von der Prozesszahl).
    """
    n_schritte = int(round(T / dt))
    if abs(n_schritte * dt - T) > 1e-9 * max(T, 1.0):
        raise ValueError("T muss ein ganzzahliges Vielfaches von dt sein")
    if n_schritte % bin_schritte:
        raise ValueError("Schrittzahl muss durch bin_schritte teilbar sein")
    ops, x_vec, d = _sparse_superoperatoren(kanal, dt)
    rho0_vec = kanal.rho0.full().ravel()
    if block is None or block >= ntraj:
        groessen, quellen = [ntraj], [seed]
    else:
        groessen = [block] * (ntraj // block) + ([ntraj % block] if ntraj % block else [])
        quellen = np.random.SeedSequence(seed).spawn(len(groessen))
    aufgaben = [(ops, x_vec, d, rho0_vec, n, n_schritte, dt, bin_schritte, pruefintervall, q)
                for n, q in zip(groessen, quellen)]
    if prozesse > 1 and len(aufgaben) > 1:
        # Kindprozesse erben die Umgebung: BLAS dort einfädig, sonst Überbuchung (Messung: Faktor 8.4 -> 11 bei 6 Prozessen)
        alt = {v: os.environ.get(v) for v in _BLAS_VARIABLEN}
        os.environ.update({v: "1" for v in _BLAS_VARIABLEN})
        try:
            with ProcessPoolExecutor(max_workers=prozesse) as pool:
                teile = list(pool.map(_block_aufgabe, aufgaben))
        finally:
            for v, w in alt.items():
                if w is None:
                    os.environ.pop(v, None)
                else:
                    os.environ[v] = w
    else:
        teile = [_block_aufgabe(a) for a in aufgaben]
    dY_bins = np.concatenate([t[0] for t in teile], axis=0)
    rho = np.concatenate([t[1].T.reshape(-1, d, d) for t in teile], axis=0)
    eig_min = float(np.min(np.linalg.eigvalsh(0.5 * (rho + np.conj(np.transpose(rho, (0, 2, 1)))))))
    if eig_min < -1e-8:
        raise TrajektorienFehler(f"bedingter Zustand nicht positiv: lambda_min = {eig_min:.2e}")
    tau_end = None
    if beobachtbar_ende is not None:
        tau_end = np.real(np.einsum("ij,nji->n", beobachtbar_ende.full(), rho))
    zeiten = dt * bin_schritte * np.arange(1, n_schritte // bin_schritte + 1)
    return TrajektorienErgebnis(zeiten_bins=zeiten, dY_bins=dY_bins, tau_z_end=tau_end, dt=dt, seed=seed)


def trajektorien_referenz(kanal: Messkanal, *, T: float, dt: float, ntraj: int, seed: int, bin_schritte: int = 10,
                          beobachtbar_ende: qt.Qobj | None = None, pruefintervall: int = 200) -> TrajektorienErgebnis:
    """Ursprünglicher dichter Integrator (Etappe 2, validiert durch VAL7) — Referenz für V3-1."""
    n_schritte = int(round(T / dt))
    if abs(n_schritte * dt - T) > 1e-9 * max(T, 1.0):
        raise ValueError("T muss ein ganzzahliges Vielfaches von dt sein")
    if n_schritte % bin_schritte:
        raise ValueError("Schrittzahl muss durch bin_schritte teilbar sein")
    rng = np.random.default_rng(seed)
    H = kanal.H.full()
    c = kanal.beobachtet.full()
    Ls = [L.full() for L in kanal.unbeobachtet]
    d = H.shape[0]
    eins = np.eye(d, dtype=complex)
    summe = sum((L.conj().T @ L for L in Ls), np.zeros((d, d), complex)) + c.conj().T @ c
    A = _propagator_ohne_spruenge(H, summe, dt)
    x = c + c.conj().T
    # Zeilenweise Vektorisierung: vec(X rho Y) = (X ⊗ Y^T) vec(rho).  M rho M^dag mit M = A + dY c:
    #   = A rho A^dag + dY (c rho A^dag + A rho c^dag) + dY^2 c rho c^dag
    S0 = np.kron(A, A.conj()) + dt * sum((np.kron(L, L.conj()) for L in Ls), np.zeros((d * d, d * d), complex))
    S1 = np.kron(c, A.conj()) + np.kron(A, c.conj())
    S2 = np.kron(c, c.conj())
    S0T, S1T, S2T = S0.T.copy(), S1.T.copy(), S2.T.copy()
    x_vec = x.T.ravel()                       # Tr(x rho) = vec(rho) · vec(x^T)
    spur_idx = np.arange(d) * (d + 1)
    V = np.broadcast_to(kanal.rho0.full().ravel(), (ntraj, d * d)).copy()
    nbins = n_schritte // bin_schritte
    dY_bins = np.zeros((ntraj, nbins))
    superoperator = d <= SUPEROPERATOR_MAX_DIM          # Kosten: d^4 (GEMM) vs. d^3 (gebündelte kleine Produkte)
    for schritt in range(n_schritte):
        erw = np.real(V @ x_vec)
        dY = erw * dt + rng.standard_normal(ntraj) * math.sqrt(dt)
        if superoperator:
            V = V @ S0T + dY[:, None] * (V @ S1T) + (dY ** 2)[:, None] * (V @ S2T)
        else:
            rho = V.reshape(ntraj, d, d)
            M = A[None, :, :] + dY[:, None, None] * c[None, :, :]
            neu = M @ rho @ np.conj(np.transpose(M, (0, 2, 1)))
            for L in Ls:
                neu += (L @ rho @ L.conj().T) * dt
            V = neu.reshape(ntraj, d * d)
        spur = np.real(V[:, spur_idx].sum(axis=1))
        V /= spur[:, None]
        dY_bins[:, schritt // bin_schritte] += dY
        if schritt % pruefintervall == 0:
            rho = V.reshape(ntraj, d, d)
            herm = np.max(np.abs(rho - np.conj(np.transpose(rho, (0, 2, 1)))))
            if not np.isfinite(herm) or herm > 1e-8 or np.any(spur <= 0):
                raise TrajektorienFehler(f"Schritt {schritt}: Hermitizitätsfehler {herm:.2e} oder Spur <= 0")
    rho = V.reshape(ntraj, d, d)
    eig_min = float(np.min(np.linalg.eigvalsh(0.5 * (rho + np.conj(np.transpose(rho, (0, 2, 1)))))))
    if eig_min < -1e-8:
        raise TrajektorienFehler(f"bedingter Zustand nicht positiv: lambda_min = {eig_min:.2e}")
    tau_end = None
    if beobachtbar_ende is not None:
        tau_end = np.real(np.einsum("ij,nji->n", beobachtbar_ende.full(), rho))
    zeiten = dt * bin_schritte * np.arange(1, nbins + 1)
    return TrajektorienErgebnis(zeiten_bins=zeiten, dY_bins=dY_bins, tau_z_end=tau_end, dt=dt, seed=seed)


def _llr_block(S_p, S_m, x_vec, d, rho0_p, rho0_m, dY_bins, dt_bin, checkpunkte):
    """Zwei bedingte Filter (Hypothese z = +1 / -1) auf denselben Messdaten; Log-Likelihood-Quotient."""
    n, nbins = dY_bins.shape
    spur_idx = np.arange(d) * (d + 1)
    W = {+1: np.repeat(rho0_p[:, None], n, axis=1), -1: np.repeat(rho0_m[:, None], n, axis=1)}
    S = {+1: S_p, -1: S_m}
    llr = np.zeros(n)
    aus = np.zeros((n, len(checkpunkte)))
    ziel = {k: i for i, k in enumerate(checkpunkte)}
    for k in range(nbins):
        dY = dY_bins[:, k]
        erw = {z: np.real(x_vec @ W[z]) for z in (1, -1)}
        llr += (erw[1] - erw[-1]) * dY - 0.5 * (erw[1] ** 2 - erw[-1] ** 2) * dt_bin
        for z in (1, -1):
            W[z] = _rr_schritt(S[z], W[z], dY)
            spur = np.real(W[z][spur_idx].sum(axis=0))
            if np.any(~np.isfinite(spur)) or np.any(spur <= 0):
                raise TrajektorienFehler(f"Filter z={z}, Bin {k}: Spur <= 0")
            W[z] /= spur[None, :]
        if k + 1 in ziel:
            aus[:, ziel[k + 1]] = llr
    return aus


def _llr_aufgabe(args):
    return _llr_block(*args)


def log_likelihood_quotient(kanal_plus: Messkanal, kanal_minus: Messkanal, dY_bins: np.ndarray, dt_bin: float, *,
                            checkpunkte: list[int] | None = None, block: int = 200, prozesse: int = 1) -> np.ndarray:
    """Bayes-Decoder (Etappe 3): ln[P(Record | z=+1) / P(Record | z=-1)] aus zwei bedingten Zuständen.

    dl = (<x>_+ - <x>_-) dY - 1/2 (<x>_+^2 - <x>_-^2) dt,  x = c + c^dag (Wiseman-Milburn, Kap. 4/5).
    Die Filter laufen auf der Binbreite dt_bin (Rouchon-Ralph-Schritt mit dem summierten Inkrement); die
    Diskretisierung ist Teil des Decoders und wird über die Binbreite geprüft (V3-2/V3-3).
    Rückgabe: (n_records, len(checkpunkte)), checkpunkte = Anzahl Bins (Standard: alle).
    """
    c_p, c_m = kanal_plus.beobachtet.full(), kanal_minus.beobachtet.full()
    if np.max(np.abs(c_p - c_m)) > 1e-14:
        raise ValueError("beide Hypothesen müssen denselben Messkanal (eta, theta, kappa_out) haben")
    n, nbins = dY_bins.shape
    checkpunkte = [nbins] if checkpunkte is None else list(checkpunkte)
    if not all(0 < k <= nbins for k in checkpunkte):
        raise ValueError("Checkpunkte außerhalb des Records")
    S_p, x_vec, d = _sparse_superoperatoren(kanal_plus, dt_bin)
    S_m, _, _ = _sparse_superoperatoren(kanal_minus, dt_bin)
    rho_p, rho_m = kanal_plus.rho0.full().ravel(), kanal_minus.rho0.full().ravel()
    aufgaben = [(S_p, S_m, x_vec, d, rho_p, rho_m, dY_bins[i:i + block], dt_bin, checkpunkte)
                for i in range(0, n, block)]
    if prozesse > 1 and len(aufgaben) > 1:
        alt = {v: os.environ.get(v) for v in _BLAS_VARIABLEN}
        os.environ.update({v: "1" for v in _BLAS_VARIABLEN})
        try:
            with ProcessPoolExecutor(max_workers=prozesse) as pool:
                teile = list(pool.map(_llr_aufgabe, aufgaben))
        finally:
            for v, w in alt.items():
                if w is None:
                    os.environ.pop(v, None)
                else:
                    os.environ[v] = w
    else:
        teile = [_llr_aufgabe(a) for a in aufgaben]
    return np.concatenate(teile, axis=0)
