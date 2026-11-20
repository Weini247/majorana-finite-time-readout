# Etappe 6 — Paritätswechsel während der Messung: Bericht und Gate G6

**Stand:** 2026-11-20 · Commit `f04eb78` · Testsuite 66/66 (37 aktiv, 29 wissenschaftlich)

## 1. Leitfrage dieser Etappe
Wie verändern Quasiteilchen-Paritätswechsel mit Rate Γ_qp während der Messung die Einzelschuss-Auslese der Majorana-Box? Konkret:
- **Q-6A:** Welche Messzeit ist optimal, und wie hängt die minimale Fehlerrate von Γ_qp ab?
- **Q-6B:** Lohnt sich ein Bayes-(Wonham-)Filter, der Wechsel explizit modelliert, gegenüber linearen Decodern?
- **Q-6C:** Verschiebt sich der fehlerminimale Arbeitspunkt ω?

## 2. Was gebaut und validiert wurde
| Baustein | Ort | Validierung | Status |
|---|---|---|---|
| Paritätswechsel als Telegrafenprozess auf ρ = ρ₊ ⊕ ρ₋ (U = 1 bei ε = 0, φ = 0) | ADR-0006, `_02_AUSFUEHRUNG/paritaetswechsel.py` | VAL10: Rabi-Basis-Überlapp mit Negativkontrolle; Γ = 0 bitgenau wie der alte Code | VERIFIED (F-6.1) |
| Trajektorien mit Poisson-Wechseln (eigener Zufallsstrom) | ebd., `trajektorien_mit_wechsel` | VAL10: Mittelwert gegen gekoppelte Mastergleichung im Raum 2⊗d; Telegrafenstatistik | VERIFIED (F-6.1) |
| Wonham-Filter je Anfangsparität (LLR der Anfangsparität) | ebd., `log_likelihood_quotient_mit_wechsel` | VAL10: Kalibrierung; Filter ohne Wechsel nachweislich überkonfident (< −4 σ) | VERIFIED (F-6.1) |
| Telegrafen-Benchmark, dispersiver Grenzfall | VAL11 | Boxcar aus Quantentrajektorien gegen unabhängige klassische Monte-Carlo-Rechnung, mit und ohne Wechsel, |z| ≤ 1.1 | VERIFIED (F-6.2) |

Die Γ_qp-Werte stammen aus der Literatur (Register §G): 14.5 µs (Microsoft-Tetron, X-Schleife), > 1 ms (Kitaev-Kette), bis ≈ 20 s.

## 3. Ergebnisse
| Befund | Aussage | Status |
|---|---|---|
| F-6.3 | **EXP-P1** (ω = 11.99, Γ_qp⁻¹ ∈ {∞, 1 ms, 100 µs, 15 µs, 5 µs}, T bis 8 µs): P_min = 0.8 / 1.3 / 4.4 / 14 / 23.5 %. Q-6B Nullresultat (größter Bayes-Vorteil 0.15 pp). Optimale endliche Messzeit nur für Γ-blinde Decoder | REPRODUCED (Q-6A), FAILED (Q-6B) |
| F-6.4 | **EXP-P2** (ω ∈ {11.97, 12.01}, Γ_qp⁻¹ ∈ {15, 5} µs): Nachbarpunkte durchweg schlechter als 11.99 (kleinste Differenz +1.8 pp) | FAILED (Q-6C) |

Kerntabelle EXP-P1 (Testfehlerrate bei T*, T* in µs; 4000 Testrecords je Punkt):

| Γ_qp⁻¹ | MF_nom | MF_Γ | Boxcar | Bayes |
|---|---|---|---|---|
| ∞ | .0095 (8) | .0095 (8) | .0080 (8) | .0083 (8) |
| 1 ms | .0125 (8) | .0125 (8) | .0125 (8) | .0128 (8) |
| 100 µs | .0465 (8) | .0450 (8) | .0505 (6) | .0435 (8) |
| 15 µs | .152 (4) | .141 (4) | .155 (4) | .142 (4) |
| 5 µs | .242 (2) | .235 (4) | .245 (2) | .235 (2) |

Fehlerrate bei T = 8 µs, also bei zu langer Messung: 15 µs: MF_nom .192, Boxcar .192 gegen Bayes .156, MF_Γ .164. 5 µs: .344 / .337 gegen .240 / .240.

Abbildung: `abbildungen/paritaetswechsel_messzeit.png` (Skript `_09_ABBILDUNGEN/abbildungen_etappe6.py`).

