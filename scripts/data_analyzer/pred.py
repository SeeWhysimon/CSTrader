import json
import pandas as pd
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 读取数据
with open("../../data/processed/steamdt.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

data = raw_data["data"]
df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit='s')

# 构造目标值
df["next_close"] = df["close"].shift(-1)
df.dropna(inplace=True)

features = ["open", "high", "low", "close", "volume", "turnover"]
X = df[features]
y = df["next_close"]

# 划分数据
X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.25)

# 模型训练（用全量数据）
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)

# 模型预测：测试集
y_pred = model.predict(X_test)

# 模型预测：未来7步（递归式）
future_preds = []
last_features = X.iloc[-1].copy()

for i in range(7):
    pred = model.predict(pd.DataFrame([last_features]))[0]
    future_preds.append(pred)
    
    # 构造新一行特征：open/close/low/high → 上一次预测的 close，其他用原值模拟
    last_features = last_features.copy()
    last_features["open"] = pred
    last_features["close"] = pred
    last_features["high"] = pred * 1.01
    last_features["low"] = pred * 0.99
    last_features["volume"] = last_features["volume"] * 0.95  # 模拟递减
    last_features["turnover"] = last_features["turnover"] * 0.95

# 构造未来时间戳（假设按天间隔）
last_time = df["timestamp"].iloc[-1]
future_times = [last_time + pd.Timedelta(days=i+1) for i in range(7)]

# 合并所有图层
full_time = df["timestamp"].iloc[:-1].reset_index(drop=True)  # 对应 y
split_idx = len(y_train)

fig = go.Figure()

# 全部真实值
fig.add_trace(go.Scatter(
    x=full_time,
    y=y.values,
    mode='lines',
    name='真实收盘价',
    line=dict(color='blue')
))

# 测试集预测
fig.add_trace(go.Scatter(
    x=full_time[split_idx:],
    y=y_pred,
    mode='lines',
    name='测试集预测',
    line=dict(color='orange')
))

# 未来 7 天预测
fig.add_trace(go.Scatter(
    x=future_times,
    y=future_preds,
    mode='lines+markers',
    name='未来7天预测',
    line=dict(color='green', dash='dash')
))

fig.update_layout(
    title="历史收盘价 + 测试预测 + 未来7天预测",
    xaxis_title="时间",
    yaxis_title="收盘价",
    legend=dict(x=0, y=1.0),
    margin=dict(l=40, r=40, t=40, b=40)
)

fig.show()
