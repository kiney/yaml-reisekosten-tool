---
id: TASK-2
title: Projekt- und Tooling-Grundlage fuer Python-Paket aufsetzen
status: next
assignee: []
created_date: '2026-06-07 19:10'
updated_date: '2026-06-07 19:12'
labels:
  - implementation
  - tooling
dependencies: []
documentation:
  - README.md
  - ARCHITECTURE.md
  - AGENTS.md
priority: high
ordinal: 1000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Richtet die technische Basis fuer die eigentliche Implementierung ein. Der aktuelle Stand enthaelt bereits `src/yaml_reisekosten_tool/` und ein Typst-Template, aber noch keinen sichtbaren Python-Projektvertrag wie `pyproject.toml`, CLI-Entry-Point, Test-Setup oder Ruff-Konfiguration. Grundlage sind `README.md`, `ARCHITECTURE.md` und die Architekturentscheidungen aus `TASK-1.*`. Projektsprache und Fehlermeldungen bleiben Deutsch.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 `pyproject.toml` beschreibt das Paket unter `src/`, die Runtime-Abhaengigkeiten und die Entwicklungswerkzeuge fuer pytest und Ruff.
- [ ] #2 Ein CLI-Entry-Point `yaml-reisekosten-tool` ist paketiert und kann mindestens eine Platzhalter-Hilfe oder kontrollierte Platzhalterausfuehrung starten.
- [ ] #3 `python -m yaml_reisekosten_tool` nutzt denselben Einstieg oder ist bewusst dokumentiert gleichwertig vorbereitet.
- [ ] #4 pytest- und Ruff-Konfiguration sind vorhanden und lassen sich lokal ausfuehren.
- [ ] #5 Mindestens ein Smoke-Test prueft, dass Paketimport und CLI-Einstieg erreichbar sind.
- [ ] #6 README oder Entwicklerhinweise nennen die lokalen Befehle fuer Installation, Tests und Linting.
<!-- AC:END -->
