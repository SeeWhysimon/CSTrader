import json
import pandas as pd
import plotly.graph_objects as go

def kline_plotter(data_path: str):
    with open(data_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    data = raw_data["data"]
    df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
    df["time"] = pd.to_datetime(df["timestamp"].astype(int), unit='s')
    df = df.sort_values("time")
    
    # 绘制 K 线图
    fig = go.Figure(data=[
        go.Candlestick(
            x=df["time"],
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="K线"
        )
    ])

    fig.update_layout(
        title="BUFF 历史 K 线图",
        xaxis_title="时间",
        yaxis_title="价格",
        xaxis_rangeslider_visible=False
    )

    fig.show()