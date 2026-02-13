"""
Assignment 04: Simple Linear Regression (REIT Annual Returns and Predictors)

This script estimates three simple OLS regressions of REIT annual returns on different
X variables:
- ret (annual) ~ div12m_me: dividend yield (12-month)
- ret (annual) ~ prime_rate: prime loan rate (interest rate sensitivity)
- ret (annual) ~ ffo_at_reit: FFO to assets (fundamental performance)

Data: Pre-built annual REIT dataset (REIT_sample_annual_*.csv), one observation
per REIT per year. Interest rates merged from interest_rates_monthly.csv (December values).

Learning objectives:
- Fit simple linear regressions using statsmodels
- Extract and interpret regression coefficients
- Visualize relationships with scatter plots
- Save results for the interpretation memo
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

try:
    from config_paths import DATA_DIR, RESULTS_DIR
except ImportError:
    _ROOT = Path(__file__).resolve().parent
    DATA_DIR = _ROOT / "data"
    RESULTS_DIR = _ROOT / "Results"
import numpy as np
import pandas as pd
from statsmodels.formula.api import ols

# Three regressions: (x_var, title, xlabel)
REGRESSION_SPECS = [
    ("div12m_me", "REIT Annual Return vs. Dividend Yield", "Dividend Yield (12m)"),
    ("prime_rate", "REIT Annual Return vs. Prime Loan Rate", "Prime Loan Rate (%)"),
    ("ffo_at_reit", "REIT Annual Return vs. FFO to Assets", "FFO / Assets"),
]


def _merge_annual_interest_rates(df: pd.DataFrame, data_dir: Path) -> pd.DataFrame:
    """
    Merge year-end (December) interest rates by year.
    Run fetch_interest_rates.py first to create interest_rates_monthly.csv.
    """
    rates_path = data_dir / "interest_rates_monthly.csv"
    if not rates_path.exists():
        raise FileNotFoundError(
            f"Missing {rates_path}\n"
            "Run fetch_interest_rates.py to download interest rate data."
        )
    rates = pd.read_csv(rates_path)
    rates["date"] = pd.to_datetime(rates["date"])
    rates["year"] = rates["date"].dt.year
    rates["month"] = rates["date"].dt.month
    rates_dec = rates[rates["month"] == 12][["year", "mortgage_30y", "prime_rate"]].copy()

    df = df.copy()
    if "year" not in df.columns and "date" in df.columns:
        df["year"] = pd.to_datetime(df["date"], errors="coerce").dt.year
    df = df.merge(rates_dec, on="year", how="left")
    return df


def load_reit_annual_data(data_path: Path) -> pd.DataFrame:
    """
    Load pre-built annual REIT data (REIT_sample_annual_*.csv).

    Steps:
    1. Read the CSV file.
    2. If 'year' is missing but 'date' exists, extract year from date.
    3. Rename ret12 to ret (annual return = 12-month cumulative return).
    4. Merge year-end interest rates using _merge_annual_interest_rates.
    5. Drop rows with missing ret, div12m_me, or prime_rate.

    Note: ffo_at_reit may have missing values; the third regression (ret ~ ffo_at_reit)
    will automatically drop those rows and may report a smaller N than the first two.

    Parameters
    ----------
    data_path : Path
        Path to the REIT annual CSV file.

    Returns
    -------
    pd.DataFrame
        REIT data with columns: ret, div12m_me, prime_rate, ffo_at_reit (and others)
    """
    df = pd.read_csv(data_path)

    if "year" not in df.columns and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["year"] = df["date"].dt.year

    df = df.rename(columns={"ret12": "ret"})

    df = _merge_annual_interest_rates(df, data_path.parent)

    # Drop rows with missing values required for the main regressions
    df = df.dropna(subset=["ret", "div12m_me", "prime_rate"])

    return df


def estimate_regression(df: pd.DataFrame, x_var: str):
    """
    Estimate OLS regression: ret ~ x_var

    Parameters
    ----------
    df : pd.DataFrame
        REIT data with 'ret' and x_var columns.
    x_var : str
        Name of the X variable (e.g., 'div12m_me', 'prime_rate', 'ffo_at_reit').

    Returns
    -------
    statsmodels.regression.linear_model.RegressionResultsWrapper
        Fitted regression model.
    """
    model = ols(f"ret ~ {x_var}", data=df).fit()
    return model


def save_regression_summary(model, output_path: Path) -> None:
    """
    Save the regression summary to a text file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(str(model.summary()))
        f.write("\n")


