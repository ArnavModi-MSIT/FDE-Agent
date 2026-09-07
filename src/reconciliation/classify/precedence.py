# The order in which a failing check is allowed to claim an invoice's final
# status, when more than one check fails at once. This is a genuine tunable
# -- the starter kit's own comment says precedence order moves macro-F1, and
# its own confirmed prose explicitly declines to state a rule for invoices
# with multiple defects -- kept separate from classifier.py so it can be
# re-ordered without touching check logic. Each entry pairs the output
# status with the CheckResult.check name that triggers it. DUPLICATE_INVOICE
# and CLEAN are deliberately not here: duplicates are only ever decided in a
# second pass over rows that are otherwise CLEAN (see duplicates/detector.py).
#
# SETTLED: matches the organizer's own reference implementation exactly
# (starter_reconciliation.py's literal if/elif chain -- MISSING_PO,
# VENDOR_MISMATCH, UOM_MISMATCH, QTY_MISMATCH, RATE_MISMATCH, GST_ERROR,
# in that order, then CLEAN). A prior experiment promoted GST_ERROR above
# QTY_MISMATCH/RATE_MISMATCH -- submitted, scored byte-identical to
# baseline (0.8700), no local rows changed either (0/250 invoices ever
# fail 2+ checks). No evidence supported that deviation, so it was
# reverted back to the organizer's own literal order once
# reconciliation_status_matrix.md's audit surfaced the starter's code
# itself as authoritative reference, not just its prose comments.
PRECEDENCE = [
    ("MISSING_PO", "po_exists"),
    ("VENDOR_MISMATCH", "vendor"),
    ("UOM_MISMATCH", "uom"),
    ("QTY_MISMATCH", "quantity"),
    ("RATE_MISMATCH", "rate"),
    ("GST_ERROR", "gst"),
]
