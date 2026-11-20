# Etappenstatus

| Etappe | Status | Gate | Letzte Änderung | Notiz |
|---|---|---|---|---|
| 0 Reconnaissance & Architektur | abgeschlossen | G0 freigegeben (2026-11-09) | 2026-11-09 | Masterplan, ADR-0001…0004 |
| 1 Referenzphysik & Reproduktion | **abgeschlossen mit Einschränkung** | **G1 geschlossen** (2026-11-09) | 2026-11-09 | Kern validiert (VAL0–5), semiklassische Referenz REPRODUCED, exakte Referenz BLOCKED (K-1, Autorenfrage offen). Offen, nicht blockierend: V1-10 Dissipator-Negativkontrollen, V1-12 RWA unter Antrieb, Eq. (27) |
| 2 Endliche Messung | **abgeschlossen** | **G2 freigegeben** (2026-11-10; Bericht `_04_BERICHTE/ETAPPE_2_BERICHT.md`) | 2026-11-10 | VAL6/VAL7 bestanden; EXP-E1, EXP-E2, EXP-E2K durchgeführt. Gauß: stationäre ω-Wahl optimal bis 8 µs; bei Sättigung Gauß zu optimistisch (F-2.7) ⇒ Frage unter echter Statistik offen. Bayes-Filter nach Etappe 3 verschoben |
| 3 Robustheit & Optimierung | **abgeschlossen** (Nullresultat) | **G3 freigegeben** (2026-11-18; Bericht `_04_BERICHTE/ETAPPE_3_BERICHT.md`) | 2026-11-18 | Integratorfehler gefunden und behoben (F-3.4, VAL9). EXP-E3 Lauf 2: ω_stat für alle Decoder optimal, Bayes ≈ MF (K-3b Nullresultat, F-3.5); Gauß-Abweichung ≈ 1.3 pp nur am Resonanzpunkt (F-3.6). EXP-E4: Robustheit Regret 0 (F-3.7) |
| 4 Scientific ML | **entfällt** (G3) | — | 2026-11-18 | Bayes-Decoder schlägt den Matched Filter nicht messbar; ein gelernter Decoder hat im Modell ohne Paritätswechsel keine Lücke zu schließen. Neu zu prüfen, falls Etappe 6 einen Bayes-Vorteil zeigt |
| 5 Research Release | **abgeschlossen** (Release) | G5 teilweise: Repo öffentlich, Kontakt zu den Autoren offen | 2026-11-18 | Öffentliches Repository: github.com/Weini247/majorana-finite-time-readout; englische README mit Abbildungen, MIT, CITATION.cff |
| 6 Paritätswechsel während der Messung | **in Arbeit** | G6a freigegeben (2026-11-18), G6 offen | 2026-11-18 | Plan `ETAPPE_6_PLAN.md`: Quasiteilchen-Paritätswechsel mit Rate Γ_qp; optimale Messzeit, Bayes-(Wonham-)Filter vs. MF. ADR-0006, Modul `_02_AUSFUEHRUNG/paritaetswechsel.py`, VAL10/VAL11 bestanden (F-6.1, F-6.2), Γ_qp-Literatur erfasst, EXP-P1 vorab registriert, Skript mit Probe geprüft. EXP-P1 abgeschlossen (F-6.3): Q-6B Nullresultat, Q-6A optimale Messzeit nur für Γ-blinde Decoder. EXP-P2 abgeschlossen (F-6.4): Q-6C Nullresultat, 11.99 bleibt optimal. Bericht `_04_BERICHTE/ETAPPE_6_BERICHT.md` liegt vor. Nächster Schritt: Entscheidung G6 |

**G3-Entscheidung (2026-11-18):** Etappe 3 als Nullresultat abgeschlossen. Etappe 4 entfällt. Etappe 5 (öffentliches Repo) durchgeführt. Nächste wissenschaftliche Etappe: Paritätswechsel (Etappe 6), weil erst dort Messzeit und Decoder einen echten Zielkonflikt haben.

**G1-Entscheidung (2026-11-09):** Etappe 2 baut auf dem eigenen, gegen Fremdreferenzen validierten Kern auf. Keine Aussage stützt sich auf die nicht reproduzierten exakten Referenzkurven des Papers.
