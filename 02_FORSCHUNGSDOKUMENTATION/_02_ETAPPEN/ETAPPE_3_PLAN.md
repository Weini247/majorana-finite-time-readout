# Etappe 3 — Robustheit & Optimierung (Detailplan)

**Status:** in Arbeit — G2 freigegeben 2026-11-10. **Zeitbox:** 2 Wochen bis zur Entscheidung über EXP-E3 (Kill K-3), danach Robustheit.

## 1. Forschungsziel und offene Frage
Q-3A: *Verschiebt sich der optimale Antriebsfrequenz-Arbeitspunkt, wenn die Fehlerrate mit dem optimalen Decoder unter der echten (nicht-gaußschen) Messstatistik statt mit dem Gauß-Benchmark bewertet wird — im gesättigten Regime n̄* = 0.3, wo F-2.7 eine Abweichung zeigt?*
Q-3B (nach Q-3A): *Welcher Arbeitspunkt minimiert die Fehlerrate im Mittel bzw. Worst-Case über realistische Unsicherheit von φ (Flussdrift), t1 und κ, und unterscheidet er sich vom nominal optimalen?*

## 2. Literatur (WP 3.0, Volltextprüfung vor EXP-E3)
| Quelle | Wozu | Status |
|---|---|---|
| Gambetta, Braff, Wallraff, Girvin, Schoelkopf, PRA 76, 012325 (2007) | optimale Auswertung kontinuierlicher QND-Messung, nichtlineare Filter | zu prüfen |
| D'Anjou & Coish, PRA 89, 012313 (2014) | optimale Nachverarbeitung bei Einzelschuss-Auslese mit Relaxation | zu prüfen |
| Wiseman & Milburn (2010), Kap. 4–5 | Likelihood aus bedingtem Zustand (Hypothesentest mit SME) | Lehrbuch, VERIFIED |
| Walter et al. 2017 (L-Register §E) | κ/χ-Kurzzeitoptimum | VERIFIED (Etappe 2) |
| Neuheitsprüfung | Bayes-/Filter-Decoder für Majorana-Paritätsauslese (L03–L06, L14) | zu prüfen |

## 3. Methode
**Bayes-Filter (Likelihood-Quotient):** Für jeden Record dY werden zwei bedingte Zustände ρ_±(t) mit dem jeweiligen Paritätsmodell propagiert (gleiche Messdaten, kein Rauschen gezogen). Log-Likelihood-Quotient
\[ d\ell = (\langle x\rangle_+ - \langle x\rangle_-)\,dY - \tfrac12(\langle x\rangle_+^2 - \langle x\rangle_-^2)\,dt,\quad x=\sqrt{\eta\kappa_{out}}(e^{-i\theta}a+e^{i\theta}a^\dagger). \]
Da die Parität während der Messung erhalten ist, ist der Test ℓ ≷ 0 (gleiche Priors) der Neyman–Pearson-optimale Decoder für das Modell.
Annahme A3-1: Parität ist während T erhalten (keine Quasiteilchenvergiftung) — `HYPOTHESIS` aus L01, später Variante mit Paritätssprüngen.

## 4. Validierungen (vorab)
| ID | Prüfung | Kriterium |
|---|---|---|
| V3-1 | Schneller Integrator = bisheriger Integrator (gleicher Seed, gleiche Zufallszahlen) | max. Abweichung der dY-Bins ≤ 1e-10 (T2) |
| V3-2 | Bayes-Filter im dispersiven Gauß-Grenzfall (VAL7-Kanal) = Matched Filter | Fehlerraten im Wilson-Intervall der Gauß-Vorhersage |
| V3-3 | Bayes-Filter nie signifikant schlechter als Matched Filter/Boxcar auf denselben Testdaten | gepaarter Vergleich, Wilson |
| V3-4 | η = 0 ⇒ Raten | Fehlerrate im Intervall um 0.5 |

## 5. Experimente
- **EXP-E3 (Q-3A):** wird vor der Rechnung in `_03_EXPERIMENTE/` registriert. Skizze: n̄* = 0.3, ω ∈ {11.95, 11.97, 11.99, 12.01, 12.03}, T ∈ {1000, 2500, 5000}, I0/θ aus EXP-E2, Decoder MF/Boxcar/Bayes, ≥ 2000 Testrecords je Parität.
- **EXP-E4 (Q-3B):** nach EXP-E3.

## 6. Abbruch- und Entscheidungskriterien
- K-3a: Erreicht der Integrator keinen Faktor ≥ 3 für d = 16, wird EXP-E3 auf einen Cutoff-reduzierten Kanal (Cutoff-Prüfung T2' nötig) oder weniger ω-Punkte zugeschnitten.
- K-3b: Zeigt der Bayes-Filter an keinem Punkt einen Vorteil > 2 pp gegenüber dem MF, ist die Nicht-Gaußizität für die Arbeitspunktwahl irrelevant (Nullresultat, dokumentieren) — weiter mit Q-3B im Gauß-Benchmark plus Kontrollpunkten.

## 7. Gate G3
Bericht mit Antworten auf Q-3A/Q-3B, Entscheidung über Etappe 4 (ML nur mit begründeter Aufgabe, z. B. lernender Decoder gegen den Bayes-Filter als Baseline).
