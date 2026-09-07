from reconciliation.uom.converter import canonicalize
from reconciliation.uom.registry import parse_uom


def test_base_unit_passes_through():
    result = canonicalize(qty=20, rate=100, uom="Nos")
    assert result.ok
    assert result.canonical_qty == 20
    assert result.canonical_rate == 100


def test_box_of_ten_converts_to_nos():
    # Real pattern from vendor_invoices.csv (INV-TRP-0186): 20 Box(10)
    # against a 200 Nos PO, rate 57816.5/box vs 5781.65/unit -- both sides
    # must reconcile once canonicalized.
    result = canonicalize(qty=20, rate=57816.5, uom="Box(10)")
    assert result.ok
    assert result.base_unit == "Nos"
    assert result.canonical_qty == 200
    assert abs(result.canonical_rate - 5781.65) < 1e-9


def test_carton_of_twenty_converts_to_nos():
    # Never observed in the practice data -- proves the registry is a
    # genuine generic "Label(N)" parser, not secretly hardcoded to "Box".
    result = canonicalize(qty=3, rate=200.0, uom="Carton(20)")
    assert result.ok
    assert result.canonical_qty == 60
    assert abs(result.canonical_rate - 10.0) < 1e-9


def test_pack_of_five_converts_to_nos():
    result = canonicalize(qty=4, rate=50.0, uom="Pack(5)")
    assert result.ok
    assert result.canonical_qty == 20
    assert abs(result.canonical_rate - 10.0) < 1e-9


def test_unknown_uom_does_not_guess():
    result = canonicalize(qty=5, rate=10, uom="Kg")
    assert not result.ok
    assert result.canonical_qty is None


def test_parse_uom_rejects_malformed_pattern():
    assert parse_uom("Box(ten)") is None
    assert parse_uom("Box(0)") is None
    assert parse_uom("") is None
