---
id: TASK-7
title: CLI-Orchestrierung und Ausgabe-Kontrakt implementieren
status: To Do
assignee: []
created_date: '2026-06-07 19:11'
labels:
  - implementation
  - cli
dependencies:
  - TASK-6
documentation:
  - README.md
  - ARCHITECTURE.md
  - examples/example.yml
priority: high
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Verdrahtet die Pipeline zum ersten nutzbaren Kommando `yaml-reisekosten-tool foo.yml`. Die CLI liest genau eine YAML-Datei, durchlaeuft Laden, Validierung, Normalisierung, Berechnung und Rendering und schreibt PDFs gemaess dem in `ARCHITECTURE.md` dokumentierten Ausgabe-Kontrakt. Fehlermeldungen sind kurz, deutsch und gehen auf stderr; erwartbare Fehler enden ohne rohen Traceback.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Der Standardaufruf `yaml-reisekosten-tool foo.yml` erzeugt fuer eine gueltige Eingabe PDF-Dateien im aktuellen Arbeitsverzeichnis.
- [ ] #2 `--output-dir DIR` schreibt in ein existierendes beschreibbares Zielverzeichnis; ungueltige Zielverzeichnisse werden kontrolliert abgelehnt.
- [ ] #3 `--force` erlaubt Ueberschreiben vorhandener Ziel-PDFs; ohne `--force` bricht eine Namenskollision vor dem Veraendern vorhandener PDFs ab.
- [ ] #4 PDF-Dateinamen folgen dem dokumentierten Slug- und Suffix-Kontrakt fuer eine oder mehrere Abrechnungen.
- [ ] #5 Fehlende Eingabedatei, YAML-/Schema-/Fachfehler, Render-Fehler und Ausgabekollisionen erzeugen nutzbare stderr-Meldungen und Exit-Code ungleich `0`.
- [ ] #6 CLI-Tests pruefen Erfolgsfall, optionale Argumente, Dateinamenbildung, Kollisionsschutz und mindestens drei Fehlerklassen.
<!-- AC:END -->
