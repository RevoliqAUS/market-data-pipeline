import { useEffect, useMemo, useState } from "react";
import { loadDashboardData } from "./api";
import { sampleDashboardData } from "./sampleData";
import type { DashboardData, SignalRow } from "./types";

function formatDate(value: string): string {
  if (!value || value === "unknown") return "unknown";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleString();
}

function formatCurrency(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2
  }).format(value);
}

function signalClass(signal: string): string {
  return `signal-pill ${signal.toLowerCase()}`;
}

function KpiCard({ label, value, hint }: { label: string; value: string | number; hint: string }) {
  return (
    <section className="kpi-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{hint}</small>
    </section>
  );
}

function DistributionChart({ signals }: { signals: SignalRow[] }) {
  const counts = ["bullish", "neutral", "bearish"].map((signal) => ({
    signal,
    count: signals.filter((row) => row.signal === signal).length
  }));
  const total = Math.max(signals.length, 1);
  return (
    <section className="panel chart-panel">
      <div className="panel-heading">
        <h2>Signal Distribution</h2>
        <span>{signals.length} tickers</span>
      </div>
      <div className="distribution">
        {counts.map((item) => (
          <div className="bar-row" key={item.signal}>
            <span>{item.signal}</span>
            <div className="bar-track">
              <div className={`bar-fill ${item.signal}`} style={{ width: `${(item.count / total) * 100}%` }} />
            </div>
            <strong>{item.count}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function MomentumChart({ signals }: { signals: SignalRow[] }) {
  const ranked = [...signals].sort((a, b) => b.signal_score - a.signal_score).slice(0, 6);
  const maxAbsScore = Math.max(...ranked.map((row) => Math.abs(row.signal_score)), 1);
  return (
    <section className="panel chart-panel">
      <div className="panel-heading">
        <h2>Momentum Ranking</h2>
        <span>signal score</span>
      </div>
      <div className="momentum-list">
        {ranked.map((row) => (
          <div className="momentum-row" key={row.ticker}>
            <span>{row.ticker}</span>
            <div className="score-track">
              <div
                className={row.signal_score >= 0 ? "score-fill positive" : "score-fill negative"}
                style={{ width: `${(Math.abs(row.signal_score) / maxAbsScore) * 100}%` }}
              />
            </div>
            <strong>{row.signal_score}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}

function SignalTable({ signals }: { signals: SignalRow[] }) {
  return (
    <section className="panel table-panel">
      <div className="panel-heading">
        <h2>Signal Ranking</h2>
        <span>latest snapshot</span>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Latest Price</th>
              <th>Signal</th>
              <th>Momentum Score</th>
              <th>Volatility Score</th>
              <th>Updated</th>
            </tr>
          </thead>
          <tbody>
            {signals.map((row) => (
              <tr key={row.ticker}>
                <td className="ticker">{row.ticker}</td>
                <td>{formatCurrency(row.close)}</td>
                <td>
                  <span className={signalClass(row.signal)}>{row.signal}</span>
                </td>
                <td>{row.signal_score}</td>
                <td>{row.volatility_20d === null ? "n/a" : `${(row.volatility_20d * 100).toFixed(1)}%`}</td>
                <td>{formatDate(row.generated_at ?? row.date)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default function App() {
  const [data, setData] = useState<DashboardData>(sampleDashboardData);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData()
      .then(setData)
      .finally(() => setIsLoading(false));
  }, []);

  const summary = useMemo(() => {
    const bullish = data.signals.filter((row) => row.signal === "bullish").length;
    const bearish = data.signals.filter((row) => row.signal === "bearish").length;
    const neutral = data.signals.filter((row) => row.signal === "neutral").length;
    return { bullish, bearish, neutral };
  }, [data.signals]);

  return (
    <main className="dashboard-shell">
      <header className="hero">
        <div>
          <p className="eyebrow">Market Intelligence Dashboard</p>
          <h1>AI-Powered Market Data Pipeline</h1>
          <p className="hero-copy">
            FastAPI-backed demo interface for DuckDB signal analytics, market rankings, and AI-assisted commentary.
          </p>
        </div>
        <div className="status-card">
          <span>Demo status</span>
          <strong>{isLoading ? "Loading" : data.source}</strong>
          <small>{data.databaseStatus}</small>
        </div>
      </header>

      <section className="kpi-grid">
        <KpiCard label="Tracked Tickers" value={data.signals.length} hint="configured watchlist snapshot" />
        <KpiCard label="Latest Run" value={formatDate(data.latestRunTime)} hint="pipeline generated_at" />
        <KpiCard label="Bullish / Neutral / Bearish" value={`${summary.bullish} / ${summary.neutral} / ${summary.bearish}`} hint="latest signals" />
        <KpiCard label="Database Status" value={data.databaseStatus} hint="FastAPI health + fallback mode" />
      </section>

      <section className="content-grid">
        <DistributionChart signals={data.signals} />
        <MomentumChart signals={data.signals} />
      </section>

      <SignalTable signals={data.signals} />

      <section className="panel insight-panel">
        <div className="panel-heading">
          <h2>AI Insight Panel</h2>
          <span>optional layer</span>
        </div>
        <p>{data.aiSummary}</p>
        <p className="muted">
          AI summaries are generated by the backend report pipeline when an OpenAI key is configured. Use <code>--no-ai</code> to run deterministic analytics only.
        </p>
      </section>
    </main>
  );
}

