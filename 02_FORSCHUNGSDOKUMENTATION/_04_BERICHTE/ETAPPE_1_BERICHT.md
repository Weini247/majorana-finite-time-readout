# Etappe 1 — Zwischenbericht (2026-11-09)

**Gate G1: offen.** Kern validiert, semiklassische Referenz reproduziert, exakte Referenz blockiert.

## 1. Was getan wurde (Arbeitspakete)
| WP | Ergebnis |
|---|---|
| 1.0 Umgebung | venv `_UMGEBUNG/venv` (Python 3.12.10, NumPy 2.5.4, SciPy 1.18.1, QuTiP 5.3.1, Matplotlib 3.11.2), Lockfile, `pip check` ok, lokales git (noch kein Commit) |
| 1.1 Referenzdaten | 13 Zenodo-Dateien geladen, md5 = API, SHA-256 abgelegt, Hash-Test |
| 1.2 Theorie | `_05_THEORIE/T1_Auslesemodell_Herleitung.md`: Amplitudenkonvention, Semiklassik = lineare Antwort bei T = 0, Vorzeichen der dispersiven Verschiebung (Schrieffer–Wolff) |
| 1.3 Konventionen | λ₀ = h·0.2 GHz entschieden; Spaltenbelegung fig3a/3e bestimmt; κ_in = κ_out konsistent |
| 1.4 Kern | `_01_GRUNDLAGEN_FORMELN` (Einheiten, abgeleitete Größen, RWA-Operatoren, Semiklassik), `_02_AUSFUEHRUNG` (stationärer Löser mit drei Methoden und harter Diagnostik), `_04_AUSWERTUNG_DIAGNOSTIK` (Fehlermaße Eqs. 43–45 in beiden Lesarten) |
| 1.5 Reproduktion | `_08_ERGEBNISSE/reproduktion_fig3.py`, Lauf `EXP-R1_20261109T193812Z` (Manifest, Abbildungen, `kennzahlen.csv`) |

**Tests:** `run_checks --scope all` → 35/35 bestanden (24 aktive Tests mit deutschen Methodennamen, 11 wissenschaftliche VAL-Prüfungen).

## 2. Validierung gegen Fremdreferenzen (VERIFIED)
VAL0 analytische Kavität · VAL1 Jaynes–Cummings-Linearantwort (Blais et al. RMP 2021) · VAL2 dispersive Verschiebung (Blais et al. PRA 2004) · VAL3 drei unabhängige Löser + Cutoff · VAL5 volles Modell Eq. (5) per exakter Diagonalisierung vs. Schrieffer–Wolff.

## 3. Reproduktion Benjadi & Egger Fig. 3
| Kurve | Ergebnis | Status |
|---|---|---|
| fig3a semiklassisch (Eq. 20), \|A\|² und arg | max. Abw. 1.4e-4 bzw. 3.6e-5 der Skala | REPRODUCED |
| fig3e semiklassisch (Eq. 26 + 22) | ≤ 1.1e-5 | REPRODUCED |
| fig3a/3e exakt | 29 % / 48 % der Skala Abweichung | BLOCKED |
| fig3c (Fehlermaße) | eigene Fehler bei linearer Antwort ≈ 0 statt bis 30 % | BLOCKED |

## 4. Wissenschaftliche Befunde
1. **F-1.4:** Im publizierten RWA-Modell (Eq. 10/12) ist die semiklassische Faktorisierung bei schwachem Antrieb praktisch exakt (bei T = 0 analytisch exakt). Die großen Fehler in L01 Fig. 3(a–d) brauchen also einen endlichen Antrieb oder eine andere „exakte" Modellierung. Beides nennt das Paper nicht.
2. **F-1.5:** Die dispersive Verschiebung nach Eq. (22)/(26) hat das entgegengesetzte Vorzeichen wie die exakte Diagonalisierung des vollen Modells. Die publizierten fig3e-Kurven folgen den gedruckten Formeln. Status `HYPOTHESIS`; die Ursache kann auch eine undokumentierte Konvention sein.
3. **F-1.3:** Die aus der exakten Referenzspalte extrahierte Selbstenergie hat einen Realteil mit umgekehrtem Vorzeichen und eine schmalere Linie. Keine getestete Variante erklärt das: Antrieb, Dephasierungsfaktor, Vorzeichen bzw. Faktor der Qubit-Verstimmung, Einheitenkonvention, kleiner Cutoff (alle verworfen, §5).

## 5. Getestete und verworfene Erklärungen für die exakte Referenz
| Hypothese | Ergebnis |
|---|---|
| Endlicher Antrieb I0 ∈ {1e-5 … 1} (Cutoff adaptiv bis 118) | beste max. Abw. 0.058 (\|A\|²) bei I0 = 0.01 — verworfen |
| Γ_φ D[τ_z] statt Γ_φ/2 D[τ_z], × I0 | verworfen |
| Qubit-Verstimmung gespiegelt / ohne Faktor ½, × I0 | beste 0.043 — verworfen |
| Kreisfrequenz-Konvention | verworfen (schon die semiklassische Spalte passt nicht) |
| Referenz mit kleinem Fock-Cutoff (2–8) × I0 (26 Werte, 1e-5 … 1) | beste Kombination nc = 4, I0 = 2.5e-2: max. Abw. 3.4e-2 (\|A\|²) und 0.13 rad (arg), weit über 1 % — verworfen |

## 6. Offene Fragen an die Autoren (nicht gesendet)
Die semiklassischen Kurven von Fig. 3 (Eqs. 20, 26) sind aus den angegebenen Parametern auf besser als 1e-4 reproduziert. Für die exakten Referenzkurven fehlen: (1) die Antriebsintensität \(I_0\) (bzw. die mittlere Photonenzahl) und der Fock-Cutoff, (2) ob die exakte Lösung mit dem RWA-Hamiltonian Eq. (10) oder mit Eq. (5)/(23) berechnet wurde. Außerdem ergibt die exakte Diagonalisierung von Eq. (5) hier eine dispersive Kavitätsverschiebung \(\omega_0-g_z^2(1/\Delta+1/\Sigma)\), also das umgekehrte Vorzeichen zu Eq. (22) (F-1.5, `HYPOTHESIS`: möglicherweise eine Konvention).

## 7. Nächste Entscheidung (Gate G1)
- **Empfehlung:** Etappe 1 mit dem Status „Kern validiert, semiklassische Referenz REPRODUCED, exakte Referenz BLOCKED (K-1)" schließen. Etappe 2 kann auf dem **eigenen, unabhängig validierten** Kern aufbauen, denn die Leitfrage braucht nicht die exakten Kurven des Papers. Die Autorenfrage läuft parallel.
- Bis zur Klärung: keine Aussage, die auf den exakten Referenzkurven des Papers beruht.
- Offen in Etappe 1: Dissipator-Negativkontrollen (V1-10), RWA-Gültigkeit unter Antrieb (V1-12), Herleitung Eq. (27).
