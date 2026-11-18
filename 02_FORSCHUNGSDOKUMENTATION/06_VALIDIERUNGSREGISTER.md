# Validierungs- und Benchmarkregister

Schema je Eintrag: Auftrag · Testfall · Referenz · Bestanden-wenn (Toleranzklasse) · Was nicht geprüft wird. Status zu Beginn überall `OPEN`.

## Etappe 0 (Kickoff)
| ID | Prüfung | Ergebnis | Status |
|---|---|---|---|
| V0-02 | fig3c.dat-Integrität gegen Zenodo-md5 | `c8d8d3df89c151eb5aa9069c9774bfc6` = API-Wert | VERIFIED |

## Etappe 1 (geplant)
| ID | Auftrag | Testfall / Referenz | Bestanden wenn | Klasse | Nicht geprüft |
|---|---|---|---|---|---|
| V1-01 | Operatoralgebra | \([a,a^\dagger]=1\) unterhalb Cutoff, \(\tau\)-Algebra, H hermitesch | ≤ 1e-12 | T1 | Physik |
| V1-02 | Leere getriebene gedämpfte Kavität | \(g=0\): \(\langle a\rangle=\sqrt{\kappa_{in}I_0}/(i\Delta_0+\kappa/2)\), kohärenter Zustand (\(N_{th}=0\)) | rel. ≤ 1e-10 | T2 | Kopplung |
| V1-03 | Thermalzustand ohne Antrieb | \(I_0=0,g=0\): \(\langle\tau_z\rangle=-\tanh(\omega_z/T)\), Kavität thermisch \(N_{th}\) | ≤ 1e-10 (+ Cutoff-Rest) | T2 | Antrieb |
| V1-04 | Faktorisierung bei \(g=0\) | \(\varepsilon_{a\tau_z}=0\), \(A_{ref}=A_{semicl}\) | ≤ 1e-10 | T2 | — |
| V1-05 | Paritätskontrast verschwindet | \(t_1=0\): Ergebnisse für z = ±1 identisch | ≤ 1e-12 | T1/T5 | — |
| V1-06 | Dispersiver Grenzfall | große Verstimmung: exakt → Eq. (26)/(27); Skalierung des Fehlers mit \((\lambda/\Delta)^2\) | Steigung im log-log ± 10 % | T3 | resonantes Regime |
| V1-07 | Methodenunabhängigkeit | M1 (QuTiP) vs. M2 (eigene Sparse) vs. M3 (Propagation) am Resonanzpunkt + 5 Zufallspunkten | rel. ≤ 1e-8 | T2 | Modellfehler |
| V1-08 | Cutoff-Konvergenz | \(N_c\to 2N_c\); oberste Fock-Population | Änderung ≤ 1e-6 rel., Pop. ≤ 1e-10 | T3 | — |
| V1-09 | Physikalität des Steady State | Spur, Hermitizität, \(\lambda_{\min}\ge-10^{-10}\), Eindeutigkeit (Spektrallücke des Liouvillians > 0) | T2 | T2 | — |
| V1-10 | Negativkontrollen | falsche Dissipatorkonvention, T = 0 (s. EXP-R1 §6) | Verletzung ≥ 100× Toleranz oder vorhergesagte Invarianz | T5 | — |
| V1-11 | Linear-Response-Unabhängigkeit | Fehlermaße für \(I_0\) über 4 Dekaden | Änderung ≤ 1e-4 im Linearbereich; Nichtlinearitätseinsatz dokumentiert | T3 | starke Treiber |
| V1-12 | RWA-Gültigkeit | 3 Punkte: Laborrahmen-Floquet/Langzeitmittel vs. RWA | Abweichung berichtet (keine Pass/Fail-Schwelle; nicht aus Solverkonvergenz schließen) | Info | — |
| V1-H | Hash-Test Referenzdaten & Referenzconfigs | SHA-256 | identisch | T1 | — |

## Etappe 2 (Vorschau, nicht final)
SME-Ensemblemittel vs. `mesolve` (T4); \(\eta=0\Rightarrow P_{err}=0.5\); \(t_1=0\Rightarrow P_{err}=0.5\); dt-Halbierung (schwache Ordnung); Gauß-Benchmark Matched Filter vs. analytische erfc-Formel; Decoder-Leakage-Test (Label-Permutation darf Featurepfad nicht ändern).

## Status Etappe 1 (2026-11-09, `run_checks --scope all`: 35/35 bestanden)
| ID | Umsetzung | Status |
|---|---|---|
| V1-01 | `test_modell_operatoren.py` (Hermitizität, Pauli-Algebra, τ₋ senkt Energie) | VERIFIED |
| V1-02 | VAL0 `test_leere_kavitaet_ergibt_kohaerenten_zustand` | VERIFIED |
| V1-03 | VAL0 `test_thermalzustand_ohne_antrieb` | VERIFIED |
| V1-04 | VAL0 (ε_A, ε_aτz < 1e-9 bei g = 0) | VERIFIED |
| V1-05 | `test_ohne_t1_sind_beide_paritaeten_identisch`, `test_phase_pi_halbe_macht_paritaeten_gleich` | VERIFIED |
| V1-06 | VAL2 (Blais 2004, Ordnung 2 in g/Δ) + VAL5 (volles Modell, ED, Schrieffer–Wolff) | VERIFIED |
| V1-07 | VAL3 `test_drei_methoden_liefern_dieselbe_amplitude` | VERIFIED |
| V1-08 | VAL3 `test_cutoff_konvergenz`; Fock-Wächter im Löser (`test_zu_kleiner_cutoff_wird_nicht_still_akzeptiert`) | VERIFIED |
| V1-09 | Diagnostik in jedem Löserlauf (`pruefe`) | VERIFIED |
| V1-10 | VAL4 Negativkontrolle Kreisfrequenz | VERIFIED; Dissipator-Negativkontrollen noch OPEN |
| V1-11 | VAL1 `test_semiklassischer_fehler_waechst_linear_mit_antrieb` — Annahme „unabhängig von I0" **widerlegt** (F-1.6) | VERIFIED (als Gegenbefund) |
| V1-12 | RWA-Gültigkeit unter Antrieb | OPEN (ED ohne Antrieb in VAL5 vorhanden) |
| V1-H | `test_alle_zenodo_dateien_entsprechen_der_md5_aus_der_api` | VERIFIED |
| EXP-R1a/e semikl. | VAL4 | REPRODUCED |
| EXP-R1 exakt + fig3c | `_08_ERGEBNISSE/reproduktion_fig3.py` | BLOCKED (F-1.3) |
