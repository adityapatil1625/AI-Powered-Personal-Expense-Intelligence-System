import { useEffect, useState } from "react";
import axios from "axios";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
} from "recharts";

interface Insights {
  total_spent: number;
  highest_spending_category: string;
  average_daily_spend: number;
  category_breakdown: Record<string, number>;
  warning?: string;
}

function App() {
  const USER_ID =
    "550e8400-e29b-41d4-a716-446655440000";

  const [insights, setInsights] =
    useState<Insights | null>(null);

  const [form, setForm] = useState({
    amount: "",
    merchant_name: "",
    category: "",
    payment_mode: "UPI",
  });

  // ✅ Fetch insights
  const fetchInsights = () => {
    axios
      .get(`http://127.0.0.1:8000/insights/${USER_ID}`)
      .then((res) => setInsights(res.data))
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchInsights();
  }, []);

  // ✅ Add transaction
  const addTransaction = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:8000/transactions",
        {
          user_id: USER_ID,
          amount: Number(form.amount),
          transaction_date: new Date()
            .toISOString()
            .split("T")[0],
          merchant_name: form.merchant_name,
          category: form.category,
          payment_mode: form.payment_mode,
        }
      );

      // reset form
      setForm({
        amount: "",
        merchant_name: "",
        category: "",
        payment_mode: "UPI",
      });

      fetchInsights();
    } catch (error) {
      console.log(error);
    }
  };

  if (!insights) return <h2>Loading...</h2>;

  const chartData = Object.entries(
    insights.category_breakdown
  ).map(([category, amount]) => ({
    name: category,
    value: amount,
  }));

  return (
    <div style={{ padding: "40px" }}>
      <h1>💰 Expense Intelligence Dashboard</h1>

      {/* ================= FORM ================= */}
      <h2>Add Expense</h2>

      <input
        placeholder="Amount"
        value={form.amount}
        onChange={(e) =>
          setForm({
            ...form,
            amount: e.target.value,
          })
        }
      />

      <br /><br />

      <input
        placeholder="Merchant"
        value={form.merchant_name}
        onChange={(e) =>
          setForm({
            ...form,
            merchant_name: e.target.value,
          })
        }
      />

      <br /><br />


      <br /><br />

      <button onClick={addTransaction}>
        Add Transaction
      </button>

      {/* ================= INSIGHTS ================= */}
      <hr />
      <h3>
Predicted Monthly Spend:
₹{insights.predicted_monthly_spend}
</h3>

      <h2>Total Spent: ₹{insights.total_spent}</h2>
      <h3>
        Top Category:{" "}
        {insights.highest_spending_category}
      </h3>
      <h4>
        Avg Daily Spend: ₹
        {insights.average_daily_spend}
      </h4>

      {insights.warning && (
        <h3 style={{ color: "red" }}>
          ⚠ {insights.warning}
        </h3>
      )}

      {/* ================= CHART ================= */}
      <PieChart width={400} height={400}>
        <Pie
          data={chartData}
          dataKey="value"
          nameKey="name"
          outerRadius={150}
          label
        >
          {chartData.map((_, index) => (
            <Cell key={index} />
          ))}
        </Pie>

        <Tooltip />
        <Legend />
      </PieChart>
    </div>
  );
}

export default App;