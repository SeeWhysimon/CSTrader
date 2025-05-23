import json
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

pio.renderers.default = "browser"

class KLineAnalyzer:
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        self.df = None
        self.X_test = None
        self.y_test = None
        self.y_pred = None
        self.future_preds = []
        self.future_times = []
    
    def load_data(self, json_path: str):
        with open(json_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
        
        data = raw_data["data"]
        df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit='s')
        df["next_close"] = df["close"].shift(-1)
        df.dropna(inplace=True)
        self.df = df
    
    def train(self):
        features = ["open", "high", "low", "close", "volume", "turnover"]
        X = self.df[features]
        y = self.df["next_close"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)
        
        self.model.fit(X_train, y_train)
        self.X_test = X_test
        self.y_test = y_test
        self.y_true = y
        self.X = X
        self.y_train_len = len(y_train)
    
    def predict_future(self, steps=7):
        last_features = self.X.iloc[-1].copy()
        self.future_preds = []
        
        for _ in range(steps):
            pred = self.model.predict(pd.DataFrame([last_features]))[0]
            self.future_preds.append(pred)
            
            last_features["open"] = pred
            last_features["close"] = pred
            last_features["high"] = pred * 1.01
            last_features["low"] = pred * 0.99
            last_features["volume"] *= 0.95
            last_features["turnover"] *= 0.95
        
        last_time = self.df["timestamp"].iloc[-1]
        self.future_times = [last_time + pd.Timedelta(days=i + 1) for i in range(steps)]
    
    def predict_test(self):
        self.y_pred = self.model.predict(self.X_test)
    
    def plot(self):
        fig = go.Figure()

        full_time = self.df["timestamp"].values
        
        # 真实收盘价曲线
        fig.add_trace(go.Scatter(
            x=full_time, 
            y=self.y_true.values, 
            mode='lines', 
            name='真实收盘价', 
            line=dict(color='blue')
        ))
        
        # 测试集预测曲线
        test_time = full_time[self.y_train_len:]
        fig.add_trace(go.Scatter(
            x=test_time, 
            y=self.y_pred, 
            mode='lines', 
            name='测试集预测', 
            line=dict(color='orange')
        ))
        
        # 未来预测曲线
        fig.add_trace(go.Scatter(
            x=self.future_times, 
            y=self.future_preds, 
            mode='lines+markers', 
            name='未来预测', 
            line=dict(color='green', dash='dash')
        ))
        
        fig.update_layout(
            title="K线预测",
            xaxis_title="时间",
            yaxis_title="收盘价",
            margin=dict(l=40, r=40, t=40, b=40)
        )
        fig.show()