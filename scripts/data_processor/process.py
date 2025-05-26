from statsmodels.tsa.stattools import adfuller

def auto_difference_until_stationary(df, target: str, max_diff: int = 3, threshold: float = 0.05):
    df_result = df.copy()
    current_series = df_result[target]
    
    for d in range(max_diff + 1):
        series = current_series.dropna()
        adf_result = adfuller(series)

        p_value = adf_result[1]
        print(f"[RESULT] Diff {d}: ADF Statistic = {adf_result[0]:.4f}, p-value = {p_value:.4g}")

        if p_value < threshold:
            print(f"[RESULT] Stationary at diff = {d}")
            return d, df_result

        if d < max_diff:
            col_name = f"{target}_diff{d+1}"
            df_result[col_name] = current_series.diff()
            current_series = df_result[col_name]
        else:
            print("[ERROR] Still non-stationary after max_diff.")
            return 0, df
