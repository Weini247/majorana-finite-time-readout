# EXP-E4 — Robustheit der Arbeitspunktwahl gegen Parameterabweichungen (Etappe 3, Q-3B)

**Klasse:** explorativ · **Status:** abgeschlossen 2026-11-18 — **Nullresultat** (F-3.7): Regret 0 für alle Budgets und T (Lauf `EXP-E4_20261111T002220Z`). Vorab registriert 2026-11-10, vor jeder Rechnung. Skript `_08_ERGEBNISSE/exp_e4_robustheit.py`.

## Frage
Kalibriert man am Nominalmodell (I0, θ, Filtergewichte, Schwelle), misst aber an einem leicht abweichenden Gerät: Ist die nominal optimale Antriebsfrequenz auch im Worst-Case bzw. im Mittel über realistische Abweichungen optimal?

## Modell und Abweichungen
Nominal wie EXP-E2 (L01 starke Kopplung, η = 0.5, ω-Raster [11.80, 12.20], I0/θ je ω aus `EXP-E2_20261109T205736Z`), Budgets n̄* ∈ {0.3, 0.01}.
Einzeln variiert: Flussphase φ ∈ {±0.1, ±0.2} rad (Drift), t1 × {0.95, 1.05}, κ (κ_in und κ_out) × {0.8, 1.2}. Insgesamt 8 Abweichungen plus nominal.

## Metriken (Gauß-Benchmark, exakte Mittelwert-Records, T ∈ {2500, 5000, 10⁴})
- P_fest: Fehlerrate des linearen Filters mit **nominalen** Gewichten und nominaler Mittelpunktschwelle auf Daten des wahren Modells (Fehlausrichtung von Gewicht und Schwelle exakt im Gauß-Bild).
- P_orakel: am wahren Modell neu kalibriert (nur Diagnose).
- Je ω: Worst-Case max über Abweichungen und Mittelwert; ω_wc = argmin Worst-Case, ω_mittel = argmin Mittel; Regret der nominalen Wahl.

## Entscheidungsregel
- **Robustheitsgewinn relevant**, wenn der Worst-Case- oder Mittel-Regret der nominalen Wahl ≥ 2 pp ist; dann Trajektorienprüfung (Bayes + MF mit Nominalkalibrierung) an ω_nominal und ω_wc für die größte Abweichung.
- Sonst Nullresultat (Gauß) für diese Abweichungsklasse.
- Gültigkeit: Gauß-Abweichung am Pilotpunkt ≲ 1–2 pp (F-3.3); Regrets unter 2 pp werden nicht interpretiert.

## Einschränkungen
Einzelabweichungen (keine Kombinationen), statisch während T, nur ω optimiert, Schwelle ohne Nachkalibrierung.