## 4. Antwort auf die Leitfrage (Stand G6)
Für die L01-Parameter, n̄* = 0.3, η = 0.5 und symmetrische, antriebsunabhängige Paritätswechsel gilt:

1. **Paritätswechsel begrenzen die Auslese.** Ab Lebensdauern von ≈ 100 µs und darunter dominieren sie die Fehlerrate. Bei 15 µs, der gemessenen Größenordnung im Tetron, liegt P_min bei ≈ 14 %.
2. **Optimale Messzeit:** Ein Decoder, der Γ_qp nicht kennt, muss die Messzeit auf etwa ein Drittel der Paritätslebensdauer abstimmen. Danach steigt seine Fehlerrate wieder, signifikant bei 15 und 5 µs.
3. **Die Kenntnis von Γ_qp schafft Robustheit, nicht Genauigkeit.** Bayes und ein linearer Matched Filter mit Γ-Gewichten erreichen dasselbe Minimum wie die Γ-blinden Decoder. Nach T* bleiben sie aber flach. Am Minimum ist der Bayes-Filter dem besten linearen Decoder nicht messbar überlegen.
4. **Der Arbeitspunkt bleibt bei ω_stat = 11.99.** Das bestätigt F-3.5 und F-3.7 auch unter Paritätswechsel.

Zulässiger Kurzclaim: „In einem validierten Homodynmodell der Majorana-Box (Benjadi & Egger 2026, starke Kopplung) mit symmetrischen Paritätswechseln senkt ein Wonham-Filter die minimale Fehlerrate nicht messbar unter die eines linearen Matched Filters. Die Kenntnis der Wechselrate macht die Auslese aber unempfindlich gegen zu lange Messzeiten, während Γ-blinde Decoder ein Optimum bei etwa einem Drittel der Paritätslebensdauer haben.“

Unzulässig:
- „Bayes-Filter sind für Paritätsauslese nutzlos.“ (Begründung: Es wurde nur die Anfangsparität dekodiert, unter symmetrischen Raten und an einem Arbeitspunkt.)
- „Die optimale Messzeit ist allgemein τ/3.“ (Begründung: Das T-Raster ist grob, es wurde ein Regime untersucht.)

Methodischer Nebenbefund: In VAL11 ist der Wonham-Filter mit Wechsel ebenfalls nicht besser als Boxcar, obwohl er ohne Wechsel klar besser ist. Ursache: Das Einschwingen des Signals und der Informationsverlust über die Anfangsparität wirken gegeneinander. Das Nullresultat von Q-6B ist also kein Artefakt dieses Modells, sondern tritt schon im einfachsten Grenzfall auf.

## 5. Nicht erledigt in Etappe 6
- **Annahmen außerhalb des Plans (§9):** asymmetrische oder antriebsabhängige (messinduzierte) Vergiftung, Mehrfachquasiteilchen, ε ≠ 0 oder φ ≠ 0 (U ≠ 1), schwache Kopplung.
- **Andere Fragestellung:** Dekodierung der Parität am Ende der Messung (relevant für Fehlerkorrektur), sequentieller Test mit variabler Messzeit.
- **Prozessnotiz:** Kriterium K-6c („EXP-P2 entfällt“) widersprach §6 des Plans. EXP-P2 wurde auf Entscheidung der Projektleitung gerechnet; der Widerspruch ist in der Registrierung dokumentiert.
- **Aus Etappe 1 weiterhin offen, nicht blockierend:** V1-10, V1-12, Eq. (27), Vorzeichenfrage Eq. (22), Autorenfrage.

## 6. Vorschlag zu G6 (zur Freigabe)
1. **Etappe 6 abschließen**, F-6.1 bis F-6.4 wie dokumentiert.
2. **Etappe 4 (ML-Decoder) bleibt gestrichen.** Auch unter Paritätswechsel gibt es keine Lücke zwischen linearem Decoder und Bayes-Filter, die ein gelerntes Modell schließen könnte.
3. **Öffentliches Repo aktualisieren**: Ergebnisse von Etappe 6, Abbildung, README-Abschnitt. Vorher Bereinigung privater Pfade wie bei Etappe 5.
4. **Optional Etappe 7**, nur mit vorab registrierter Frage. Kandidaten:
   - (a) messinduzierte Vergiftung, Γ_qp wächst mit dem Antrieb. Das ergibt einen echten Zielkonflikt zwischen Signal und Wechseln.
   - (b) Dekodierung der Endparität, wo der Wonham-Filter seinen strukturellen Vorteil ausspielen könnte.
5. **Kontakt zu den Autoren:** Der Stand reicht für ein Gespräch (Reproduktion, endliche Messzeit, Paritätswechsel). 
