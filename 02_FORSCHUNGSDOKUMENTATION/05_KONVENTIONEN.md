# Physikalische und numerische Konventionen (v1.0, Etappe 1)

Änderungen nur mit Versionssprung und ADR. Jede Konvention nennt ihre Quelle.

## 1. Einheiten

- \(\hbar=k_B=1\) (L01).
- Interne Energieeinheit: \(\lambda_0\). Alle Configs speichern **dimensionslose** Werte in Einheiten von \(\lambda_0\) plus das Feld `konvention_lambda0 ∈ {"gewoehnlich", "kreisfrequenz"}` und `lambda0_value = 0.2`.
- Temperatur wird nur über \(T/\lambda_0\) eingespeist. Umrechnung \(k_B T/h = 20.837\,\text{GHz/K}\cdot T\); bei `ordinary_GHz`: \(T/\lambda_0 = 20.837\,T[\text{K}]/0.2\); bei `angular`: \(T/\lambda_0 = 2\pi\cdot 20.837\,T[\text{K}]/0.2\). **Entschieden (D-1.1, 2026-11-09): `gewoehnlich`, d. h. λ₀ = h·0.2 GHz** — datenbasiert über die semiklassische Phase von fig3a (Abw. 3.6e-5 vs. 0.28 rad für Kreisfrequenz; VAL4, Befund F-1.1).
- Zeiten in \(1/\lambda_0\).

## 2. Hilbertraum und Basis

- Tensorordnung: **Resonator ⊗ Doppelpunkt** (Fock-Cutoff \(N_c\), dann 2-dim.). Operatoren `a = destroy(N_c) ⊗ 1`, `tau_k = 1 ⊗ σ_k`.
- Doppelpunkt-Pauli \(\tau_{x,y,z}\) wirken in der **Rabi-Eigenbasis** (L01 nach Eq. 4); \(\tau_z=+1\) = obere Eigenenergie \(+\omega_z\). \(\tau_\pm=(\tau_x\pm i\tau_y)/2\), \(\tau_-\) senkt die Energie.
- Paritätssektor \(z=\pm1\) ist ein **Parameter** (getrennte Simulation je Sektor), kein dynamischer Freiheitsgrad, solange keine Paritätsflips modelliert werden.
- Interferenz: \(t_z = t_0 + z\,t_1 e^{i\varphi}\) mit reellen \(t_0,t_1\ge0\) (Eichung: Phase in \(t_1\)); konsistent mit L01 Eq. (2) für komplexe \(t_0,t_1\).

## 3. Hamiltonoperatoren (Hierarchie, explizit benannt)

| Name | Definition | Gültigkeit |
|---|---|---|
| `H_full_lab` | L01 Eq. (5) + Antrieb Eq. (9), Laborrahmen, zeitabhängig | Referenz für RWA-Prüfung |
| `H_rwa_rot` | L01 Eq. (10): \(\tfrac{\Delta_z}{2}\tau_z+\Delta_0a^\dagger a+g_z(a\tau_++a^\dagger\tau_-)+i\sqrt{\kappa_{in}I_0}(a^\dagger-a)\) | \(|\omega_0-2\omega_z|\ll\min(\omega_0,\omega_z)\) |
| `H_disp_rot` | L01 Eq. (23) | \(\lambda\ll\min(\omega_0,|\omega_0\pm2\omega_z|)\) |

\(g_z=-\lambda|t_z|/(2\omega_z)\) (L01 Eq. 7, **mit Vorzeichen**). \(\Delta_z=2\omega_z-\omega\), \(\Delta_0=\omega_0-\omega\).

## 4. Dissipation, Messung, Statistik

