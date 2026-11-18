"""Stationärer Zustand der Lindblad-Gleichung mit Diagnostik — keine stillen Löserfehler.

Methoden (unabhängig voneinander):
  qutip_direkt      qutip.steadystate(method="direct")
  sparse_spurzeile  eigene Liouvillian-Matrix (spaltenweise Vektorisierung), eine Zeile durch
                    die Spurbedingung ersetzt, scipy.sparse.linalg.spsolve
  propagation       qutip.mesolve von rho(0) über lange Zeit; nur Gegencheck, nicht für Sweeps

Jedes Ergebnis wird geprüft: Residuum ||L rho||, Spur, Hermitizität, minimaler Eigenwert,
Population des obersten Fockzustands. Verletzung -> StationaerLoeserFehler.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import qutip as qt
import scipy.sparse as sp
import scipy.sparse.linalg as spla

from _01_GRUNDLAGEN_FORMELN.operatoren_rwa import Modelloperatoren

# Begründung in SCHWELLEN.md (Klasse T2)
RESIDUUM_MAX = 1.0e-9
SPUR_FEHLER_MAX = 1.0e-10
HERMITIZITAET_MAX = 1.0e-10
EIGENWERT_MIN = -1.0e-10
PROPAGATION_ZEITEN_IN_RELAXATION = 60.0


class StationaerLoeserFehler(RuntimeError):
    def __init__(self, methode: str, grund: str, diagnostik: dict[str, float]) -> None:
        self.methode = methode
        self.grund = grund
        self.diagnostik = dict(diagnostik)
        werte = ", ".join(f"{k}={v:.3e}" for k, v in diagnostik.items())
        super().__init__(f"Stationärer Löser '{methode}' verworfen: {grund}; {werte}")


@dataclass(frozen=True)
class StationaerErgebnis:
    rho: qt.Qobj
    methode: str
    residuum: float
    spur_fehler: float
    hermitizitaet_fehler: float
    min_eigenwert: float
    oberste_fock_population: float

    def diagnostik(self) -> dict[str, float]:
        return {"residuum": self.residuum, "spur_fehler": self.spur_fehler,
                "hermitizitaet_fehler": self.hermitizitaet_fehler,
                "min_eigenwert": self.min_eigenwert,
                "oberste_fock_population": self.oberste_fock_population}


def _loese_sparse_spurzeile(ops: Modelloperatoren) -> qt.Qobj:
    L = qt.liouvillian(ops.H, list(ops.c_ops)).data.as_scipy().tocsr().astype(np.complex128)
    dim = ops.H.shape[0]
    # Spur in spaltenweiser Vektorisierung: Einträge (k,k) bei Index k*dim + k
    spur_zeile = np.zeros(dim * dim, dtype=np.complex128)
    spur_zeile[[k * dim + k for k in range(dim)]] = 1.0
    L = L.tolil()
    L[0, :] = spur_zeile
    rhs = np.zeros(dim * dim, dtype=np.complex128)
    rhs[0] = 1.0
    vec = spla.spsolve(L.tocsc(), rhs)
    rho = vec.reshape((dim, dim), order="F")
    return qt.Qobj(rho, dims=ops.H.dims)


def _loese_propagation(ops: Modelloperatoren, kappa: float, gamma_min: float) -> qt.Qobj:
    dim_res = ops.H.dims[0][0]
    rho0 = qt.tensor(qt.fock_dm(dim_res, 0), qt.fock_dm(2, 1))
    rate = max(min(kappa, gamma_min), 1.0e-12)
    t_end = PROPAGATION_ZEITEN_IN_RELAXATION / rate
    opts = {"atol": 1e-12, "rtol": 1e-10, "nsteps": 10**7}
    res = qt.mesolve(ops.H, rho0, [0.0, t_end], c_ops=list(ops.c_ops), options=opts)
    return res.states[-1]


def pruefe(ops: Modelloperatoren, rho: qt.Qobj, methode: str, max_fock: float) -> StationaerErgebnis:
    L = qt.liouvillian(ops.H, list(ops.c_ops))
    rho_vec = qt.operator_to_vector(rho)
    residuum = float(np.linalg.norm((L * rho_vec).full()))
    matrix = rho.full()
    spur_fehler = float(abs(np.trace(matrix) - 1.0))
    herm = float(np.max(np.abs(matrix - matrix.conj().T)))
    eig_min = float(np.min(np.linalg.eigvalsh(0.5 * (matrix + matrix.conj().T))))
    fock = float(abs(qt.expect(ops.projektor_oberster_fock, rho)))
    erg = StationaerErgebnis(rho=rho, methode=methode, residuum=residuum, spur_fehler=spur_fehler,
                             hermitizitaet_fehler=herm, min_eigenwert=eig_min, oberste_fock_population=fock)
    if residuum > RESIDUUM_MAX:
        raise StationaerLoeserFehler(methode, "Residuum zu groß", erg.diagnostik())
    if spur_fehler > SPUR_FEHLER_MAX:
        raise StationaerLoeserFehler(methode, "Spur verletzt", erg.diagnostik())
    if herm > HERMITIZITAET_MAX:
        raise StationaerLoeserFehler(methode, "nicht hermitesch", erg.diagnostik())
    if eig_min < EIGENWERT_MIN:
        raise StationaerLoeserFehler(methode, "nicht positiv semidefinit", erg.diagnostik())
    if fock > max_fock:
        raise StationaerLoeserFehler(methode, "Cutoff zu klein (oberster Fockzustand besetzt)", erg.diagnostik())
    return erg


def loese_stationaer(ops: Modelloperatoren, methode: str, *, kappa: float, gamma_min: float,
                     max_fock: float = 1.0e-10) -> StationaerErgebnis:
    if methode == "qutip_direkt":
        rho = qt.steadystate(ops.H, list(ops.c_ops), method="direct")
    elif methode == "sparse_spurzeile":
        rho = _loese_sparse_spurzeile(ops)
    elif methode == "propagation":
        rho = _loese_propagation(ops, kappa, gamma_min)
    else:
        raise ValueError(f"unbekannte Methode {methode}")
    return pruefe(ops, rho, methode, max_fock)
