# Research Gap / Novelty Register

Regel: Eine Aussage wird erst als potenziell originell geführt, wenn (a) die nächstliegende Literatur im Volltext geprüft ist und (b) ein konvergentes Resultat vorliegt. Bis dahin höchstens `HYPOTHESIS`.

## 1. Bereits bekannt — NICHT als neu beanspruchen

| # | Aussage | Beleg | Status |
|---|---|---|---|
| N-K1 | Stationäre parity-abhängige Suszeptibilität im Crossover dispersiv↔resonant; semiklassische Fehler (dispersiv < 0.1 %, resonant einige %) | L01 | VERIFIED (Literatur) |
| N-K2 | Endliche Temperatur im stationären Modell | L01 Sec. III.2.3 | VERIFIED (Literatur) |
| N-K3 | **Zeitaufgelöste / kontinuierliche Majorana-Paritätsmessung** (SME, QD-Ladungssensor) | L04, L05 | VERIFIED (Abstract-Ebene) |
| N-K4 | SNR als Funktion der Messzeit für dispersiven Box-/Transmon-Majorana-Readout; κ = 2χ optimal bei langer Integration | L03 | VERIFIED (Abstract-Ebene) |
| N-K5 | Rauschen (1/f) auf Dot-Parametern reduziert Visibility; resonante Messung meist vorzuziehen | L06 | VERIFIED (Abstract-Ebene) |
| N-K6 | Allgemeine optimale Filter für endliche kontinuierliche Messungen mit Relaxation | L20, L21 | VERIFIED (Abstract-Ebene) |
| N-K7 | Experimentell optimierte Integrationszeit bei Paritätsauslese | L14 | VERIFIED (Abstract-Ebene) |
| N-K8 | Paritätssignal allein identifiziert keine Majoranas | L16, L17 | VERIFIED (Abstract-Ebene) |

| N-K9 | **In dispersiver cQED-Auslese ist das Langzeit-Optimum (κ = 2χ) bei kurzer Integrationszeit nicht optimal** (Transmon, qualitativ) | L28 (Volltext) | VERIFIED (Literatur) |
| N-K10 | Optimale Messzeit bei Relaxation und Filterhierarchie Boxcar < Exponential < optimal linear < Bayes | L20 | VERIFIED (teilweise Volltext) |

**Konsequenz:** „Zeitabhängige Auslese" oder „endliche Messzeit" ist **für sich genommen nicht neu**, und auch „stationär-optimal ≠ endlichzeit-optimal" ist als **allgemeines** cQED-Phänomen bekannt (N-K9). 

**Update WP 2.0 (2026-11-09):** Keine der Majorana-Arbeiten (L03–L06) berechnet eine **Einzelschuss-Fehlerwahrscheinlichkeit mit physikalischem Messkanal (Homodyn, Effizienz η)**, keine behandelt das **resonante Regime** der Box–Doppelpunkt–Resonator-Auslese zeitaufgelöst, keine optimiert **robust gegen Drift**. N-C1 bleibt offen, ist aber auf die Box-spezifische Physik einzugrenzen: paritätsabhängige Kopplung \(g_z\) und Frequenz \(2\omega_z\) (nicht nur Dispersivverschiebung), Qubit-Sättigung bei sehr kleinen Photonenzahlen im resonanten Regime, Nicht-QND, Interferenzdrift. Originalität weiterhin vorläufig **4–6/10**; ein reines „κ/χ-Verhältnis bei kurzer Zeit"-Resultat wäre durch N-K9 abgedeckt.

## 2. Neuheitskandidaten (alle `HYPOTHESIS`, Originalität vorläufig 4–6/10)

| # | Kandidat | Warum möglicherweise offen | Was ihn entwerten würde |
|---|---|---|---|
| N-C1 | **Regret der stationären Arbeitspunktwahl** im *resonanten/intermediären* Regime des L01-Modells (wo die Semiklassik versagt und τ_x-Kopplung nicht QND ist) gegenüber dem endlichzeit-optimalen Arbeitspunkt bei gleicher Photonenressource | L03 behandelt das dispersive Limit; L01 nur Steady State; L06 Visibility ohne explizite Arbeitspunkt-Regret-Analyse | L03/L28/L06 enthalten bereits Regretkarten über \(\varepsilon,\omega\), oder Regret < 2 pp im gesamten Gebiet |
| N-C2 | **Flussphasen-/Interferenz-Drift** (\(\varphi\), \(t_0\)) als Störgröße: Robustheit des Arbeitspunkts, da \(|t_0+zt_1e^{i\varphi}|\) die Paritätsunterscheidung direkt trägt | Spezifisch für Box-Interferometrie; L06 rauscht φ als 1/f, aber nicht die robuste Auswahl | L06 Volltext enthält genau diese Auswahlanalyse |
| N-C3 | Quantitative **Gültigkeitsgrenze der stationären Kontrastmetrik** als Proxy für den Single-Shot-Fehler (Karte: Steady-State-Kontrast vs. \(P_{err}(T)\) Rangkorrelation) | Verbindet L01-Fehlermaße mit operationaler Fehlerrate | Analytisch trivial ableitbar (Gauß-Limit), ohne neue Parameterabhängigkeit |
| N-C4 | Nicht-QND-Effekte (paritätsinterne Anregung durch τ_x-Kopplung) als Grenze der optimalen Messdauer bei resonanter Auslese | Folgt aus L01 Eq. (5)/(40) und L03 („nur näherungsweise QND") | Bekannte Einschwing-/Purcell-Physik ohne interessante Parameterabhängigkeit (Kill K-2) |

## 3. Explizit ausgeschlossen (nicht Ziel von P1)

- Quasiteilchenvergiftung als zufälliger Paritätswechsel (benötigt erweitertes Modell, Vorrecherche).
- Majorana-Identifizierung aus Readout-Fidelity.
- Gerätekalibrierte Fidelity-Vorhersagen.
- ML-Decoder ohne klassische Baseline.

## 4. Entscheidungsregel für Neuheitsaussagen

Vor jedem Statuswechsel eines N-C-Eintrags auf mehr als `HYPOTHESIS`: (1) R-1/R-2 abgeschlossen, (2) Ergebnis konvergent (Cutoff, dt, Records), (3) Effekt > Relevanzschwelle mit Konfidenzintervall, (4) kontrollierte Ablation zeigt, welche Modellannahme den Effekt trägt.
