# Etappe 2 — Endliche Messung: Bericht und Gate G2

**Stand:** 2026-11-10 · Commit `737e40e` · Testsuite 51/51 (35 aktiv, 16 wissenschaftlich)

## 1. Leitfrage dieser Etappe
Wählt die Maximierung des stationären Auslesekontrasts denselben Arbeitspunkt wie die Minimierung der Einzelschuss-Fehlerrate bei endlicher Messzeit T, realistischer Detektionseffizienz η und gleicher Resonatorbesetzung?

## 2. Was gebaut und validiert wurde
| Baustein | Ort | Validierung | Status |
|---|---|---|---|
| Homodyn-Messkanal (η, θ), kein Doppelzählen des Resonatorzerfalls | `_02_AUSFUEHRUNG/homodyn_trajektorien.py`, ADR-0005 | Tests `_04_MESSUNG_DECODER` | VERIFIED |
| SME-Integrator (Rouchon–Ralph, positivitätserhaltend; Superoperator- bzw. gebündelter Pfad) | ebd. | VAL7: Ensemble = Mastergleichung, η = 0 ⇒ Raten | VERIFIED |
| SNR-Einschwingen | `referenzfaelle_dispersiv.py` | VAL6: Smith et al. 2020 Eq. (29) auf 1e-4 | VERIFIED |
| Decoder (Matched Filter, Boxcar, Schwelle auf getrennten Kalibrierdaten, Wilson-95 %) | `_04_AUSWERTUNG_DIAGNOSTIK/decoder.py` | VAL7: Matched Filter = Gauß-Vorhersage im dispersiven Grenzfall | VERIFIED |

## 3. Ergebnisse
| Befund | Aussage | Status |
|---|---|---|
| F-2.1 | Das allgemeine Phänomen „stationär-optimal ≠ endlichzeit-optimal" ist aus cQED bekannt (Walter 2017); für Majorana-Boxen mit Homodynkanal/η nicht berechnet | VERIFIED (Volltexte) |
| F-2.3 / F-2.5 | Pilot T ≤ 320 ns: zu nahe am Raten; Pilotdesign als Fehlschlag dokumentiert | Nullresultat (Gauß) / FAILED als Design |
| F-2.6 | Bis 8 µs: bei n̄* = 0.3 ist ω_stat = 11.99 für jedes T optimal (Regret 0), P_G(8 µs) = 0.0076; bei n̄* = 0.01 nicht entscheidbar (P_G = 0.30) | Nullresultat nur im Gauß-Benchmark |
| F-2.7 | Trajektorien-Kontrollpunkte: Gauß gültig an 3/4 Punkten; **bei n̄* = 0.3, T = 2500 zu optimistisch** (0.116 vs. 0.133 [0.119, 0.149]); Boxcar dort nicht schlechter als Matched Filter; dt-Halbierung bestanden | Gauß-Gültigkeit bei Sättigung + langem T: verletzt ⇒ F-2.6 dort `HYPOTHESIS` |

Ohne Rechnung (EXP-E2-Vorabanmerkung): Im Gauß-Benchmark hängt die Arbeitspunktwahl nicht von η ab (SNR² ∝ η), und für T → ∞ geht ω_T zwangsläufig gegen ω_stat.

## 4. Antwort auf die Leitfrage (Stand G2)
Für den einzigen untersuchten Arbeitspunktparameter (Antriebsfrequenz ω) und die L01-Parameter der starken Kopplung: **Im Gauß-Benchmark ja — die stationäre Wahl ist optimal.** Unter echter Messstatistik bei gesättigtem Qubit ist das **offen**, weil der Gauß-Benchmark dort nachweislich zu optimistisch ist und der Gauß-optimale Decoder (Matched Filter) nicht mehr optimal sein muss.

Zulässiger Kurzclaim: „In einem validierten Homodynmodell der Majorana-Box (Benjadi & Egger 2026, starke Kopplung) ist die stationär gewählte Antriebsfrequenz im Gauß-Benchmark für Messzeiten bis 8 µs optimal; bei gesättigtem Qubit unterschätzt der Gauß-Benchmark die Fehlerrate um ≈ 2 pp."
Unzulässig: „Stationäre Optimierung ist allgemein ausreichend." / „Nicht-Gaußizität nachgewiesen." (eine Stichprobe, ≈ 2σ)

## 5. Nicht erledigt in Etappe 2
- Bayes-/Zustandsfilter-Decoder (optimal jenseits Gauß) — nach Etappe 3 verschoben, dort zentral.
- Arbeitspunktparameter jenseits ω (I0-Budget als freie Variable, Pulsform), Drift, Parameterunsicherheit — Etappe 3.
- Schnellerer Integrator für d ≥ 16 (ein Kontrollpunkt ≈ 2 h).
- Aus Etappe 1 weiterhin offen, nicht blockierend: V1-10, V1-12, Eq. (27), Autorenfrage (F-1.3, F-1.5).

## 6. Vorschlag für Etappe 3 (zur Freigabe bei G2)
1. **Integrator beschleunigen** (Zielfaktor ≥ 5 für d = 16), Regression gegen VAL7.
2. **EXP-E3 (vorab registrieren):** n̄* = 0.3, ω-Raster um 11.99, T ∈ {1000, 2500, 5000}; Decoder Matched Filter, Boxcar und Bayes-Filter (Zwei-Hypothesen-Likelihood aus dem bedingten Zustand); Frage: verschiebt sich ω_T unter echter Statistik?
3. **Robustheit:** Arbeitspunkt bei Unsicherheit in t1, φ (Drift des Flusses) und κ — Fehlerrate im Mittel/Worst-Case statt am Nominalpunkt.
4. Erst danach Entscheidung über Etappe 4 (ML nur mit begründeter Aufgabe und Baseline, z. B. Decoder gegen Bayes-Filter).
