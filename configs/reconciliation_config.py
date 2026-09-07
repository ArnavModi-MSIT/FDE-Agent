# Tunable thresholds for the reconciliation engine. Centralized so nothing
# in checks/ or classify/ hardcodes a business rule -- every value here was
# confirmed against the real practice data before being set (see CLAUDE.md).

GST_RATE_PCT = 18.0            # every one of 250 practice invoices declares this
GST_TOLERANCE_RUPEES = 0.05    # matches the starter kit's own tolerance
RATE_TOLERANCE_RUPEES = 0.01   # matches the starter kit's own tolerance
QTY_TOLERANCE = 1e-6           # float equality slack after uom canonicalization
