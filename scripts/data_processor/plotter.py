import plotly.graph_objects as go
import plotly.io as pio
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scripts.data_processor.loader import load_dataframe_from_json

def kline_plotter(data_path: str):
    # 设置 Plotly 渲染器为浏览器
    pio.renderers.default = 'browser'

    df = load_dataframe_from_json(json_path=data_path)
    
    # 绘制 K 线图
    fig = go.Figure(data=[
        go.Candlestick(
            x=df["timestamp"],
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