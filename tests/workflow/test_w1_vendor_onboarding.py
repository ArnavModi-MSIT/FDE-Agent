from workflow.w1_vendor_onboarding import find_existing_vendor_in_list, GSTIN, VENDOR_NAME


def test_no_match_returns_none():
    vendors = [{"vendor_id": "V-1", "vendor_name": "Someone Else", "gstin": "AAAAA0000A1Z5"}]
    assert find_existing_vendor_in_list(vendors) is None


def test_matches_on_exact_gstin():
    vendors = [{"vendor_id": "V-99", "vendor_name": "A Totally Different Name", "gstin": GSTIN}]
    result = find_existing_vendor_in_list(vendors)
    assert result is not None and result["vendor_id"] == "V-99"


def test_matches_on_case_insensitive_name():
    vendors = [{"vendor_id": "V-99", "vendor_name": VENDOR_NAME.upper(), "gstin": "AAAAA0000A1Z5"}]
    result = find_existing_vendor_in_list(vendors)
    assert result is not None and result["vendor_id"] == "V-99"


def test_real_sandbox_shape_no_false_positive():
    # Real near-duplicate pattern confirmed in the sandbox: a different
    # real vendor's ALL-CAPS formal-name duplicate must
    # never accidentally match Sri Ranga Castings.
    vendors = [{"vendor_id": "V-1055", "vendor_name": "SHARMA BEARINGS PVT. LTD.", "gstin": "29XBJJU05331ZB"}]
    assert find_existing_vendor_in_list(vendors) is None
