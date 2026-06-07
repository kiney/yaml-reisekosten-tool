---
id: TASK-6
title: Typst-Rendering aus berechneter Abrechnung implementieren
status: To Do
assignee: []
created_date: '2026-06-07 19:11'
labels:
  - implementation
  - rendering
  - typst
dependencies:
  - TASK-5
documentation:
  - ARCHITECTURE.md
  - src/yaml_reisekosten_tool/templates/reisekosten.typ
  - examples/rendered/reisekosten_typst.pdf
priority: high
ordinal: 6000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Schliesst die berechnete Abrechnung an das vorhandene Typst-Template `src/yaml_reisekosten_tool/templates/reisekosten.typ` an. Die Aufgabe baut einen Render-Kontext, findet das Template als Package-Daten und ruft Typst so auf, dass ein PDF entsteht. Die CLI-Orchestrierung und Dateinamenlogik werden erst im folgenden CLI-Task final verdrahtet.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `rendering.py` baut aus einer berechneten Abrechnung einen stabilen Typst-Render-Kontext mit allen fuer das Template noetigen Werten.
- [ ] #2 Das vorhandene Template wird als Package-Daten gefunden, ohne vom aktuellen Arbeitsverzeichnis abzuhaengen.
- [ ] #3 Der Typst-Aufruf ist gekapselt und gibt kontrollierte Fehler fuer fehlendes Typst, fehlendes Template oder fehlgeschlagenes Rendering zurueck.
- [ ] #4 Das Rendering schreibt ein PDF an einen explizit uebergebenen Zielpfad oder erzeugt eine klar testbare Zwischenausgabe fuer den finalen Schreibschritt.
- [ ] #5 Unit-Tests pruefen Render-Kontext, Template-Aufloesung und Typst-Aufruf mit gefaktem Prozessaufruf.
- [ ] #6 Wenn Typst lokal installiert ist, gibt es optional einen Integrationstest oder dokumentierten manuellen Check mit `examples/example.yml`.
<!-- AC:END -->
