# For scripts tests
from scripts.data_analyzer.arima_analyzer import ARIMAModel
from scripts.data_processor.loader import load_dataframe_from_json

if __name__ == "__main__":
    df = load_dataframe_from_json("./data/processed/steamdt.json")
    model = ARIMAModel()
    model.run(df, "close")    
