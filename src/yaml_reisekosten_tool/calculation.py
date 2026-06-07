"""Berechnung von Reisekosten aus normalisierten Eingabedaten."""

from __future__ import annotations

from datetime import datetime
from decimal import ROUND_HALF_UP, Decimal

from yaml_reisekosten_tool.models import (
    Auslage,
    AuslagenPosition,
    BerechneteAbrechnung,
    BerechneteFahrt,
    BerechnungsSummen,
    Fahrt,
    ReisekostenEingabe,
)
from yaml_reisekosten_tool.rates import get_kilometerpauschale, get_verpflegungspauschalen_inland

_CENT = Decimal("0.01")


class CalculationError(ValueError):
    """Fachlicher Fehler bei der Reisekostenberechnung."""


def calculate_reisekosten(eingabe: ReisekostenEingabe) -> BerechneteAbrechnung:
    """Berechne Einzelpositionen und Summen fuer eine normalisierte Abrechnung."""

    berechnete_fahrten = tuple(
        _calculate_fahrt(index, fahrt) for index, fahrt in enumerate(eingabe.fahrten)
    )
    auslagen = tuple(position for fahrt in berechnete_fahrten if (position := fahrt.auslage))
    fahrtkosten = _sum_money(fahrt.fahrtkosten_eur for fahrt in berechnete_fahrten)
    verpflegung = _sum_money(fahrt.verpflegungspauschale_eur for fahrt in berechnete_fahrten)
    auslagen_summe = _sum_money(position.betrag_eur for position in auslagen)
    gesamt = _money(fahrtkosten + verpflegung + auslagen_summe)

    return BerechneteAbrechnung(
        eingabe=eingabe,
        fahrten=berechnete_fahrten,
        auslagen=auslagen,
        summen=BerechnungsSummen(
            fahrtkosten_eur=fahrtkosten,
            verpflegungspauschalen_eur=verpflegung,
            auslagen_eur=auslagen_summe,
            gesamt_eur=gesamt,
        ),
    )


def _calculate_fahrt(index: int, fahrt: Fahrt) -> BerechneteFahrt:
    if fahrt.datum is None:
        raise CalculationError(f"fahrten[{index}].datum fehlt")
    if fahrt.verkehrsmittel is None:
        raise CalculationError(f"fahrten[{index}].verkehrsmittel fehlt")
    if fahrt.gesamt_km is None:
        raise CalculationError(f"fahrten[{index}].gesamt_km fehlt")

    kilometerpauschale = get_kilometerpauschale(fahrt.datum.year, fahrt.verkehrsmittel)
    fahrtkosten = _money(fahrt.gesamt_km * kilometerpauschale)
    abwesenheit_minuten = _abwesenheit_minuten(index, fahrt)
    verpflegung = _verpflegungspauschale(fahrt.datum.year, abwesenheit_minuten)
    auslage = _auslagen_position(index, fahrt)
    auslage_betrag = auslage.betrag_eur if auslage else Decimal("0.00")
    gesamt = _money(fahrtkosten + verpflegung + auslage_betrag)

    return BerechneteFahrt(
        index=index,
        fahrt=fahrt,
        abwesenheit_minuten=abwesenheit_minuten,
        kilometerpauschale_eur=kilometerpauschale,
        fahrtkosten_eur=fahrtkosten,
        verpflegungspauschale_eur=verpflegung,
        auslage=auslage,
        gesamt_eur=gesamt,
    )


def _abwesenheit_minuten(index: int, fahrt: Fahrt) -> int:
    if fahrt.datum is None or fahrt.startzeit is None or fahrt.endzeit is None:
        raise CalculationError(f"fahrten[{index}].startzeit oder endzeit fehlt")

    start = datetime.combine(fahrt.datum, fahrt.startzeit)
    end = datetime.combine(fahrt.datum, fahrt.endzeit)
    if end <= start:
        raise CalculationError(f"fahrten[{index}].endzeit muss nach startzeit liegen")
    return int((end - start).total_seconds() // 60)


def _verpflegungspauschale(year: int, abwesenheit_minuten: int) -> Decimal:
    pauschalen = get_verpflegungspauschalen_inland(year)
    if abwesenheit_minuten >= 24 * 60:
        return pauschalen.vierundzwanzig_stunden_eur
    if abwesenheit_minuten > 8 * 60:
        return pauschalen.mehr_als_acht_stunden_eur
    return Decimal("0.00")


def _auslagen_position(index: int, fahrt: Fahrt) -> AuslagenPosition | None:
    auslage = fahrt.auslage
    if auslage is None:
        return None
    if fahrt.datum is None:
        raise CalculationError(f"fahrten[{index}].datum fehlt")
    _require_auslage(index, auslage)
    return AuslagenPosition(
        fahrt_index=index,
        datum=fahrt.datum,
        art=auslage.art,
        betrag_eur=_money(auslage.betrag_eur),
        beschreibung=auslage.beschreibung,
        beleg=auslage.beleg,
    )


def _require_auslage(index: int, auslage: Auslage) -> None:
    if auslage.art is None:
        raise CalculationError(f"fahrten[{index}].auslage.art fehlt")
    if auslage.betrag_eur is None:
        raise CalculationError(f"fahrten[{index}].auslage.betrag_eur fehlt")
    if auslage.beschreibung is None:
        raise CalculationError(f"fahrten[{index}].auslage.beschreibung fehlt")


def _sum_money(values) -> Decimal:
    return _money(sum(values, Decimal("0.00")))


def _money(value: Decimal) -> Decimal:
    return value.quantize(_CENT, rounding=ROUND_HALF_UP)
