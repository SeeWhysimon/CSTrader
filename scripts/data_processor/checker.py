import pandas as pd

from statsmodels.tsa.stattools import adfuller

from scripts.utils import load_dataframe_from_json

def check_adf(df: pd.DataFrame, target: str):
    result = adfuller(df[target])
    
    print("ADF Statistic:", result[0])
    print("p-value:", result[1])
    
    return result[0]

if __name__ == "__main__":
    df = load_dataframe_from_json("../../data/processed/steamdt.json")
    check_adf(df, "close")