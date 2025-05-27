import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

from scripts.data_processor.checker import check_stationary

class ARIMAModel():
    def __init__(self):
        pass

    def run(self, df: pd.DataFrame, target: str, steps: int = 7, verbose=False):
        series = df[target].dropna()
        d = check_stationary(series=series)

        order = (1, d, 1)
        model = ARIMA(series, order=order)

        model_fit = model.fit()
        # 模型摘要
        if verbose:
            print(model_fit.summary())
        # 预测未来 N 步
        forecast = model_fit.forecast(steps=steps)
        print("[RESULT] Forecast")
        print(forecast)

