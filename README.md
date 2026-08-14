# Market-Making & Quantitative Betting Simulator

A modular Python framework built from scratch to simulate quantitative trading strategies, market-making dynamics, optimal stopping problems, and probabilistic decision-making under uncertainty. 

Originally developed as part of an algorithmic trading and market-making challenge on Deep-ML, this project implements core components of automated market makers (AMMs), limit-order books, risk management (inventory skew and adverse selection), and dynamic belief updating.

---

## Key Modules & Architecture

The simulator is broken down into 14 progressive steps, moving from fundamental expected-value calculations to a full multi-round market-making execution engine:

1. **Expected Value & Probability Engine (`expected_value`)**: Core utility calculating dot-product expectations over discrete outcome distributions.
2. **Optimal Stopping / Die Games (`one_reroll_die_value`, `pay_per_reroll_die_game`)**: Implements threshold-based stopping policies and recursive value iterations for optional-reroll mechanics.
3. **Card-Game Dynamic Programming (`red_black_card_game_value`, `update_remaining_card_value`)**: Dynamic programming tables and state-space updates for colored-card draw games and real-time belief adjustments.
4. **Quoting Engine (`make_quotes`, `uncertainty_spread`, `inventory_skewed_quotes`)**: 
   * Generates symmetric bid/ask spreads around fair value.
   * Dynamically widens spreads based on parameter uncertainty to protect against **adverse selection**.
   * Skews quotes symmetrically to discourage further accumulation when carrying directional inventory risk.
5. **Trade Execution & Inventory Management (`execute_trade`, `update_fair_value_from_trade`)**: Simulates fills against counterparty flow (`buy`/`sell`), updates cash and inventory positions, and adjusts fair-value beliefs based on order flow toxicity.
6. **Risk & Performance Analytics (`mark_to_market_pnl`, `run_market_making_episode`, `summarize_episode_pnls`)**:
   * Evaluates mark-to-market P&L upon final settlement.
   * Runs multi-round episode simulations logging complete audit trails.
   * Summarizes performance metrics across large batches of runs (mean, population standard deviation `ddof=0`, and worst-case drawdowns).

---

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.8+
* NumPy

### Running the Simulator
Execute the test scaffold to verify all modules and edge cases:

```bash
python scaffold.py