- \(D[L]\rho=L\rho L^\dagger-\tfrac12\{L^\dagger L,\rho\}\). Dephasierung als \(\tfrac{\Gamma_\phi}{2}D[\tau_z]\) ⇒ Kohärenzzerfall mit Rate \(\Gamma_\phi\) (L01 Eq. 12, 15).
- Kanalzerlegung: \(\kappa=\kappa_{in}+\kappa_{out}\) (L01 Eq. 8); zusätzlich interne Verluste \(\kappa_{int}\) erst ab Etappe 2 und dann \(\kappa=\kappa_{in}+\kappa_{out}+\kappa_{int}\). **Kein Doppelzählen**: Der gemessene Port ist ein Teil von \(\kappa D[a]\), nicht zusätzlich.
- Homodyn (Wiseman–Milburn, L23), gemessener Port mit Effizienz \(\eta\):
  \(d\rho_c=\mathcal L\rho_c\,dt+\sqrt{\eta\kappa_{out}}\,\mathcal H[e^{-i\theta}a]\rho_c\,dW\),
  \(dY=\sqrt{\eta\kappa_{out}}\langle e^{-i\theta}a+e^{i\theta}a^\dagger\rangle_c\,dt+dW\), \(dW^2=dt\) (Itô).
  Ineffizienz ≙ unbeobachteter Anteil \((1-\eta)\kappa_{out}\) im unbedingten Lindblad-Term. Im Laborrahmen enthält der Ausgang zusätzlich \(b_{in}\)-Terme; ein bekannter kohärenter Offset wird in der Auswertung subtrahiert und dokumentiert.
- Photonenressource: \(\bar n_{\max}=\max_t\langle a^\dagger a\rangle\) und Pulsenergie \(\int|\mathcal E|^2dt\) werden für jeden Arbeitspunktvergleich **gleich** begrenzt.
- Fehlerrate: \(P_{err}(T)=\tfrac12[P(\hat z=-|z=+)+P(\hat z=+|z=-)]\) mit gleichen Priors. Konfidenzintervalle: Wilson-Score (95 %) über unabhängige Records, nie über Zeitpunkte. Kalibrier- und Testrecords haben disjunkte Seed-Zweige.
- Zufallszahlen: `numpy.random.SeedSequence(root).spawn(...)`; Root-Seed in jedem Manifest.

## 5. Toleranzklassen (Werte vorläufig, endgültig in WP 1.0)

| Klasse | Wofür | Vorläufiger Wert | Begründung |
|---|---|---|---|
| T1 exakt | Operatoridentitäten, Hermitizität von H, Spurerhaltung des Liouvillians | ≤ 1e-12 abs. | Rundungsniveau bei Einträgen O(10–100) |
| T2 Solver | Steady-State-Residuum \(\|\mathcal L\rho\|_F\), \(|\mathrm{Tr}\rho-1|\), \(\lambda_{\min}(\rho)\ge-\)tol | ≤ 1e-10 bzw. ≥ −1e-10 | direkte Sparse-Lösung, Konditionszahl wird mitprotokolliert |
| T3 Konvergenz/Reproduktion | Cutoff-/dt-Konvergenz; Vergleich mit Referenzdaten | eigene Konvergenz ≤ 1e-4 rel. auf Observablen; Reproduktion ≤ 1 % des Kurvenmaßstabs bzw. abs. ≤ 1e-4 nahe Nullstellen | Vorrecherche; eigene Numerik eine Größenordnung strenger als die Reproduktionstoleranz |
| T4 statistisch | SME-Ensemble vs. Mastergleichung; Fehlerraten | |Δ| ≤ 3σ (Standardfehler) und Wilson-CI | stochastische Größen |
| T5 Negativkontrolle | z. B. \(t_1=0\) muss Kontrast < T2 liefern; absichtlich falsches Vorzeichen muss T3 deutlich verletzen | Verletzung ≥ 100 × Toleranz | — |

## 6. Statuskennzeichnung

| Status | Bedeutung |
|---|---|
| `VERIFIED` | Eigene Rechnung/Herleitung geprüft gegen unabhängige Referenz (analytisch oder zweite Methode) |
| `REPRODUCED` | Ergebnis einer Publikation innerhalb vorab registrierter Toleranz nachgerechnet, Daten-/Parameterzuordnung dokumentiert |
| `HYPOTHESIS` | Begründete, noch ungeprüfte Annahme oder Vermutung |
| `OPEN` | Frage ohne bisherigen Prüfversuch |
| `FAILED` | Geprüft und widerlegt bzw. Reproduktion außerhalb Toleranz — bleibt dokumentiert |
| `BLOCKED` | Prüfung nicht möglich wegen fehlender Information/Ressource; Blocker benannt |
