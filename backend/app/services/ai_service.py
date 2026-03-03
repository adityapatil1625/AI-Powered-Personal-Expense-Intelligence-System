"""AI-powered financial insights and chat service."""


def generate_chat_response(message: str, insights: dict) -> str:
    """Generate AI response based on user query and insights."""
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

    # Overspending Analysis
    if "over" in message or "too much" in message:
        return (
            f"Highest spending: {top_category} ({top_percentage:.1f}%). "
            f"Cut by 20% to save ₹{breakdown[top_category] * 0.2:.0f}/month."
        )

    # Savings Strategy
    if "save" in message:
        suggestions = [
            f"{cat}: {pct:.1f}% (reduce it)"
            for cat, pct in category_percentages.items()
            if pct > 25
        ]
        return (
            "Savings opportunities:\n" + "\n".join(suggestions)
            if suggestions
            else "Your spending is balanced."
        )

    # Monthly Forecast
    if "month" in message:
        return f"Projected monthly spend: ₹{predicted:.0f}"

    # Health Score
    if "health" in message or "score" in message:
        return (
            f"Financial health: {health}/100. "
            f"Based on spending distribution and patterns."
        )

    # Category Query
    for cat in breakdown.keys():
        if cat.lower() in message:
            return f"Spent ₹{breakdown[cat]:.0f} on {cat}."

    return "Ask about overspending, savings, forecast, or specific category."
