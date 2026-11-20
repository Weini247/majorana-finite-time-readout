# EXP-P1 — Optimale Messzeit und Decoder unter Paritätswechsel (Etappe 6, Q-6A/Q-6B)

**Klasse:** explorativ · **Status:** abgeschlossen 2026-11-19 (Lauf `EXP-P1_20261118T152412Z`) — Q-6B `FAILED` (Nullresultat), Q-6A beantwortet (F-6.3). Vorab registriert 2026-11-18, nach VAL10/VAL11 und vor jeder EXP-P1-Rechnung.

## Fragen
- **Q-6A:** Wie hängen minimale Fehlerrate P_min und beste Messzeit T* von der Paritätswechselrate Γ_qp ab, je Decoder, am Arbeitspunkt ω_stat = 11.99?
- **Q-6B:** Schlägt der Bayes-(Wonham-)Filter den stärksten linearen Decoder (beide bei ihrem besten T) um mehr als 2 pp?

## Fixiert
- Modell, Messkanal, η = 0.5, n̄* = 0.3, Cutoff 8 wie EXP-E3; ω = 11.99; I0 und θ aus `EXP-E2_20261109T205736Z`. Paritätswechsel nach ADR-0006 (U = 1).
- **Γ_qp-Raster** (Paritätslebensdauer Γ_qp⁻¹): ∞, 1 ms, 100 µs, 15 µs, 5 µs; in Modelleinheiten mit 1 µs = 1256.6 λ₀⁻¹. Begründung siehe Literatur (unten); 15 µs statt 20 µs aus dem Planentwurf, weil eine gemessene Lebensdauer bei 14.5 µs liegt (Änderung vor jeder Rechnung).
- **Messzeiten:** T ∈ {500, 1000, 2500, 5000, 7500, 10⁴} λ₀⁻¹ (0.4–8 µs), als Anfangsstücke derselben Records.
- Je Γ_qp und Startparität 2000 Kalibrier- und 2000 Testrecords, neue Seeds (Basis 6000), dt = 0.2, Binbreite 0.4.
- **Decoder:**
  - MF_nom: Gewichte μ₊ − μ₋ aus dem Modell **ohne** Wechsel.
  - MF_Γ: Gewichte aus den Mittelwert-Records des gekoppelten Modells (Startparität ±1, gleiche Γ_qp).
  - Boxcar.
  - Bayes: Wonham-Filter mit der wahren Γ_qp, Schwelle 0.
  - MF und Boxcar mit Schwelle aus den Kalibrierrecords je T.
- **Beste Messzeit T\*:** je Decoder das T mit der kleinsten Fehlerrate auf den **Kalibrierrecords** (für Bayes: LLR auf den Kalibrierrecords, Schwelle 0). Bewertet wird nur auf den Testrecords. Bei Gleichstand das kürzere T.
- Skript `_08_ERGEBNISSE/_04_PARITAETSWECHSEL/exp_p1_paritaetswechsel.py`.

## Entscheidungsregel
- **Q-6B positiv**, wenn an mindestens einem Γ_qp gilt: P_Bayes(T*_Bayes) liegt um mehr als 2 pp unter dem besten linearen Decoder min(MF_nom, MF_Γ, Boxcar) bei dessen T*, **und** die Wilson-95-%-Intervalle sind disjunkt. Sonst Nullresultat mit Angabe des größten beobachteten Vorteils und seines Intervalls.
- **Q-6A** wird deskriptiv beantwortet: Tabelle T*(Γ_qp) und P_min(Γ_qp) je Decoder, mit der Auflösung des T-Rasters als Einschränkung. Eine „optimale Messzeit“ wird nur behauptet, wenn die Testfehlerrate bei T* signifikant (disjunkte Intervalle) unter der bei T = 10⁴ liegt.

## Gültigkeitsbedingungen (je Γ_qp, vor der Auswertung prüfen)
- Bayes-LLR-Mittel zeigt für beide Startparitäten zur wahren Parität.
- Bayes ist auf den Testdaten bei keinem T signifikant schlechter als Boxcar (gepaarter Vergleich, |z| < 4; V6-6).
- Γ_qp = 0: T = 2500 und 5000 im Wilson-Intervall der EXP-E3-Werte bei 11.99 (Konsistenz mit Lauf 2).
- Anteil der Testtrajektorien mit gekippter Parität bei T = 10⁴ im Intervall um ½(1 − e^{−2Γ_qp T}).
Verletzung ⇒ Punkt ungültig, Ursache klären, nicht auswerten.

## Diagnose (keine Entscheidung)
Fehlerrate getrennt nach Testtrajektorien mit und ohne Paritätswechsel bis T; Anteil gekippter Trajektorien je T.

