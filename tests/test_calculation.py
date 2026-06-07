from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from pathlib import Path

import pytest

from yaml_reisekosten_tool.calculation import calculate_reisekosten
from yaml_reisekosten_tool.normalization import normalize_reisekosten_input
from yaml_reisekosten_tool.rates import MissingRatesError
from yaml_reisekosten_tool.yaml_io import load_yaml_mapping


def _valid_input() -> dict:
    return {
        "abrechnung": {
            "titel": "Reisekosten",
            "zeitraum": {"von": "2026-01-01", "bis": "2026-01-31"},
            "waehrung": "EUR",
        },
        "mitarbeiter": {"name": "Max Mustermann"},
        "arbeitgeber": {
            "name": "Beispiel GmbH",
            "anschrift": {"strasse": "Stadtweg 8", "plz": "54321", "ort": "Musterstadt"},
        },
        "defaults": {
            "fahrt": {
                "start": "Zuhause",
                "ziel": "Beispiel GmbH",
                "anlass": "Kundentermin",
                "verkehrsmittel": "privater_pkw",
                "gesamt_km": "84",
                "startzeit": "07:45",
                "endzeit": "19:00",
            },
            "auslage": {
                "art": "parken",
                "betrag_eur": "12.00",
                "beschreibung": "Parkhaus",
            },
        },
        "fahrten": [{"datum": "2026-01-08"}],
    }


def test_calculates_example_totals_for_renderer_context() -> None:
    data = load_yaml_mapping(Path("examples/example.yml"))
    eingabe = normalize_reisekosten_input(data)

    abrechnung = calculate_reisekosten(eingabe)

    assert len(abrechnung.fahrten) == 5
    assert len(abrechnung.auslagen) == 5
    assert abrechnung.summen.fahrtkosten_eur == Decimal("130.20")
    assert abrechnung.summen.verpflegungspauschalen_eur == Decimal("56.00")
    assert abrechnung.summen.auslagen_eur == Decimal("62.00")
    assert abrechnung.summen.gesamt_eur == Decimal("248.20")


def test_calculates_kilometer_costs_with_cent_rounding() -> None:
    data = _valid_input()
    data["fahrten"][0]["gesamt_km"] = "98.335"
    eingabe = normalize_reisekosten_input(data)

    abrechnung = calculate_reisekosten(eingabe)

    assert abrechnung.fahrten[0].kilometerpauschale_eur == Decimal("0.30")
    assert abrechnung.fahrten[0].fahrtkosten_eur == Decimal("29.50")


@pytest.mark.parametrize(
    ("startzeit", "endzeit", "expected"),
    [
        ("08:00", "16:00", Decimal("0.00")),
        ("08:00", "16:01", Decimal("14.00")),
        ("08:00", "15:59", Decimal("0.00")),
    ],
)
def test_meal_allowance_uses_strict_more_than_eight_hours_rule(
    startzeit: str, endzeit: str, expected: Decimal
) -> None:
    data = _valid_input()
    data["fahrten"][0]["startzeit"] = startzeit
    data["fahrten"][0]["endzeit"] = endzeit
    eingabe = normalize_reisekosten_input(data)

    abrechnung = calculate_reisekosten(eingabe)

    assert abrechnung.fahrten[0].verpflegungspauschale_eur == expected


def test_keeps_expenses_separately_and_in_totals() -> None:
    data = _valid_input()
    data["fahrten"][0]["auslage"] = {"betrag_eur": "14.555", "beschreibung": "Ausweichparkhaus"}
    eingabe = normalize_reisekosten_input(data)

    abrechnung = calculate_reisekosten(eingabe)

    assert abrechnung.auslagen[0].fahrt_index == 0
    assert abrechnung.auslagen[0].art == "parken"
    assert abrechnung.auslagen[0].betrag_eur == Decimal("14.56")
    assert abrechnung.summen.auslagen_eur == Decimal("14.56")


def test_reports_missing_rates_table_by_year() -> None:
    data = deepcopy(_valid_input())
    data["abrechnung"]["zeitraum"] = {"von": "2027-01-01", "bis": "2027-01-31"}
    data["fahrten"][0]["datum"] = "2027-01-08"
    eingabe = normalize_reisekosten_input(data)

    with pytest.raises(MissingRatesError) as exc_info:
        calculate_reisekosten(eingabe)

    assert exc_info.value.year == 2027
