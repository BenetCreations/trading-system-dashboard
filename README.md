# Trading System Dashboard — Phase 4: Tracking & Analytics

A rule-enforcement dashboard for systematic momentum investing, built as a single standalone HTML file.

## What This Is

This is the tracking and analytics layer of a 4-phase personal investing system built around Stan Weinstein's Stage Analysis framework. Phases 1–3 define the philosophy, trade setups, and execution rules. Phase 4 is the tooling that feeds real-time data back into those rules so the system is self-correcting rather than static.

Every tool in this dashboard exists to serve a specific execution rule. Nothing is built for curiosity — every output feeds a decision.

## How It Works

One HTML file. Open it in Chrome. Your data persists in the browser's localStorage between sessions. No server, no database, no accounts, no dependencies beyond a single Chart.js CDN link.

### Tools

- **Trade Log & R-Multiple Tracker** — Records every closed trade, auto-calculates R-multiples, tracks cumulative R, win rate (overall and rolling), average gain/loss across multiple windows, and win rate breakdowns by setup type and tier
- **Adaptive Sell Threshold (Rule 4)** — Auto-calculates the sell-into-strength target as the higher of the 5-trade or 10-trade average gain on winners, with an 8% cold-start default
- **Open Position Dashboard** — Real-time view of all positions with equity risk validation, sector concentration tracking (regime-aware caps), single-name exposure limits, and earnings date alerts
- **Equity Curve & Drawdown Tracker** — Equity curve with high-water mark, drawdown status bands mapped to specific emergency override thresholds (margin elimination at 7%, hard stop at 10%), monthly P&L, and Elder's 6% monthly rule
- **Adaptive Kelly Calculator** — Half-Kelly deployment ceiling on a rolling 10-trade window, activates after 10 closed trades, hard-capped at 150%
- **Regime Tracker** — Tracks the two-regime deployment system with Kelly authority transitions (Silent → Informational → Partial → Primary → Full Control)
- **ATR Extension Monitor** — *(In development)* ATR% multiple from 21 EMA for sell-into-strength Rule 4B, with backtest calibration

### Summary Strip

A sticky header bar shows system status at a glance: equity, drawdown, cumulative R, win rate, deployment percentage, open risk, current regime, Rule 4 threshold, and active alerts.

## Architecture Decisions

- **Vanilla JavaScript + Chart.js** — No frameworks, no build chain, no transpilation. One file, zero failure points beyond a single CDN dependency
- **localStorage for persistence** — Data lives in the browser, backed up via JSON export. No server, no database, no authentication
- **Finnhub API integration** — *(Planned)* Free-tier market data for position price refresh and ATR/EMA calculations

## How This Was Built

This system was designed and built using Claude (Anthropic) as a development partner. The AI wrote the code; I designed the system architecture, defined every rule and threshold, made the technical tradeoffs (React vs. vanilla JS, spreadsheet vs. web app, artifact vs. standalone file), and directed the iterative build process.

The methodology documents (Phases 1–3) represent several hundred hours of studying momentum trading systems from Weinstein, Minervini, and others, synthesized into a unified, executable framework.

## Data Safety

- **Export**: Config panel includes full JSON backup (config + all trades + all positions) and CSV trade export
- **Restore**: JSON backup can be restored to recover all data after a browser cache clear or machine change
- **Recommendation**: Export a JSON backup after every batch of trades

## Status

- [x] Trade Log & R-Multiple Tracker
- [x] Rolling Average Gain Tracker (Rule 4 feed)
- [x] Open Position Dashboard
- [x] Equity Curve & Drawdown Tracker
- [x] Adaptive Kelly Calculator
- [x] Regime Tracker
- [ ] Finnhub API price refresh
- [ ] ATR Extension Monitor with backtest calibration
- [ ] Localhost launcher for API integration
