# ADR-0003 — Numerischer Werkzeugstapel

**Status:** proposed (Versionen werden in WP 1.0 fixiert)

| Aufgabe | Wahl | Begründung | Unabhängiger Gegencheck |
|---|---|---|---|
| Operatoren, Lindblad, Steady State | **QuTiP 5** (`steadystate`, `liouvillian`) | Etabliert, dokumentiert (L30); keine Eigenimplementierung eines allgemeinen Lindblad-Solvers | Eigene Liouvillian-Konstruktion als Sparse-Matrix (vektorisiert, column-stacking) + `scipy.sparse.linalg.spsolve` mit Spurbedingung; **und** Zeitpropagation `mesolve` bis Konvergenz |
| SME / Homodyn (Etappe 2) | QuTiP `smesolve` | Messkanäle, Effizienz, Records verfügbar | Eigener einfacher Euler–Maruyama/Milstein-Integrator für 1–2 Testfälle; Ensemblemittel vs. `mesolve` |
| Analytik | SymPy (optional) | Herleitungsprüfung L01 Eqs. (18), (27), (40) | numerische Grenzfälle |
| Statistik | NumPy/SciPy | Wilson-CI, Bootstrap | — |
| Daten | NumPy `.npz` für Etappe 1; HDF5 (h5py) ab Etappe 2 für Records | einfach, portabel | Hashes im Manifest |
| Plots | Matplotlib | Standard | — |
| JAX/Dynamiqs | **zurückgestellt** | erst nach Profiling eines realen Engpasses (Etappe 3), Genauigkeit vs. CPU-Referenz | — |

Präzision: complex128 / float64 überall. Windows: Python 3.12.10 vorhanden (`py -3.12`); QuTiP-5-Wheels für Windows/3.12 sind verfügbar (in WP 1.0 zu bestätigen). Threading (BLAS) im Manifest protokollieren.
