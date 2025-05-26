import json
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

def load_json(json_path: str):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to load JSON from {json_path}: {e}")
        return []
    
def load_config(config_path: str, 
                     debug: bool = False):
    config = load_json(config_path)

    url = config.get("url")
    params = config.get("params", {})
    headers = config.get("headers", {})

    if not url:
        print("[ERROR] Config missing required field: 'url'")
        return None

    if debug:
        print(f"[DEBUG] URL: {url}")
        print(f"[DEBUG] Params: {params}")
        print(f"[DEBUG] Headers: {headers}")

    return url, params, headers
    
def get_json_response(url, params=None, headers=None, proxies=None, timeout=10):
    try:
        response = requests.get(url=url, 
                                params=params, 
                                headers=headers, 
                                proxies=proxies, 
                                timeout=timeout)
        response.raise_for_status()
        json_data = response.json()
        if not isinstance(json_data, dict):
            print("[ERROR] Unexpected response format (not a dict)")
            return None
        return json_data
    except Exception as e:
        print(f"[ERROR] Failed to get JSON from {url}: {e}")
        return None
    
def load_dataframe_from_json(json_path: str):
    raw_data = load_json(json_path=json_path)
    
    data = raw_data["data"]
    df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
    
    # Convert the data type of ["timestamp"] to int
    df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit='s')
    return df

def kline_plotter(data_path: str):
    # 设置 Plotly 渲染器为浏览器
    pio.renderers.default = 'browser'

    raw_data = load_json(data_path)

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