def plot_scatter_with_regression(
    df: pd.DataFrame, model, x_var: str, title: str, xlabel: str, output_path: Path
) -> None:
    """
    Create a scatter plot with the fitted regression line, 95% confidence band,
    and a residuals subplot below the main figure.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_plot = df[[x_var, "ret"]].dropna()
    if df_plot.empty:
        return

    # Prediction grid (central 2-98 percentiles)
    x_min = float(df_plot[x_var].quantile(0.02))
    x_max = float(df_plot[x_var].quantile(0.98))
    x_grid = np.linspace(x_min, x_max, 200)
    pred_df = pd.DataFrame({x_var: x_grid})

    # Get prediction with confidence intervals (uses formula API names)
    try:
        pred = model.get_prediction(pred_df)
        pred_summary = pred.summary_frame(alpha=0.05)
        y_mean = pred_summary["mean"]
        ci_lower = pred_summary["mean_ci_lower"]
        ci_upper = pred_summary["mean_ci_upper"]
    except Exception:
        # Fallback: use analytic line without CI
        intercept = float(model.params.get("Intercept", 0.0))
        slope = float(model.params.get(x_var, 0.0))
        y_mean = intercept + slope * x_grid
        ci_lower = y_mean.copy()
        ci_upper = y_mean.copy()

    # Create main + residuals subplot
    fig, (ax, ax_resid) = plt.subplots(
        2,
        1,
        figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=False,
    )

    # Scatter + fit + CI
    ax.scatter(df_plot[x_var], df_plot["ret"], alpha=0.6, label="observations")
    ax.plot(x_grid, y_mean, color="C1", linewidth=2, label="fitted line")
    ax.fill_between(x_grid, ci_lower, ci_upper, color="C1", alpha=0.2, label="95% CI")

    # Axis limits (zoom to central data)
    y_lo = float(df_plot["ret"].quantile(0.02))
    y_hi = float(df_plot["ret"].quantile(0.98))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_lo, y_hi)

    ax.set_title(f"{title} (R² = {model.rsquared:.3f})")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Annual Return")
    ax.legend()

    # Residuals vs X
    fitted_vals = model.predict(df_plot)
    resid = df_plot["ret"] - fitted_vals
    ax_resid.scatter(df_plot[x_var], resid, alpha=0.6)
    ax_resid.axhline(0, color="k", linewidth=0.8)
    r_lo = float(resid.quantile(0.02))
    r_hi = float(resid.quantile(0.98))
    ax_resid.set_xlim(x_min, x_max)
    ax_resid.set_ylim(r_lo, r_hi)
    ax_resid.set_xlabel(xlabel)
    ax_resid.set_ylabel("Residuals")

    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


def print_key_results(model, x_var: str) -> None:
    """
    Print key regression results to the console.
    """
    intercept = float(model.params.get("Intercept", np.nan))
    slope = float(model.params.get(x_var, np.nan))
    se = float(model.bse.get(x_var, np.nan))
    tstat = float(model.tvalues.get(x_var, np.nan))
    pval = float(model.pvalues.get(x_var, np.nan))
    r2 = float(model.rsquared)
    adj_r2 = float(model.rsquared_adj)
    n = int(model.nobs)

    print("\n" + "=" * 60)
    print(f"ret (annual) ~ {x_var.upper()}")
    print("=" * 60)
    print(f"Intercept (β₀): {intercept:.4f}")
    print(f"Slope (β₁)  : {slope:.4f}  (SE={se:.4f}, t={tstat:.3f}, p={pval:.3g})")
    print(f"R-squared   : {r2:.4f}   Adj R² = {adj_r2:.4f}   N = {n}")
    sig_text = "significant (p < 0.05)" if pval < 0.05 else "not significant (p ≥ 0.05)"
    direction = "positive" if slope > 0 else "negative" if slope < 0 else "zero"
    print(f"Slope is {direction} and {sig_text} at 5% level.")
    print("=" * 60 + "\n")


def _find_reit_data(data_dir: Path) -> Path:
    """Find REIT_sample_annual_*.csv in data folder (uses most recently modified)."""
    candidates = list(data_dir.glob("REIT_sample_annual_*.csv"))
    if not candidates:
        raise FileNotFoundError(
            f"No REIT_sample_annual_*.csv found in {data_dir}\n"
            "Use the pre-built annual dataset: REIT_sample_annual_2004_2024.csv"
        )
    return max(candidates, key=lambda p: p.stat().st_mtime)


def main() -> None:
    """Main execution function."""
    data_dir = DATA_DIR
    data_path = _find_reit_data(data_dir)
    results_dir = RESULTS_DIR

    print("Loading REIT annual data (REIT_sample_annual_*.csv)...")
    df = load_reit_annual_data(data_path)
    print(f"Loaded {len(df)} firm-year observations.")
    print(f"Years: {df['year'].min():.0f}–{df['year'].max():.0f}")

    for x_var, title, xlabel in REGRESSION_SPECS:
        print(f"\nEstimating regression: ret (annual) ~ {x_var}")
        model = estimate_regression(df, x_var)
        print_key_results(model, x_var)

        summary_path = results_dir / f"regression_{x_var}.txt"
        plot_path = results_dir / f"scatter_{x_var}.png"
        save_regression_summary(model, summary_path)
        print(f"Saved: {summary_path}")
        plot_scatter_with_regression(df, model, x_var, title, xlabel, plot_path)
        print(f"Saved: {plot_path}")

    print("\n✓ Assignment 04 complete!")
    print("Next steps:")
    print("  1. Review regression outputs in Results/")
    print("  2. Compare coefficients across dividend yield, prime rate, and FFO/Assets")
    print("  3. Complete assignment04_report.md with your interpretation")
    print("  4. Complete AI_AUDIT_APPENDIX.md")


if __name__ == "__main__":
    main()
