"""
ANALYTICAL == Past & Present Only
"""
import pandas as pd
import numpy as np 
import logging
from datetime import date, timedelta
from collections import defaultdict
class StatisticalAnalytics:

    NET_CASH_FLOW = "net_cash_flow"                         #for enum category
    INCOME_SUMMARY = "income_summary"
    EXPENSE_SUMMARY = "expense_summary"
    MONTHLY_SPEND = "monthly_spend"
    SAVINGS_RATE = "savings_rate"
    INCOME_EXPENSE_RATIO = "income_expense_ratio"
    CATEGORY_BREAKDOWN = "category_breakdown"
    CASH_FLOW_SERIES = "cash_flow_series"
    VOLATILITY = "volatility"
    ANOMALY_DETECTION = "anomaly_detection"
    MONTH_OVER_MONTH_CHANGE = "month_over_month_change"    #for enum category
