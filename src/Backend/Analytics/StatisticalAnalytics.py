"""
=======================================================
LAYER q — ANALYTICAL (Descriptive: Past & Present Only)
=======================================================

1. Net Cash Flow
Net Cash Flow = sum(amount)

2. Income
Income = sum(amount where amount > 0)

3. Expenses
Expenses = sum(amount where amount < 0)

4. Monthly Spend
Monthly Spend = sum(amount) grouped by month

5. Burn Rate (Daily)
Burn Rate = abs(total expenses over last 30 days) / 30

6. Savings Rate
Savings Rate = (Income - abs(Expenses)) / Income

7. Income vs Expense Ratio
Ratio = Income / abs(Expenses)

8. Category Totals
Category Total = sum(amount grouped by category)

9. Category Share (%)
Category Share = Category Total / Total Spending

10. Rolling Average (7-Day Example)
RollingAvg_7d(t) = (sum of amounts from t-6 through t) / 7

11. Running Total (Cumulative Flow)
Cumulative(t) = sum of all transaction amounts from start through time t

12. Volatility (Standard Deviation)
Volatility = sqrt( average( (x - mean)^2 ) )

13. Z-Score (Anomaly Detection)
Z = (x - mean) / standard_deviation
Flag anomaly if abs(Z) > 2

14. Month-Over-Month Change
MoM = (ThisMonth - LastMonth) / LastMonth
"""