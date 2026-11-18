# Python-Umgebung und Reproduzierbarkeit

| Komponente | Version |
|---|---|
| Python | CPython 3.12.10, Windows x86-64 |
| NumPy / SciPy / QuTiP / Matplotlib | siehe `requirements.txt`; transitive Pins in `requirements-lock.txt` (`pip freeze`) |

**venv** unter `_UMGEBUNG\venv` (gitignored), pip-Cache unter `_UMGEBUNG\pip-cache`. Keine globalen Installationen.

```powershell
py -3.12 -m venv _UMGEBUNG\venv
$env:PIP_CACHE_DIR = "_UMGEBUNG\pip-cache"
$Python = "_UMGEBUNG\venv\Scripts\python.exe"
& $Python -m pip install -r _05_INFRASTRUKTUR\requirements-lock.txt
& $Python -m pip check
```

Aus `01_PRL_CODE`:

```powershell
& $Python -B -m _05_INFRASTRUKTUR.run_checks --scope all                       # 35 Tests (24 aktiv, 11 VAL)
& $Python -B -m _05_INFRASTRUKTUR.referenzdaten.zenodo_benjadi_egger --laden   # Referenzdaten + md5
& $Python -B -m _08_ERGEBNISSE._01_REPRODUKTION.reproduktion_fig3                               # EXP-R1, Manifest in 10_Raw_Outputs
```

Versionspins garantieren keine bitidentischen Ergebnisse über Plattformen/BLAS hinweg; jeder Lauf schreibt seine tatsächliche Umgebung ins Manifest.
