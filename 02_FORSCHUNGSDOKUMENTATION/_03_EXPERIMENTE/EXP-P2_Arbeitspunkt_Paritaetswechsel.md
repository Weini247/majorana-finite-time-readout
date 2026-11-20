# EXP-P2 — Arbeitspunkt unter Paritätswechsel (Etappe 6, Q-6C)

**Klasse:** explorativ · **Status:** abgeschlossen 2026-11-20 (Lauf `EXP-P2_20261119T103251Z`) — Q-6C `FAILED` (Nullresultat, F-6.4). Vorab registriert 2026-11-19, nach EXP-P1 (F-6.3) und vor jeder EXP-P2-Rechnung. Start freigegeben von der Projektleitung am 2026-11-19.

## Auslöser
Laut ETAPPE_6_PLAN §6 wird EXP-P2 gerechnet, wenn EXP-P1 einen Bayes-Vorteil zeigt **oder** wenn T* stark von Γ_qp abhängt. Die zweite Bedingung ist erfüllt (T* fällt von ≥ 8 µs auf 2–4 µs). Kriterium K-6c im Plan („EXP-P2 entfällt“ bei Nullresultat für Q-6B) widerspricht dem und ist enger formuliert. Diese Spannung ist hier dokumentiert. Die Entscheidung trifft die Projektleitung, nicht eine Nachinterpretation.

## Frage
- **Q-6C:** Verschiebt sich der fehlerminimale Arbeitspunkt ω unter Γ_qp > 0 weg von ω_stat = 11.99?

Ohne Wechsel ist 11.99 klar am besten (EXP-E3, T = 5000: MF 0.056 gegen 0.100/0.099 bei 11.97/12.01).

## Fixiert
- Protokoll, Decoder, T-Raster, Bestimmung von T\*, Kalibrier-/Testaufteilung und Gültigkeitsbedingungen **identisch mit EXP-P1**. Ausgenommen ist die E3-Konsistenzprüfung, weil hier kein Γ = 0 gerechnet wird. Der Code ruft dieselbe Funktion `punkt` auf, nur ω ist ein Parameter.
- ω ∈ {11.97, 12.01}. I0 und θ je ω aus `EXP-E2_20261109T205736Z` (Budget n̄* = 0.3).
- Γ_qp⁻¹ ∈ {15 µs, 5 µs}, also die beiden Punkte, an denen EXP-P1 eine Γ-Abhängigkeit von T* zeigte.
- **Referenz ω = 11.99:** die Werte aus EXP-P1 (`EXP-P1_20261118T152412Z`) bei denselben Γ_qp. 11.99 wird nicht neu gerechnet.
- 2000 Kalibrier- und 2000 Testrecords je Startparität, Seed-Basis 7000 (disjunkt zu EXP-P1).
- Skript `_08_ERGEBNISSE/_04_PARITAETSWECHSEL/exp_p2_arbeitspunkt.py`.

## Entscheidungsregel
- Je Γ_qp ist P_min(ω) die Testfehlerrate des besten Decoders (über MF_nom, MF_Γ, Boxcar, Bayes) bei dessen T\*.
- **Q-6C positiv**, wenn bei mindestens einem Γ_qp gilt: P_min an 11.97 oder 12.01 liegt **unter** P_min an 11.99, und die Wilson-95-%-Intervalle sind disjunkt.
- Sonst Nullresultat: Der Arbeitspunkt verschiebt sich auf dem Raster nicht. Angegeben wird die kleinste beobachtete Differenz P_min(Nachbar) − P_min(11.99) mit Intervallen.

## Gültigkeitsbedingungen (je Punkt)
- Bayes-LLR-Mittel zeigt für beide Startparitäten zur wahren Parität.
- Bayes ist bei keinem T signifikant schlechter als Boxcar (gepaarter Vergleich, z < +4).
- Der Anteil gekippter Testtrajektorien bei T = 10⁴ liegt im Intervall um ½(1 − e^{−2Γ_qp T}) (|z| < 4).

Verletzung ⇒ Punkt ungültig, Ursache klären, nicht auswerten.

## Bekannte Einschränkungen
- ω-Raster grob (0.02); eine Verschiebung unterhalb der Rasterweite ist nicht auflösbar.
- Die Referenz 11.99 stammt aus einem anderen Lauf mit anderen Seeds, ist aber statistisch unabhängig. Die Intervalle berücksichtigen das.
- Gleiche Modell- und Ratenannahmen wie EXP-P1 (A6-1, U = 1 nur für ε = 0, φ = 0; ω ≠ 11.99 ändert ε und φ nicht).

## Ergebnis (Lauf `EXP-P2_20261119T103251Z`, 2026-11-20, Laufzeit ≈ 14 h)

**Gültigkeit:** an allen vier Punkten erfüllt (LLR-Vorzeichen korrekt; Bayes − Boxcar größtes z = +0.69; gekippte Trajektorien |z| ≤ 1.66).

| Γ_qp⁻¹ | ω = 11.97 | ω = 11.99 (EXP-P1) | ω = 12.01 |
|---|---|---|---|
| 15 µs | 0.1845 [0.168, 0.202] (MF_Γ) | 0.1407 [0.126, 0.157] (MF_Γ) | 0.1660 [0.150, 0.183] (Bayes) |
| 5 µs | 0.2640 [0.245, 0.284] (MF_Γ) | 0.2348 [0.217, 0.254] (MF_Γ) | 0.2528 [0.234, 0.272] (Bayes) |

P_min = Testfehlerrate des besten Decoders bei seinem T*, Wilson-95-%-Intervall.

**Q-6C: Nullresultat.** An keinem Γ_qp liegt ein Nachbarpunkt unter 11.99. Kleinste Differenz P_min(Nachbar) − P_min(11.99): +1.8 pp (12.01, 5 µs; Intervalle überlappen) und +2.5 pp (12.01, 15 µs). Der Arbeitspunkt ω_stat = 11.99 bleibt auf dem Raster optimal.

Nebenbeobachtung (keine Entscheidung): An den Nachbarpunkten ist das Signal schwächer (LLR-Mittel ≈ ±0.8 bis ±2.3 statt +5.4/−2.2 bzw. +2.2/−0.9 an 11.99); Bayes liegt dort an zwei Punkten vorn, aber nie > 2 pp mit disjunkten Intervallen vor dem besten linearen Decoder (12.01, 15 µs: 0.166 gegen 0.185, Intervalle überlappen knapp).
