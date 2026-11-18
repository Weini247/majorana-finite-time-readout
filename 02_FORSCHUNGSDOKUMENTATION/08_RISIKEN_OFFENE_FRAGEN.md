# Open Questions, Risks & Kill Criteria

## Projektfragen
| ID | Frage | Warum relevant |
|---|---|---|
| Q-2 | ~~Freigabe des Plans~~ — **erledigt** 2026-11-09 | — |
| Q-4 | ~~venv/Installation~~ — **erledigt** (`_UMGEBUNG/venv`, QuTiP 5.3.1) | — |
| Q-5 | ~~Zenodo-Download, git init~~ — **erledigt** (md5 aller 13 Dateien geprüft; lokales Repo ohne Remote, noch kein Commit) | — |
| Q-6 | Offene Fragen an die Autoren (Benjadi/Egger): Entwurf in `_04_BERICHTE/ETAPPE_1_BERICHT.md` §6, nicht gesendet | F-1.3/F-1.5 sind ohne Autorenauskunft nicht auflösbar |

## Wissenschaftliche offene Fragen
| ID | Frage | Status | Geplant in |
|---|---|---|---|
| Q-3 | λ₀-Konvention | **geklärt: gewöhnlich** (F-1.1) | — |
| Q-7 | Spaltenzuordnung fig3c; Sweep-Variable für \(\Delta_z\) | OPEN | WP 1.1/1.3 |
| Q-8 | Vorzeichen Eq. (35) | **geklärt** für die Reproduktion (Daten folgen Eq. 20) | — |
| Q-9 | \(I_0\) und Modell der „exakten" Referenz | **BLOCKED** (F-1.3); κ_in = κ_out konsistent | Autorenfrage |
| Q-13 | Vorzeichen der dispersiven Verschiebung Eq. (22)/(26) | HYPOTHESIS (F-1.5) | Autorenfrage |
| Q-10 | Hat L03/L06/L28 die Frage „stationär vs. endlichzeitoptimal" bereits beantwortet? | OPEN | WP 2.0 (R-1) |
| Q-11 | Welcher physikalische Messkanal ist für das Box-Readout realistisch (Reflektometrie-Port, Verstärkereffizienz)? | OPEN | WP 2.1 |
| Q-12 | Ist Startzustand „Rabi-Grundzustand" realistisch oder ist der Dot vor dem Puls thermisch/gemischt? | OPEN | WP 2.1 |

## Risiken
| ID | Risiko | Wahrscheinlichkeit | Gegenmaßnahme |
|---|---|---|---|
| R-1 | Reproduktion scheitert an unpublizierten Konventionen | mittel | registrierte Variantenmatrix, Zeitbox, Autorenfrage |
| R-2 | Neuheit bereits durch L03/L06/L28 abgedeckt | mittel–hoch | WP 2.0 vor Code; Projekt kann als validiertes Werkzeug enden |
| R-3 | Kontrast im resonanten Regime zu klein für endliche Messung | mittel | Ressourcenfaire Vergleiche, Nullresultat zulässig |
| R-4 | Nicht-QND-Effekte (τ_x-Kopplung) dominieren → Modell braucht Mehrniveau | mittel | WP 2.6-Diagnostik, K-7 |
| R-5 | SME-Kosten für Regretkarten zu hoch | mittel | Gauß-/Linearantwort-Surrogat validiert gegen SME; Profiling vor JAX |
| R-6 | Scope Creep (Framework statt Frage) | mittel | Gates, ADR-0001 |
| R-7 | Rechtliches/Attribution Referenzdaten | gering | CC-BY-4.0, Zitation in README |

## Kill Criteria
| ID | Kriterium | Konsequenz |
|---|---|---|
| K-1 | Nach 2 Wochen scheitert Referenzreproduktion an ungeklärten Konventionen | Erweiterungen pausieren, konkrete Frage formulieren (Vorrecherche) |
| K-2 | Endliche Zeit erzeugt nur bekannten, analytisch erklärbaren Einschwingeffekt | Projekt als Reproduktionswerkzeug abschließen |
| K-3 | Robustes Design im gesamten vorab gewählten Gebiet unter Relevanzschwelle | kein größerer ML-Sweep zur Effekterzwingung; Nullresultat berichten |
| K-4 | Relevante Nichtidealitäten erfordern unkontrollierte Vollgerätebeschreibung | keine Hardware-Fidelity-Aussagen |
| K-5 | Interne/externe Arbeit deckt die konkrete Frage ab | als Validierungsmodul anbieten oder zu P2/P3 wechseln |
| K-6 | (neu) Mehrere Konventionsvarianten reproduzieren gleich gut | Mehrdeutigkeit dokumentieren, keine willkürliche Wahl |
| K-7 | (neu) Nicht-QND-Physik verhindert ein wohldefiniertes Zwei-Hypothesen-Problem im Zielregime | Regime einschränken oder Modell erweitern (neue ADR) |