## Literatur zum Γ_qp-Raster (Abstract-/Zusammenfassungsebene, vor Zitation prüfen)
- Microsoft Quantum, *Distinct lifetimes for X and Z loop measurements in a Majorana tetron device*, arXiv:2507.08795 (2025): Paritätswechselzeiten ≈ 14.5 µs (X-Schleife) und ≈ 12.4 ms (Z-Schleife).
- arXiv:2606.03884 (2026), InAs–Pb-Tetron: Wechselzeit ≈ 20 s (nur Abstract gesehen).
- N. van Loo et al., *Single-shot parity readout of a minimal Kitaev chain*, Nature 650, 334 (2026), arXiv:2507.01606: Lebensdauer > 1 ms.
Das Raster reicht von „praktisch kein Wechsel während T“ (12 ms, 20 s ≈ ∞ bei T ≤ 8 µs) bis an die Messzeit heran (5 µs).

## Bekannte Einschränkungen
- Symmetrische, antriebsunabhängige Wechselrate (A6-1); ein Arbeitspunkt; U = 1 nur für ε = 0, φ = 0.
- T* nur auf dem Raster aufgelöst.
- Die Fehlerrate ist auf die Anfangsparität bezogen. Für Anwendungen, die die Parität am Ende brauchen, wäre die Frage anders gestellt.

## Ergebnis (Lauf `EXP-P1_20261118T152412Z`, 2026-11-19, Laufzeit ≈ 16.8 h)

**Gültigkeit:** an allen fünf Γ_qp-Punkten erfüllt. LLR-Mittel zur wahren Parität (Γ⁻¹ = ∞: +11.8/−10.2; 5 µs: +2.2/−0.86). Bayes nie signifikant schlechter als Boxcar (größtes z = +0.33; negative z = Bayes besser, bis −13.5 bei 5 µs, T = 10⁴). Γ = 0 konsistent mit EXP-E3 (MF 0.128/0.054, Bayes 0.122/0.051 bei T = 2500/5000; E3: 0.130/0.056, 0.127/0.055). Gekippte Testtrajektorien bei T = 10⁴: |z| ≤ 0.54 an allen Punkten.

| Γ_qp⁻¹ | MF_nom (T*) | MF_Γ (T*) | Boxcar (T*) | Bayes (T*) | Bayes − bester linearer |
|---|---|---|---|---|---|
| ∞ | 0.0095 (10⁴) | 0.0095 (10⁴) | 0.0080 (10⁴) | 0.0083 (10⁴) | +0.03 pp |
| 1 ms | 0.0125 (10⁴) | 0.0125 (10⁴) | 0.0125 (10⁴) | 0.0128 (10⁴) | +0.03 pp |
| 100 µs | 0.0465 (10⁴) | 0.0450 (10⁴) | 0.0505 (7500) | 0.0435 (10⁴) | −0.15 pp |
| 15 µs | 0.1520 (5000) | 0.1407 (5000) | 0.1552 (5000) | 0.1417 (5000) | +0.10 pp |
| 5 µs | 0.2415 (2500) | 0.2348 (5000) | 0.2448 (2500) | 0.2350 (2500) | +0.02 pp |

Testfehlerraten bei T* (T* auf den Kalibrierrecords bestimmt), je 4000 Testrecords; Wilson-95-%-Halbbreite ≈ 0.4 pp (∞) bis 1.9 pp (5 µs).

**Q-6B: Nullresultat.** An keinem Γ_qp liegt Bayes mehr als 2 pp unter dem besten linearen Decoder. Größter beobachteter Vorteil: 0.15 pp bei 100 µs (Bayes 0.0435 [0.0355, 0.0532] gegen MF_Γ 0.0450 [0.0368, 0.0550], Intervalle überlappen).

**Q-6A:** P_min steigt von 0.8 % (kein Wechsel) über 1.3 % (1 ms) und 4.4 % (100 µs) auf 14 % (15 µs) und 23.5 % (5 µs). T* fällt von 10⁴ (8 µs) auf 5000 (4 µs) bei 15 µs und 2500–5000 (2–4 µs) bei 5 µs. Eine optimale endliche Messzeit im Sinne der Regel (P(T*) signifikant unter P(10⁴)) besteht nur für die Γ-blinden Decoder: MF_nom und Boxcar bei 15 µs (0.152 gegen 0.192 bzw. 0.155 gegen 0.192) und bei 5 µs (0.242 gegen 0.344 bzw. 0.245 gegen 0.337). Für MF_Γ und Bayes nicht: deren Fehlerrate bleibt nach T* flach (15 µs: Bayes 0.142 → 0.156, MF_Γ 0.141 → 0.164; 5 µs: 0.235 → 0.240), Intervalle überlappen.

**Einordnung (Interpretation, keine Entscheidung):** Γ-Kenntnis zahlt sich nicht in einer niedrigeren Minimalfehlerrate aus, sondern in Robustheit gegen zu lange Messung. Ein Γ-blinder linearer Decoder muss die Messzeit auf ≈ 1/(3 Γ_qp) abstimmen; Bayes oder ein MF mit Γ-Gewichten erreichen bei jedem T ≥ T* dasselbe Minimum. Am Minimum ist der lineare MF mit Γ-Gewichten praktisch optimal.
