import { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";
import "./App.css";

interface Insights {
  total_spent: number;
  highest_spending_category: string;
  average_daily_spend: number;
  predicted_monthly_spend: number;
  financial_health_score: number;
  financial_status: string;
  category_breakdown: Record<string, number>;
  ai_advice: string[];
  warning?: string;

  monthly_budget?: number;
  budget_warning?: string;
}

const USER_ID = "550e8400-e29b-41d4-a716-446655440000";

const COLORS = [
  "#2D3748",
  "#4A5568",
  "#718096",
  "#A0AEC0",
  "#CBD5E0",
  "#E2E8F0",
  "#667eea",
  "#764ba2",
  "#5A67D8",
  "#434190",
];

function App() {
  const [insights, setInsights] = useState<Insights | null>(null);
  const [messages, setMessages] = useState<
    { role: "user" | "ai"; text: string }[]
  >([]);
  const [input, setInput] = useState("");

  // ================= FETCH INSIGHTS =================
  useEffect(() => {
    axios
      .get(`http://127.0.0.1:8000/insights/${USER_ID}`)
      .then((res) => setInsights(res.data))
      .catch((err) => console.error(err));
  }, []);

  // ================= SEND CHAT MESSAGE =================
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user" as const, text: input };
    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await axios.post(
        `http://127.0.0.1:8000/chat/${USER_ID}`,
        input,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const aiMessage = {
        role: "ai" as const,
        text: res.data.response,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error(error);
    }

    setInput("");
  };

  if (!insights)
    return (
      <div className="loading-container">
        <div className="card">
          <div className="loading-content">
            <div className="loading-spinner" />
            <h2 className="loading-text">Loading insights...</h2>
          </div>
        </div>
      </div>
    );

  const chartData = Object.entries(
    insights.category_breakdown
  ).map(([category, amount]) => ({
    name: category,
    value: amount,
  }));

  const budgetPercentage =
    insights.monthly_budget && insights.monthly_budget > 0
      ? Math.min(
          (insights.predicted_monthly_spend / insights.monthly_budget) * 100,
          100
        )
      : 0;

  const isOver = insights.predicted_monthly_spend > (insights.monthly_budget || 0);

  return (
    <div className="app-container">
      <div className="app-content">
        {/* ================= HEADER ================= */}
        <div className="app-header">
          <h1 className="app-title">Expense Intelligence</h1>
          <p className="app-subtitle">Financial insights powered by AI</p>
        </div>

        {/* ================= TOP METRICS GRID ================= */}
        <div className="metrics-grid">
          {/* Total Spent Card */}
          <div className="card">
            <div>
              <p className="metric-label">Total Spent</p>
              <h2 className="metric-value">
                ₹{insights.total_spent.toLocaleString("en-IN")}
              </h2>
            </div>
          </div>

          {/* Avg Daily Spend */}
          <div className="card">
            <div>
              <p className="metric-label">Daily Average</p>
              <h2 className="metric-value">
                ₹{insights.average_daily_spend.toLocaleString("en-IN")}
              </h2>
            </div>
          </div>

          {/* Top Category */}
          <div className="card">
            <div>
              <p className="metric-label">Top Category</p>
              <h2 className="metric-value-small">
                {insights.highest_spending_category}
              </h2>
            </div>
          </div>

          {/* Financial Health */}
          <div className="card">
            <div>
              <p className="metric-label">Health Score</p>
              <div style={{ display: "flex", alignItems: "baseline", gap: "6px" }}>
                <h2
                  className="metric-value"
                  style={{
                    color:
                      insights.financial_health_score >= 70
                        ? "#48BB78"
                        : insights.financial_health_score >= 50
                          ? "#ED8936"
                          : "#F56565",
                  }}
                >
                  {insights.financial_health_score}
                </h2>
                <span style={{ fontSize: "16px", color: "#A0AEC0" }}>/100</span>
              </div>
            </div>
          </div>
        </div>

        {/* ================= WARNING BANNER ================= */}
        {insights.warning && (
          <div className="warning-banner">
            <p className="warning-text">{insights.warning}</p>
          </div>
        )}

        <div className="main-grid">
          {/* ================= LEFT SECTION: BUDGET + CHART ================= */}
          <div>
            {/* Budget Card */}
            {insights.monthly_budget != null && (
              <div className="card" style={{ marginBottom: "30px" }}>
                <div>
                  <div className="budget-header">
                    <h3 className="budget-title">Monthly Budget</h3>
                    <span className={`budget-badge ${isOver ? "over-budget" : "on-track"}`}>
                      {isOver ? "Over Budget" : "On Track"}
                    </span>
                  </div>

                  <div className="budget-amounts">
                    <div>
                      <p className="budget-amount-label">Budget</p>
                      <p className="budget-amount-value" style={{ color: "#2D3748" }}>
                        ₹{insights.monthly_budget.toLocaleString("en-IN")}
                      </p>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <p className="budget-amount-label">Predicted</p>
                      <p
                        className="budget-amount-value"
                        style={{ color: isOver ? "#F56565" : "#48BB78" }}
                      >
                        ₹{insights.predicted_monthly_spend.toLocaleString("en-IN")}
                      </p>
                    </div>
                  </div>

                  {/* Progress Bar */}
                  <div className="budget-progress-bar">
                    <div
                      className={`budget-progress-fill ${isOver ? "over-budget" : "on-track"}`}
                      style={{ width: `${budgetPercentage}%` }}
                    />
                  </div>

                  <p className="budget-progress-text">
                    {budgetPercentage.toFixed(0)}% of budget
                  </p>

                  {insights.budget_warning && (
                    <p className="budget-warning">{insights.budget_warning}</p>
                  )}
                </div>
              </div>
            )}

            {/* Pie Chart */}
            <div className="card chart-container">
              <div>
                <h3 className="chart-title">Spending Breakdown</h3>
                <PieChart width={350} height={350}>
                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    outerRadius={120}
                    label={{
                      fill: "#666",
                      fontSize: 12,
                      fontWeight: "600",
                    }}
                  >
                    {chartData.map((_, index) => (
                      <Cell
                        key={`cell-${index}`}
                        fill={COLORS[index % COLORS.length]}
                      />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      background: "rgba(0, 0, 0, 0.8)",
                      border: "none",
                      borderRadius: "8px",
                      color: "white",
                      padding: "10px",
                    }}
                    formatter={(value: number | undefined) =>
                      value ? `₹${value.toLocaleString("en-IN")}` : "₹0"
                    }
                  />
                  <Legend
                    wrapperStyle={{
                      paddingTop: "20px",
                    }}
                  />
                </PieChart>
              </div>
            </div>
          </div>

          {/* ================= RIGHT SECTION: AI ADVISOR + CHAT ================= */}
          <div>
            {/* AI Advisor Card */}
            <div className="card" style={{ marginBottom: "30px" }}>
              <h3 className="advisor-title">AI Financial Advisor</h3>

              <div className="advice-list">
                {insights.ai_advice.map((advice, index) => (
                  <div key={index} className="advice-item">
                    {advice}
                  </div>
                ))}
              </div>
            </div>

            {/* Chat Section */}
            <div className="card chat-container">
              <h3 className="chat-title">Ask AI Assistant</h3>

              {/* Chat Messages */}
              <div className="chat-messages">
                {messages.length === 0 ? (
                  <div className="chat-empty">
                    <p>Ask me anything about your expenses</p>
                  </div>
                ) : (
                  messages.map((msg, index) => (
                    <div
                      key={index}
                      className={`chat-message ${msg.role}`}
                    >
                      <div className={`chat-bubble ${msg.role}`}>
                        {msg.text}
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Chat Input */}
              <div className="chat-input-container">
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === "Enter") sendMessage();
                  }}
                  placeholder="Type your question..."
                  className="chat-input"
                />

                <button onClick={sendMessage} className="chat-button">
                  Send
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;