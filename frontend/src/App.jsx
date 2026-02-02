import { useState } from "react";

const API_BASE = "https://ai-business-decision-engine.onrender.com";

export default function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const runDecision = async () => {
    setLoading(true);
    setError(null);

    try {
      const res = await fetch(
        `${API_BASE}/api/decision/marketing-spend`,
        { method: "POST" }
      );

      if (!res.ok) {
        throw new Error("Backend error");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Failed to run decision engine");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>AI Business Decision Engine</h1>
      <p className="subtitle">
        Turn business data into actionable decisions.
      </p>

      <button onClick={runDecision} disabled={loading}>
        {loading ? "Running decision..." : "Run Decision"}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="card">
          <h2>
            Recommendation:{" "}
            <span className="highlight">
              {result.recommendation}
            </span>
          </h2>

          <p><strong>Confidence:</strong> {result.confidence}</p>

          <h3>Explanation</h3>
          <pre className="explanation">{result.explanation}</pre>

          <h3>Key Metrics</h3>
          <ul>
            <li>Revenue Trend: {result.metrics.revenue_trend}</li>
            <li>CAC: {result.metrics.cac}</li>
            <li>Burn Rate: {result.metrics.burn_rate}</li>
            <li>Runway: {result.metrics.runway_months}</li>
          </ul>

          <h3>Scenarios</h3>
          <table>
            <thead>
              <tr>
                <th>Spend Change</th>
                <th>Revenue</th>
                <th>Customers</th>
                <th>Burn</th>
                <th>Runway</th>
              </tr>
            </thead>
            <tbody>
              {result.scenarios.map((s, i) => (
                <tr key={i}>
                  <td>{s.change_percent}%</td>
                  <td>{s.expected_revenue}</td>
                  <td>{s.expected_customers}</td>
                  <td>{s.burn_rate}</td>
                  <td>{s.runway_months}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
