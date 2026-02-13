# AI Audit Appendix (Assignment 04)

## Tool(s) Used
- GitHub Copilot (assistant)
- Model: Raptor mini (Preview)

## Task(s) Where AI Was Used
- Implemented missing code in `assignment04_regression.py` (`estimate_regression`, `save_regression_summary`, `plot_scatter_with_regression`, `print_key_results`).
- Enhanced plotting to include 95% confidence bands and residual diagnostics.
- Drafted and populated `assignment04_report.md` using regression outputs.
- Drafted this AI Audit Appendix and updated repository files.
- Created a feature branch and opened a pull request (automated commit & push).

## Prompt(s)
- "Implement the TODOs in `assignment04_regression.py` so the script runs and saves regression summaries and scatter plots."
- "Add 95% confidence bands and a residuals subplot to `plot_scatter_with_regression`."
- "Fill `assignment04_report.md` with numeric regression results from `Results/` and provide concise interpretation and next steps."

## Output Summary
- Code changes to implement OLS estimation, summary saving, and plotting with CI/residuals.
- Updated `assignment04_report.md` with numeric results and interpretation.
- Created/updated `Results/` files (regression summaries + scatter plots) and verified tests pass.

## Verification & Modifications (Disclose • Verify • Critique)
- **Verify:** Ran the full test suite (`pytest`) — all tests pass (10/10). Inspected `Results/` regression summaries and plots.
- **Critique:** Initial implementation used a synthetic `interest_rates_monthly.csv`. I added functionality and documentation; real FRED data will replace the synthetic CSV when `fetch_interest_rates.py` is run with a valid `FRED_API_KEY`.
- **Modify:** Adjusted code for clearer plotting (CI + residuals), populated the report with current regression output, and added reproducibility notes. Final verification should be done after fetching real FRED data (see instructions in README).

**Transparency statement:** AI assistance was used to implement code and draft report text. All outputs were validated by running the script and the test suite; where appropriate I edited or corrected generated content to ensure accuracy.

