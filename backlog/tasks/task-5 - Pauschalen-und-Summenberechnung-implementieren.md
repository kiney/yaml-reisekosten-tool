---
id: TASK-5
title: Pauschalen und Summenberechnung implementieren
status: Done
assignee:
  - Codex
created_date: '2026-06-07 19:11'
updated_date: '2026-06-07 20:00'
labels:
  - implementation
  - calculation
dependencies:
  - TASK-4
documentation:
  - README.md
  - ARCHITECTURE.md
  - examples/example.yml
modified_files:
  - src/yaml_reisekosten_tool/models.py
  - src/yaml_reisekosten_tool/rates.py
  - src/yaml_reisekosten_tool/calculation.py
  - tests/test_calculation.py
  - README.md
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implementiert die fachliche Berechnungsschicht der Reisekostenabrechnung. Aus den normalisierten Fahrten und Auslagen werden Kilometerkosten, Verpflegungsmehraufwand und Gesamtsummen berechnet. Die Software verwendet interne Jahrestabellen statt Werte aus dem YAML; fehlende Tabellenjahre werden als fachlicher Fehler gemeldet. Rendering und CLI-Ausgabe sind nicht Bestandteil dieser Aufgabe.

Für die Implementierung werden im ersten Schritt fachliche Werte für 2026 und falls verfügbar 2027 recherchiert.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 `rates.py` enthaelt interne Regeln oder Tabellen fuer Kilometerpauschalen und Verpflegungspauschalen fuer die im Beispiel benoetigten Jahre.
- [x] #2 `calculation.py` berechnet Fahrtkosten aus Gesamt-Kilometern und Kilometerpauschale.
- [x] #3 Verpflegungspauschalen werden aus Datum, Startzeit und Endzeit anhand der internen Regeln berechnet oder kontrolliert als nicht berechenbar gemeldet.
- [x] #4 Auslagen werden in die Abrechnungssummen uebernommen und separat ausweisbar gehalten.
- [x] #5 Das Ergebnis enthaelt eine berechnete Abrechnung mit Einzelpositionen und Gesamtsummen, die fuer den Render-Kontext nutzbar ist.
- [x] #6 Unit-Tests decken Kilometerkosten, Verpflegungspauschale, Auslagen, Rundung und fehlende Pauschalentabellen ab.
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
Genehmigter Implementierungsplan:
1. `rates.py` neu anlegen mit internen Tabellen fuer 2026: privater Pkw `0.30 EUR/km`, Verpflegung Inland `14 EUR` bei mehr als 8 Stunden und `28 EUR` bei 24 Stunden. Fuer 2027 wird keine Tabelle angelegt, solange keine belastbare offizielle Quelle verfuegbar ist; fehlende Jahre werden als fachlicher Fehler gemeldet.
2. Rechtslage fuer die 8-Stunden-Grenze pruefen und das Verhalten klar dokumentieren: genau 8:00 Stunden ergibt keine Verpflegungspauschale, erst mehr als 8 Stunden ergibt die Tagespauschale.
3. `models.py` um berechnete, immutable Ergebnis-Dataclasses erweitern: berechnete Fahrtpositionen, Auslagenpositionen, Summen und berechnete Abrechnung.
4. `calculation.py` neu anlegen: pro Fahrt Kilometerkosten, Verpflegungspauschale und Auslage berechnen, Geldwerte auf Cent runden, Summen bilden, fehlende Pauschalentabellen/unsupported Verkehrsmittel kontrolliert melden.
5. Tests ergaenzen: Beispielabrechnung, Kilometerkosten, Verpflegung bei >8h, genau 8h und <8h, Auslagenpositionen, Rundung und fehlendes Tabellenjahr.
6. README um Berechnungsregeln und Grenzfaelle ergaenzen.
7. `pytest` und wenn verfuegbar `ruff check .` ausfuehren; danach Acceptance Criteria und Tasknotizen aktualisieren.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implementiert `rates.py` fuer 2026 mit privater-Pkw-Kilometerpauschale 0.30 EUR/km und Inlands-Verpflegungspauschalen 14.00/28.00 EUR. 2027 bleibt bewusst nicht hinterlegt, da keine belastbare offizielle 2027-Tabelle verfuegbar war; fehlende Jahre werfen `MissingRatesError`.

Die Verpflegungspauschale fuer eintagige Fahrten nutzt die gesetzliche Formulierung mehr als 8 Stunden. Exakt 8:00 Stunden wird daher mit 0.00 EUR berechnet; ab 8:01 Stunden mit 14.00 EUR.

Berechnungsergebnis enthaelt renderbare Einzelpositionen pro Fahrt, separat ausgewiesene Auslagenpositionen und Summen fuer Fahrtkosten, Verpflegung, Auslagen und Gesamtbetrag.

Validierung: `.venv/bin/python -m pytest` mit 26 passed; `ruff check .` ohne Befund.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Berechnungsschicht fuer Reisekosten implementiert.

Geaendert wurden Domain-Modelle, neue Pauschalentabellen und die eigentliche Berechnungspipeline. `rates.py` enthaelt die 2026er internen Saetze fuer `privater_pkw` und Inlands-Verpflegungspauschalen. `calculation.py` berechnet pro Fahrt Kilometerkosten, Verpflegungspauschale, Auslagen und Gesamtsumme mit kaufmaennischer Cent-Rundung. Fehlende Jahre und nicht hinterlegte Verkehrsmittel werden kontrolliert als fachliche Fehler gemeldet.

Die README dokumentiert die Berechnungsregeln und den wichtigen Grenzfall: genau 8:00 Stunden Abwesenheit ergibt keine Verpflegungspauschale; erst mehr als 8 Stunden, praktisch ab 8:01, ergibt 14.00 EUR.

Tests ergaenzt fuer Beispielabrechnung, Kilometerkosten, Rundung, Auslagen, fehlende Pauschalentabellen und die >8h-Grenze. Validierung: `.venv/bin/python -m pytest` -> 26 passed; `ruff check .` -> passed.
<!-- SECTION:FINAL_SUMMARY:END -->
