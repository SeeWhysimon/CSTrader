# For scripts tests
from scripts.data_analyzer.arima_analyzer import ARIMAModel
from scripts.DataProcessor.loader import load_steamdt_json

if __name__ == "__main__":
    df = load_steamdt_json("./data/processed/steamdt.json")
    model = ARIMAModel()
    model.run(df, "close")    
