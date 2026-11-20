# ADR-0006 — Paritätswechsel während der Messung (Etappe 6)

**Status:** accepted · 2026-11-18 · Grundlage: `_02_ETAPPEN/ETAPPE_6_PLAN.md` §3, ADR-0005, L01 Eqs. (2)–(5), (10), (12)

## Modell
- Paritätsregister z ∈ {+1, −1} als klassischer Index (Superauswahl): ρ = ρ₊ ⊕ ρ₋, keine Kohärenzen zwischen den Sektoren. Jeder Block folgt dem RWA-Lindblad-Modell seiner Parität mit gemeinsamem Homodynkanal (ADR-0005).
- Paritätswechsel als symmetrischer Markov-Telegrafenprozess mit Rate Γ_qp pro Richtung, unabhängig von Antrieb, Resonator- und Doppelpunktzustand (A6-1):
  \(\dot\rho_\pm = \mathcal L_\pm\rho_\pm + \Gamma_{qp}(U\rho_\mp U^\dagger - \rho_\pm)\). Äquivalent im erweiterten Raum: Sprungoperator \(\sqrt{\Gamma_{qp}}\,\sigma_x\otimes 1\) mit blockdiagonalem H und Dissipatoren \(P_z\otimes L_z\).
- Ein Wechsel ist instantan und lässt den physikalischen Zustand von Resonator und Doppelpunkt unverändert (A6-2). In der paritätsabhängigen Rabi-Basis ist daher \(U = 1\otimes V_{-z}^\dagger V_z\).
- **L01-Parameter (ε = 0, φ = 0):** \(t_z = t_0 \pm t_1\) ist für beide Paritäten reell und positiv, die Rabi-Eigenbasen stimmen überein, also U = 1. Der rotierende Rahmen (Antriebsfrequenz ω) ist für beide Sektoren derselbe. Geprüft in VAL10 (V6-0), mit Negativkontrolle φ = 0.1. Für φ ≠ 0 oder ε ≠ 0 ist dieses ADR nicht anwendbar.
- Zu dekodieren ist die Parität zu Beginn der Messung.

## Numerik
- **Trajektorien:** Der wahre Paritätsverlauf wird als Poisson-Prozess gezogen (Wechselwahrscheinlichkeit \(1-e^{-\Gamma_{qp}dt}\) je Schritt, eigener Zufallsstrom). Wegen U = 1 und zustandsunabhängiger Rate ist das eine exakte Entfaltung: Der bedingte Zustand wird mit dem Rouchon-Ralph-Schritt (exakter kohärenter Propagator, F-3.4) des jeweils aktuellen Sektors propagiert, der Wechsel ändert nur, welcher Sektor gilt.
- **Bayes-Filter (Wonham-artig):** je Anfangsparität ein Filter über den gekoppelten Zustand (W₊, W₋): Rouchon-Ralph-Schritt je Block, danach Mischung mit Wahrscheinlichkeit \(1-e^{-\Gamma_{qp}\Delta t}\), gemeinsame Normierung. Log-Likelihood-Inkrement wie bisher aus \(\langle x\rangle\) des Gesamtzustands der jeweiligen Hypothese. Für Γ_qp = 0 identisch mit dem Etappe-3-Filter.
- **Mittelwerte:** `qutip.mesolve` im erweiterten Raum (2 × d).
- Γ_qp·dt ≤ 3·10⁻⁵ im geplanten Raster; Wechsel in erster Ordnung pro Schritt sind unkritisch.

## Konsequenzen
- Für Γ_qp = 0 reproduziert der Code die Etappe-3-Ergebnisse bitgenau (V6-1); jede Abweichung ist ein Fehler.
- Asymmetrische oder antriebsabhängige Vergiftung, Vergiftung des Doppelpunkts und nichttriviales U sind ausgeschlossen (Plan §9).
