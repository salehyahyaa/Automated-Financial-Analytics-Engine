"""
Flags logic if anomaly decides something is unusual (Z-score, thresholds).
"""

# -----------------------------------------------------------------------------
# PRIVATE NOTES — What belongs in AnomalyDetector (same format as Layer 1 & 2)
# -----------------------------------------------------------------------------
#
# AnomalyDetector does NOT compute:
#   - Mean (μ)
#   - Stddev / Volatility (σ)
#   - Monthly spend, burn rate, or any other descriptive metric
# Those stay in StatisticalAnalytics. This class only USES precomputed values.
#
# -----------------------------------------------------------------------------
# STEP 1 — Z-Score
# -----------------------------------------------------------------------------
#   Z = (x - μ) / σ
#
#   Where:
#     x  = value to check (e.g. single transaction amount or daily total)
#     μ  = mean (passed in from StatisticalAnalytics)
#     σ  = stddev (passed in from StatisticalAnalytics)
#
#   Guard: if σ == 0, do not divide; treat as no anomaly or skip.
#
# -----------------------------------------------------------------------------
# STEP 2 — Threshold (flag anomaly)
# -----------------------------------------------------------------------------
#   Flag anomaly if:  |Z| > threshold
#
#   Typical threshold = 2  (or 3 for stricter).
#
#   Returns: list of flagged points / anomalies (e.g. indices, values, or rows).
#
# -----------------------------------------------------------------------------
# Summary: AnomalyDetector receives (x, mean, stddev) → computes Z → applies
#          threshold → returns flags. No descriptive math lives here.
# -----------------------------------------------------------------------------


"""
-Flags unusual transactions like:
-A $900 restaurant charge when your average is $40
-A duplicate transaction


Time-Series Anomalies
-Looks at trends over time:
-Monthly spend jumps 3x
-Daily balance drops faster than expected
"""