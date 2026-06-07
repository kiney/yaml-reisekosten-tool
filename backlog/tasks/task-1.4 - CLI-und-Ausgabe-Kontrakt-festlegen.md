---
id: TASK-1.4
title: CLI- und Ausgabe-Kontrakt festlegen
status: To Do
assignee: []
created_date: '2026-06-07 15:18'
updated_date: '2026-06-07 15:18'
labels:
  - architecture
  - cli
dependencies:
  - TASK-1.1
  - TASK-1.3
parent_task_id: TASK-1
priority: medium
ordinal: 5000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Definiert das erwartete Verhalten des einfachen CLI-Interfaces fuer die erste nutzbare Version. Ohne Zusatzargumente soll `yaml-reisekosten-tool foo.yml` im aktuellen Verzeichnis PDF-Dateien mit sinnvollen Namen erzeugen und keinen unnoetigen Output hinterlassen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Der Standardaufruf mit einer YAML-Datei und das erwartete Ausgabeverzeichnis sind festgelegt.
- [ ] #2 Regeln fuer PDF-Dateinamen sind definiert, inklusive Verhalten bei mehreren Abrechnungen oder Namenskollisionen.
- [ ] #3 Das Verhalten bei ungueltiger Eingabe, fehlender Datei und Render-Fehlern ist grob entschieden.
- [ ] #4 Es ist entschieden, welche optionalen CLI-Argumente fuer die erste Version aufgenommen oder bewusst weggelassen werden.
<!-- AC:END -->
