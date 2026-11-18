# Master Research Plan — ParityReadoutLab

**Version 0.1 · 2026-11-09 · Status: zur Prüfung durch die Projektleitung vorgelegt (Gate G0).**
Jede Etappe folgt dem Zyklus **Literatur → Fragestellung → Modell → Methode → Experiment → Validierung → Interpretation → nächste Entscheidung**. Eine Etappe ist erst abgeschlossen, wenn ihre wissenschaftlichen Akzeptanzkriterien erfüllt sind, nicht wenn Code läuft.

## 1. Präzisierte Forschungsfrage

**Leitfrage (P1):** Im effektiven Box–Doppelpunkt–Resonator-Modell von L01: Stimmt der Arbeitspunkt \((\varepsilon,\omega,\varphi,\bar n)\), der den **stationären** Paritätskontrast maximiert, mit dem Arbeitspunkt überein, der den **Single-Shot-Fehler \(P_{err}(T)\) einer Homodynmessung der Dauer \(T\)** mit Effizienz \(\eta\) bei gleicher Photonenressource minimiert — nominal und unter Parameterdrift?

**Was bereits beantwortet ist (siehe `02_NEUHEITSREGISTER.md`):** stationäre Physik (L01); SNR(τ) im dispersiven Limit mit κ = 2χ (L03); zeitaufgelöste Messung mit QD-Ladungssensor (L04/L05); Rauschvisibility, resonant bevorzugt (L06). → Die Frage ist **nur im resonanten/intermediären Regime, mit explizitem Messkanal, Ressourcenfairness und Drift** potenziell offen. Originalität vorläufig 4–6/10.

**Teilfragen:**
- Q-A (Etappe 1): Kann ich L01 Fig. 3(c) innerhalb registrierter Toleranz reproduzieren, inkl. Einheiten-, Antriebs- und Vorzeichenkonvention?
- Q-B (Etappe 2): Wie hängt \(P_{err}(T)\) im L01-Modell von \(\Delta_z,\varepsilon,\eta,\bar n\) ab, und wie gut sagt der stationäre Kontrast die Rangfolge der Arbeitspunkte voraus?
- Q-C (Etappe 3): Ist der Regret der stationären Wahl größer als 2 Prozentpunkte (vorab fixiert) in einem physikalisch relevanten Gebiet, nominal oder unter Drift in \(t_0,\varphi,\varepsilon\)? Welche Modellannahme trägt ihn?
- Q-D (Etappe 4, bedingt): Bringt ein gelernter Decoder/Optimierer messbaren Mehrwert gegenüber Bayes-Filter und Matched Filter?

**Ergebnisklassen (vorab):** (1) Reproduktion · (2) Validierung eigener Numerik · (3) explorative Rechnungen · (4) potenziell originelle Resultate. Jede Abbildung und jeder Befund wird genau einer Klasse zugeordnet.

## 2. Etappenübersicht und Gates

| Etappe | Ziel | Gate am Ende | Grobaufwand (12–18 h/Woche) |
|---|---|---|---|
| 0 | Reconnaissance & Architektur | **G0**: Plan freigegeben | erledigt bis auf Freigabe |
| 1 | Referenzphysik & Reproduktion Fig. 3(c) | **G1**: REPRODUCED oder begründet BLOCKED (Kill K-1 nach 2 Wochen) | 2–3 Wochen |
| 2 | Endliche Messung (SME, Decoder, \(P_{err}(T)\)) | **G2**: konvergente Fehler–Zeit-Kurven + Literaturabgleich R-1 bestanden | 3–4 Wochen |
| 3 | Robustheit & Arbeitspunktoptimierung | **G3**: Regret-Befund (positiv oder Nullresultat mit engem CI) | 3–5 Wochen |
| 4 | Scientific ML (nur falls G3 eine begründete Aufgabe liefert) | **G4**: Mehrwert nachgewiesen oder Negativresultat | 3–6 Wochen, optional |
| 5 | Research Release | **G5**: reproduzierbares Repo + Bericht | 2–3 Wochen |

## 3. Etappenpläne (einheitliches Schema)

### Etappe 0 — Research Reconnaissance & Architecture
1. **Ziel/offene Frage:** Ist P1 als Einstieg tragfähig und wo genau liegt die mögliche Lücke?
2. **Literatur:** L01–L06, L14, L20 (Kickoff-Tiefe siehe Register).
3. **Annahmen/Gleichungen:** L01 Eqs. (1)–(45) extrahiert; Konventionen v0.1.
4. **Aufgaben:** Vorrecherche ✔, Literatur ✔ (Kickoff-Tiefe), Novelty ✔, Architektur ✔ (ADR-0001…0004 (`_01_ENTSCHEIDUNGEN/`)), Stage-1-Plan ✔.
5. **Module:** keine (bewusst).
6. **Validierung:** fig3c md5 verifiziert.
7. **Ergebnisdateien:** `02_FORSCHUNGSDOKUMENTATION/*`.
8. **DoD:** Plan durch die Projektleitung geprüft; offene Fragen Q-2…Q-6 beantwortet oder bewusst vertagt.
9. **Risiken:** Plan überdimensioniert → Gates und Kill Criteria.
10. **Abhängigkeit:** Etappe 1 braucht G0 + Freigabe für Umgebung/Datendownload.

