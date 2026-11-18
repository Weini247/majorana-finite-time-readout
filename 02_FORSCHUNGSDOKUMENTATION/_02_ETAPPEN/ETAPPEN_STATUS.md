# Etappenstatus

| Etappe | Status | Gate | Letzte Änderung | Notiz |
|---|---|---|---|---|
| 0 Reconnaissance & Architektur | abgeschlossen | G0 freigegeben (2026-11-09) | 2026-11-09 | Masterplan, ADR-0001…0004 |
| 1 Referenzphysik & Reproduktion | **abgeschlossen mit Einschränkung** | **G1 geschlossen** (2026-11-09) | 2026-11-09 | Kern validiert (VAL0–5), semiklassische Referenz REPRODUCED, exakte Referenz BLOCKED (K-1, Autorenfrage offen). Offen, nicht blockierend: V1-10 Dissipator-Negativkontrollen, V1-12 RWA unter Antrieb, Eq. (27) |
| 2 Endliche Messung | **abgeschlossen** | **G2 freigegeben** (2026-11-10; Bericht `_04_BERICHTE/ETAPPE_2_BERICHT.md`) | 2026-11-10 | VAL6/VAL7 bestanden; EXP-E1, EXP-E2, EXP-E2K durchgeführt. Gauß: stationäre ω-Wahl optimal bis 8 µs; bei Sättigung Gauß zu optimistisch (F-2.7) ⇒ Frage unter echter Statistik offen. Bayes-Filter nach Etappe 3 verschoben |
| 3 Robustheit & Optimierung | **in Arbeit** (Rechnungen abgeschlossen, Bericht offen) | G3 offen | 2026-11-18 | Integratorfehler gefunden und behoben (F-3.4, VAL9). EXP-E3 Lauf 2: ω_stat für alle Decoder optimal, Bayes ≈ MF (K-3b Nullresultat, F-3.5); Gauß-Abweichung ≈ 1.3 pp nur am Resonanzpunkt (F-3.6). EXP-E4: Robustheit Regret 0 (F-3.7). Nächster Schritt: Etappe-3-Bericht und G3 |
| 4 Scientific ML | OPEN (bedingt) | — | — | nur bei positiver Begründung aus G3 |
| 5 Research Release | OPEN | — | — | — |

**G1-Entscheidung (2026-11-09):** Etappe 2 baut auf dem eigenen, gegen Fremdreferenzen validierten Kern auf. Keine Aussage stützt sich auf die nicht reproduzierten exakten Referenzkurven des Papers.
