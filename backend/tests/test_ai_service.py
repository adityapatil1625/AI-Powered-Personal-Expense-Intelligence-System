"""AI service response behavior tests."""

from app.services.ai_service import generate_chat_response


SAMPLE_INSIGHTS = {
    "total_spent": 20000,
    "category_breakdown": {
        "Food": 7000,
        "Entertainment": 5000,
        "Transport": 3000,
        "Shopping": 5000,
    },
    "predicted_monthly_spend": 26000,
    "financial_health_score": 58,
    "budget_warning": "Projected to exceed budget by ₹4,000",
    "subscriptions": [{"merchant": "Netflix"}, {"merchant": "Spotify"}],
    "anomalies": [{"date": "2026-05-10", "amount": 1800}],
    "monthly_summary": (
        "Spent ₹20,000. Top category: Food (35%). "
        "Projected monthly: ₹26,000. Health score: 58/100."
    ),
}


def test_health_query_returns_health_details() -> None:
    """Health prompt should return health score content."""
    response = generate_chat_response("how is my financial health?", SAMPLE_INSIGHTS)
    assert "Financial health" in response
    assert "58/100" in response


def test_forecast_query_returns_monthly_projection() -> None:
    """Forecast prompt should return projected monthly spend."""
    response = generate_chat_response("monthly forecast and budget", SAMPLE_INSIGHTS)
    assert "Monthly forecast" in response
    assert "₹26,000" in response


def test_savings_and_overspending_can_be_answered_together() -> None:
    """Multi-intent prompt should return both overspending and savings advice."""
    response = generate_chat_response("am i overspending and how to save", SAMPLE_INSIGHTS)
    assert "Overspending signal" in response
    assert "Savings plan" in response


def test_open_ended_prompt_returns_snapshot_not_empty_fallback() -> None:
    """Generic prompt should still return useful AI snapshot guidance."""
    response = generate_chat_response("hi", SAMPLE_INSIGHTS)
    assert "Quick snapshot" in response
    assert "projected monthly spend" in response


def test_category_query_returns_category_view() -> None:
    """Category prompt should return amount and percentage for category."""
    response = generate_chat_response("how much on entertainment", SAMPLE_INSIGHTS)
    assert "Category view" in response
    assert "Entertainment" in response
    assert "25.0%" in response
