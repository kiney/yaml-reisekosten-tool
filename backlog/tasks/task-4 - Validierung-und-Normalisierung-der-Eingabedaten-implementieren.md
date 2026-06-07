---
id: TASK-4
title: Validierung und Normalisierung der Eingabedaten implementieren
status: To Do
assignee: []
created_date: '2026-06-07 19:10'
labels:
  - implementation
  - validation
  - normalization
dependencies:
  - TASK-3
documentation:
  - README.md
  - ARCHITECTURE.md
  - examples/example.yml
priority: high
ordinal: 4000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Ergaenzt die fachliche Eingangspruefung und Normalisierung nach dem in `README.md` dokumentierten YAML-Format. Defaults aus `defaults.fahrt` und `defaults.auslage` werden auf einzelne Eintraege angewendet, Overrides bleiben erhalten, und Datums-, Zeit-, Geld- und Kilometerwerte werden in stabile Python-Werte ueberfuehrt. Fehler sollen Feldpfade enthalten, damit die CLI spaeter nutzbare deutsche Meldungen ausgeben kann.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Pflichtbereiche und Pflichtfelder aus dem README werden validiert, inklusive `abrechnung`, `mitarbeiter`, `arbeitgeber` und `fahrten`.
- [ ] #2 Defaults fuer Fahrten und Auslagen werden korrekt angewendet; ein einzelner Fahrt- oder Auslagenwert ueberschreibt den Default.
- [ ] #3 Datumswerte, Uhrzeiten im Format `HH:MM`, Euro-Betraege und Kilometer werden in stabile Python-Typen normalisiert.
- [ ] #4 Fehler fuer fehlende oder ungueltige Felder enthalten einen nachvollziehbaren Feldpfad wie `fahrten[3].datum`.
- [ ] #5 Fachlich unplausible Basisdaten wie negative Kilometer oder Endzeit vor Startzeit werden kontrolliert abgelehnt.
- [ ] #6 Unit-Tests decken Default/Override-Verhalten, gueltige Normalisierung und mehrere Fehlerfaelle ab.
<!-- AC:END -->
