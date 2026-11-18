# EXP-R1 — Reproduktion L01 Fig. 3(a), 3(c) [+ Gegenprobe 3(g)]

**Klasse:** Reproduktion · **Status:** semiklassische Spalten 3(a)/3(e) `REPRODUCED`; exakte Spalten und 3(c) `BLOCKED` (Lauf `EXP-R1_20261109T193812Z`, Befunde F-1.1–F-1.6). Vorab registriert 2026-11-09, vor jeder Rechnung.

## 1. Ziel
Nachrechnen der stationären Phase \(\arg A_\omega(\omega)\) (3a) und der drei semiklassischen Fehlermaße vs. \(\Delta_z\) (3c) im Regime starker Kopplung.

## 2. Referenzdaten
Zenodo 10.5281/zenodo.20623730 v1 (CC-BY-4.0): `fig3a.dat` (md5 `3e54e58cf919a7aa9e1e1a8c7e257618`), `fig3c.dat` (md5 `c8d8d3df89c151eb5aa9069c9774bfc6`, lokal verifiziert: 101 × 4, x ∈ [−1,1], Δx = 0.02), `fig3g.dat` (md5 `969e52a731eea2ab6bca3382b307879f`).

## 3. Parameter (L01 Fig.-3-Caption, Einheiten λ₀)
\(|t_0|=5,\ |t_1|=1,\ \varphi=0,\ z=+1\ (|t_z|=6),\ \varepsilon=0,\ \omega_0=11.99,\ \gamma=0.003,\ \Gamma_\phi=0.1,\ \lambda=0.1,\ \kappa=0.04,\ \omega=\omega_0\) (Basis), T = 30 mK.
Abgeleitet: \(\omega_z=6\), \(2\omega_z=12\), \(g_z=-0.05\), \(\Delta_z(\omega_0)=0.01\).
Nicht publiziert → Varianten: \(\kappa_{in}=\kappa_{out}=\kappa/2\) (Basis), \(I_0\in\{10^{-6},10^{-4},10^{-2}\}\cdot\kappa\) (Linear-Response-Test).

## 4. Metriken und Akzeptanzregel (fixiert)
Für jede Spalte \(c\) mit Referenz \(r_c(x_i)\) und Rechnung \(s_c(x_i)\):
- **Primär:** \(\max_i|s_c-r_c|\le 0.01\cdot\max_i r_c\) (1 % des Kurvenmaßstabs, Vorrecherche).
- **Sekundär (wegen log-Darstellung):** Median\(_i\,|s_c-r_c|/r_c\le 0.02\) über alle Punkte mit \(r_c>10^{-5}\).
- Eigene numerische Konvergenz muss ≥ 10× strenger sein als die Abweichung zur Referenz (T3).
`REPRODUCED` ⇔ Primär **und** Sekundär für alle Spalten von 3a und 3c unter genau **einer** Konventionsvariante. 3g muss nur Primär erfüllen.

## 5. Konventionsdiskriminierung (vorab festgelegtes Raster)
| Achse | Werte |
|---|---|
| Sweep-Variante | (a) \(\omega=2\omega_z-\Delta_z\), \(\omega_z\) fest; (b) \(\omega=\omega_0\) fest, \(\omega_z\) über \(\varepsilon\) bzw. Parameter so variiert, dass \(\Delta_z\) die x-Werte trifft |
| λ₀-Konvention | ordinary GHz / angular |
| \(\varepsilon_{a\tau_z}\)-Definition | exakt/exakt/exakt vs. exakt \(\langle a\tau_z\rangle\) gegen semiklassisches Produkt |
| Spaltenzuordnung | alle 6 Permutationen der Spalten 2–4 (nur zur Erkennung; keine Wahl ohne physikalische Begründung) |
| \(I_0\) | 3 Werte (s. o.) |
**Entscheidungsregel:** Die Variante mit kleinster primärer Residuennorm wird nur übernommen, wenn sie die Akzeptanzregel erfüllt **und** die zweitbeste Variante sie um mindestens Faktor 3 verfehlt. Sonst `BLOCKED` (Mehrdeutigkeit, K-6) mit Autorenfrage.

## 6. Negativkontrollen
Falsches Vorzeichen von \(g_z\) (muss für \(\varepsilon_\phi\) invariant sein — Test der Erwartung); \(\Gamma_\phi\) statt \(\Gamma_\phi/2\) in \(D[\tau_z]\); T = 0 statt 30 mK. Erwartung: deutliche Verletzung, außer wo physikalisch Invarianz vorhergesagt wird (wird vorab je Kontrolle notiert).

## 7. Ausgaben
F1-1, F1-2, F1-3, F1-5; `metrics.csv` mit allen Residuen je Variante; Manifest.
