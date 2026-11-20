# Etappe 6 — Paritätswechsel während der Messung (Detailplan)

**Status:** in Arbeit — G6a freigegeben 2026-11-18. **Zeitbox:** 4 Wochen bis G6; Kill-Kriterien §8.

## 1. Motivation und Einordnung
Etappen 2–3 setzen voraus, dass die Parität während der Messung erhalten bleibt (Annahme A3-1). Dann wird jede Messung mit wachsender Zeit T besser, und der lineare Matched Filter ist praktisch optimal (F-3.5). In realen Majorana-Bauelementen kippt die Parität durch Quasiteilchen-Vergiftung zufällig. Das erzeugt einen echten Zielkonflikt: Längeres Messen sammelt mehr Signal, erhöht aber die Wahrscheinlichkeit, dass sich die gesuchte Größe während der Messung ändert. Erst damit gibt es eine optimale Messzeit T*, und ein nichtlinearer Filter kann Sprünge erkennen, die ein linearer Filter verschmiert.

**Bekannt (vor Neuheitsbehauptung prüfen):** Für supraleitende Qubits mit T1-Zerfall während der Auslese sind optimale Integrationszeit, gewichtete Filter und Nichtlinearfilter beschrieben (L20 Gambetta et al. 2007; D'Anjou & Coish 2014). Ein Paritätswechsel ist das symmetrische Analogon (Telegrafenprozess statt einseitigem Zerfall). **Offen, Stand Etappe 0:** keine Rechnung dieser Art im Box–Doppelpunkt–Resonator-Modell mit Homodynkanal, η und Sättigung des Doppelpunkts. Der Beitrag wäre die quantitative Antwort für dieses Modell, nicht das allgemeine Phänomen.

## 2. Forschungsfragen
- **Q-6A (Hauptfrage):** Wie hängt die minimale Fehlerrate und die optimale Messzeit T* von der Paritätswechselrate Γ_qp ab, für Matched Filter, Boxcar und Bayes-Filter am Arbeitspunkt ω_stat = 11.99?
- **Q-6B:** Gibt es ein Γ_qp-Gebiet, in dem der Bayes-Filter den Matched Filter (beide bei ihrem jeweils besten T) um mehr als 2 pp schlägt, mit disjunkten Wilson-Intervallen?
- **Q-6C (nachrangig):** Verschiebt sich der fehlerminimale Arbeitspunkt ω unter Γ_qp > 0?

Zu dekodieren ist die **Parität zu Beginn der Messung** (Zustandspräparation bzw. Syndrom zum Messzeitpunkt). Die Parität am Ende wird als Nebengröße mitprotokolliert.

## 3. Modell
**Erweiterung:** Paritätsregister z ∈ {+1, −1} als klassischer Index. Der Zustand ist blockdiagonal, ρ = ρ₊ ⊕ ρ₋ (Paritätssuperauswahl, keine Kohärenz zwischen Sektoren). Jeder Block entwickelt sich mit dem bisherigen RWA-Lindblad-Modell seiner Parität (Eq. 10/12) und dem gemeinsamen Homodynkanal. Neu ist ein Sprungterm, der Wahrscheinlichkeit zwischen den Blöcken verschiebt:
\[ \dot\rho_\pm \supset \Gamma_{qp}\,(U\rho_\mp U^\dagger - \rho_\pm). \]

**Abbildung U zwischen den Sektoren:** Ein Paritätswechsel ändert den physikalischen Zustand von Resonator und Doppelpunkt nicht, nur den Hamiltonoperator. In der paritätsabhängigen Rabi-Basis ist U = 1 ⊗ V₋ᶻ†Vᶻ. **Für die L01-Parameter (ε = 0, φ = 0) ist t_z = t0 ± t1 für beide Paritäten reell und positiv, die Rabi-Eigenbasen stimmen überein, und U = 1** (Rahmen bei der Antriebsfrequenz für beide Sektoren gleich). Das wird vor der Implementierung analytisch geprüft (V6-0). Für φ ≠ 0 oder ε ≠ 0 wäre U nichttrivial; diese Fälle sind ausgeschlossen (siehe §9).

**Annahmen:**
- A6-1: Paritätswechsel als Markov-Telegrafenprozess mit symmetrischer Rate Γ_qp, unabhängig von Antrieb und Resonatorzustand. `HYPOTHESIS` (Vergiftung kann asymmetrisch und antriebsabhängig sein, L09).
- A6-2: Ein Wechsel ist instantan, ohne Änderung von Resonator- und Doppelpunktzustand.
- A6-3: Alle übrigen Parameter wie EXP-E3 (L01 stark, n̄* = 0.3, η = 0.5, Cutoff 8, I0/θ aus EXP-E2).

Die Modellentscheidung wird vor der Implementierung als **ADR-0006** festgehalten.

**Physikalische Raten (WP 6.0, Literatur vor EXP-P1 prüfen):** Berichtete Paritätslebensdauern in Majorana- und Kitaev-Ketten-Bauelementen liegen grob zwischen etwa 10 µs und einigen ms (zu verifizieren: L09, van Loo et al. Nature 2026, Messungen von Microsoft 2025). Das Raster deckt diesen Bereich bis an die Messzeit heran ab:
Γ_qp⁻¹ ∈ {∞, 1 ms, 100 µs, 20 µs, 5 µs}, in Modelleinheiten Γ_qp⁻¹ ≈ {∞, 1.26·10⁶, 1.26·10⁵, 2.5·10⁴, 6.3·10³} λ₀⁻¹ (1 µs ≈ 1257 λ₀⁻¹). **Nachtrag 2026-11-18 (vor EXP-P1):** 20 µs durch 15 µs ersetzt (gemessene X-Schleifen-Wechselzeit 14.5 µs, Literaturregister §G).

## 4. Methode
**Trajektorien:** Der bestehende blockweise Integrator mit exaktem kohärentem Propagator (F-3.4) wird auf zwei gekoppelte Blöcke erweitert. Der Paritätssprung wird als zusätzlicher Sprungterm erster Ordnung behandelt (wie die übrigen Sprungterme; Γ_qp·dt ≤ 3·10⁻⁵, unkritisch). Jede Trajektorie startet in einer definierten Parität; der wahre Paritätsverlauf wird gezogen und gespeichert (für Diagnose, nicht für Decoder).

**Decoder:**
- **Matched Filter / Boxcar** wie bisher, Gewichte aus dem Nominalmodell **ohne** Paritätswechsel (so würde ein Experiment ohne Vergiftungsmodell auswerten), Schwelle auf getrennten Kalibrierdaten. Zusätzlich ein MF mit Gewichten aus dem Modell **mit** Γ_qp (Mittelwerttrajektorien des erweiterten Modells), damit der Vergleich Bayes vs. linear fair ist.
- **Bayes-Filter (Wonham-artig):** Zwei Filter, einer je Anfangsparität, propagieren jeweils den gekoppelten Zustand ρ₊ ⊕ ρ₋ mit denselben Messdaten. Log-Likelihood-Quotient der Anfangsparitäten aus den Normierungen. Das ist für das Modell der optimale Test der Anfangsparität.
- **Messzeit:** Alle Decoder werden an denselben Kontrollzeitpunkten ausgewertet; T* je Decoder ist das Minimum über das Raster, mit Auswahl auf Kalibrierdaten und Bewertung auf getrennten Testdaten (keine Auswahl auf Testdaten).

**Aufwand:** EXP-E3 brauchte ≈ 1 h je ω-Punkt bei T = 5000. Mit T_max = 10⁴ und gekoppelten Blöcken ≈ 3–4 h je Punkt, 6 Prozesse. Hauptexperiment (5 Γ-Werte bei ω_stat) ≈ 18 h, also in zwei Nachtläufen.

## 5. Validierungen (vorab, alle vor EXP-P1)
| ID | Prüfung | Kriterium |
|---|---|---|
| V6-0 | U = 1 für L01-Parameter: Rabi-Eigenvektoren beider Paritäten bei ε = 0, φ = 0 | Überlapp ≥ 1 − 1e-12 (T1); für φ = 0.1 nachweislich ≠ 1 (Negativkontrolle) |
| V6-1 (VAL10) | Γ_qp = 0 ⇒ Integrator und Bayes-Filter identisch mit dem bisherigen Code | Records und LLR ≤ 1e-10 (T2) |
| V6-2 (VAL10) | Ensemblemittel der Trajektorien = Mastergleichung des gekoppelten Modells (mesolve) bei Γ_qp⁻¹ = 5 µs, auch abseits der Resonanz (Lehre aus F-3.4) | z ≤ 4 wie VAL9 |
| V6-3 (VAL10) | Paritätsstatistik: Anteil gekippter Trajektorien = ½(1 − e^{−2Γ_qp t}) | im Wilson-Intervall an 3 Zeitpunkten |
| V6-4 (VAL11) | Bayes-Filter mit Γ_qp im Grenzfall linearer Antwort gegen den analytischen Telegrafen-Benchmark (Gauß-Rauschen + zufälliger Vorzeichenwechsel des Mittelwerts; Analogie zu L20, Eq. für Boxcar mit Zerfall) | Fehlerrate im Wilson-Intervall der Vorhersage |
| V6-5 | Γ_qp T ≫ 1 ⇒ Anfangsparität nicht mehr dekodierbar | Fehlerrate → 0.5 im Intervall |
| V6-6 | Bayes nie signifikant schlechter als MF/Boxcar auf denselben Testdaten | gepaarter Vergleich |

**Stand 2026-11-18:** V6-0, V6-1, V6-2, V6-3 und die Filterkalibrierung bestanden (VAL10, F-6.1). V6-2 erwies sich als kaum trennscharf für den Wechsel selbst; die Kalibrierung mit Negativkontrolle übernimmt diese Rolle. V6-4 bis V6-6 offen. **Nachtrag:** V6-4 als VAL11 umgesetzt, nicht über die Formel aus L20, sondern als unabhängige klassische Monte-Carlo-Rechnung im dispersiven Grenzfall (kohärente Amplitude bei gegebenem Paritätsverlauf exakt); bestanden mit V6-6 (F-6.2). EXP-P1 registriert.

V6-4 braucht vorher die Journalfassung von L20 (Nichtlinearfilter und Zerfallsterm), offen seit R-1.

## 6. Experimente
- **EXP-P1 (Q-6A, Q-6B):** wird vor der Rechnung in `_03_EXPERIMENTE/` registriert. Skizze: ω = 11.99; Γ_qp-Raster aus §3; T-Kontrollpunkte {500, 1000, 2500, 5000, 7500, 10⁴} λ₀⁻¹ (0.4–8 µs); Decoder MF (nominal und mit Γ_qp), Boxcar, Bayes; je Parität 2000 Kalibrier- und 2000 Testrecords; neue Seeds.
- **Nachtrag 2026-11-19:** EXP-P1 abgeschlossen (F-6.3). Kein Bayes-Vorteil; T* hängt stark von Γ_qp ab (8 µs → 2–4 µs), damit ist die Bedingung für EXP-P2 erfüllt. Start nur nach Freigabe.
- **EXP-P2 (Q-6C):** nur wenn EXP-P1 bei einem Γ_qp einen Bayes-Vorteil zeigt oder T* stark von Γ_qp abhängt; ω ∈ {11.97, 11.99, 12.01} bei zwei Γ_qp-Werten.

**Vorab fixierte Schwelle:** Bayes-Vorteil > 2 pp mit disjunkten Intervallen an mindestens einem Γ_qp-Punkt (beide Decoder bei ihrem besten T) ⇒ positiver Befund für Q-6B. Sonst Nullresultat mit oberer Intervallgrenze.

## 7. Abbildungen
- Fehlerrate über T je Γ_qp und Decoder (Kernabbildung, zeigt T*).
- T*(Γ_qp) und P_min(Γ_qp) je Decoder.
- Bayes-Vorteil gegenüber MF über Γ_qp mit Intervallen.
- Diagnose: Fehlerrate getrennt nach Trajektorien mit und ohne Wechsel.

## 8. Abbruch- und Entscheidungskriterien
- K-6a: V6-2 oder V6-3 nach einer Woche nicht bestanden ⇒ Modellannahme oder Integrator klären, keine Experimente.
- K-6b: Laufzeit je Punkt > 8 h ⇒ T_max auf 7500 oder Γ_qp-Raster auf 4 Werte kürzen (vorher registrieren).
- K-6c: Kein Bayes-Vorteil > 2 pp an keinem Γ_qp ⇒ Nullresultat für Q-6B dokumentieren; Q-6A (T*-Kurven) bleibt als Ergebnis bestehen, EXP-P2 entfällt.

## 9. Nicht Teil dieser Etappe
- Asymmetrische oder antriebsabhängige Vergiftung, Mehrfachquasiteilchen, Vergiftung des Doppelpunkts.
- φ ≠ 0 oder ε ≠ 0 (nichttriviales U), schwache Kopplung.
- Echtzeit-Entscheidung (sequentieller Test mit variabler Messzeit). Möglicher Folgeschritt, wenn Q-6B positiv ist.

## 10. Gate G6
Bericht mit Antworten auf Q-6A/Q-6B (und Q-6C, falls gerechnet). Entscheidung über: Veröffentlichung im öffentlichen Repo, Neubewertung von Etappe 4 (ML-Decoder nur bei nachgewiesener Lücke zum Bayes-Filter), Kontakt zu den Autoren.
