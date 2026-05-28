import type { DashboardData } from "./types";

export const sampleDashboardData: DashboardData = {
  source: "sample data",
  databaseStatus: "sample fallback",
  latestRunTime: "2026-05-28T22:31:04Z",
  aiSummary:
    "Sample AI insight: leadership remains concentrated in mega-cap technology, with momentum strongest in semiconductor names. Neutral signals suggest the pipeline is waiting for broader confirmation from volume and volatility before upgrading the overall market regime. AI summaries can be disabled by running the backend pipeline with --no-ai.",
  signals: [
    {
      ticker: "NVDA",
      date: "2026-05-28",
      signal: "bullish",
      signal_score: 2,
      trend_alignment: "bullish stack",
      volume_price_state: "high-volume advance",
      cost_health: "majority profitable, trend intact",
      volatility_20d: 0.421,
      close: 128.5,
      change_pct: 1.84,
      generated_at: "2026-05-28T22:31:04Z"
    },
    {
      ticker: "MSFT",
      date: "2026-05-28",
      signal: "neutral",
      signal_score: 1,
      trend_alignment: "mixed",
      volume_price_state: "range-bound",
      cost_health: "mixed positioning",
      volatility_20d: 0.238,
      close: 460.12,
      change_pct: 0.22,
      generated_at: "2026-05-28T22:31:04Z"
    },
    {
      ticker: "AAPL",
      date: "2026-05-28",
      signal: "neutral",
      signal_score: 0,
      trend_alignment: "mixed",
      volume_price_state: "low-volume decline",
      cost_health: "mixed positioning",
      volatility_20d: 0.284,
      close: 199.75,
      change_pct: -0.41,
      generated_at: "2026-05-28T22:31:04Z"
    },
    {
      ticker: "TSLA",
      date: "2026-05-28",
      signal: "bearish",
      signal_score: -2,
      trend_alignment: "bearish stack",
      volume_price_state: "high-volume decline",
      cost_health: "elevated profit-taking risk",
      volatility_20d: 0.648,
      close: 321.44,
      change_pct: -2.18,
      generated_at: "2026-05-28T22:31:04Z"
    }
  ]
};

