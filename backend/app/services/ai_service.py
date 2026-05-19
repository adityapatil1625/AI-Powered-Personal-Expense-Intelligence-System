"""AI-powered financial insights and chat service."""

from __future__ import annotations

import re


def _contains_any(text: str, phrases: list[str]) -> bool:
    """Return True if any phrase appears in text."""
    return any(phrase in text for phrase in phrases)


def _tokenize(text: str) -> set[str]:
    """Normalize free text into lowercase word tokens."""
    return set(re.findall(r"[a-zA-Z]+", text.lower()))


def _format_inr(amount: float) -> str:
    """Format currency in rounded INR style for concise chat responses."""
    return f"₹{amount:,.0f}"


def _detect_intents(message: str, tokens: set[str]) -> list[str]:
    """Rank intents by relevance and return matched intents."""
    intent_rules = {
        "overspending": {
            "keywords": {
                "over", "overspend", "overspending", "excess", "expensive",
                "waste", "wasting", "high", "more", "control"
            },
            "phrases": [
                "too much", "spending too much", "where am i overspending",
                "am i overspending", "high spend",
            ],
        },
        "savings": {
            "keywords": {
                "save", "saving", "savings", "reduce", "cut", "cheaper",
                "optimize", "optimise"
            },
            "phrases": ["how to save", "save money", "cut cost", "reduce spending"],
        },
        "forecast": {
            "keywords": {
                "month", "monthly", "forecast", "projection", "projected",
                "future", "estimate", "budget"
            },
            "phrases": ["this month", "next month", "how much will i spend"],
        },
        "health": {
            "keywords": {"health", "score", "status", "stable", "risk"},
            "phrases": ["financial health", "health score", "how am i doing"],
        },
        "subscriptions": {
            "keywords": {"subscription", "subscriptions", "recurring", "autopay"},
            "phrases": ["recurring payments", "auto debit", "monthly charges"],
        },
        "anomalies": {
            "keywords": {"anomaly", "anomalies", "spike", "spikes", "unusual"},
            "phrases": ["unusual spending", "spending spike", "odd transactions"],
        },
        "summary": {
            "keywords": {"summary", "report", "overview", "recap"},
            "phrases": ["monthly summary", "overall summary", "quick summary"],
        },
    }

    scores: dict[str, int] = {}
    for intent, rules in intent_rules.items():
        keyword_hits = len(tokens.intersection(rules["keywords"]))
        phrase_hits = sum(2 for phrase in rules["phrases"] if phrase in message)
        total_score = keyword_hits + phrase_hits
        if total_score > 0:
            scores[intent] = total_score

    ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return [intent for intent, _ in ranked]


def _build_savings_suggestions(category_percentages: dict[str, float]) -> list[str]:
    """Build targeted savings suggestions from category share thresholds."""
    prioritized = sorted(
        category_percentages.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    suggestions = [
        f"- {cat}: {pct:.1f}% of spend. Try trimming 10-20%."
        for cat, pct in prioritized
        if pct >= 20
    ]

    return suggestions[:3]


def generate_chat_response(message: str, insights: dict) -> str:
    """Generate context-aware AI response based on user query and insights."""
    original_message = message.strip()
    message = original_message.lower()
    tokens = _tokenize(message)

    total = float(insights.get("total_spent", 0) or 0)
    breakdown = {
        cat: float(amount)
        for cat, amount in (insights.get("category_breakdown", {}) or {}).items()
    }
    predicted = float(insights.get("predicted_monthly_spend", 0) or 0)
    health = int(insights.get("financial_health_score", 0) or 0)
    subscriptions = insights.get("subscriptions", []) or []
    anomalies = insights.get("anomalies", []) or []
    monthly_summary = insights.get("monthly_summary", "") or ""
    budget_warning = insights.get("budget_warning", "") or ""

    if total <= 0 or not breakdown:
        return (
            "You don't have enough transaction data yet. Add a few expenses first, "
            "then ask me things like: 'Where am I overspending?', "
            "'What is my monthly forecast?', or 'How can I save more?'."
        )

    category_percentages = {
        cat: (amt / total) * 100
        for cat, amt in breakdown.items()
        if total > 0
    }

    sorted_categories = sorted(
        breakdown.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    top_category, top_amount = sorted_categories[0]
    top_percentage = category_percentages[top_category]

    mentioned_categories = [
        cat for cat in breakdown.keys()
        if cat.lower() in message
    ]

    intents = _detect_intents(message, tokens)

    response_parts: list[str] = []

    if mentioned_categories:
        details = []
        for cat in mentioned_categories[:2]:
            amount = breakdown[cat]
            pct = category_percentages.get(cat, 0)
            details.append(f"{cat}: {_format_inr(amount)} ({pct:.1f}% of total)")
        response_parts.append("Category view: " + " | ".join(details))

    if "overspending" in intents:
        response_parts.append(
            "Overspending signal: "
            f"{top_category} is highest at {_format_inr(top_amount)} "
            f"({top_percentage:.1f}%). "
            f"A 20% cut there saves about {_format_inr(top_amount * 0.2)}/month."
        )

    if "forecast" in intents:
        forecast_line = f"Monthly forecast: {_format_inr(predicted)}."
        if budget_warning:
            forecast_line += f" {budget_warning}."
        response_parts.append(forecast_line)

    if "health" in intents:
        if health >= 80:
            health_text = "strong"
        elif health >= 60:
            health_text = "stable"
        elif health >= 40:
            health_text = "average"
        else:
            health_text = "at risk"

        response_parts.append(
            f"Financial health: {health}/100 ({health_text})."
        )

    if "savings" in intents:
        suggestions = _build_savings_suggestions(category_percentages)
        if suggestions:
            response_parts.append("Savings plan:\n" + "\n".join(suggestions))
        else:
            response_parts.append(
                "Savings plan: your spending mix is fairly balanced right now."
            )

    if "subscriptions" in intents:
        if subscriptions:
            response_parts.append(
                f"Recurring payments found: {len(subscriptions)} active subscription(s)."
            )
        else:
            response_parts.append("No clear recurring subscriptions detected yet.")

    if "anomalies" in intents:
        if anomalies:
            response_parts.append(
                f"Detected {len(anomalies)} unusual spending spike(s) in recent trends."
            )
        else:
            response_parts.append("No unusual spending spikes detected recently.")

    if "summary" in intents and monthly_summary:
        response_parts.append("Summary: " + monthly_summary)

    # Friendly fallback for open-ended prompts.
    if not response_parts:
        top_two = sorted_categories[:2]
        quick_focus = ", ".join(
            f"{cat} ({(amount / total) * 100:.1f}%)"
            for cat, amount in top_two
        )
        response_parts.append(
            "Quick snapshot: "
            f"spent {_format_inr(total)} so far, top areas are {quick_focus}, "
            f"and projected monthly spend is {_format_inr(predicted)}."
        )
        response_parts.append(
            "Ask me for: overspending check, savings plan, health score, "
            "monthly forecast, subscriptions, anomalies, or category breakdown."
        )

    # Keep responses concise but informative.
    return "\n\n".join(response_parts[:3])
