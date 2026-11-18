# EXP-E1 — Pilot: stationär gewählter vs. endlichzeit-optimaler Arbeitspunkt

**Klasse:** explorativ (Etappe 2) · **Status:** durchgeführt (Lauf `EXP-E1_20261109T203942Z`). Ergebnis: Gauß-Regret ≤ 0.8 pp (Nullresultat im Pilotgebiet), Trajektorien nicht entscheidend; Pilotgebiet zu nahe am Raten (F-2.3–F-2.5). Vorab registriert 2026-11-09, vor jeder Rechnung.

## Frage
Wählt die Maximierung der stationären Trennrate denselben Antriebsfrequenz-Arbeitspunkt ω wie die Minimierung der Fehlerrate einer Homodynmessung der Dauer T, bei gleicher maximaler Resonatorbesetzung?

## Modell (fixiert)
L01-Parameter der starken Kopplung (Fig. 3a–d), λ₀ = h·0.2 GHz, T = 30 mK, κ_in = κ_out = 0.02, ε = 0, φ = 0.
Paritäten: z = +1 (|t_z| = 6, ω_z = 6, resonant) vs. z = −1 (|t_z| = 4, ω_z = 4, weit verstimmt). RWA-Modell Eq. (10)/(12), Messkanal ADR-0005, Startzustand thermisch.
Effizienz η = 0.5 (Pilot); Rechteckpuls ab t = 0.

## Ressourcenregel
Für jedes ω wird I0 so kalibriert, dass \(\bar n_{\max}=\max_{t\le T_{\max},z}\langle a^\dagger a\rangle=\bar n^*\). Zwei Budgets: \(\bar n^*\) = 0.01 (lineare Antwort) und 0.3 (Sättigung des resonanten Qubits erwartet, n_sat ≈ 0.03).

## Metriken
- Quadratur θ(ω): maximiert die stationäre Mittelwerttrennung.
- Stationär: \(D_{ss}(\omega)=(\mu_+^{ss}-\mu_-^{ss})^2\) ⇒ \(\omega_{stat}=\arg\max D_{ss}\).
- Endlich (Gauß-Benchmark aus exakten Mittelwert-Records, ADR-0005): \(P_G(T;\omega)\), \(T\in\{25,50,100,200,400\}\,\lambda_0^{-1}\) (20–320 ns) ⇒ \(\omega_T=\arg\min P_G\); Regret \(R(T)=P_G(T;\omega_{stat})-P_G(T;\omega_T)\).
- Trajektorien (Gültigkeitsprüfung des Gauß-Benchmarks): an ω_stat und ω_T für das T mit größtem Regret, Matched Filter + Boxcar, 2000 Kalibrier- und 2000 Testrecords je Parität, Wilson-95-%-Intervalle; dt = 0.2 mit Halbierungsprüfung an einem Punkt.

## Raster
ω ∈ [11.80, 12.20] in Schritten von 0.01 (41 Punkte).

## Relevanz- und Entscheidungsregel
Relevanzschwelle 2 Prozentpunkte. „Regret relevant", wenn die Trajektorien-Fehlerraten an ω_stat und ω_T sich um > 2 pp unterscheiden **und** die Wilson-Intervalle disjunkt sind. Nullresultat, wenn |ΔP| < 2 pp mit Intervallobergrenze < 2 pp. Ein reiner Gauß-Benchmark-Regret ohne Trajektorienbestätigung ist nur `HYPOTHESIS`.

## Bekannte Einschränkungen (vorab)
Nur ein Arbeitspunktparameter (ω), kein Pulsdesign, keine Drift, RWA. Das Ergebnis ist Klasse „explorativ" und kein Neuheitsclaim (N-K9 deckt das allgemeine Phänomen in cQED ab).
