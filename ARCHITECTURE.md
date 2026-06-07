# Architektur

Dieses Dokument legt die erste Implementierungsarchitektur fuer das Python-Projekt fest. Ziel ist ein kleines, testbares Kommandozeilenwerkzeug: YAML laden, validieren und normalisieren, ein Abrechnungsmodell bilden und daraus per Typst ein PDF erzeugen.

## Zielbild fuer den MVP

Der MVP bleibt bewusst linear:

1. CLI nimmt Eingabe- und Ausgabepfad entgegen.
2. YAML wird sicher geladen.
3. Defaults aus der Eingabe werden auf Fahrten und Auslagen angewendet.
4. Die normalisierten Daten werden in Python-Domain-Objekte ueberfuehrt.
5. Pauschalen und Summen werden anhand interner Regeln berechnet.
6. Ein Typst-Template wird mit den berechneten Daten gerendert.
7. Das erzeugte PDF wird an den gewuenschten Ausgabepfad geschrieben.

Es gibt keine Datenbank, keine Web- oder GUI-Schicht und keine parallele Renderer-Abstraktion. Typst ist der Renderer fuer den MVP.

## Vorgesehene Module

Die Implementierung soll unter `src/yaml_reisekosten_tool/` wachsen. Die folgenden Module sind der vorgesehene Zuschnitt fuer die ersten Code-Tasks:

- `cli.py`: Argumente parsen, Eingabe-/Ausgabepfade pruefen, Hauptablauf starten und Exit-Codes setzen.
- `yaml_io.py`: YAML-Datei lesen, `safe_load` verwenden und reine Ladefehler von fachlicher Validierung trennen.
- `models.py`: Domain-Dataclasses fuer Abrechnung, Mitarbeiter, Arbeitgeber, Fahrzeug, Fahrt, Auslage und berechnete Abrechnung.
- `validation.py`: Pflichtfelder, Typen, Wertebereiche und fachliche Konsistenz pruefen.
- `normalization.py`: Defaults und Overrides anwenden, Datums-/Zeit-/Geldwerte in stabile Python-Typen ueberfuehren.
- `rates.py`: Interne Jahrestabellen und Regeln fuer Kilometer- und Verpflegungspauschalen.
- `calculation.py`: Fahrtkosten, Verpflegungsmehraufwand, Auslagen und Gesamtsummen berechnen.
- `rendering.py`: Render-Kontext fuer Typst bauen, Template-Datei finden und `typst compile` ausfuehren.
- `templates/`: Typst-Templates als Package-Daten, aktuell `templates/reisekosten.typ`.

`__main__.py` kann spaeter ergaenzt werden, damit `python -m yaml_reisekosten_tool` denselben Einstieg wie die CLI nutzt. Ein separates `app.py` oder Service-Layer ist fuer den MVP nicht noetig; die CLI darf den linearen Ablauf direkt orchestrieren.

## Datenfluss

Der Datenfluss ist absichtlich eine Pipeline mit klaren Fehlergrenzen:

1. `cli.py` ermittelt `input.yml` und `output.pdf`.
2. `yaml_io.py` liest die Datei und liefert ein rohes Mapping.
3. `validation.py` prueft die grobe Struktur und meldet fehlende oder unerwartete Felder.
4. `normalization.py` merged `defaults.fahrt` und `defaults.auslage` in die einzelnen Eintraege.
5. `normalization.py` wandelt Datumswerte, Uhrzeiten und Geldbetraege in stabile Python-Werte um.
6. `models.py` nimmt die normalisierten Daten als Dataclasses auf.
7. `rates.py` liefert die fuer das Reisedatum gueltigen Pauschalwerte.
8. `calculation.py` bildet aus Domain-Modell und Pauschalen die berechnete Abrechnung.
9. `rendering.py` uebersetzt die berechnete Abrechnung in einen Typst-Render-Kontext.
10. `rendering.py` ruft Typst auf und schreibt das PDF.

Die Pipeline soll in Tests stufenweise pruefbar sein. Besonders wichtig sind Tests fuer Default/Override-Verhalten, Datums- und Uhrzeitnormalisierung, Summenbildung und die Parameter, mit denen Typst aufgerufen wird.

## Fehlerpunkte

Fehler sollen moeglichst frueh und mit klarer Ursache gemeldet werden:

- Dateisystem: Eingabedatei fehlt, ist nicht lesbar oder Ausgabeverzeichnis ist nicht beschreibbar.
- YAML-Syntax: Datei ist kein gueltiges YAML oder `safe_load` liefert kein Mapping.
- Schema: Pflichtbereiche wie `abrechnung`, `mitarbeiter`, `arbeitgeber` oder `fahrten` fehlen.
- Feldwerte: Datum, Uhrzeit, Geldbetrag, Kilometer oder Waehrung haben ein unerwartetes Format.
- Defaults: Ein Fahrt- oder Auslagen-Eintrag bleibt nach Default-Anwendung unvollstaendig.
- Fachlogik: Reisedatum liegt ausserhalb vorhandener Pauschalentabellen oder Zeiten ergeben keine plausible Dauer.
- Rendering: Typst ist nicht installiert, das Template fehlt oder `typst compile` bricht ab.
- Ausgabe: PDF kann nicht geschrieben werden oder ein vorhandener Zielpfad darf nicht ueberschrieben werden.

Die CLI soll diese Fehler spaeter in lesbare Meldungen und nicht in rohe Tracebacks uebersetzen. Interne Exceptions duerfen trotzdem spezifisch bleiben, damit Tests sie eindeutig pruefen koennen.

## Bewusst ausgelassener Scope

Folgender Scope wird fuer die erste Architektur bewusst nicht eingeplant:

- Kein Webframework, keine REST-API und keine GUI.
- Keine Datenbank und keine persistente Historie von Abrechnungen.
- Kein Plugin-System fuer Renderer oder Pauschalen.
- Kein LaTeX-Fallback parallel zu Typst.
- Keine automatische Belegverarbeitung oder OCR.
- Keine Online-Abfrage gesetzlicher Pauschalen.
- Keine komplexe Formular-Engine fuer beliebige PDF-Vorlagen.
- Keine Mehrmandanten- oder Benutzerverwaltung.

Diese Entscheidungen halten die erste Implementierung klein. Wenn spaeter Bedarf entsteht, koennen die genannten Punkte als eigene Tasks bewertet werden.

## Hinweise fuer erste Tests

Der Projektstart kann mit fokussierten Unit-Tests erfolgen:

- `yaml_io.py`: gueltige Datei laden, YAML-Syntaxfehler abfangen, leere Datei erkennen.
- `normalization.py`: Fahrtdefaults anwenden, einzelne Overrides respektieren, Auslagendefaults anwenden.
- `validation.py`: fehlende Pflichtfelder und fehlerhafte Datums-/Zeitformate melden.
- `calculation.py`: Kilometerkosten, Verpflegungspauschalen, Auslagen und Gesamtsumme berechnen.
- `rendering.py`: Template-Pfad und Typst-Aufruf mit einem gefakten `subprocess` pruefen.

Integrationstests koennen spaeter `examples/example.yml` durch die Pipeline schicken und, sofern Typst installiert ist, ein PDF erzeugen.
