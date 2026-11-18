# ADR-0004 — Umgebung, Versionskontrolle, Provenienz

**Status:** proposed — benötigt Freigabe durch die Projektleitung (Q-4, Q-5)

1. **venv** unter `_env\` (innerhalb des Projektordners, wie im Auftrag gefordert; gitignored, nicht im Quellbaum `src/`). Erstellung: `py -3.12 -m venv _env`. Keine globalen Installationen, keine Änderung an PATH/Systemeinstellungen. pip-Cache über `PIP_CACHE_DIR=_env\pip-cache` ins Projekt gelenkt.
2. **Lockfile** `requirements-lock.txt` (pip freeze) + `pip check`; Umgebungsbericht als JSON pro Validierungslauf.
3. **Git** als eigenes Repository.
4. **Manifest je Run:** run_id, UTC-Zeit, git HEAD + dirty (`git --no-optional-locks`), Lockfile-SHA-256, Python/NumPy/SciPy/QuTiP-Versionen, BLAS-Info, Float-Präzision, vollständige Config, Root-Seed, Input-Hashes (Zenodo-Dateien), Toleranzen, Solvermethode und Diagnostik.
5. **Referenzdaten:** Download der 13 Zenodo-Dateien nach `03_Quellen/Referenzdaten_Zenodo_20623730/`, md5 gegen Zenodo-API prüfen, zusätzlich SHA-256 ablegen, Dateien danach read-only behandeln (Hash-Test).
