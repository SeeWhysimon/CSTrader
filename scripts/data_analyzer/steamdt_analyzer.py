import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score 
from sklearn.model_selection import train_test_split, GridSearchCV

from scripts.data_processor.loader import load_dataframe_from_json
from scripts.data_processor.features import add_moving_averages

class random_forest_model():
    def __init__(self):
        self.model = RandomForestRegressor()

    def find_best_params(self, X_train, y_train, param_grid=None):
        if param_grid is None:
            param_grid = {
                'n_estimators': [50, 100, 200], 
                'max_depth': [None, 10, 20], 
                'min_samples_split': [2, 5, 7], 
                'max_features': [7, 11, 13, 19]
            }

        grid_search = GridSearchCV(estimator=self.model, 
                                   param_grid=param_grid, 
                                   cv=5, 
                                   scoring="neg_mean_squared_error", 
                                   n_jobs=-1)
        grid_search.fit(X_train, y_train)

        print(f"Best parameter: {grid_search.best_params_}")
        print(f"Best score: {grid_search.best_score_}")

        return grid_search.best_params_
    
    def create_dataframe_from_json(self, json_path: str, csv_save_path: str = None):
        # 读取json文件
        # Read json file
        df = load_dataframe_from_json(json_path=json_path)

        # 数据处理
        # Data process
        df = add_moving_averages(df, [7, 14, 21, 42])
        df["next_close"] = df["close"].shift(-1)
        df.dropna(inplace=True)

        features  = ["open", "close", "high", "low", "volume", "turnover",
                    "ma7", "ma14", "ma21", "ma42"]
        # [ALERT] 需要完善 (多个特征)
        target = ["next_close"]

        if csv_save_path:
            df.to_csv(csv_save_path, index=False)
            print(f"[INFO] CSV file saved: {csv_save_path}")
        
        return df, features, target

    def run(self, data_path: str, params=None, param_grid=None, steps=7):
        # 数据准备
        # Data preparation
        df, features, target = self.create_dataframe_from_json(json_path=data_path,
                                                          csv_save_path="./data/processed/steamdt.csv")
        X = df[features]
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

        # 模型训练
        # Train
        if params:
            self.model.set_params(**params)

        best_params = self.find_best_params(X_train=X_train, y_train=y_train.values.ravel(), param_grid=param_grid)
        self.model.set_params(**best_params)
        
        self.model.fit(X_train, y_train.values.ravel())

        # 测试
        # Test
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"[RESULT] MSE: {mse} R2 Score: {r2}")

        # 预测
        # Prediction
        last_features = X.iloc[-1].copy()
        future_preds  = []

        for _ in range(steps):
            pred = self.model.predict(pd.DataFrame([last_features]))[0]
            future_preds.append(pred)

            # [ALERT] 需要完善 (利用多个特征预测多个特征)
            last_features["open"] = pred
            last_features["close"] = pred
            last_features["high"] = pred * 1.01
            last_features["low"] = pred * 0.99
            last_features["volume"] *= 0.95
            last_features["turnover"] *= 0.95
        
        last_time = df["timestamp"].iloc[-1]
        future_times = [last_time + pd.Timedelta(days=i+1) for i in range(steps)]

        # 绘图
        # Plot
        full_time = df["timestamp"].values
        test_time = full_time[len(y_train):]

        plt.figure(figsize=(12, 6))
        # 真实收盘价曲线
        plt.plot(full_time, y, '-o', label='True close price', color='blue')
        # 测试集预测曲线
        plt.plot(test_time, y_pred, '-o', label='Test prediction', color='orange')
        # 未来预测曲线
        plt.plot(future_times, future_preds, label='Prediction', color='green', linestyle='--', marker='o')

        plt.title("K line prediction")
        plt.xlabel("Time")
        plt.ylabel("Close price")
        plt.legend()
        plt.tight_layout()
        plt.grid(True)
        plt.show()


from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

from scripts.data_processor.checker import check_stationary

class arima_model():
    def __init__(self):
        pass

    def plot_acf_pacf(self, series, lags=20):
        _, ax = plt.subplots(2, 1, figsize=(10, 8))
        plot_pacf(series, lags=lags, ax=ax[0])
        ax[0].set_title('PACF Plot')
        plot_acf(series, lags=lags, ax=ax[1])
        ax[1].set_title('ACF Plot')
        plt.tight_layout()
        plt.show()

    def run(self, df: pd.DataFrame, target: str, steps: int = 7, verbose=False):
        series = df[target].dropna()
        d = check_stationary(series=series)

        self.plot_acf_pacf(series=series, lags=50)

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