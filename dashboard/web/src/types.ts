export type SignalLabel = "bullish" | "neutral" | "bearish";

export type SignalRow = {
  ticker: string;
  date: string;
  signal: SignalLabel | string;
  signal_score: number;
  trend_alignment: string;
  volume_price_state: string;
  cost_health: string;
  volatility_20d: number | null;
  close: number;
  change_pct: number;
  generated_at?: string;
};

export type DashboardData = {
  source: "live API" | "sample data";
  databaseStatus: "online" | "sample fallback" | "unavailable";
  latestRunTime: string;
  aiSummary: string;
  signals: SignalRow[];
};

