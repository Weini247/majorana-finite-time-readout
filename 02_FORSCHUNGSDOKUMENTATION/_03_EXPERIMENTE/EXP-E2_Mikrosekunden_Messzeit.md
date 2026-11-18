# EXP-E2 — Arbeitspunktwahl im Mikrosekundenbereich (Folge von EXP-E1)

**Klasse:** explorativ (Etappe 2) · **Status:** Gauß-Stufe durchgeführt (Lauf `EXP-E2_20261109T205736Z`, F-2.6): Regret 0 bei n̄* = 0.3 mit P_G(10⁴) = 0.0076 ⇒ Nullresultat-Bedingung erfüllt; n̄* = 0.01 nicht entscheidbar (P_G(10⁴) = 0.30). Stufe 2 (Regret ≥ 2 pp) entfällt. Kontrollpunkte (Lauf `EXP-E2K_20261110T000043Z`, F-2.7): Gauß gültig bei n̄* = 0.01/T = 10⁴ und n̄* = 0.3/T = 1000 (dt-Halbierung bestanden), **verletzt bei n̄* = 0.3/T = 2500** (Gauß 0.116 vs. Matched Filter 0.133 [0.119, 0.149]) ⇒ Nullresultat für n̄* = 0.3 bei langem T nur `HYPOTHESIS`. Vorab registriert 2026-11-09, vor jeder Rechnung.

## Begründung
EXP-E1 lag bei T ≤ 320 ns nahe am Raten (F-2.5). Die Leitfrage ist erst dort aussagekräftig, wo die Fehlerraten deutlich unter 0.5 fallen.

## Unverändert gegenüber EXP-E1
Modell, Paritäten, Messkanal, η = 0.5, Ressourcenregel, ω-Raster [11.80, 12.20] (Schritt 0.01), Budgets n̄* ∈ {0.01, 0.3}, Metriken (D_ss, P_G, Regret).

## Geändert
- Messzeiten T ∈ {400, 1000, 2500, 5000, 10000} λ₀⁻¹ (0.32–8 µs).
- Stufe 1: nur Gauß-Benchmark (gültig im Pilotgebiet laut F-2.4).
- Stufe 2 (nur falls Gauß-Regret ≥ 2 pp irgendwo): Trajektorienprüfung an ω_stat und ω_T bei diesem T, 2000 + 2000 Records je Parität, dt-Halbierungsprüfung.

## Kontrollpunkte (präzisiert 2026-11-10, vor der Rechnung; Skript `_08_ERGEBNISSE/exp_e2_kontrollpunkt.py`)
Gültigkeit des Gauß-Benchmarks bei langem T, unabhängig vom Regret. Arbeitspunkt jeweils ω_stat mit I0 und θ unverändert aus dem EXP-E2-Lauf; 2000 Kalibrier- + 2000 Testrecords je Parität, Matched Filter (Gewichte = exakte Mittelwert-Records, Bins 5 λ₀⁻¹) und Boxcar, Wilson-95 %.
1. n̄* = 0.01, T = 10⁴, dt = 0.2
2. n̄* = 0.3, T = 2500, dt = 0.2 (T = 10⁴ aus Laufzeitgründen nicht: d = 16 ≈ 10× teurer pro Schritt)
3. + 4. n̄* = 0.3, T = 1000, dt = 0.2 und 0.1 (dt-Halbierung)

Kriterium: Gauß-Vorhersage (gleiche Binbreite) im Wilson-Intervall des Matched Filters ⇒ Gauß gültig an diesem Punkt; dt-Halbierung: Fehlerraten innerhalb der Intervalle gleich. Andernfalls gilt der Gauß-Scan bei langem T nur als `HYPOTHESIS`.

## Vorab-Anmerkung (2026-11-10): was ohne Rechnung folgt
- **η:** Die unbedingte Dynamik hängt nicht von η ab, nur die Messrate: SNR² ∝ η exakt. P_G ist monoton in SNR², also ist ω_T = argmin P_G **unabhängig von η** (im Gauß-Benchmark). η verschiebt nur die Fehlerraten, nicht die Arbeitspunktwahl.
- **T → ∞:** Nach dem Einschwingen sind die Mittelwert-Records konstant, SNR²(T) ≈ D_ss·T + const. Für große T geht ω_T deshalb zwangsläufig gegen ω_stat. Ein Regret kann nur bei mittleren T auftreten, wo Einschwingvorgänge zählen. Längere T-Scans brauchen keine neue Rechnung (Extrapolation), beantworten die Leitfrage aber auch nicht neu.

## Entscheidungsregel
Wie EXP-E1. Zusätzlich: Liegt der Gauß-Regret überall < 2 pp **und** fällt P_G bei T = 10⁴ unter 0.1, gilt für dieses Modell/Raster: „stationäre Wahl der Antriebsfrequenz ist hinreichend" (Nullresultat, Klasse explorativ). Der Trajektorienbestätigung bedarf das Nullresultat nur an einem Kontrollpunkt (Gauß-Gültigkeit bei langem T).
