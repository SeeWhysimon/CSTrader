import plotly.graph_objects as go
import plotly.io as pio
import pandas as pd

def visualize_kline(data: pd.DataFrame):
    # 设置 Plotly 渲染器为浏览器
    pio.renderers.default = 'browser'
    
    # 绘制 K 线图
    fig = go.Figure(data=[
        go.Candlestick(
            x=data["timestamp"],
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
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