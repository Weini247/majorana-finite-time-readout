# Etappe 3 — Robustheit & Optimierung: Bericht und Gate G3

**Stand:** 2026-11-18 · Commit `50f16f6` · Testsuite 58/58 (37 aktiv, 21 wissenschaftlich)

## 1. Leitfrage dieser Etappe
Bleibt die stationär gewählte Antriebsfrequenz ω_stat = 11.99 auch unter echter (nicht-gaußscher) Messstatistik mit optimalem Decoder und unter Parameterunsicherheit der fehlerminimale Arbeitspunkt bei endlicher Messzeit?

## 2. Was gebaut und validiert wurde
| Baustein | Ort | Validierung | Status |
|---|---|---|---|
| Dünnbesetzter, blockweiser SME-Integrator (≈ 7× schneller, 6 Prozesse, d = 16) | `_02_AUSFUEHRUNG/homodyn_trajektorien.py` | Regression gegen Referenzpfad, VAL7 | VERIFIED (F-3.1) |
| Bayes-Decoder (LLR aus zwei bedingten Zuständen, ohne Kalibrierung) | ebd., `log_likelihood_quotient` | VAL8: linearer Grenzfall = Matched Filter (≤ 1e-3), η = 0 ⇒ LLR = 0 | VERIFIED (F-3.2) |
| Exakter kohärenter Propagator A = exp[−(iH + ½ΣL†L + ½c†c)dt], faktorisiert | ebd. | VAL9: Trajektorienmittel = mesolve abseits der Resonanz (ω = 12.03), LLR binbreitenunabhängig; Gegenprobe mit altem Schritt fällt durch | VERIFIED (F-3.4) |

## 3. Ergebnisse
| Befund | Aussage | Status |
|---|---|---|
| F-3.3 | Pilot am F-2.7-Punkt: Bayes ≈ MF, Gauß-Abweichung ≈ 1 pp grenzwertig | Pilot, durch F-3.6 ersetzt |
| F-3.4 | **EXP-E3 Lauf 1 ungültig:** linearisierter Rouchon-Ralph-Schritt bei ‖H‖dt ≈ 0.4–0.8 abseits von ω_stat zu grob (bis 12 σ neben mesolve, Bayes ≈ 0.5). Am Resonanzpunkt klein, daher von Pilot, VAL7, VAL8 nicht erfasst | Lauf 1 FAILED; Fix VERIFIED |
| F-3.5 | **EXP-E3 Lauf 2: Nullresultat.** Für MF, Boxcar und Bayes und T ∈ {2500, 5000} ist 11.99 der fehlerminimale Punkt; Bayes höchstens 1.05 pp besser als MF, nie disjunkt (K-3b) | REPRODUCED (ein Lauf, 2000 Testrecords je Punkt) |
| F-3.6 | Gauß-Benchmark nur am Resonanzpunkt leicht optimistisch (+1.2 / +1.4 pp), sonst im MF-Intervall; F-2.7 damit eingegrenzt | REPRODUCED |
| F-3.7 | **EXP-E4: Nullresultat.** Bei Fehlkalibrierung von φ, t1, κ bleibt 11.99 nominal, im Mittel und im Worst-Case optimal (Regret 0); die Fehlerrate steigt (0.116 → 0.170), der beste Punkt verschiebt sich nicht | REPRODUCED (Gauß-Benchmark) |

Kerntabelle EXP-E3 Lauf 2 (Fehlerrate, T = 2500 / 5000):

| ω | Gauß | MF | Boxcar | Bayes |
|---|---|---|---|---|
| 11.95 | .269 / .192 | .274 / .195 | .278 / .196 | .272 / .191 |
| 11.97 | .174 / .091 | .183 / .100 | .185 / .100 | .176 / .089 |
| **11.99** | .116 / .044 | **.130 / .056** | **.127 / .058** | **.127 / .055** |
| 12.01 | .174 / .092 | .177 / .099 | .184 / .103 | .179 / .098 |
| 12.03 | .271 / .195 | .273 / .195 | .275 / .197 | .266 / .188 |

## 4. Antwort auf die Leitfrage (Stand G3)
Für ω als Arbeitspunktparameter, die L01-Parameter (starke Kopplung), n̄* = 0.3 und η = 0.5: **Ja.** Die stationäre Wahl ist auch unter echter Statistik, mit optimalem Decoder und bei Fehlkalibrierung der fehlerminimale Punkt. Der optimale Decoder bringt gegenüber dem linearen Matched Filter keinen messbaren Vorteil.

Zulässiger Kurzclaim: „In einem validierten Homodynmodell der Majorana-Box (Benjadi & Egger 2026, starke Kopplung) ist die stationär gewählte Antriebsfrequenz für Messzeiten 2–4 µs (T = 2500/5000 λ₀⁻¹) auch mit Bayes-optimalem Decoder und unter Fehlkalibrierung von φ, t1, κ optimal; der Matched Filter liegt höchstens ≈ 1 pp über dem Bayes-Decoder."
Unzulässig: „Stationäre Optimierung ist allgemein ausreichend." (ein Parameterregime, ein Arbeitspunktparameter) / „Bayes-Decoding ist nutzlos." (nur dieses Regime)

Methodischer Nebenbefund: Ein Integratorfehler, der nur abseits des Resonanzpunkts sichtbar wird, hätte ein Scheinergebnis erzeugt. Er wurde über die vorab registrierte Plausibilitätslogik (MF unter Gauß-Schranke unmöglich) entdeckt; VAL9 sichert ihn jetzt ab.

## 5. Nicht erledigt in Etappe 3
- Arbeitspunktparameter jenseits ω (Budget, Pulsform), schwache Kopplung, n̄* = 0.01 unter echter Statistik, kombinierte Parameterabweichungen.
- Robustheit unter echter Statistik (EXP-E4 nur im Gauß-Benchmark; durch F-3.6 auf ≲ 1.4 pp gestützt).
- Aus Etappe 1 weiterhin offen, nicht blockierend: V1-10, V1-12, Eq. (27), Autorenfrage (F-1.3, F-1.5).

## 6. Vorschlag zu G3 (zur Freigabe)
**Entscheidung 2026-11-18:** freigegeben. Etappe 4 entfällt; Etappe 5 als öffentliches Repository durchgeführt; Etappe 3b wird als Etappe 6 (Paritätswechsel, `_02_ETAPPEN/ETAPPE_6_PLAN.md`) weitergeführt.

1. **Etappe 4 (ML-Decoder) nicht starten.** Der Bayes-Decoder ist für dieses Modell optimal und schlägt den Matched Filter nicht messbar; ein gelernter Decoder hat keine begründete Aufgabe und keine Lücke zu schließen.
2. **Optional Etappe 3b:** gezielte Suche nach einem Regime mit Regret > 0 (schwächere Kopplung, kombinierte Abweichungen, Budget als freie Variable), nur mit vorab registrierter Frage.
3. **Etappe 5:** reproduzierbares öffentliches Repository mit Abbildungen und englischer README.
