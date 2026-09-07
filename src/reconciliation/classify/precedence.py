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
# EXPERIMENT (2026-09-07, not yet locally verifiable): 0 of 250 practice
# invoices fail more than one check, so this order has never actually been
# exercised against real data -- any choice here is a genuine hypothesis,
# not a proven-correct rule. Current hypothesis, one isolated change from
# the starter kit's own order: GST_ERROR promoted above QTY_MISMATCH/
# RATE_MISMATCH. Reasoning: gst is the only check computed entirely from
# the invoice's own fields (taxable_value vs gst_amount) -- quantity/rate
# both depend on comparing against an external reference (the PO), which
# could plausibly tolerate legitimate real-world variance in ways an
# internal arithmetic inconsistency shouldn't. See CLAUDE.md's experiment
# log for the submitted result once known.
PRECEDENCE = [
    ("MISSING_PO", "po_exists"),
    ("VENDOR_MISMATCH", "vendor"),
    ("UOM_MISMATCH", "uom"),
    ("GST_ERROR", "gst"),
    ("QTY_MISMATCH", "quantity"),
    ("RATE_MISMATCH", "rate"),
]