### Etappe 1 — Reference Physics & Reproduction → Detailplan `02_FORSCHUNGSDOKUMENTATION/_02_ETAPPEN/ETAPPE_1_PLAN.md`
1. **Ziel:** Vertrauenswürdiger Steady-State-Kern; Fig. 3(c) reproduziert.
2. **Literatur:** L01 vollständig inkl. PDF-Version (Abbildungsgrafiken), L25 (Input-Output), Breuer–Petruccione-Konventionen.
3. **Gleichungen:** L01 Eqs. (10)–(20), (33)–(37), (43)–(45).
4. **Aufgaben:** WP 1.0–1.6 (Umgebung, Daten, Herleitung, Konventionsdiskriminierung, Solver, Reproduktion, Fehlerbudget).
5. **Module:** `params`, `model`, `steady`, `semiclassical`, `observables`, `reference`, `provenance`.
6. **Validierung:** V1-01 … V1-12 (`06_VALIDIERUNGSREGISTER.md`).
7. **Abbildungen:** R1 Overlay + Residuenpanel Fig. 3(c); Cutoff-Konvergenz; Konventions-Diskriminierungsplot.
8. **DoD:** EXP-R1 `REPRODUCED` gemäß registrierter Toleranz *oder* `BLOCKED` mit konkreter Autorenfrage.
9. **Kill:** K-1 (2 Wochen), K-6.
10. **Abhängigkeit:** Etappe 2 nutzt `model`/`steady` als Mittelwert-Referenz für SME.

### Etappe 2 — Finite-Time Measurement
1. **Ziel/Frage:** Q-B. Fehlerrate als Funktion der Messzeit im L01-Modell mit physikalischem Messkanal.
2. **Literatur (WP 2.0, vor Code):** Volltexte L03, L04, L05, L06, L20, L28; R-2 Forward-Citations. Ergebnis: Novelty-Update, ggf. Umplanung.
3. **Modell:** SME (Konventionen §4), Puls \(\mathcal E(t)\) (Rechteck, dann geglättet), Startzustand Vakuum ⊗ Rabi-Grundzustand je Parität; \(\eta\in\{0.2,0.5,1\}\); \(\kappa_{int}\) optional.
4. **Aufgaben:** WP 2.1 Detektormodell spezifizieren (ADR); WP 2.2 SME-Integration (QuTiP `smesolve`, Homodyn) + unabhängiger Mittelwerttest; WP 2.3 Decoder-Leiter: integrierter Record → Matched Filter (aus Mittelwerttrajektorien) → modellbasierte Likelihood/Bayes-Filter (L20); WP 2.4 analytischer Gauß-Benchmark im linearen Regime (Fehler \(\tfrac12\mathrm{erfc}(\mathrm{SNR}/2\sqrt2)\)); WP 2.5 \(P_{err}(T)\)-Kurven für 2 Arbeitspunkte; WP 2.6 Nicht-QND-Diagnostik (paritätsinterne Anregung \(\langle\tau_z\rangle(t)\)).
5. **Module:** `measurement`, `trajectories`, `records`, `decoders`, `statistics`.
6. **Validierung:** Ensemblemittel SME = Mastergleichung (T4); \(\eta=0\) ⇒ \(P_{err}=0.5\) im CI; \(t_1=0\) ⇒ \(P_{err}=0.5\); dt-Halbierung; Matched Filter = Likelihood im Gauß-Limit.
7. **Abbildungen:** \(P_{err}(T)\) mit CI je \(\eta\); stationärer Kontrast vs. \(P_{err}(T)\) (Rangkorrelation); Einschwing-/Nicht-QND-Panel.
8. **DoD:** konvergente Kurven (Cutoff, dt, Recordzahl) für ≥ 2 Arbeitspunkte × 3 Effizienzen; Literaturabgleich dokumentiert.
9. **Kill:** K-2 (nur triviale Einschwingzeit), K-7 (Nicht-QND dominiert unkontrolliert).
10. **Abhängigkeit:** Etappe 3 braucht schnelle \(P_{err}\)-Auswertung → evtl. Gauß-/Linearantwort-Surrogat, validiert gegen SME.

