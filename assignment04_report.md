# Assignment 04 Interpretation Memo

**Student Name:** [Your Name]
**Date:** [Submission Date]
**Assignment:** REIT Annual Returns and Predictors (Simple Linear Regression)

---

## 1. Regression Overview

You estimated **three** simple OLS regressions of REIT *annual* returns on different predictors:

| Model | Y Variable | X Variable | Interpretation Focus |
|-------|------------|------------|----------------------|
| 1 | ret (annual) | div12m_me | Dividend yield |
| 2 | ret (annual) | prime_rate | Interest rate sensitivity |
| 3 | ret (annual) | ffo_at_reit | FFO to assets (fundamental performance) |

For each model, summarize the key results in the sections below.

---

## 2. Coefficient Comparison (All Three Regressions)

**Model 1: ret ~ div12m_me**
- Intercept (β₀): 0.1082 (SE: 0.0060, p < 0.001)
- Slope (β₁): -0.0687 (SE: 0.0320, p = 0.035)
- R²: 0.002 | N: 2527

**Model 2: ret ~ prime_rate**
- Intercept (β₀): 0.2506 (SE: 0.0160, p < 0.001)
- Slope (β₁): -0.0304 (SE: 0.0031, p < 0.001)
- R²: 0.037 | N: 2527

**Model 3: ret ~ ffo_at_reit**
- Intercept (β₀): 0.0973 (SE: 0.0092, p < 0.001)
- Slope (β₁): 0.5770 (SE: 0.5670, p = 0.309)
- R²: ~0.000 | N: 2518

*Note: Model 3 uses slightly fewer observations because `ffo_at_reit` has some missing values.*

---

## 3. Slope Interpretation (Economic Units)

**Dividend Yield (div12m_me):**
- Estimated slope = -0.0687. Since `div12m_me` is reported in decimal form, a 1 percentage point increase in dividend yield (Δ = 0.01) implies an expected change in annual return of -0.000687 — i.e. about -0.0687 percentage points. Economically this effect is very small.

**Prime Loan Rate (prime_rate):**
- Estimated slope = -0.0304. A 1 percentage point (1.0) increase in the year‑end prime rate is associated with a -0.0304 change in annual return (≈ -3.04 percentage points). This is economically meaningful and negative, consistent with higher rates compressing REIT returns.

**FFO to Assets (ffo_at_reit):**
- Estimated slope = 0.5770. FFO/Assets is typically a small fraction, so a 0.01 increase in `ffo_at_reit` implies ≈ +0.00577 (≈ +0.577 percentage points) in annual return — but see statistical significance below.
---

## 4. Statistical Significance

For each slope, at the 5% significance level:
- **div12m_me:** Significant (p = 0.035) — slope is negative but explains almost no variance (very small economic effect).
- **prime_rate:** Significant (p < 0.001) — negative slope with the strongest statistical evidence among the three predictors.
- **ffo_at_reit:** Not significant (p = 0.309) — cannot reject no relationship in this simple regression.

**Which predictor has the strongest statistical evidence of a relationship with annual returns?** prime_rate (largest t‑stat and smallest p‑value).
---

## 5. Model Fit (R-squared)

Compare R² across the three models:
- `prime_rate` has the highest R² (≈ 0.037), but even that explains only ~3.7% of cross‑sectional variation in annual returns.
- `div12m_me` and `ffo_at_reit` have effectively zero explanatory power (R² ≈ 0.002 and ~0.000 respectively).
- Overall R² values are very low → most of the variation in REIT annual returns is not explained by these single predictors. This suggests important omitted factors (market returns, firm characteristics, sector effects, momentum, etc.).
---

## 6. Omitted Variables

By using only one predictor at a time, we may be omitting important covariates such as:
- Market return or CAPM beta: overall market performance strongly affects firm returns and may correlate with dividend yield or FFO.
- Firm size / leverage / sector: these firm characteristics can drive returns and be correlated with the predictors.
- Momentum or recent returns: past performance often predicts cross‑sectional returns.

**Potential bias:** If an omitted variable is correlated with both the predictor and `ret`, the OLS slope will be biased. For example, if larger REITs both pay higher dividends and systematically earn different returns, the `div12m_me` slope may confound size effects with dividend yield effects.
---

## 7. Summary and Next Steps

**Key Takeaway:**
- Prime rate shows the most consistent and statistically significant relationship with REIT annual returns (negative slope). Dividend yield shows a statistically significant but economically tiny (and practically unimportant) negative relationship. FFO/Assets is not statistically significant in the simple cross‑sectional regressions.

**What we would do next:**
- Estimate multivariate regressions (include market return, size, leverage, and sector fixed effects).
- Run diagnostic tests (heteroskedasticity, influential observations) and consider robust standard errors.
- Explore interactions and time‑variation (split sample by period or sector).

---

## Reproducibility Checklist
- [x] Script runs end-to-end without errors (pytest: 10 passed)
- [x] Regression output saved to `Results/regression_div12m_me.txt`, `regression_prime_rate.txt`, `regression_ffo_at_reit.txt`
- [x] Scatter plots saved to `Results/scatter_div12m_me.png`, `scatter_prime_rate.png`, `scatter_ffo_at_reit.png`
- [x] Report accurately reflects regression results (values taken from `Results/`)
- [x] All interpretations are expressed in economic units where helpful
