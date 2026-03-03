import { useEffect, useState } from "react";
import axios from "axios";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
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
  subscriptions?: {
  merchant: string;
  amount: number;
  frequency: string;
  next_billing_date: string;
  annual_cost: number;
}[];
spending_trend?: {
  date: string;
  amount: number;
}[];
anomalies?: {
  date: string;
  amount: number;
}[];
}

const USER_ID = "550e8400-e29b-41d4-a716-446655440000";

const COLORS = [
  "#5A67D8",  // Purple/Indigo
  "#48BB78",  // Green
  "#F56565",  // Red
  "#ED8936",  // Orange
  "#4299E1",  // Blue
  "#9F7AEA",  // Purple
  "#38B2AC",  // Teal
  "#ECC94B",  // Yellow
  "#ED64A6",  // Pink
  "#667EEA",  // Light Purple
];

function App() {
  const [insights, setInsights] = useState<Insights | null>(null);
  const [messages, setMessages] = useState<
    { role: "user" | "ai"; text: string }[]
  >([]);
  const [input, setInput] = useState("");
  const [showExpenseModal, setShowExpenseModal] = useState(false);
  const [expenseForm, setExpenseForm] = useState({
    amount: "",
    merchant_name: "",
    category: "Food",
    payment_mode: "Card",
    transaction_date: new Date().toISOString().split("T")[0],
  });

  // ================= FETCH INSIGHTS =================
  const fetchInsights = () => {
    axios
      .get(`http://127.0.0.1:8000/insights/${USER_ID}`)
      .then((res) => setInsights(res.data))
      .catch((err) => console.error(err));
  };

  useEffect(() => {
    fetchInsights();
  }, []);

  // ================= ADD EXPENSE =================
  const addExpense = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await axios.post("http://127.0.0.1:8000/transactions", {
        user_id: USER_ID,
        amount: parseFloat(expenseForm.amount),
        transaction_date: expenseForm.transaction_date,
        merchant_name: expenseForm.merchant_name,
        category: expenseForm.category,
        payment_mode: expenseForm.payment_mode,
      });

      // Reset form
      setExpenseForm({
        amount: "",
        merchant_name: "",
        category: "Food",
        payment_mode: "Card",
        transaction_date: new Date().toISOString().split("T")[0],
      });

      // Close modal and refresh insights
      setShowExpenseModal(false);
      fetchInsights();
    } catch (error) {
      console.error("Error adding expense:", error);
      alert("Failed to add expense. Please try again.");
    }
  };

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
          <div className="flex-between">
            <div>
              <h1 className="app-title">Expense Intelligence</h1>
              <p className="app-subtitle">Financial insights powered by AI</p>
            </div>
            <button
              onClick={() => setShowExpenseModal(true)}
              className="add-expense-button"
            >
              + Add Expense
            </button>
          </div>
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
              <div className="flex-baseline">
                <h2
                  className={`metric-value ${
                    insights.financial_health_score >= 70
                      ? "health-score-good"
                      : insights.financial_health_score >= 50
                        ? "health-score-medium"
                        : "health-score-poor"
                  }`}
                >
                  {insights.financial_health_score}
                </h2>
                <span className="score-suffix">/100</span>
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
              <div className="card mb-30">
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
                      <p className="budget-amount-value budget-amount-dark">
                        ₹{insights.monthly_budget.toLocaleString("en-IN")}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="budget-amount-label">Predicted</p>
                      <p
                        className={`budget-amount-value ${isOver ? "budget-amount-over" : "budget-amount-good"}`}
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
            <div className="card">
              <h3 className="chart-title">Spending Breakdown</h3>
              <div className="chart-wrapper">
                <PieChart width={450} height={400}>
                  <Pie
                    data={chartData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    labelLine={false}
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
                      background: "#2D3748",
                      border: "none",
                      borderRadius: "8px",
                      padding: "12px",
                      boxShadow: "0 4px 12px rgba(0, 0, 0, 0.15)",
                    }}
                    labelStyle={{
                      color: "white",
                      fontWeight: "600",
                      marginBottom: "4px",
                    }}
                    itemStyle={{
                      color: "#E2E8F0",
                    }}
                    formatter={(value: number | undefined) => {
                      if (!value) return ["₹0", "Amount"];
                      return [`₹${value.toLocaleString("en-IN")}`, "Amount"];
                    }}
                  />
                </PieChart>
              </div>

              {/* Breakdown Table */}
              <div className="breakdown-table">
                {chartData.map((item, index) => (
                  <div key={index} className="breakdown-row">
                    <div className="breakdown-color" style={{ backgroundColor: COLORS[index % COLORS.length] }}></div>
                    <span className="breakdown-label">{item.name}</span>
                    <span className="breakdown-value">₹{item.value.toLocaleString("en-IN")}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Anomaly Card */}
            {insights.anomalies && insights.anomalies.length > 0 && (
              <div className="card" style={{ marginTop: "30px" }}>
                <h3
                  style={{
                    fontSize: "18px",
                    fontWeight: "700",
                    marginBottom: "16px",
                    color: "#fa709a",
                  }}
                >
                  🚨 Unusual Spending Detected
                </h3>

                {insights.anomalies.map((a, index) => (
                  <div
                    key={index}
                    style={{
                      padding: "10px",
                      marginBottom: "10px",
                      background: "rgba(250, 112, 154, 0.1)",
                      borderRadius: "8px",
                    }}
                  >
                    {a.date} — ₹{a.amount.toLocaleString("en-IN")}
                  </div>
                ))}
              </div>
            )}

            {/* Trend Chart */}
            {insights.spending_trend && (
              <div className="card" style={{ marginTop: "30px" }}>
                <h3
                  style={{
                    fontSize: "18px",
                    fontWeight: "700",
                    marginBottom: "16px",
                  }}
                >
                  📈 30-Day Spending Trend
                </h3>

                <LineChart
                  width={450}
                  height={250}
                  data={insights.spending_trend}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" hide />
                  <YAxis />
                  <Tooltip
                    formatter={(value: number | undefined) => {
                      if (!value) return "₹0";
                      return `₹${value.toLocaleString("en-IN")}`;
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="amount"
                    stroke="#667eea"
                    strokeWidth={3}
                    dot={false}
                  />
                </LineChart>
              </div>
            )}
          </div>

          {/* ================= RIGHT SECTION: AI ADVISOR + CHAT ================= */}
          <div>
            {/* AI Advisor Card */}
            <div className="card mb-30">
              <h3 className="advisor-title">AI Financial Advisor</h3>

              <div className="advice-list">
                {insights.ai_advice.map((advice, index) => (
                  <div key={index} className="advice-item">
                    {advice}
                  </div>
                ))}
              </div>
            </div>

            {/* Subscription Card */}
            {insights.subscriptions && insights.subscriptions.length > 0 && (
              <div className="card mb-30">
                <h3
                  style={{
                    fontSize: "20px",
                    fontWeight: "700",
                    marginBottom: "16px",
                  }}
                >
                  🔁 Detected Subscriptions
                </h3>

                {insights.subscriptions.map((sub, index) => (
                  <div
                    key={index}
                    style={{
                      padding: "12px",
                      marginBottom: "12px",
                      background: "rgba(102, 126, 234, 0.08)",
                      borderRadius: "8px",
                      fontSize: "14px",
                    }}
                  >
                    <strong>{sub.merchant}</strong><br />
                    ₹{sub.amount.toLocaleString("en-IN")} / {sub.frequency}<br />
                    Next Billing: {sub.next_billing_date}<br />
                    Annual Cost: ₹{sub.annual_cost.toLocaleString("en-IN")}
                  </div>
                ))}
              </div>
            )}

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

        {/* ================= ADD EXPENSE MODAL ================= */}
        {showExpenseModal && (
          <>
            <div
              className="modal-overlay"
              onClick={() => setShowExpenseModal(false)}
            />
            <div className="modal">
              <div className="card modal-card">
                <div className="modal-header">
                  <h3 className="advisor-title mb-0">
                    Add New Expense
                  </h3>
                  <button
                    onClick={() => setShowExpenseModal(false)}
                    className="close-button"
                  >
                    ×
                  </button>
                </div>

                <form onSubmit={addExpense}>
                  <div className="form-group">
                    <label className="form-label">Amount (₹)</label>
                    <input
                      type="number"
                      step="0.01"
                      required
                      value={expenseForm.amount}
                      onChange={(e) =>
                        setExpenseForm({ ...expenseForm, amount: e.target.value })
                      }
                      className="form-input"
                      placeholder="0.00"
                    />
                  </div>

                  <div className="form-group">
                    <label className="form-label">Merchant Name</label>
                    <input
                      type="text"
                      required
                      value={expenseForm.merchant_name}
                      onChange={(e) =>
                        setExpenseForm({ ...expenseForm, merchant_name: e.target.value })
                      }
                      className="form-input"
                      placeholder="e.g., Starbucks, Amazon"
                    />
                  </div>

                  <div className="form-row">
                    <div className="form-group">
                      <label className="form-label">Category</label>
                      <select
                        value={expenseForm.category}
                        onChange={(e) =>
                          setExpenseForm({ ...expenseForm, category: e.target.value })
                        }
                        className="form-input"
                      >
                        <option value="Food">Food</option>
                        <option value="Transport">Transport</option>
                        <option value="Shopping">Shopping</option>
                        <option value="Entertainment">Entertainment</option>
                        <option value="Bills">Bills</option>
                        <option value="Healthcare">Healthcare</option>
                        <option value="Other">Other</option>
                      </select>
                    </div>

                    <div className="form-group">
                      <label className="form-label">Payment Mode</label>
                      <select
                        value={expenseForm.payment_mode}
                        onChange={(e) =>
                          setExpenseForm({ ...expenseForm, payment_mode: e.target.value })
                        }
                        className="form-input"
                      >
                        <option value="Card">Card</option>
                        <option value="Cash">Cash</option>
                        <option value="UPI">UPI</option>
                        <option value="Net Banking">Net Banking</option>
                      </select>
                    </div>
                  </div>

                  <div className="form-group">
                    <label className="form-label">Date</label>
                    <input
                      type="date"
                      required
                      value={expenseForm.transaction_date}
                      onChange={(e) =>
                        setExpenseForm({ ...expenseForm, transaction_date: e.target.value })
                      }
                      className="form-input"
                    />
                  </div>

                  <div className="form-actions">
                    <button type="submit" className="submit-button">
                      Add Expense
                    </button>
                    <button
                      type="button"
                      onClick={() => setShowExpenseModal(false)}
                      className="cancel-button"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default App;