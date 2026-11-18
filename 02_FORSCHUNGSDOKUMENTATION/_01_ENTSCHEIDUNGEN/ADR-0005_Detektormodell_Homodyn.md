# ADR-0005 — Detektormodell: Homodynmessung am Ausgangsport (Etappe 2)

**Status:** accepted · 2026-11-09 · Grundlage: Konventionen §4, L23 (Wiseman–Milburn), L01 Eqs. (8), (33)–(35)

## Modell
- Rotierender Rahmen bei der Antriebsfrequenz ω, RWA-Hamiltonian L01 Eq. (10) mit zeitabhängigem Antrieb \(\mathcal E(t)=\sqrt{\kappa_{in}I_0}\,f(t)\) (Rechteckpuls ab t = 0 als Basis).
- Dissipatoren wie L01 Eq. (12). Der Resonatorzerfall wird zerlegt: \(\kappa D[a] = \kappa_{in}D[a] + (1-\eta)\kappa_{out}D[a] + \eta\kappa_{out}D[a]\); nur der letzte Teil ist beobachtet. **Kein Doppelzählen.**
- Bedingte Dynamik (Itô): \(d\rho_c=\mathcal L\rho_c\,dt+\sqrt{\eta\kappa_{out}}\,\mathcal H[e^{-i\theta}a]\rho_c\,dW\).
- Record: \(dY=\sqrt{\eta\kappa_{out}}\langle e^{-i\theta}a+e^{i\theta}a^\dagger\rangle_c\,dt+dW\), Einheit √Zeit; der kohärente Eingangsanteil \(b_{in}\) ist paritätsunabhängig und wird abgezogen.
- Quadratur θ: vor allen Testrecords fest gewählt, maximiert die stationäre Mittelwerttrennung \(|{\rm Re}[e^{-i\theta}(\langle a\rangle_+-\langle a\rangle_-)]|\).
- Startzustand je Parität: Resonator thermisch (\(N_{th}\)), Doppelpunkt thermisch (\(\langle\tau_z\rangle=-\tanh(\omega_z/T)\)), unkorreliert. Begründung: der Dot relaxiert vor dem Puls; „Rabi-Grundzustand" ist der T → 0-Grenzfall (Q-12).
- Ressource: max. Resonatorbesetzung \(\bar n_{\max}=\max_{t,z}\langle a^\dagger a\rangle\) ist bei Arbeitspunktvergleichen gleich (I0 wird je Arbeitspunkt auf \(\bar n_{\max}\) kalibriert).

## Numerik
- Mittelwerte (Ensemble) über `qutip.mesolve` — exakter Mittelwert der Records.
- Trajektorien: eigener, über Trajektorien vektorisierter Integrator im positivitätserhaltenden Schema nach Rouchon & Ralph (PRA 91, 012118 (2015)): \(\rho\mapsto (M\rho M^\dagger+\sum_k L_k\rho L_k^\dagger dt + (1-\eta)\ldots)/\mathrm{Tr}\) mit \(M=1-iH\,dt-\tfrac12\sum L^\dagger L\,dt+\sqrt{\eta}\,c\,dY\). Gegencheck gegen `qutip.smesolve` (VAL7) und Ensemblemittel gegen `mesolve`.
- dt-Konvergenz (Halbierung) verpflichtend.

## Konsequenzen
- Gauß-Benchmark: Ist die Recorddynamik bei gegebener Parität deterministisch bis auf weißes Rauschen (lineare Antwort, QND), dann gilt für den Matched Filter \(P_{err}=\tfrac12\mathrm{erfc}(\mathrm{SNR}/2\sqrt2)\), \(\mathrm{SNR}^2=\int_0^T(\mu_+-\mu_-)^2dt\). Abweichungen der Trajektorien-Fehlerrate von dieser Formel messen Nicht-Gaußizität (Sättigung, Nicht-QND).
