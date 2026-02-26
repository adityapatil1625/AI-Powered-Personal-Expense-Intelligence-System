from datetime import date
from collections import defaultdict


def generate_insights(transactions):

    if not transactions:
        return {}

    total_spent = float(sum(t.amount for t in transactions))

    # -------------------------
    # Category breakdown
    # -------------------------
    category_totals = defaultdict(float)

    for t in transactions:
        category_totals[t.category] += float(t.amount)

    highest_category = max(
        category_totals,
        key=category_totals.get
    )

    # -------------------------
    # Average daily spend
    # -------------------------
    days = len(set(t.transaction_date for t in transactions))
    avg_daily = total_spent / days if days else 0

    # -------------------------
    # Spending Prediction AI
    # -------------------------
    today = date.today().day
    predicted_monthly_spend = (
        avg_daily * 30
    )

    # -------------------------
    # Overspending Warning
    # -------------------------
    warning = None

    if category_totals[highest_category] > total_spent * 0.4:
        warning = (
            f"High spending detected in {highest_category}"
        )

    return {
        "total_spent": round(total_spent, 2),
        "highest_spending_category": highest_category,
        "average_daily_spend": round(avg_daily, 2),
        "predicted_monthly_spend": round(predicted_monthly_spend, 2),
        "category_breakdown": dict(category_totals),
        "warning": warning,
    }