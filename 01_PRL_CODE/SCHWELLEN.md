# Schwellen, Toleranzen und Definitionen

Jeder Zahlenwert, mit dem der Code prüft, gehört zu genau einer Klasse und ist begründet.
Maßgeblich sind die Konstanten im Code. Messwerte sind nie Begründung.

## Prüfschwellen T1–T5

| Klasse | Wofür | Schwelle | Begründung | Konstanten |
|---|---|---|---|---|
| **T1** exakt | Operatoridentitäten, Hermitizität von H, Paritätssymmetrie bei t1 = 0 | ≤ 1e-12 abs. | Einträge bis O(10) (ω₀ ≈ 12–16 λ₀ im Laborrahmen, im rotierenden Rahmen ≤ 1), ε_mach ≈ 2.2e-16, Faktor 100 Reserve | `EXAKT` (Tests) |
| **T2** Löser | Residuum ‖𝓛ρ‖, Spurfehler, Hermitizität, λ_min(ρ), Methodenvergleich | Residuum ≤ 1e-9; Spur/Herm. ≤ 1e-10; λ_min ≥ −1e-10; Methoden ≤ 1e-8 rel. | Direkte LU-Lösung erreicht ~1e-15; Konditionszahl des Liouvillians bis ~1e5 bei γ = 0.003, κ = 0.04 ⇒ 1e-10 mit Reserve | `RESIDUUM_MAX`, `SPUR_FEHLER_MAX`, `HERMITIZITAET_MAX`, `EIGENWERT_MIN`, `METHODEN_REL_MAX` |
| **T2'** Cutoff-Wächter | Population des obersten Fockzustands | ≤ 1e-10 | Abschneidefehler einer Observablen ≲ n_c · p(n_c); bei n_c ≤ 160 bleibt er < 1e-7 und damit unter T3 | `max_oberste_fock_population` |
| **T3** Konvergenz/Reproduktion | Cutoff-Verdopplung; analytische Referenzen; Reproduktion | eigene Konvergenz ≤ 1e-6 rel.; Reproduktion ≤ 1 % des Kurvenmaßstabs (primär) und Median rel. ≤ 2 % | Reproduktionstoleranz aus Vorrecherche / EXP-R1 §4; eigene Numerik ≥ 1000× strenger | `CUTOFF_REL_MAX`, `REPRODUKTION_REL_SKALA`, `MEDIAN_REL_MAX`, `REL_MAX` (VAL1) |
| **T4** statistisch | (Etappe 2) SME-Ensemble vs. Mastergleichung, Fehlerraten | ≤ 3 Standardfehler; Wilson-95 %-Intervalle | stochastische Größen | — |
| **T5** Negativkontrolle | z. B. Kreisfrequenz-Konvention muss von den Daten verworfen werden | Verletzung > T3 **und** ≥ Faktor 3 schlechter als die gewählte Variante | EXP-R1 §5 | `NEGATIVKONTROLLE_FAKTOR` |

## Einzeln begründete Werte (Anwendbarkeit)

| Stelle | Wert | Begründung |
|---|---|---|
| VAL1 `I0_LINEAR` | 1e-8 | Nichtlineare Korrektur ∝ I0 (im Test als Steigung 1 nachgewiesen); n̄ ≈ 50·I0 ≪ n_sat ≈ ΓΓ̃/(4g²) ≈ 0.03, d. h. Korrektur ~ 1e-6·(Vorfaktor) bei I0 = 1e-8 — unter `REL_MAX` = 1e-6 |
| VAL1 `ORDNUNG_TOLERANZ` | 0.1 | Steigung 1 ± 10 % in log–log über eine Dekade |
| VAL2 `STEIGUNG_TOLERANZ` | 0.25 | erwartete Ordnung 2 in g/Δ; drei Punkte, Faktor 4 Spannweite |
| VAL5 `SW_REL_MAX` | 0.05 | höhere Ordnungen ~ (g/Δ)² ≈ 1 % bei g/Δ ≈ 0.09; Reserve |
| VAL6 `REL_MAX` | 1e-4 | mesolve atol/rtol 1e-10/1e-8 und Trapezintegration (Δt = 0.05) über 200 Zeiteinheiten; Diskretisierungsfehler ~ (Δt χ)² ≈ 6e-6 |
| VAL7 `SIGMA_GRENZE` | 4.5 | 120 Bins gleichzeitig: P(max \|z\| > 4.5) ≈ 120 · 6.8e-6 ≈ 8e-4 bei korrektem Integrator; Euler-Fehler O(dt) ≪ Standardfehler |
| `SUPEROPERATOR_MAX_DIM` | 10 | Kostenwahl, keine Physik: GEMM ~ d⁴ vs. gebündelte Produkte ~ d³ mit Python-Overhead; Umschaltpunkt gemessen |
| VAL3 `PROPAGATION_REL_MAX` | 1e-6 | Zeitintegration rtol = 1e-10 über ~60 Relaxationszeiten; nur Gegencheck |

- **VAL8** (Bayes-Filter): `LINEAR_REL_MAX = 1e-3` bei Binbreite 0.5 und 0.2 (seit 2026-11-11, F-3.4: exakter Propagator, gemessen 8e-5 / 5e-5; ersetzt `0.01` + Ordnungsprüfung `(1.8, 3.2)`, die den Fehler erster Ordnung des linearisierten Schritts prüfte); Fehlerrate gegen Gauß: T4 (Wilson-95 %).
- **VAL9** (Majorana-Kanal abseits der Resonanz): `Z_MAX = 4.0` (T4-artig, 6 Fenster, 400 Trajektorien je Parität), `LLR_REL_MAX = 0.35` (Filterdiskretisierung 0.4 vs. 0.2 relativ zur LLR-Streuung). Gegenprobe mit linearisiertem Schritt: 4.3 σ bzw. 6.6.
- **VAL10** (Paritätswechsel, Etappe 6): `BASIS_MIN = 1 − 1e-12` (T1, Überlapp der Rabi-Basen bei ε = 0, φ = 0), `BASIS_KONTROLLE_MAX = 1 − 1e-4` (Negativkontrolle φ = 0.1), `IDENTISCH_MAX = 1e-10` (T2, Γ_qp = 0 gegen Etappe-3-Code; gemessen 0.0), `Z_MAX = 4.0` für Mittelwert gegen gekoppelte Mastergleichung, Telegrafenstatistik und Filterkalibrierung (400 Trajektorien je Startparität, Prüfrate Γ_qp = 1/200). Der Mittelwerttest ist für den Wechsel kaum trennscharf (0.9 σ gegen das Modell ohne Wechsel); trennscharf sind Telegrafenstatistik und Kalibrierung (Filter ohne Wechsel überkonfident < −4 σ).
- **VAL11** (Telegrafen-Benchmark, dispersiver Grenzfall): `Z_MAX = 4.0` für Boxcar-Fehlerrate gegen klassische Monte-Carlo-Vorhersage (2000 Trajektorien je Startparität, 2·10⁵ klassische Verläufe), mit und ohne Wechsel; Trennschärfe: Daten mit Wechsel liegen > 4 σ neben der Vorhersage ohne Wechsel; V6-6 gepaart Bayes − Boxcar < 4 σ. Gemessen: |z| ≤ 1.1 in allen vier Fällen.
