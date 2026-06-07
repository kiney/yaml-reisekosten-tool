---
id: TASK-1.2
title: 'Dokumentenerzeugung entscheiden: Typst vs. LaTeX'
status: To Do
assignee: []
created_date: '2026-06-07 15:18'
labels:
  - architecture
  - pdf
  - decision
dependencies: []
parent_task_id: TASK-1
priority: high
ordinal: 3000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Fuehrt einen kurzen Spike zur PDF-Erzeugung durch und entscheidet, ob Typst fuer die Reisekostenabrechnung praktikabel ist oder ob LaTeX als Fallback verwendet wird. Die Entscheidung soll Build-/Runtime-Anforderungen, Template-Wartbarkeit und PDF-Qualitaet gegen die Lexware-Vorlage abwaegen.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Typst und LaTeX sind anhand derselben minimalen Abrechnungsskizze verglichen oder nachvollziehbar bewertet.
- [ ] #2 Die Entscheidung benennt den gewaelten Renderer und die wichtigsten Gruende, inklusive Installations-/CI-Auswirkungen.
- [ ] #3 Die Entscheidung beschreibt, wie Templates im Projekt abgelegt und aus Python heraus angesteuert werden sollen.
- [ ] #4 Falls Typst gewaehlt wird, ist klar dokumentiert, unter welchen Bedingungen auf LaTeX zurueckgefallen wird oder warum kein Fallback noetig ist.
<!-- AC:END -->
