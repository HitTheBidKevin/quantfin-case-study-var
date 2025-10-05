"""
Portfolio Historical VaR Analysis Script

This script allows interactive calculation of Value at Risk (VaR) for a weighted multi-asset portfolio using historical (non-parametric) methodology.
Features:
- Download asset prices via yfinance for user-specified tickers and user-supplied weights.
- Enforces complete portfolio data for the selected lookback period (no interpolation or gaps).
- Offers both rolling window (calendar-aligned, e.g. 2y, shifted yearly, last window up to today) and full-period VaR options.
- Computes and reports VaR at 90%, 95%, and 99% confidence levels.
- Presents VaR results graphically (plot) and in console output, with all asset tickers and weights in title.

Intended for interactive use in educational, prototyping, or finance study contexts.

***************************************************
This project was created with the assistance of artificial intelligence tools.
***************************************************

Run as: python main.py

Author: Kevin Wollbach
Date: 2025/10/03
"""

from src.data_loader import download_prices
from src.risk_metrics import calculate_historical_var, rolling_historical_var
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    tickers_input = input("Enter ticker symbols separated by commas (e.g. SPY,AGG): ")
    tickers = [t.strip() for t in tickers_input.split(',')]
    period = input("Enter total lookback period (e.g. 10y): ")
    portfolio_value = float(input("Enter your portfolio value (e.g. 100000): "))

    weights_input = input(f"Enter portfolio weights for {', '.join(tickers)} separated by commas (must sum to 1): ")
    weights = [float(w.strip()) for w in weights_input.split(',')]
    if not np.isclose(sum(weights), 1.0):
        print("Warning: weights do not sum to 1. Normalizing.")
        total = sum(weights)
        weights = [w/total for w in weights]

    method = input("Calculate VaR as Rolling Window or Whole Period? (R/W): ").strip().upper()

    prices = download_prices(tickers, period)
    print("Downloaded prices shape:", prices.shape)

    if prices.isnull().any().any():
        missing_mask = prices.isnull().any()
        missing_tickers = [col for col, missing in zip(prices.columns, missing_mask) if missing]
        print(f"Error: The following tickers have missing data: {', '.join(missing_tickers)}")
        print("Exiting.")
        return

    returns = prices.pct_change().dropna()

    confidence_levels = [0.90, 0.95, 0.99]
    weights_percent = [f"{tickers[i]} {weights[i]*100:.1f}%" for i in range(len(tickers))]
    portfolio_str = ", ".join(weights_percent)

    if method == 'R':
        window_years = int(input("Enter rolling window in years (e.g., 2): "))

        rolling_vars = {}
        for cl in confidence_levels:
            rolling_vars[cl] = rolling_historical_var(returns, weights, window_years, confidence_level=cl)

        # Print results similar to original format
        print("\nCalendar-Aligned Rolling VaR:")
        for date in rolling_vars[confidence_levels[0]].index:
            print(f"{date.date()}: " + ", ".join([f"VaR {int(cl*100)}% = {rolling_vars[cl][date]*100:.2f}%" for cl in confidence_levels]))

        plt.figure(figsize=(12, 6))
        ax1 = plt.gca()
        ax2 = ax1.twinx()

        for cl in confidence_levels:
            var_pct = rolling_vars[cl] * 100
            var_pnl = rolling_vars[cl] * portfolio_value
            ax1.plot(rolling_vars[cl].index, var_pct, marker='o', label=f'VaR {int(cl*100)}%')
            ax2.plot(rolling_vars[cl].index, var_pnl, marker='x', linestyle='--', label=f'PnL VaR {int(cl*100)}%')
            for x, y, pct in zip(rolling_vars[cl].index, var_pnl, var_pct):
                # Annotate PnL VaR with % VaR next to it
                ax2.annotate(f"{y:.2f}\n({pct:.2f}%)", (x, y), textcoords="offset points", xytext=(0,5),
                             ha='center', fontsize=8, color='tab:blue')

        ax1.set_ylabel("VaR (%)")
        ax2.set_ylabel("PnL VaR (Portfolio Currency)")
        ax1.set_xlabel("Window End Date")
        ax1.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter())
        plt.title(f"Rolling {window_years}y Calendar-Aligned VaR\nPortfolio: {portfolio_str}")

        lines_1, labels_1 = ax1.get_legend_handles_labels()
        lines_2, labels_2 = ax2.get_legend_handles_labels()
        ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')
        ax1.grid(True)
        plt.show()

    elif method == 'W':
        portfolio_returns = (returns * weights).sum(axis=1)
        print("\nWhole period VaR:")
        for cl in confidence_levels:
            var = calculate_historical_var(portfolio_returns, cl)
            pnl = var * portfolio_value
            print(f"VaR {int(cl*100)}%: {var*100:.2f}%, Portfolio PnL: {pnl:.2f}")

        plt.figure(figsize=(8, 6))
        bars = plt.bar([f"VaR {int(c*100)}%" for c in confidence_levels],
                       [calculate_historical_var(portfolio_returns, c) * 100 for c in confidence_levels])
        plt.ylabel("VaR (%)")
        plt.title(f"Full Period VaR - Portfolio: {portfolio_str}")

        for bar, cl in zip(bars, confidence_levels):
            height = bar.get_height()
            pnl = calculate_historical_var(portfolio_returns, cl) * portfolio_value
            pct = calculate_historical_var(portfolio_returns, cl) * 100
            plt.annotate(f"{pnl:.2f}\n({pct:.2f}%)",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=8, color='black')

        plt.show()
    else:
        print("Invalid selection.")


if __name__ == "__main__":
    main()
