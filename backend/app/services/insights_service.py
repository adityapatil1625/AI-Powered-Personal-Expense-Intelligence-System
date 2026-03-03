"""Financial insights and analytics service."""
from collections import defaultdict
from datetime import datetime, timedelta
from math import fabs
from sqlalchemy.orm import Session
from app.models.models import Transaction, Budget
from app.services.transaction_service import get_user_transactions


def calculate_financial_health(insights: dict) -> int:
    """Calculate financial health score (0-100)."""
    total = float(insights.get("total_spent", 0))
    breakdown = insights.get("category_breakdown", {})

    score = 100
    if total > 0:
        food_pct = (float(breakdown.get("Food", 0)) / total)
        ent_pct = (float(breakdown.get("Entertainment", 0)) / total)

        if food_pct > 0.3:
            score -= 20
        if ent_pct > 0.2:
            score -= 15

    savings = float(breakdown.get("Savings", 0))
    if savings > 0:
        score += 10

    return max(0, min(100, score))


def get_expense_insights(db: Session, user_id: str) -> dict:
    """Generate comprehensive expense insights for a user."""
    transactions = get_user_transactions(db, user_id)

    if not transactions:
        return {
            "total_spent": 0,
            "highest_spending_category": "N/A",
            "average_daily_spend": 0,
            "predicted_monthly_spend": 0,
            "financial_health_score": 100,
            "financial_status": "Excellent",
            "category_breakdown": {},
            "ai_advice": ["Start tracking expenses for insights!"],
        }

    # Calculate totals
    total_spent = sum(float(t.amount) for t in transactions)
    category_breakdown = defaultdict(float)

    for txn in transactions:
        category_breakdown[txn.category] += float(txn.amount)

    highest_category = max(
        category_breakdown,
        key=category_breakdown.get
    )

    # Calculate trends
    first_date = min(t.transaction_date for t in transactions)
    days_tracked = max((datetime.now().date() - first_date).days, 1)
    avg_daily = total_spent / days_tracked
    predicted_monthly = avg_daily * 30

    insights = {
        "total_spent": round(total_spent, 2),
        "highest_spending_category": highest_category,
        "average_daily_spend": round(avg_daily, 2),
        "predicted_monthly_spend": round(predicted_monthly, 2),
        "category_breakdown": dict(category_breakdown),
        "ai_advice": [],
    }

    # Financial health
    health = calculate_financial_health(insights)
    insights["financial_health_score"] = health

    if health >= 80:
        insights["financial_status"] = "Excellent"
        insights["ai_advice"].append("Great job managing your finances!")
    elif health >= 60:
        insights["financial_status"] = "Good"
        insights["ai_advice"].append("Good progress, room for improvement.")
    elif health >= 40:
        insights["financial_status"] = "Average"
        insights["ai_advice"].append("Review spending in high categories.")
    else:
        insights["financial_status"] = "Needs Improvement"
        insights["ai_advice"].append("Focus on budgeting and expense control.")

    # Budget warning
    budget = db.query(Budget).filter(Budget.user_id == user_id).first()
    if budget:
        insights["monthly_budget"] = budget.monthly_limit
        if predicted_monthly > budget.monthly_limit:
            insights["budget_warning"] = (
                f"Projected to exceed budget by "
                f"₹{predicted_monthly - budget.monthly_limit:.0f}"
            )

    # Category analysis
    if total_spent > 0:
        ent_pct = float(category_breakdown.get("Entertainment", 0)) / total_spent
        food_pct = float(category_breakdown.get("Food", 0)) / total_spent

        if ent_pct > 0.2:
            insights["ai_advice"].append("Reduce entertainment expenses.")
        if food_pct > 0.3:
            insights["ai_advice"].append("Food >30%. Try meal planning.")

    insights["subscriptions"] = detect_recurring_subscriptions(transactions)
    insights["spending_trend"] = generate_spending_trend(transactions)
    insights["anomalies"] = detect_spending_anomalies(
        insights["spending_trend"]
    )
    insights["monthly_summary"] = generate_monthly_summary(insights)

    return insights


def detect_recurring_subscriptions(transactions: list) -> list:
    """Detect recurring subscriptions from transactions."""
    merchant_map = defaultdict(list)

    for txn in transactions:
        merchant_map[txn.merchant_name].append(txn)

    subscriptions = []

    for merchant, txns in merchant_map.items():
        if len(txns) < 2:
            continue

        txns.sort(key=lambda x: x.transaction_date)

        for i in range(1, len(txns)):
            prev, curr = txns[i - 1], txns[i]
            days_diff = (curr.transaction_date - prev.transaction_date).days
            amount_diff = fabs(float(curr.amount) - float(prev.amount))
            avg_amount = (float(curr.amount) + float(prev.amount)) / 2

            if (
                25 <= days_diff <= 35
                and avg_amount > 0
                and (amount_diff / avg_amount) <= 0.1
            ):
                next_billing = curr.transaction_date + timedelta(days=30)
                annual_cost = float(curr.amount) * 12

                subscriptions.append({
                    "merchant": merchant,
                    "amount": round(float(curr.amount), 2),
                    "frequency": "Monthly",
                    "next_billing_date": next_billing.isoformat(),
                    "annual_cost": round(annual_cost, 2)
                })
                break

    return subscriptions


def generate_spending_trend(transactions: list) -> list:
    """Generate 30-day spending trend."""
    today = datetime.now().date()
    last_30_days = today - timedelta(days=30)
    daily_totals = defaultdict(float)

    for txn in transactions:
        if txn.transaction_date >= last_30_days:
            daily_totals[txn.transaction_date] += float(txn.amount)

    trend_data = []
    for i in range(31):
        day = last_30_days + timedelta(days=i)
        trend_data.append({
            "date": day.isoformat(),
            "amount": round(daily_totals.get(day, 0), 2)
        })

    return trend_data


def detect_spending_anomalies(trend_data: list) -> list:
    """Detect unusual spending spikes (>2x average)."""
    amounts = [d["amount"] for d in trend_data if d["amount"] > 0]

    if not amounts:
        return []

    avg = sum(amounts) / len(amounts)
    return [d for d in trend_data if d["amount"] > avg * 2]


def generate_monthly_summary(insights: dict) -> str:
    """Generate AI-style financial summary."""
    total = insights["total_spent"]
    top_cat = insights["highest_spending_category"]
    predicted = insights["predicted_monthly_spend"]
    health = insights["financial_health_score"]

    breakdown = insights["category_breakdown"]
    top_amt = breakdown.get(top_cat, 0)
    pct = (top_amt / total * 100) if total > 0 else 0

    summary = (
        f"Spent ₹{total:,.2f}. Top category: {top_cat} ({pct:.1f}%). "
        f"Projected monthly: ₹{predicted:,.2f}. "
        f"Health score: {health}/100."
    )

    if health >= 80:
        summary += " Excellent financial management."
    elif health >= 60:
        summary += " Stable, but room to improve."
    else:
        summary += " Spending needs attention."

    if insights.get("subscriptions"):
        summary += f" {len(insights['subscriptions'])} subscription(s)."

    if insights.get("anomalies"):
        summary += f" {len(insights['anomalies'])} spending spike(s)."

    return summary
