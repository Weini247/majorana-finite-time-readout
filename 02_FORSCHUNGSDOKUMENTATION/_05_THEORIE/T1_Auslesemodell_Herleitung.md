# T1 — Auslesemodell: Herleitungsprüfungen (WP 1.2)

Stand 2026-11-09. Gleichungsnummern: Benjadi & Egger, arXiv:2603.06482v2 (L01).

## 1. Antrieb und Amplitudenkonvention (Eqs. 9, 10, 18, 20, 35)
Aus \(H_{dr}\) im rotierenden Rahmen \(i\sqrt{\kappa_{in}I_0}(a^\dagger-a)\) folgt \(\langle\dot a\rangle\ni-i\langle[a,H]\rangle=+\sqrt{\kappa_{in}I_0}\).
Ohne Kopplung: \(\langle a\rangle_{ss}=\sqrt{\kappa_{in}I_0}/(i\Delta_0+\kappa/2)=-i\sqrt{\kappa_{in}I_0}/(\Delta_0-i\kappa/2)\) ⇒ \(A=\sqrt{\kappa_{out}/I_0}\langle a\rangle\) hat die Form von Eq. (20), \(\arg A\to-\pi/2\) für \(\omega<\omega_0\).
**Datenbefund:** fig3a Spalte 4 folgt exakt dieser Konvention (Abw. ≤ 4e-5). Die Vorzeichenfrage zu Eq. (34)/(35) ist für die Reproduktion damit **gegenstandslos** (Eq. 20/35 definieren A; ob \(S_{21}\) dasselbe Vorzeichen hat, ist eine reine Phasenkonvention von π). Status: geklärt für die Reproduktion.

## 2. Semiklassik = lineare Antwort bei T = 0 (Eqs. 16–20)
Für \(T=0\), \(I_0\to0\) ist das Qubit im Grundzustand, \(\langle a\tau_z\rangle=-\langle a\rangle+O(I_0^{3/2})\). Damit ist Eq. (18) mit \(\langle\tau_z\rangle=-1\) die **exakte** lineare Antwort des dissipativen Jaynes–Cummings-Modells (Vakuum-Rabi-Transmission). Numerisch bestätigt: VAL1 (rel. ≤ 1e-6), Fehler \(\varepsilon_A\propto I_0\).
**Konsequenz:** Im RWA-Modell (Eq. 10/12) bei schwachem Antrieb und \(T=30\) mK (\(n_{th}=0.022\)) ist die Semiklassik bis auf ~\(10^{-3}\) genau. Die in L01 Fig. 3(a–d) gezeigten Abweichungen von 10–30 % können daher **nicht** aus diesem Modell bei linearer Antwort stammen.

## 3. Dispersive Verschiebung im vollen Modell (Eqs. 5, 21, 22, 26)
Störungstheorie 2. Ordnung für \(H=\omega_z\tau_z+\omega_0a^\dagger a+g_z(a+a^\dagger)\tau_x\), Zustand \(|{\downarrow},n\rangle\):
\[
E^{(2)}_{\downarrow,n}=\frac{g_z^2 n}{\omega_0-2\omega_z}-\frac{g_z^2(n+1)}{2\omega_z+\omega_0}
\Rightarrow \omega_{cav|\downarrow}=\omega_0-g_z^2\Big(\frac1\Delta+\frac1\Sigma\Big)=\omega_0-\frac{g_z^2}{\omega_z-\omega_0^2/(4\omega_z)},
\]
\(\Delta=2\omega_z-\omega_0\), \(\Sigma=2\omega_z+\omega_0\). Mit \(H_{eff}=(\omega_0+\chi\tau_z)a^\dagger a\) und \(\tau_z=-1\) folgt \(\chi=+g_z^2/(\omega_z-\omega_0^2/4\omega_z)\).
L01 Eq. (22) trägt das **entgegengesetzte Vorzeichen**. Exakte Diagonalisierung von Eq. (5) inkl. Longitudinalterm (\(\varepsilon=6\)) bestätigt \(\omega_0-\chi_{SW}\) (VAL5: 15.99181 vs. SW 15.99171; L01-Daten fig3e: Maximum bei 16.008).
**Status:** `HYPOTHESIS` — Vorzeichenfehler in Eq. (22)/(26) *oder* eine im Paper nicht dokumentierte Konvention (z. B. \(\tau_z=+1\) als Grundzustand in der Numerik). Für die Fehlermaße (Vergleich Semiklassik vs. „exakt" mit demselben Hamiltonian) kann das irrelevant sein; für absolute Frequenzlagen nicht. **Klärungsfrage an die Autoren.**

## 4. Thermische Größen (Eqs. 13, 15, 17)
\(\langle\tau_z\rangle=-\tanh(\omega_z/T)\) ist die Gleichgewichtspolarisation eines Niveaupaars mit Aufspaltung \(2\omega_z\) — konsistent mit \(n_{th}=1/(e^{2\omega_z/T}-1)\) wegen \(-\tanh(x)=-(1)/(2n+1)\) mit \(x=\omega_z/T\). Numerisch bestätigt (VAL0). Einheitenkonvention: \(\lambda_0=h\cdot0.2\) GHz (Datenentscheid, VAL4).

## 5. Offene Herleitungen
- Eq. (27) (exakte schwache Kopplung inkl. \(\gamma\)-Term) — noch nicht nachgerechnet.
- Welcher Hamiltonian liefert die „exakten" Referenzspalten (fig3a/3e Spalten 3, 5)? → `BLOCKED` (siehe Befund F-1.3).
