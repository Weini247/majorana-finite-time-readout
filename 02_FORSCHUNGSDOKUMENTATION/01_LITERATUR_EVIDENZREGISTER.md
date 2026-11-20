# Literature & Evidence Register

**Prüftiefe:** `FULL` Volltext gelesen (Gleichungen extrahiert) · `ABS` Abstract/Metadaten · `CITED` nur über Zitat in anderer Quelle bekannt · `DATA` Daten gesichtet.
**Kickoff-Stand 2026-11-09.** Jede Quelle trägt eine ID; Architektur-/Modellentscheidungen verweisen auf diese IDs.

## A. Kernquelle und Referenzdaten

### L01 — Benjadi & Egger (2026), *Parity readout in Majorana box qubits from the dispersive to the resonant regime*
- arXiv:2603.06482 (v1 06.03.2026, v2 12.06.2026, „accepted by PRB"); DOI 10.1103/j2x7-1h9c (PRB 114, 034503; Band/Seite nicht selbst gesehen). **Prüftiefe: FULL (HTML v2, Abbildungsgrafiken nicht inspiziert).**
- Konventionen: \(\hbar=k_B=1\); Energien in \(\lambda_0=0.2\) GHz (Kreis- vs. gewöhnliche Frequenz **nicht spezifiziert**).
- Modell: Paritäten Eq. (1) \(\hat z=i\gamma_2\gamma_3\); Eq. (2) \(t_z=t_0+t_1\hat z\); Doppelpunkt Eq. (3); Rabi-Frequenz Eq. (4) \(\omega_z=\sqrt{\varepsilon^2+|t_0+zt_1|^2}\); Resonatorkopplung Eq. (5) \(\tfrac{\lambda}{2}(a+a^\dagger)(1-\tfrac{\varepsilon}{\omega_z}\tau_z-\tfrac{|t_z|}{\omega_z}\tau_x)\); RWA Eq. (6); \(g_z=-\lambda|t_z|/(2\omega_z)\) Eq. (7); \(\kappa=\kappa_{in}+\kappa_{out}\) Eq. (8); Antrieb Eq. (9); rotierender Rahmen Eqs. (10)–(11).
- Lindblad Eq. (12) mit \(\tfrac{\Gamma_\phi}{2}D[\tau_z]\), \(\gamma[(n_{th}+1)D[\tau_-]+n_{th}D[\tau_+]]\), \(\kappa[(N_{th}+1)D[a]+N_{th}D[a^\dagger]]\); Eq. (13) \(n_{th}=1/(e^{2\omega_z/T}-1)\), \(N_{th}=1/(e^{\omega_0/T}-1)\); Eq. (15) \(\Gamma_{tot}=\Gamma_\phi+\tilde\gamma/2\).
- Semiklassik Eqs. (16)–(20); dispersiv Eqs. (21)–(27) (inkl. exakter Bewegungsgleichungen (24)–(25)); Quantenkapazität Eqs. (28)–(32); Input-Output Eqs. (33)–(37); volle Suszeptibilität Eq. (40); Fehlermaße Eqs. (41), (43)–(45); Regimeparameter \(\varrho\) Eq. (42).
- Fig. 3: (a–d) starke Kopplung, \(|t_0|=5\lambda_0,|t_1|=\lambda_0,\varphi=0,\varepsilon=0,\omega_0=11.99\lambda_0,\gamma=0.003\lambda_0,\Gamma_\phi=0.1\lambda_0,\lambda=0.1\lambda_0,\kappa=0.04\lambda_0,\omega=\omega_0\), T = 30 mK; (c) Fehlermaße vs. \(\Delta_z\). (e–h) schwache Kopplung, \(\varepsilon=6\lambda_0,\lambda=0.25\lambda_0,\gamma=0.015\lambda_0,\Gamma_\phi=0.05\lambda_0,\omega_0=16\lambda_0\).
- **Nicht** behandelt: endliche Messzeit, SNR, Homodynrauschen, Detektionseffizienz, Backaction, Drift, Quasiteilchenvergiftung (nur Einleitung).
- Kickoff-Auffälligkeiten (eigene Prüfung, `HYPOTHESIS`): Vorzeichen Eq. (35) vs. (34)/(20); Subskript „s" in Eq. (43); \(I_0\), \(\kappa_{in}/\kappa_{out}\) fehlen in Fig.-3-Caption.
- Rolle: **Reproduktionsziel Etappe 1; Modellbasis Etappen 2–3.**

### L02 — Benjadi & Egger, Zenodo-Datensatz
- DOI 10.5281/zenodo.20623730 (Concept 10.5281/zenodo.20623729), v1 10.06.2026, **CC-BY-4.0**. **Prüftiefe: DATA** (Metadaten-API, fig3c vollständig).
- 13 Dateien: fig2a/b (je 678 000 B), fig3a–h, fig4, fig5a/b; md5 je Datei im Manifest `03_Quellen/Referenzdaten_Zenodo_20623730/MANIFEST.md` (noch nicht heruntergeladen — Download in WP 1.1 nach Freigabe).
- Keine Spaltenbeschreibung. fig3c: 101 × 4, x ∈ [−1, 1], Δx = 0.02.

## B. Majorana-Readout: unmittelbare Konkurrenz/Vorarbeiten

| ID | Quelle | Prüftiefe | Relevanz für P1 |
|---|---|---|---|
| L03 | T. B. Smith, M. C. Cassidy, D. J. Reilly, S. D. Bartlett, A. L. Grimsmo, *Dispersive readout of Majorana qubits*, PRX Quantum 1, 020313 (2020), arXiv:2009.00027 | ABS (+Snippets) | **SNR(τ) einer Heterodynmessung**, κ = 2χ optimal für lange Zeiten, Infidelity vs. Readoutzeit; Box-Qubit nur näherungsweise QND, longitudinale Auslese schneller. → Endliche Messzeit im **dispersiven** Limit ist bekannt. Volltextlektüre Pflicht (WP 2.0) |
| L04 | J. F. Steiner, F. von Oppen, *Readout of Majorana qubits*, PRR 2, 033255 (2020), arXiv:2004.02124 | ABS (+Snippets) | Zeitaufgelöste, schwache kontinuierliche Messung (SME) mit QD-Ladungssensor; misst kombinierte Parität inkl. Dot-Ladung; Messzeiten deutlich länger als konventionelle QD-Auslese |
| L05 | M. I. K. Munk, J. Schulenborg, R. Egger, K. Flensberg, *Parity-to-charge conversion in Majorana qubit readout*, PRR 2, 033254 (2020), arXiv:2004.02123 | CITED/ABS | Egger-Koautorschaft; zeitabhängige Paritäts-Ladungs-Konversion. Volltextlektüre Pflicht (WP 2.0) |
| L06 | A. Khindanov, D. Pikulin, T. Karzig, *Visibility of noisy quantum dot-based measurements of Majorana qubits*, SciPost Phys. 10, 127 (2021), arXiv:2007.11024 | ABS | 1/f-Rauschen auf Verstimmung/Tunneln/Phase, nicht-perturbativ, SNR-Visibility; **resonante Messung meist vorzuziehen**. Direkt relevant für Drift-Teil (Etappe 3) |
| L07 | G. Széchenyi, A. Pályi, PRB 101, 235441 (2020) | CITED | Paritäts-Ladungs-Konversion |
| L08 | J. Schulenborg, M. Burrello, M. Leijnse, K. Flensberg, PRB 103, 245407 (2021) | CITED | Mehrniveaueffekte — Modellgrenze für Etappe 3 |
| L09 | J. Schulenborg et al., PRB 107, L121401 (2023), arXiv:2209.08082 | CITED/ABS | Paritätsflips durch Vergiftung — Abgrenzung Quasiteilchenvergiftung |
| L10 | M. I. K. Munk, R. Egger, K. Flensberg, PRB 99, 155419 (2019) | CITED | Fidelity/Visibility-Verlust durch Umgebungsmoden |
| L11 | C. Ohm, F. Hassler, PRB 91, 085406 (2015); K. Yavilberg et al., PRB 92, 075143 (2015) | CITED | Mikrowellen-/cQED-Majorana-Readout, frühe Vorarbeiten |
| L12 | S. Plugge, A. Rasmussen, R. Egger, K. Flensberg, *Majorana box qubits*, NJP 19, 012001 (2017) | CITED | Box-Qubit-Grundlage, Interferometrie \(t_0+t_1\hat z\) |
| L13 | T. Karzig et al., PRB 95, 235305 (2017) | CITED | Skalierbare Designs, Messprotokolle |
| L14 | N. van Loo et al., *Single-shot parity readout of a minimal Kitaev chain*, Nature 650, 334 (2026), arXiv:2507.01606 | ABS | **Experiment, Quantenkapazität, endliche Integrationszeit**: optimiert 150 µs → 6 % minimaler Fehler; SNR=1 nach 40 µs; Paritätslebensdauer > 1 ms. Daten/Code: 10.4121/227fd419-… |
| L15 | Microsoft Azure Quantum, *Interferometric single-shot parity measurement in InAs–Al hybrid devices*, Nature 638, 651 (2025) | CITED | Experimenteller zeitaufgelöster Paritätsreadout (Quantenkapazität) |
| L16 | T. D. Stanescu, S. Tewari, arXiv:2505.23741 | ABS (Vorrecherche) | Triviale Zustände imitieren Paritätssignale → keine Majorana-Identifikation aus Fidelity |
| L17 | R. A. Dourado et al., arXiv:2606.21580 (2026) | ABS (Vorrecherche) | Inferenz aus Quantenkapazität (P7-relevant, P1-Abgrenzung) |
| L18 | J. D. Sau, S. Das Sarma, PRB 111, 224509 (2025) | CITED | Kapazitätsbasierter Paritätsreadout |
| L19 | Weitere Punkte: Point-contact-Readout bei endlicher Bias (arXiv:2406.10812) | ABS | SNR-Fenster; anderes Detektormodell |

## C. Finite-Time Measurement, SME, optimale Diskriminierung (allgemein)

| ID | Quelle | Prüftiefe | Relevanz |
|---|---|---|---|
| L20 | J. Gambetta, W. A. Braff, A. Wallraff, S. M. Girvin, R. J. Schoelkopf, *Protocols for optimal readout of qubits using a continuous QND measurement*, PRA 76, 012325 (2007), cond-mat/0701078 | ABS | Linearfilter vs. nichtlinearer optimaler Filter bei Relaxation; optimale Fidelity bei endlicher Zeit. **Methodische Baseline für Decoder (Etappe 2)** |
| L21 | S. Ng, M. Tsang, *Optimal signal processing for continuous qubit readout*, PRA 90, 022325 (2014), arXiv:1405.7262 | ABS | Optimaler Bayes-Filter, Robustheit gegen Modellunsicherheit |
| L22 | A. A. Clerk et al., *Introduction to quantum noise, measurement, and amplification*, RMP 82, 1155 (2010) | CITED | Rausch-/Verstärkerkonvention, Messrate vs. Dephasierung |
| L23 | H. M. Wiseman, G. J. Milburn, *Quantum Measurement and Control* (CUP 2010) | Lehrbuch (bekannt) | SME-/Homodynkonventionen, Effizienz η |
| L24 | K. Jacobs, D. A. Steck, *A straightforward introduction to continuous quantum measurement*, Contemp. Phys. 47, 279 (2006) | bekannt | SME-Einführung, Itô-Konventionen |
| L25 | A. Blais et al., PRA 69, 062320 (2004); A. Blais et al., RMP 93, 025005 (2021) | CITED/bekannt | cQED-Dispersivauslese, Input-Output |
| L26 | Tornberg/Johansson-artige SME-Paritätsmessung, arXiv:1311.1963 | ABS | Transienten verschlechtern Paritätsfidelity (supraleitend) — methodische Analogie |
| L27 | Magesan et al., PRL 114, 200501 (2015) | bekannt, nicht geprüft | ML-Trajektoriendiskriminierung — Baseline-Literatur für Etappe 4 |
| L28 | Walter et al., PR Applied 7, 054020 (2017) | bekannt, nicht geprüft | Schnelle dispersive Auslese, Einschwingzeit vs. κ/χ — **möglicherweise schon „stationär ≠ endlichzeitoptimal" für Transmons gezeigt** → Pflichtlektüre WP 2.0 |

> `bekannt` = aus Vorwissen bekannt, bibliographische Angaben im Kickoff nicht nachgeprüft — vor Zitation verifizieren.

## D. Software

| ID | Werkzeug | Prüftiefe | Rolle |
|---|---|---|---|
| L30 | QuTiP 5 — `steadystate`, `mesolve`, `smesolve` (heterodyne/homodyne, `sc_ops`, Effizienz über aufgeteilte Kanäle) | Doku (Vorrecherche) | Referenzbackend |
| L31 | Dynamiqs (JAX) | Doku (Vorrecherche) | Optional nach Profiling |
| L32 | SciPy sparse (`spsolve`, `eigs`) | bekannt | Unabhängiger Steady-State-Gegencheck |

## E. WP 2.0 — Volltextlektüre (2026-11-09, ar5iv-HTML; Gleichungsnummern vor Zitation gegen Journalfassung prüfen)

| ID | Prüftiefe neu | Kernaussagen für P1 |
|---|---|---|
| L03 Smith et al. 2020 | FULL bis App. A (Eq. 34); App. B–E nicht verbatim | Box-Qubit über **einen** Dot an Inselladung gekoppelt (Eq. 18–28), nicht \(t_0+zt_1\). **Readout nur dispersiv**, Arbeitspunkt fest (Δ/g = −10, n̄/n_crit = 1/5). SNR(τ) Heterodyn, η = 1, **Eq. (29)**: \(\mathrm{SNR}=2|\epsilon|\sqrt{\tau/\chi}[1-\frac{1}{\chi\tau}(1-e^{-\chi\tau}\cos\chi\tau)]\) bei κ = 2χ; **Eq. (30)** \(F=1-\tfrac12\mathrm{erfc}(\mathrm{SNR}/2)\). Ausdrücklich ausgeschlossen: Rauschen, Drift, Purcell, messinduzierte Übergänge, resonantes Regime; „not meant to be quantitative predictions" |
| L04 Steiner & von Oppen 2020 | FULL (bis auf Teile App. B, C, F, G) | QPC-Ladungssensor, SME Eq. (20) ohne Effizienzparameter; Messzeit nur als Größenordnungsabschätzung Eq. (39)–(41), optimiert nur Messstärke k; **keine Fehlerwahrscheinlichkeit, kein Resonator** (cQED-Kopplung Eq. 53 nur qualitativ); Doppelpunkt (Eq. 44, \(t_Z=t_0+i t_1t_2^*Z/E_c\)) als „future work" |
| L05 Munk et al. 2020 | FULL (bis auf Konklusion/App. A-Anfang) | Effektive Lindblad-Raten für Ohmsches Bad/LC/QPC (Eq. 59–70), stationäre Visibility; **dispersive Auslese als Ausblick IV.1** („requires including the driving fields"); keine Zeitreihe, kein SNR. Inkonsistenz Eq. (6) vs. (34) (Faktor 2 bei \(sa\sin\varphi\)) laut Lesung |
| L06 Khindanov et al. 2021 | FULL (ar5iv) | 1/f auf Δ, t, φ (Eq. 22, 47, 48), störungstheoretisch; S/N stationär, Messzeit nur logarithmisch; **keine Einzelschuss-Fehlerwahrscheinlichkeit, kein Detektor/η, keine Drift-robuste Arbeitspunktwahl**; kapazitiv: Δ = 0 vermutlich optimal; φ-Optimum kann von π/2 abweichen (nicht quantifiziert) |
| L20 Gambetta et al. 2007 | PARTIAL (Modell, Boxcar, Tab. 1 verbatim; Optimal-/Nichtlinearfilter nur Zusammenfassung) | Boxcar ohne Zerfall \(F=\mathrm{erf}(\sqrt{\tau_f\mathrm{SNR}/2})\) (Eq. 6); mit T₁ endliches optimales τ; Bayes-Filter ohne optimales τ — **Decoder-Leiter für Etappe 2** |
| L28 Walter et al. 2017 | FULL Haupttext | **Für Transmons: Langzeit-Optimum |χ/κ| = 0.5 ist bei kurzen Zeiten (χτ ≲ 4.5) nicht optimal**; Experiment wählt 0.2 für τ ≤ 50 ns. Qualitativ (QSS-Modell, s(τ)), ohne formale Fehleroptimierung |

**Forward-Citation-Suche (R-2, Websuche):** keine Arbeit zu transientem/Einzelschuss-Readout im Benjadi–Egger-Modell gefunden (Suchindex-Ebene, kein Nachweis der Abwesenheit).

## F. Offene Rechercheaufgaben

- R-1 (WP 2.0): erledigt bis auf L20 Nichtlinearfilter-Gleichungen (Journalfassung lesen, bevor der Bayes-Filter zitiert wird).
- R-2: erledigt auf Suchindex-Ebene; vor Publikation INSPIRE/Scholar-Zitationsliste von L01 und L03 prüfen.
- R-3 (WP 3.0): Robuste Readout-Optimierung unter Drift (cQED), Bayes'sche Arbeitspunktwahl.
- R-4 (WP 4.0, nur falls Etappe 4 freigegeben): ML-Decoder vs. Matched Filter, faire Baselines.

## F. WP 3.0 — Decoder jenseits Gauß (Stand 2026-11-10, Abstract-Ebene)
| Quelle | Inhalt | Relevanz | Status |
|---|---|---|---|
| D'Anjou & Coish, PRA 89, 012313 (2014), arXiv:1311.2979 | Vergleich Boxcar, Peak-Signal und Maximum-Likelihood-Auswertung; zufällige Einschaltzeit erhöht die Fehlerrate stets | Präzedenz: ML-Decoder schlägt Boxcar, wenn das Signal nicht stationär-gaußsch ist; Spin-zu-Ladung-Kontext, kein Homodyn/Resonator | VERIFIED (Abstract) |
| Gambetta et al., PRA 76, 012325 (2007) | optimale Auswertung kontinuierlicher QND-Messung | bereits Referenz für VAL7/VAL8 | VERIFIED (Etappe 2) |
| Majorana-Paritätsauslese über Quantenpunkt (arXiv:1601.07506; PRR 2, 033255 (2020)); Kitaev-Kette Einzelschuss (arXiv:2507.01606, Nature 650, 334 (2026)) | Ladungs-/Kapazitätsauslese, Telegraphensignal, Paritätslebensdauer > 1 ms | kein Likelihood-Filter mit Homodyn/η im resonanten Box-Regime gefunden; Neuheitslücke vorläufig bestätigt | Abstract-Ebene; Volltextprüfung offen |

## G. WP 6.0 — Paritätslebensdauern (Stand 2026-11-18, Abstract-/Zusammenfassungsebene)
| Quelle | Inhalt | Relevanz | Status |
|---|---|---|---|
| Microsoft Quantum, arXiv:2507.08795 (2025), *Distinct lifetimes for X and Z loop measurements in a Majorana tetron device* | Wiederholte Einzelschussmessungen: Wechselzeit ≈ 14.5 µs (X-Schleife, interne Paritätswechsel), ≈ 12.4 ms (Z-Schleife, externe Vergiftung); Zuordnungsfehler 16 % bzw. 0.5 % | Γ_qp-Raster EXP-P1 (15 µs, ms-Bereich) | ABS |
| arXiv:2606.03884 (2026), InAs–Pb-Tetron | Wechselzeit ≈ 20 s | oberes Ende: praktisch kein Wechsel während µs-Messungen | ABS (nur Abstract) |
| N. van Loo et al., Nature 650, 334 (2026), arXiv:2507.01606 | Kitaev-Kette, Quantenkapazität, Telegrafenschalten, Lebensdauer > 1 ms, Einzelschuss in µs | Γ_qp = 1/(1 ms) | ABS (Lebensdauer aus Abstract/Presse) |

Hinweis: Die Interpretation der Microsoft-Messungen als topologisch ist umstritten; für EXP-P1 werden nur die gemessenen Wechselzeiten als Größenordnung genutzt.
