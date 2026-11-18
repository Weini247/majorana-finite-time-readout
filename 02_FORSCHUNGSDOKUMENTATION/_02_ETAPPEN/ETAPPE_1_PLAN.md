# Etappe 1 — Reference Physics & Reproduction (Detailplan)

**Status:** `OPEN` — wartet auf Gate G0 (Freigabe des Plans, der Umgebung und des Datendownloads).
**Zeitbox:** 2 Wochen bis zur Reproduktionsentscheidung (Kill K-1), maximal 3 Wochen inkl. Bericht.

## 1. Forschungsziel und offene Frage

Ein numerischer Referenzkern für das stationäre Readout-Problem von L01, dem man später transiente und stochastische Rechnungen anvertrauen kann. Offene Frage Q-A: *Lässt sich L01 Fig. 3(a) und 3(c) (starke Kopplung) aus den publizierten Gleichungen und Parametern innerhalb einer vorab registrierten Toleranz reproduzieren, und welche nicht publizierten Konventionen (Einheiten, Antrieb, Vorzeichen, Sweep-Variable) sind dafür nötig?*

**Warum Fig. 3(c) als erste Reproduktion?** (i) Rohdaten liegen vor (fig3c.dat, md5 verifiziert); (ii) starke Kopplung/Resonanz ist genau das Regime, in dem Semiklassik versagt und in dem der spätere Neuheitskandidat N-C1 liegt; (iii) die Fehlermaße hängen empfindlich vom exakten Steady State ab — ein strenger Test des Solvers. **Fig. 3(a)** (Phase \(\arg A_\omega\) vs. \(\omega\)) wird vorgeschaltet, weil sie die Vorzeichen-/Phasenkonvention (Eq. 35) und die Einheitenfrage mit einer einzigen Observablen isoliert. Fig. 3(g) (schwache Kopplung, Fehler ≲ 0.1 %) dient als Gegenprobe.

## 2. Primärliteratur

L01 (alle Gleichungen unten; zusätzlich PDF-Fassung und Abbildungsgrafiken zu sichten — Legenden/Linienstile fehlen im HTML-Text), L02 (Daten), L25 (Input-Output-Konvention), L23 (Lindblad-/Rahmenkonventionen). Rechercheaufgabe WP 1.2: prüfen, ob die PRB-Fassung von arXiv v2 abweicht (Erratum, geänderte Gleichungen).

## 3. Physikalische Annahmen und Modellgleichungen

Rotierender Rahmen bei Antriebsfrequenz \(\omega\), RWA (L01 Eq. 10):
\[
H_{sc}=\frac{\Delta_z}{2}\tau_z+\Delta_0a^\dagger a+g_z(a\tau_++a^\dagger\tau_-)+i\sqrt{\kappa_{in}I_0}\,(a^\dagger-a),\quad
\Delta_z=2\omega_z-\omega,\ \Delta_0=\omega_0-\omega,
\]
\(\omega_z=\sqrt{\varepsilon^2+|t_0+zt_1e^{i\varphi}|^2}\) (Eq. 4), \(g_z=-\lambda|t_z|/(2\omega_z)\) (Eq. 7).
Lindblad (Eq. 12) mit \(n_{th}=1/(e^{2\omega_z/T}-1)\), \(N_{th}=1/(e^{\omega_0/T}-1)\) (Eq. 13).

**Exakte Referenz:** \(\rho_{ss}\) mit \(\mathcal L\rho_{ss}=0\), \(\mathrm{Tr}\rho_{ss}=1\); daraus \(\langle a\rangle_{ss}\), \(\langle\tau_z\rangle_{ss}\), \(\langle a\tau_z\rangle_{ss}\), \(A_{ref}=\sqrt{\kappa_{out}/I_0}\,\langle a\rangle_{ss}\).
**Semiklassik:** \(\langle\tau_z\rangle=-\tanh(\omega_z/T)\) (17); \(\chi_z=-g_z^2/(\Delta_z-i\Gamma_{tot})\) (19), \(\Gamma_{tot}=\Gamma_\phi+(2n_{th}+1)\gamma/2\) (15); \(\langle a\rangle\) (18); \(A_{semicl}\) (20).
**Fehlermaße:** \(\varepsilon_{a\tau_z}\) (43), \(\varepsilon_A\) (44), \(\varepsilon_\phi\) (45).

