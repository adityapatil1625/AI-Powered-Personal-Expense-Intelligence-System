from sqlalchemy.orm import Session
from models import Transaction, Budget
from schemas import TransactionCreate
from datetime import datetime
from collections import defaultdict
import uuid


# =========================================
# CREATE TRANSACTION
# =========================================
def create_transaction(db: Session, transaction: TransactionCreate):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


# =========================================
# GET USER TRANSACTIONS
# =========================================
def get_user_transactions(db: Session, user_id: str):
    return (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .all()
    )


# =========================================
# FINANCIAL HEALTH SCORE
# =========================================
def calculate_financial_health(insights):

    total = float(insights["total_spent"])
    breakdown = insights["category_breakdown"]

    food_spending = float(breakdown.get("Food", 0))
    entertainment = float(breakdown.get("Entertainment", 0))
    savings = float(breakdown.get("Savings", 0))

    score = 100

    if total > 0:
        if (food_spending / total) > 0.3:
            score -= 20

        if (entertainment / total) > 0.2:
            score -= 15

    if savings > 0:
        score += 10

    return max(0, min(100, score))


# =========================================
# EXPENSE INSIGHTS ENGINE
# =========================================
def get_expense_insights(db: Session, user_id: str):

    transactions = get_user_transactions(db, user_id)

    # --------- No Transactions ----------
    if not transactions:
        return {
            "total_spent": 0,
            "highest_spending_category": "N/A",
            "average_daily_spend": 0,
            "predicted_monthly_spend": 0,
            "financial_health_score": 100,
            "financial_status": "Excellent",
            "category_breakdown": {},
            "ai_advice": [
                "Start tracking your expenses to get personalized insights!"
            ],
        }

    # --------- Total Spend ----------
    total_spent = sum(float(t.amount) for t in transactions)

    # --------- Category Breakdown ----------
    category_breakdown = defaultdict(float)

    for txn in transactions:
        category_breakdown[txn.category] += float(txn.amount)

    highest_category = max(
        category_breakdown,
        key=category_breakdown.get
    )

    # --------- Date Handling (FIXED) ----------
    first_date = min(t.transaction_date for t in transactions)
    days_tracked = (datetime.now().date() - first_date).days
    days_tracked = max(days_tracked, 1)

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

    # --------- Financial Health ----------
    health = calculate_financial_health(insights)
    insights["financial_health_score"] = health

    if health >= 80:
        insights["financial_status"] = "Excellent"
        insights["ai_advice"].append(
            "Great job! You're managing your finances well."
        )
    elif health >= 60:
        insights["financial_status"] = "Good"
        insights["ai_advice"].append(
            "You're doing well, but there's room for improvement."
        )
    elif health >= 40:
        insights["financial_status"] = "Average"
        insights["ai_advice"].append(
            "Consider reviewing your spending in high categories."
        )
    else:
        insights["financial_status"] = "Needs Improvement"
        insights["ai_advice"].append(
            "Your spending needs attention. Focus on budgeting."
        )

    # --------- Smart Warning ----------
    if predicted_monthly > 50000:
        insights["warning"] = (
            "You're on track to spend over ₹50,000 this month!"
        )
        insights["ai_advice"].append(
            "Set a monthly budget limit to control expenses."
        )
    
    budget = db.query(Budget).filter(
    Budget.user_id == user_id
    ).first()

    if budget:
        insights["monthly_budget"] = budget.monthly_limit

        if predicted_monthly > budget.monthly_limit:
            insights["budget_warning"] = (
                f"You are projected to exceed your monthly budget by "
                f"₹{predicted_monthly - budget.monthly_limit:.0f}."
            )

    # --------- Safe Ratio Checks ----------
    if total_spent > 0:

        if (
            float(category_breakdown.get("Entertainment", 0))
            / total_spent
        ) > 0.2:
            insights["ai_advice"].append(
                "Entertainment spending is high. Consider reducing discretionary expenses."
            )

        if (
            float(category_breakdown.get("Food", 0))
            / total_spent
        ) > 0.3:
            insights["ai_advice"].append(
                "Food expenses are above 30%. Try meal planning to save money."
            )

    return insights
def generate_chat_response(message: str, insights: dict):

    message = message.lower()

    total = insights.get("total_spent", 0)
    breakdown = insights.get("category_breakdown", {})
    predicted = insights.get("predicted_monthly_spend", 0)
    health = insights.get("financial_health_score", 0)

    if total == 0:
        return "You don't have enough transaction data yet."

    # Calculate percentages
    category_percentages = {
        cat: (amt / total) * 100
        for cat, amt in breakdown.items()
    }

    top_category = max(breakdown, key=breakdown.get)
    top_percentage = category_percentages[top_category]

    # -----------------------------
    # Overspending Analysis
    # -----------------------------
    if "over" in message or "too much" in message:
        return (
            f"You are spending most on {top_category} "
            f"({top_percentage:.1f}% of total expenses). "
            f"Reducing this category by 20% could save you "
            f"approximately ₹{breakdown[top_category] * 0.2:.0f} per month."
        )

    # -----------------------------
    # Savings Strategy
    # -----------------------------
    if "save" in message:
        suggestions = []

        for cat, percent in category_percentages.items():
            if percent > 25:
                suggestions.append(
                    f"{cat} is {percent:.1f}% of spending. Consider reducing it."
                )

        if not suggestions:
            return "Your spending distribution is balanced. Focus on increasing income or setting strict budgets."

        return "Here’s where you can save:\n" + "\n".join(suggestions)

    # -----------------------------
    # Monthly Forecast
    # -----------------------------
    if "month" in message:
        return (
            f"Based on your current daily average, "
            f"you are projected to spend ₹{predicted:.0f} this month."
        )

    # -----------------------------
    # Financial Health Explanation
    # -----------------------------
    if "health" in message or "score" in message:
        return (
            f"Your financial health score is {health}/100. "
            f"It is calculated based on category distribution "
            f"and overspending patterns."
        )

    # -----------------------------
    # Category Question
    # -----------------------------
    for cat in breakdown.keys():
        if cat.lower() in message:
            return f"You have spent ₹{breakdown[cat]:.0f} on {cat}."

    return (
        "I analyzed your finances. Ask about overspending, savings, "
        "monthly projection, health score, or a specific category."
    )

def set_budget(db: Session, user_id: str, monthly_limit: float):

    existing = db.query(Budget).filter(
        Budget.user_id == user_id
    ).first()

    if existing:
        existing.monthly_limit = monthly_limit
    else:
        new_budget = Budget(
            id=str(uuid.uuid4()),
            user_id=user_id,
            monthly_limit=monthly_limit
        )
        db.add(new_budget)

    db.commit()
    return {"message": "Budget saved successfully"}