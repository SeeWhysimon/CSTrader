# For scripts tests
from scripts.data_processor.checker import check_adf
from scripts.utils import load_dataframe_from_json

if __name__ == "__main__":
    df = load_dataframe_from_json("./data/processed/steamdt.json")
    check_adf(df, "close")

    df['close_diff'] = df['close'].diff().dropna()
    df = df.dropna()
    check_adf(df, "close_diff")
