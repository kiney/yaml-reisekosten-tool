"""Interne Pauschalentabellen fuer Reisekostenberechnungen."""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Verpflegungspauschalen:
    mehr_als_acht_stunden_eur: Decimal
    vierundzwanzig_stunden_eur: Decimal


@dataclass(frozen=True)
class JahresPauschalen:
    jahr: int
    kilometerpauschalen_eur: dict[str, Decimal]
    verpflegung_inland: Verpflegungspauschalen


class RatesError(ValueError):
    """Fachlicher Fehler beim Zugriff auf Pauschalentabellen."""


class MissingRatesError(RatesError):
    """Fuer das angefragte Kalenderjahr ist keine Pauschalentabelle hinterlegt."""

    def __init__(self, year: int) -> None:
        self.year = year
        super().__init__(f"Keine Pauschalentabelle fuer {year} hinterlegt")


class UnsupportedTransportError(RatesError):
    """Fuer das Verkehrsmittel ist keine Kilometerpauschale hinterlegt."""

    def __init__(self, transport: str, year: int) -> None:
        self.transport = transport
        self.year = year
        super().__init__(f"Keine Kilometerpauschale fuer {transport!r} in {year} hinterlegt")


_RATES_BY_YEAR: dict[int, JahresPauschalen] = {
    2026: JahresPauschalen(
        jahr=2026,
        kilometerpauschalen_eur={"privater_pkw": Decimal("0.30")},
        verpflegung_inland=Verpflegungspauschalen(
            mehr_als_acht_stunden_eur=Decimal("14.00"),
            vierundzwanzig_stunden_eur=Decimal("28.00"),
        ),
    ),
}


def get_rates_for_year(year: int) -> JahresPauschalen:
    try:
        return _RATES_BY_YEAR[year]
    except KeyError as exc:
        raise MissingRatesError(year) from exc


def get_kilometerpauschale(year: int, transport: str) -> Decimal:
    rates = get_rates_for_year(year)
    try:
        return rates.kilometerpauschalen_eur[transport]
    except KeyError as exc:
        raise UnsupportedTransportError(transport, year) from exc


def get_verpflegungspauschalen_inland(year: int) -> Verpflegungspauschalen:
    return get_rates_for_year(year).verpflegung_inland