**Annahmen mit Status:**
| ID | Annahme | Status |
|---|---|---|
| A1-1 | x-Spalte fig3c = \(\Delta_z/\lambda_0\) | HYPOTHESIS (Maxima bei x≈0.04–0.06 ≈ \(g_z=0.05\lambda_0\)) |
| A1-2 | Spalten 2–4 = \(\varepsilon_{a\tau_z},\varepsilon_A,\varepsilon_\phi\) in dieser Reihenfolge | HYPOTHESIS |
| A1-3 | \(\Delta_z\)-Sweep über \(\omega\) (Variante a) oder über \(\omega_z\) bei \(\omega=\omega_0\) (Variante b) | OPEN |
| A1-4 | \(\lambda_0=0.2\) GHz ordinary vs. angular | OPEN |
| A1-5 | \(I_0\), \(\kappa_{in}/\kappa_{out}\): Fehlermaße im Linear-Response-Limit \(I_0\to0\) unabhängig davon | HYPOTHESIS (prüfen: Sweep über \(I_0\)) |
| A1-6 | In (43) sind alle drei Größen exakt (Faktorisierungsfehler des exakten Zustands) — alternativ \(\langle a\tau_z\rangle_{exakt}\) vs. semiklassisches Produkt | OPEN, beide rechnen |
| A1-7 | Vorzeichen Eq. (35) vs. (34)/(20): \(\varepsilon_\phi\) ist invariant, wenn beide Amplituden dieselbe Konvention nutzen; kritisch nur bei Mischkonvention | HYPOTHESIS |
| A1-8 | φ = 0, z = +1 in Fig. 3 | VERIFIED (Caption: \(|t_z|=6\lambda_0\)) |

## 4. Arbeitspakete

| WP | Inhalt | Ergebnis | Schätzung |
|---|---|---|---|
| **1.0** | Umgebung (ADR-0004): venv in `_env`, QuTiP 5/NumPy/SciPy/Matplotlib, Lockfile, `pip check`, Umgebungsbericht; `git init`; Toleranzklassen T1–T5 final begründen (`05_KONVENTIONEN.md` §5 → v1.0) | lauffähige, gelockte Umgebung; leeres Paket mit Testrunner | 0.5 Tag |
| **1.1** | Referenzdaten: 13 Zenodo-Dateien laden, md5 gegen API, SHA-256 ablegen, `03_Quellen/Referenzdaten_Zenodo_20623730/MANIFEST.md`; Hash-Test; deskriptive Analyse aller fig3*-Dateien (Spaltenanzahl, Gitter, Symmetrie) **ohne** Modellfit | unveränderte Daten + Manifest + Datenbeschreibung | 0.5 Tag |
| **1.2** | Theorie: Herleitung Eq. (5)+(9) → (10) (Rahmen, RWA), Heisenberg-Gleichungen → (18)–(20), Prüfung (27) und (40); Vorzeichen (33)–(37) unabhängig nachrechnen; Dokument `02_FORSCHUNGSDOKUMENTATION/_05_THEORIE/T1_Auslesemodell_Herleitung.md` mit SymPy-Check | geprüfte Gleichungskette, Liste von Abweichungen/Tippfehlern (Status je Punkt) | 2–3 Tage |
| **1.3** | Konventionsdiskriminierung (vorab registriert in EXP-R1 §5): Raster {A1-3 a/b} × {A1-4 ordinary/angular} × {A1-6 Variante} × \(I_0\)-Werte; Vergleich mit fig3a/fig3c | Entscheidung D-1.1 mit Begründung oder BLOCKED | 2 Tage |
| **1.4** | Steady-State-Kern: `params`, `model`, `steady` (Methode M1 QuTiP `steadystate` direkt; M2 eigene Sparse-Liouvillian + `spsolve` mit Spurzeile; M3 `mesolve`-Propagation bis Konvergenz für Stichproben), `semiclassical`, `observables`; Diagnostik und Fehlerobjekte | getesteter Kern, V1-01…V1-10 grün | 3–4 Tage |
| **1.5** | Reproduktionslauf EXP-R1a (fig3a) und EXP-R1b (fig3c) + Gegenprobe fig3g; Overlay- und Residuenpanels; Manifest | Abbildungen R1a/R1b, Kennzahlen-CSV | 1 Tag |
| **1.6** | Fehlerbudget (Cutoff, Solver, Konvention, Datenrundung), Konvergenzbericht, `07_BEFUNDE.md`-Eintrag, Stage-Bericht, Gate G1 | Bericht `02_FORSCHUNGSDOKUMENTATION/_04_BERICHTE/ETAPPE_1_BERICHT.md` | 1 Tag |

Reihenfolge: 1.0 → 1.1 → (1.2 ∥ 1.4) → 1.3 → 1.5 → 1.6. WP 1.3 darf erst nach 1.2 und V1-01…V1-08 laufen (keine Konventionswahl mit ungeprüftem Solver).

## 5. Module und Schnittstellen (Etappe 1)

