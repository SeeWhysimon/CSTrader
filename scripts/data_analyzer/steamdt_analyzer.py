import json
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score 

def create_dataframe_from_json(json_path: str):
    # 读取json文件
    # Read json file
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to read existing saved data: {e}")
        return None
    
    # 创建DataFrame
    # Create DataFrame
    cols = ["timestamp", "open", "close", "high", "low", "volume", "turnover"]
    data = raw_data["data"]
    df = pd.DataFrame(data, columns=cols)
    
    # 数据处理
    # Data process
    df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit='s')
    df["ma7"] = df["close"].rolling(window=7).mean()
    df["ma14"] = df["close"].rolling(window=14).mean()
    df["ma21"] = df["close"].rolling(window=21).mean()
    df["ma42"] = df["close"].rolling(window=42).mean()
    df["next_close"] = df["close"].shift(-1)
    df.dropna(inplace=True)

    features  = ["open", "close", "high", "low", "volume", "turnover",
                 "ma7", "ma14", "ma21", "ma42"]
    # [ALERT] 需要完善 (多个特征)
    target = ["next_close"]
    
    return df, features, target

class MachineLearningModel():
    def __init__(self, steps: int=7):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.steps = steps
        self.X = None
        self.y = None

    def run(self, data_path: str):
        # 数据准备
        # Data preparation
        df, features, target = create_dataframe_from_json(json_path=data_path)
        X = df[features]
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

        # 模型训练
        # Train
        self.model.fit(X_train, y_train)

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

        for _ in range(self.steps):
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
        future_times = [last_time + pd.Timedelta(days=i+1) for i in range(self.steps)]

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