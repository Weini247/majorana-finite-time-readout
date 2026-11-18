# ADR-0002 — Ordnerstruktur und Benennung

**Status:** accepted · 2026-11-09 (revidiert: deutsche, nummerierte Struktur; deutsche Testmethodennamen; Validierungen gegen Fremdpaper als eigene VAL-Ordner)

```
ParityReadoutLab/
├── README.md
├── 01_PRL_CODE/                          # Arbeitsverzeichnis für alle Python-Aufrufe
│   ├── SCHWELLEN.md                      # jede Toleranz/Definition begründet (Klassen T1–T5)
│   ├── _01_GRUNDLAGEN_FORMELN/           # Einheiten, Operatoren, Hamiltonoperatoren, Dissipation, Semiklassik
│   ├── _02_AUSFUEHRUNG/                  # Löser (stationär; später SME/Trajektorien), Fallausführung
│   ├── _03_WISSENSCHAFTLICHE_PRUEFUNGEN/ # VALn_<THEMA>/ je mit README (Auftrag · Testfall · Referenz · Bestanden wenn · Nicht geprüft)
│   ├── _04_AUSWERTUNG_DIAGNOSTIK/        # Ausgangsamplitude, Fehlermaße, (später) Decoder, Statistik
│   ├── _05_INFRASTRUKTUR/                # konfiguration/, runtime/ (Provenienz, Export), referenzdaten/, configs/, requirements*, ENVIRONMENT.md, run_checks.py
│   ├── _06_TESTS/                        # _01_MODELL_NUMERIK, _02_KONFIGURATION, _03_REFERENZDATEN_PROVENIENZ, …
│   ├── _08_ERGEBNISSE/                   # Experimentskripte je Etappe (Unterordner seit 2026-11-18)
│   │   ├── _01_REPRODUKTION/             # EXP-R1
│   │   ├── _02_ENDLICHE_MESSZEIT/        # EXP-E1, EXP-E2, EXP-E2K
│   │   └── _03_BAYES_ROBUSTHEIT/         # Pilot, EXP-E3, EXP-E4
│   └── _09_ABBILDUNGEN/                  # Abbildungen aus committeten Ergebnis-CSVs
├── 02_FORSCHUNGSDOKUMENTATION/           # Masterplan, Register, Konventionen, _01_ENTSCHEIDUNGEN … _05_THEORIE
├── 03_Quellen/                           # Referenzdaten (Zenodo, unverändert + Hashes)
├── 10_Raw_Outputs/<lauf_id>/             # manifest.json, config.json, Rohdaten (npz/HDF5)
├── 11_Processed_Outputs/<lauf_id>/       # Abbildungen, Kennzahltabellen
└── _UMGEBUNG/                            # venv + pip-Cache (gitignored)
```

**Benennung:**
- Ordner: nummeriert mit deutschen Großbuchstaben-Namen (`_0n_THEMA`); Python-Pakete sind gültige Bezeichner (führender Unterstrich).
- Module: deutsch, snake_case ohne Umlaute (`stationaer_loeser.py`, `fehlermasse.py`).
- Tests: `test_<thema>.py`, Klassen `<Thema>Vertrag`, **Methodennamen deutsch** (`test_leere_kavitaet_ergibt_kohaerenten_zustand`).
- Validierungen: `val<n>_<thema>.py` in `VALn_<THEMA>/`; Fremdpaper-Validierungen nennen Paper, Gleichung und DOI im Kopf.
- Physikalische Symbole dürfen mathematisch bleiben (`kappa`, `omega_z`, `g_z`).

**Regeln:** `_01_GRUNDLAGEN_FORMELN` kennt keine Löser; Löser kennen keine Auswertung; Decoder sehen keine wahren Labels im Featurepfad; Notebooks sind keine Wahrheitsquelle; Ergebnisse nur mit Manifest. Aufrufe immer aus `01_PRL_CODE` (`python -B -m _05_INFRASTRUKTUR.run_checks --scope all`).
- Struktur und Grundidee sind verbindlich, nicht die genaue Ordnerliste: neue Ordner oder Unterordner werden angelegt, wenn sie die Zuordnung klarer machen (2026-11-18: `_08_ERGEBNISSE` nach Etappen gegliedert, `_09_ABBILDUNGEN` neu).