```python
@dataclass(frozen=True)
class ModelParams:            # alle Energien in λ0
    t0: float; t1: float; phi: float; epsilon: float
    omega0: float; lam: float
    kappa_in: float; kappa_out: float; gamma: float; gamma_phi: float
    temperature: float        # T/λ0 (Umrechnung dokumentiert in Config-Metadaten)
@dataclass(frozen=True)
class DriveParams:  omega: float; I0: float
@dataclass(frozen=True)
class NumericsParams: cutoff: int; method: Literal["qutip_direct","sparse_spsolve","propagate"]; tol: float

def derived(p: ModelParams, z: int) -> Derived            # ω_z, |t_z|, g_z, n_th, N_th, Γ_tot
def build_rwa(p, d, z, n) -> ModelOperators               # H, c_ops, Operatoren a, τ_z, aτ_z
def solve_steady(ops, n) -> SteadyStateResult             # ρ, residual, trace_err, min_eig, hermiticity_err, method, message, top_fock_pop
def semiclassical_amplitude(p, d, z) -> complex           # Eq. (20)
def exact_amplitude(res, p, d) -> complex                 # sqrt(κ_out/I0) <a>
def error_measures(...) -> dict[str, float]               # Eqs. (43)-(45), beide A1-6-Varianten
```
Fehlerpolitik: `SteadyStateError`, wenn Residuum > T2, Spurfehler > T2, \(\lambda_{\min}(\rho)<-\)T2 oder Population im obersten Fockzustand > 1e-10 — nie stilles Weiterrechnen.

## 6. Tests und wissenschaftliche Validierung

Siehe `06_VALIDIERUNGSREGISTER.md`, Einträge V1-01 … V1-12 (analytische Kavität, Thermalzustand ohne Antrieb, \(g=0\)-Faktorisierung, \(t_1=0\)-Symmetrie, dispersiver Grenzfall Eq. 22/26, Methodenvergleich M1/M2/M3, Cutoff-Konvergenz, Spur/Positivität, Negativkontrollen, Hash-Tests, Linear-Response-Unabhängigkeit von \(I_0\), RWA-Prüfpunkte).

## 7. Abbildungen und Ergebnisdateien

| ID | Inhalt | Klasse |
|---|---|---|
| F1-1 | fig3a: \(\arg A_\omega\) vs. \(\omega\), eigene exakte + semiklassische Kurve über Referenzdaten; Residuenpanel | Reproduktion |
| F1-2 | fig3c: drei Fehlermaße vs. \(\Delta_z\) (log), Referenz vs. eigene; Residuenpanel abs./rel. | Reproduktion |
| F1-3 | Konventionsdiskriminierung: Residuennorm je Variante (Balken), inkl. Negativkontrollen | Validierung |
| F1-4 | Cutoff- und Methodenkonvergenz am Resonanzpunkt | Validierung |
| F1-5 | Gegenprobe fig3g (schwache Kopplung) | Reproduktion |
Ergebnisse: `results/<run_id>/{manifest.json, config.json, curves.npz, metrics.csv, figures/*.pdf|png}`.

## 8. Definition of Done

1. V1-01 … V1-12 bestanden (oder einzeln begründet `BLOCKED`).
2. EXP-R1a und EXP-R1b nach registrierter Regel `REPRODUCED` — oder `FAILED/BLOCKED` mit Fehlerbudget, das zeigt, dass die Abweichung **nicht** numerisch ist, plus formulierte fachliche Frage an die Autoren.
3. Alle Konventionsentscheidungen (A1-1 … A1-7) haben Status ≠ `OPEN` und sind in `05_KONVENTIONEN.md` v1.0 eingetragen.
4. Manifest erlaubt Reproduktion per einer Kommandozeile.
5. `07_BEFUNDE.md` und `08_RISIKEN_OFFENE_FRAGEN.md` aktualisiert; Gate-G1-Entscheidung dokumentiert.

## 9. Risiken und Kill Criteria

- **K-1:** Nach 2 Wochen keine Reproduktion wegen ungeklärter Konventionen → Erweiterungen pausieren; konkrete Frage an Benjadi/Egger formulieren (nicht senden ohne Freigabe).
- **K-6:** Mehrere Konventionsvarianten passen gleich gut → als Mehrdeutigkeit dokumentieren, nicht willkürlich wählen.
- Numerisch: schlecht konditionierter Liouvillian bei sehr kleinen \(\gamma\) (0.003 λ₀) und \(\kappa\) (0.04 λ₀) → Konditionszahl protokollieren, M2/M3 als Gegencheck.
- Datenseitig: Rundung/Abtastung der .dat-Dateien begrenzt die erreichbare Übereinstimmung → abs. Untergrenze im Kriterium.

## 10. Abhängigkeiten zur Etappe 2

- `model.build_*` muss Laborrahmen-/zeitabhängige Antriebe zulassen (Schnittstelle bereits so geschnitten, Implementierung erst Etappe 2).
- Exakter Steady State liefert den Langzeit-Mittelwert, gegen den SME-Ensembles in Etappe 2 validiert werden.
- Die in WP 1.3 entschiedenen Konventionen (Einheiten, Antrieb) werden für Etappe 2 übernommen; ihre Unsicherheit wird als Sensitivität mitgeführt.
