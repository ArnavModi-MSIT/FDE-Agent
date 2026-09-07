from reconciliation.normalization.common import safe_float


def test_safe_float_handles_csv_string():
    assert safe_float("176") == 176.0
    assert safe_float("17773.86") == 17773.86


def test_safe_float_handles_json_native_numbers():
    # Real bug found reusing normalization/ against the sandbox API:
    # /erp/invoices returns qty as a native JSON int (176), not a string
    # ("176") like the local CSV -- the old implementation called
    # value.strip() unconditionally and crashed with AttributeError.
    assert safe_float(176) == 176.0
    assert safe_float(17773.86) == 17773.86


def test_safe_float_blank_and_none_use_default():
    assert safe_float("") == 0.0
    assert safe_float(None) == 0.0
    assert safe_float(None, default=None) is None


def test_safe_float_unparseable_string_uses_default():
    assert safe_float("not a number") == 0.0
