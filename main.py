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
    portfolio_returns = (returns * weights).sum(axis=1)
    confidence_levels = [0.90, 0.95, 0.99]
    weights_percent = [f"{tickers[i]} {weights[i]*100:.1f}%" for i in range(len(tickers))]
    portfolio_str = ", ".join(weights_percent)

    if method == 'R':
        window_years = int(input("Enter rolling window in years (e.g., 2): "))
        years_series = pd.Series(portfolio_returns.index.year, index=portfolio_returns.index)
        min_year, max_year = years_series.min(), years_series.max()
        results = {cl: [] for cl in confidence_levels}
        window_end_labels = []

        for start_year in range(min_year, max_year - window_years + 2):
            start_date = pd.Timestamp(f"{start_year}-01-01")
            end_year = start_year + window_years - 1
            if end_year < max_year:
                end_date = pd.Timestamp(f"{end_year}-12-31")
                if end_date not in portfolio_returns.index:
                    mask = portfolio_returns.index.year == end_year
                    if not mask.any():
                        continue
                    end_date = portfolio_returns.index[mask][-1]
            else:
                end_date = portfolio_returns.index[-1]

            window_data = portfolio_returns[(portfolio_returns.index >= start_date) & (portfolio_returns.index <= end_date)]
            if len(window_data) < 30:
                continue

            window_end_labels.append(str(end_date.date()))
            for cl in confidence_levels:
                var = -np.percentile(window_data, (1 - cl) * 100)
                results[cl].append(var)

        print("\nCalendar-Aligned Rolling VaR:")
        for i, end_str in enumerate(window_end_labels):
            print(f"{end_str}: " + ", ".join([f"VaR {int(cl*100)}% = {results[cl][i]*100:.2f}%" for cl in confidence_levels]))

        plt.figure(figsize=(12, 6))
        ax1 = plt.gca()
        ax2 = ax1.twinx()

        for cl in confidence_levels:
            var_pct = [v * 100 for v in results[cl]]
            var_pnl = [v * portfolio_value for v in results[cl]]
            ax1.plot(window_end_labels, var_pct, marker='o', label=f'VaR {int(cl*100)}%')
            ax2.plot(window_end_labels, var_pnl, marker='x', linestyle='--', label=f'PnL VaR {int(cl*100)}%')

            # Annotate PnL VaR near each point
            for x, y in zip(window_end_labels, var_pnl):
                ax2.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(0,5),
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
        print("\nWhole period VaR:")
        for cl in confidence_levels:
            var = -np.percentile(portfolio_returns, (1 - cl) * 100)
            pnl = var * portfolio_value
            print(f"VaR {int(cl*100)}%: {var*100:.2f}%, Portfolio PnL: {pnl:.2f}")

        plt.figure(figsize=(8, 6))
        bars = plt.bar([f"VaR {int(c*100)}%" for c in confidence_levels],
                       [v*100 for v in [ -np.percentile(portfolio_returns, (1 - c) * 100) for c in confidence_levels ]])
        plt.ylabel("VaR (%)")
        plt.title(f"Full Period VaR - Portfolio: {portfolio_str}")

        # Plot PnL VaR values on top of bars
        for bar, cl in zip(bars, confidence_levels):
            height = bar.get_height()
            pnl = -np.percentile(portfolio_returns, (1 - cl) * 100) * portfolio_value
            plt.annotate(f"{pnl:.2f}",
                         xy=(bar.get_x() + bar.get_width() / 2, height),
                         xytext=(0, 3),
                         textcoords="offset points",
                         ha='center', va='bottom', fontsize=8, color='black')

        plt.show()
    else:
        print("Invalid selection.")

if __name__ == "__main__":
    main()
