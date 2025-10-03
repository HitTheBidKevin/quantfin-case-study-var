# QuantFin – Case Study: VaR

**Portfolio Historical Value at Risk (VaR) Calculator**

---

## Overview

This interactive Python project allows users to download and analyze historical price data for multi-asset portfolios, calculate Value at Risk (VaR), and visualize risk both as a percentage and in portfolio monetary terms. The project features both rolling calendar-aligned window analysis and full-period VaR calculations, robust input checking, and clear data completeness enforcement.

- **Rolling VaR Analysis**: Calculate VaR for moving calendar windows (e.g., rolling 2-year windows) for multiple confidence levels.
- **Full-Period VaR**: Calculate VaR for the entire dataset at once.
- **Custom Portfolio Weights**: Specify asset weights interactively.
- **Dual Y-Axis Visualization**: View risk in percent and absolute (portfolio currency) terms.
- **Clean, modular code**: Project is organized for extensibility, with clear code separation.

---

## Features

- Interactive command-line input for tickers, weights, rolling window, and analysis mode.
- Data completeness validation for robust finance analytics (no dropped assets).
- Rolling and/or whole-period analysis with matplotlib plots.
- Professional code documentation (module and function docstrings).
- Modular structure (`src/` folder, helper modules, tests folder prepared).

---

## Installation & Requirements

1. Clone this repository:
    ```
    git clone <repo-url>
    cd QuantFin-Case-Study-VaR
    ```
2. Install dependencies (recommended via Poetry):
    ```
    poetry install
    # or
    pip install -r requirements.txt
    ```
3. Confirm you have Python 3.8+ and the following packages:
    - numpy, pandas, matplotlib, yfinance

---

## Usage

From the root project folder:
python main.py

Follow the prompt instructions:
- Enter the asset tickers you wish to analyze (e.g. SPY,GLD,IBIT,GCC)
- Define portfolio weights (MUST sum to 1)
- Choose lookback period (e.g. 10y)
- Choose rolling window or full-period mode
- View printed output and risk plots

---

## File Structure

├── main.py
├── src/
│ ├── data_loader.py
│ ├── risk_metrics.py
│ └── init.py
├── tests/
│ └── (test files, optional)
├── blanknotebook.ipynb
├── pyproject.toml (if using Poetry)
└── README.md

---

## Author & Attribution

- **Author:**: Kevin Wollbach
- **Released:**: 2025/10/03
- **AI-Assisted:**: Created with the assistance of artificial intelligence tools.

---

## License

---

## Acknowledgements

- [yfinance](https://github.com/ranaroussi/yfinance)
- Python community and open-source contributors

---
