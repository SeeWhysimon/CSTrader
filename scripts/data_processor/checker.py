import pandas as pd

from statsmodels.tsa.stattools import adfuller

def check_stationary(series: pd.Series, max_diff: int = 3, threshold: float = 0.05, verbose=False):
    current_series = series.copy()

    for d in range(max_diff + 1):
        series_clean = current_series.dropna()
        adf_result = adfuller(series_clean)
        p_value = adf_result[1]

        if verbose:
            print(f"[RESULT] Diff {d}: ADF Statistic = {adf_result[0]:.4f}, p-value = {p_value:.4g}")

        if p_value < threshold:
            print(f"[RESULT] Stationary at diff = {d}")
            return d

        if d < max_diff:
            current_series = current_series.diff()
        else:
            print("[ERROR] Still non-stationary after max_diff.")
            return -1