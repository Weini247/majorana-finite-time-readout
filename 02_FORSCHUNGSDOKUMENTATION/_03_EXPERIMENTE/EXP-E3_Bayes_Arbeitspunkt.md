# EXP-E3 — Arbeitspunktwahl unter echter Messstatistik (Etappe 3, Q-3A)

**Klasse:** explorativ · **Status:** `OPEN` — vorab registriert 2026-11-10, nach dem Designpilot und vor jeder EXP-E3-Rechnung. Lauf 1 (`EXP-E3_20261110T214052Z`) `FAILED` wegen Integratorfehler (F-3.4), nicht ausgewertet. **Lauf 2 (`EXP-E3_20261117T194320Z`) abgeschlossen 2026-11-18: Nullresultat** (F-3.5, F-3.6).

## Frage
Verschiebt sich bei gesättigtem Qubit (n̄* = 0.3) der fehlerminimierende Antriebsfrequenz-Arbeitspunkt, wenn die Fehlerrate aus Trajektorien mit Bayes-Filter, Matched Filter und Boxcar gemessen wird statt aus dem Gauß-Benchmark (EXP-E2: ω_stat = ω_T = 11.99)?

## Designpilot (Lauf `PILOT-E3_20261110T203052Z`, ω = 11.99, T = 2500, 2000 + 2000 Records je Parität; nur Design)
| Decoder | Fehlerrate [Wilson-95 %] |
|---|---|
| Gauß-Benchmark | 0.116 |
| Matched Filter | 0.123 [0.109, 0.138] |
| Boxcar | 0.125 [0.111, 0.140] |
| Bayes, Binbreite 1.0 | 0.136 [0.121, 0.151] |
| Bayes, Binbreite 0.4 | 0.122 [0.108, 0.137] |
| Bayes, Binbreite 0.2 | 0.121 [0.108, 0.136] |
Designfolgen: Binbreite 0.4 (gegenüber 0.2 auf 0.1 pp konvergiert; 1.0 zu grob). Laufzeit ≈ 45 min je ω bis T = 5000. Am Pilotpunkt kein messbarer Vorteil des Bayes-Filters gegenüber dem Matched Filter (gleiche Testdaten).

## Fixiert
Modell, Messkanal, η = 0.5, Cutoff 8 wie EXP-E2; I0 und θ je ω unverändert aus `EXP-E2_20261109T205736Z`. ω ∈ {11.95, 11.97, 11.99, 12.01, 12.03}; T ∈ {2500, 5000} (T = 2500 als Anfangsstück derselben Records). Je ω und Parität 2000 Kalibrier- + 2000 Testrecords (neue Seeds), dt = 0.2, Binbreite 0.4. Decoder: Bayes-LLR mit Schwelle 0; Matched Filter und Boxcar mit Schwelle aus den Kalibrierrecords. Skript `_08_ERGEBNISSE/exp_e3_bayes_arbeitspunkt.py`.

## Entscheidungsregel
- **Verschiebung relevant**, wenn für einen Decoder und ein T gilt: P(ω_stat) − min_ω P(ω) > 2 pp **und** die Wilson-Intervalle sind disjunkt.
- **Nullresultat**, wenn für alle Decoder und T die Differenz < 2 pp ist.
- **K-3b:** Bayes-Vorteil gegenüber dem Matched Filter an keinem Punkt > 2 pp mit disjunkten Intervallen ⇒ Nicht-Gaußizität für Decoder und Arbeitspunktwahl in diesem Modell irrelevant.
- Gauß-Abweichung (F-2.7) wird an allen 10 Punkten mitprotokolliert (MF-Intervall vs. P_G).

## Nachtrag 2026-11-11 (vor Lauf 2, nach Kenntnis von Lauf 1)
- Lauf 1 ist ungültig: linearisierter Schritt erster Ordnung abseits von ω_stat zu grob (F-3.4). Seine Zahlen werden nicht interpretiert und nicht mit Lauf 2 gepoolt.
- Lauf 2 mit exaktem kohärentem Propagator (VAL9 bestanden). Frage, Raster, T, Recordzahlen, dt = 0.2, Binbreite 0.4, Decoder und Entscheidungsregel **unverändert**; neue Seeds (Basis 5000 statt 3000).
- Zusätzliche Gültigkeitsbedingung je ω: Bayes-LLR-Mittel zeigt für beide Paritäten zur wahren Parität, und das MF-Intervall liegt nicht signifikant unter P_G (ein linearer Filter kann die Gauß-Schranke nicht unterbieten). Verletzung ⇒ Punkt ungültig, Ursache klären.
- Kenntnis von Lauf 1: Er zeigte am Punkt 11.99 dieselben Werte wie der Pilot; Lauf 2 wird ohne Kenntnis eines gültigen Ergebnisses abseits von 11.99 gerechnet.

## Ergebnis Lauf 2 (2026-11-18)
| ω | T | P_G | MF [Wilson-95 %] | Boxcar | Bayes [Wilson-95 %] |
|---|---|---|---|---|---|
| 11.95 | 2500 | 0.269 | 0.274 [0.255, 0.294] | 0.278 | 0.272 [0.253, 0.292] |
| 11.95 | 5000 | 0.192 | 0.195 [0.178, 0.213] | 0.196 | 0.191 [0.174, 0.209] |
| 11.97 | 2500 | 0.174 | 0.183 [0.167, 0.201] | 0.185 | 0.176 [0.160, 0.194] |
| 11.97 | 5000 | 0.091 | 0.100 [0.087, 0.113] | 0.100 | 0.089 [0.077, 0.102] |
| 11.99 | 2500 | 0.116 | 0.130 [0.116, 0.146] | 0.127 | 0.127 [0.113, 0.142] |
| 11.99 | 5000 | 0.044 | 0.056 [0.047, 0.067] | 0.058 | 0.055 [0.046, 0.066] |
| 12.01 | 2500 | 0.174 | 0.177 [0.161, 0.194] | 0.184 | 0.179 [0.163, 0.196] |
| 12.01 | 5000 | 0.092 | 0.099 [0.087, 0.113] | 0.103 | 0.098 [0.086, 0.112] |
| 12.03 | 2500 | 0.271 | 0.273 [0.254, 0.293] | 0.275 | 0.266 [0.248, 0.286] |
| 12.03 | 5000 | 0.195 | 0.195 [0.178, 0.213] | 0.197 | 0.188 [0.171, 0.205] |

Regelanwendung: Gültigkeit an allen Punkten erfüllt. Verschiebung: für alle Decoder und T argmin = 11.99 ⇒ **Nullresultat**. K-3b: max. Bayes-Vorteil 1.05 pp, nie disjunkt ⇒ **erfüllt (Nullresultat)**. Gauß-Abweichung: P_G nur bei 11.99 außerhalb des MF-Intervalls (+1.4 / +1.2 pp).

## Bekannte Einschränkungen
Nur ω als Arbeitspunktparameter; Ressourcenregel aus EXP-E2 (I0 je ω); Parität während T erhalten (A3-1); 5-Punkt-Raster (Auflösung 0.02).
