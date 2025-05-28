import pandas as pd
    
def add_moving_averages(df: pd.DataFrame, windows=[5, 10, 20]):
    for w in windows:
        df[f"ma{w}"] = df["close"].rolling(window=w).mean()
    
    df.dropna(inplace=True)
    return df