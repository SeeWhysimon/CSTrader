import pandas as pd

from sklearn.model_selection import train_test_split

from scripts.data_collector.steamdt.steamdt_collector import SteamDTDataCollector
from scripts.data_processor.steamdt_processor import SteamDTDataProcessor
from scripts.predictor.random_forest_predictor import RandomForestPredictor
from scripts.visualizer import visualize_kline

class RandomForestPipeline:
    def __init__(self):
        self.collector = SteamDTDataCollector()
        self.data_processor = SteamDTDataProcessor()
        self.predictor = RandomForestPredictor(params={'estimator__max_depth': 10, 
                                                     'estimator__max_features': 7, 
                                                     'estimator__min_samples_split': 5, 
                                                     'estimator__n_estimators': 50})

    def run(self):
        config_path = "./scripts/data_collector/steamdt/steamdt_config.json"
        _, save_path_with_timestamp = self.collector.collect(config_path=config_path, 
                                                             save_path="./data/raw/steamdt")

        self.data_processor.append_data(json_raw_path=save_path_with_timestamp, 
                                        json_save_path="./data/processed/steamdt.json")
        df = self.data_processor.load_data(path="./data/processed/steamdt.json")
        visualize_kline(df)
        df = self.data_processor.add_features(df)
        df, features, targets = self.data_processor.prepare_data(df)

        X = df[features]
        y = df[targets]
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

        self.predictor.train(X_train=X_train, y_train=y_train)

        test_result = self.predictor.eval(X_test=X_test, y_test=y_test)
        print(f"[RESULT]: {test_result}")

        steps = 7
        last_time = df["timestamp"].iloc[-1]
        future_times = [last_time + pd.Timedelta(days=i+1) for i in range(steps)]
        X_preds, y_preds = self.predictor.predict(X=X, y=y, steps=steps)
        
        future_times = pd.DataFrame(future_times, columns=["timestamp"])
        preds = pd.concat([future_times, X_preds.reset_index(drop=True)], axis=1)
        print(preds)
        visualize_kline(preds)