### Etappe 3 — Robustness & Optimization
1. **Ziel/Frage:** Q-C. Regret \(R=P_{err}(x_{stat})-\min_x P_{err}(x)\) unter gleicher Ressource, nominal und unter Drift.
2. **Literatur (WP 3.0):** R-3; L06 vertieft; robuste Bayes'sche Designkriterien.
3. **Modell:** Drift als vorab fixierte Verteilung pro Record (Kalibrierdrift) in \(t_0\) (0/1/5 %), \(\varphi\), \(\varepsilon\); Decoder kalibriert auf Nominalmodell (Mismatch) vs. adaptiv.
4. **Aufgaben:** WP 3.1 Designraum + Ressourcenconstraints; WP 3.2 Gittersuche (Baseline) über \((\varepsilon,\omega)\); WP 3.3 Regretkarten; WP 3.4 robuste Auswahl (Worst-Case, Erwartungswert); WP 3.5 Ablation: welche Annahme trägt den Effekt (RWA, Temperatur, Nicht-QND, η); WP 3.6 statistische Absicherung.
5. **Module:** `design`, `robust`, `report`.
6. **Validierung:** Regret auf disjunkten Testrecords; Konvergenz in Gitterauflösung; Zufalls-Arbeitspunkt-Kontrolle.
7. **Abbildungen:** Regretkarte; Fehler–Zeit-Paretofront bei gleicher Photonenzahl; Ablationsabbildung.
8. **DoD:** Befund „Regret > 2 pp in Gebiet X mit CI" oder „Regret < 2 pp im gesamten vorab gewählten Gebiet mit CI-Obergrenze".
9. **Kill:** K-3 (kein Effekt ⇒ kein immer größerer Sweep), K-4.
10. **Abhängigkeit:** Etappe 4 nur, wenn eine teure Optimierung/Inferenz identifiziert ist, deren Baseline klar definiert ist.

### Etappe 4 — Scientific ML Extensions (bedingt)
Nur bei positiver Begründung aus G3. Kandidaten: (a) Bayes'sche Optimierung bei teuren SME-Sweeps vs. Gittersuche; (b) Decoder für Drift-Mismatch vs. Bayes-Filter mit Parameterinferenz. Pflicht: Train/Test-Trennung über Seeds *und* Parameterfamilien, Kalibrierung (Reliability), mindestens 5 Trainingsseeds, Kosten getrennt (Simulation/Online/Training). DoD: Mehrwert über stärkster klassischer Baseline mit CI oder dokumentiertes Negativresultat.

### Etappe 5 — Research Release
Wissenschaftliches Audit, Referenzlauf per einer Kommandozeile, Benchmarks (Fehler vs. Laufzeit), publikationsfähige Abbildungen, `02_FORSCHUNGSDOKUMENTATION/07_BEFUNDE.md`, Attribution der Zenodo-Daten (CC-BY-4.0), kritische Einordnung gegenüber L01–L06. Optional: Anschluss P2 bewerten. GitHub-Veröffentlichung nur nach ausdrücklicher Freigabe.

## 4. Entscheidungspunkte

| ID | Zeitpunkt | Entscheidung | Kriterium |
|---|---|---|---|
| D-0 | jetzt | Plan freigeben, Umgebung/Datendownload erlauben | Projektleitung |
| D-1.1 | WP 1.3 | Einheitenkonvention λ₀ | Datenanpassung fig3c, beide Varianten gerechnet |
| D-1.2 | G1 | Reproduktion akzeptiert / Autorenfrage | Toleranz T3 |
| D-2.1 | WP 2.0 | Parameterbasis Etappe 2 (Paper-nah primär, Vorrecherche-Pilot sekundär) | Literaturabgleich |
| D-2.2 | G2 | Weiter zu Etappe 3 / Projekt als Reproduktionswerkzeug abschließen | K-2 |
| D-3 | G3 | Etappe 4 ja/nein | Regret-Befund |

## 5. Querschnittsregeln

- Keine Neuheitsbehauptung ohne R-1/R-2 (`02_NEUHEITSREGISTER.md` §4).
- Jede Etappe beginnt mit einem Literatur-WP und endet mit einem Eintrag in `07_BEFUNDE.md` und Statusupdate in `02_FORSCHUNGSDOKUMENTATION/_02_ETAPPEN/`.
- Negativresultate und gescheiterte Hypothesen werden mit Status `FAILED` behalten, nicht gelöscht.
- Experimente werden **vor** der Rechnung in `02_FORSCHUNGSDOKUMENTATION/_03_EXPERIMENTE/` registriert (Parameter, Metrik, Relevanzschwelle, Stichprobengröße).
