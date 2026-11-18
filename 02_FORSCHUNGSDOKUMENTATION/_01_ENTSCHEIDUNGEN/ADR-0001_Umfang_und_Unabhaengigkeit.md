# ADR-0001 — Projektumfang und Unabhängigkeit

**Status:** accepted (Kickoff) · 2026-11-09

## Kontext
P1 (Paritätsauslese bei endlicher Messzeit) ist das Einstiegsprojekt; P2 (RecordBasedSteering) bleibt spätere Option.

## Entscheidung
1. Erster Meilenstein beschränkt auf das effektive Box–Doppelpunkt–Resonator-Modell aus L01 (zwei Paritätssektoren, ein Resonatormode, ein Rabi-Zweiniveausystem).
2. Keine Mehrniveau-, Vergiftungs- oder BdG-Mikroskopik vor G3.
3. Eigenständiger Code; keine Übernahme fremden Codes.
4. P2 wird nicht implementiert; Schnittstellen (Records, Decoder) werden so geschnitten, dass ein späterer P2-Anschluss nicht verbaut ist — ohne Vorabimplementierung.

## Konsequenzen
Kleiner, prüfbarer Kern; Gefahr einer zu engen Frage wird durch Gate G2/G3 adressiert.
