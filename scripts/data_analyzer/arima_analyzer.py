import pandas as pd

from statsmodels.tsa.arima.model import ARIMA

from scripts.data_processor.checker import check_stationary

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt

def plot_acf_pacf(series, lags=20):
    fig, ax = plt.subplots(2, 1, figsize=(10, 8))
    plot_pacf(series, lags=lags, ax=ax[0])
    ax[0].set_title('PACF Plot')
    plot_acf(series, lags=lags, ax=ax[1])
    ax[1].set_title('ACF Plot')
    plt.tight_layout()
    plt.show()


class ARIMAModel():
    def __init__(self):
        pass

    def run(self, df: pd.DataFrame, target: str, steps: int = 7, verbose=False):
        series = df[target].dropna()
        d = check_stationary(series=series)

        plot_acf_pacf(series=series, lags=50)

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

