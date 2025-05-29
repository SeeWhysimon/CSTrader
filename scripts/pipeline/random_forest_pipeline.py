from sklearn.model_selection import train_test_split

from scripts.data_collector.steamdt.steamdt_collector import SteamDTDataCollector
from scripts.data_processor.steamdt_processor import SteamDTDataProcessor
from scripts.trainer.random_forest_trainer import RandomForestTrainer
from scripts.predictor.random_forest_predictor import RandomForestPredictor
from scripts.visualizer import visualize_kline

class RandomForestPipeline:
    def __init__(self):
        self.collector = SteamDTDataCollector()
        self.data_processor = SteamDTDataProcessor()
        self.trainer = RandomForestTrainer()

    def run(self):
        config_path = "./scripts/data_collector/steamdt/steamdt_config.json"
        _, save_path_with_timestamp = self.collector.collect(config_path=config_path, 
                                                             save_path="./data/raw/steamdt")

        self.data_processor.append_data(json_raw_path=save_path_with_timestamp, 
                                        json_save_path="./data/processed/steamdt.json")
        df = self.data_processor.load_data(path="./data/processed/steamdt.json")
        df = self.data_processor.add_features(df)
        df, features, target = self.data_processor.prepare_data(df)

        X = df[features]
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, shuffle=False, test_size=0.2)

        self.trainer.search_params(X_train=X_train, y_train=y_train)
        model = self.trainer.train(X_train=X_train, y_train=y_train)
        y_pred = self.trainer.predict(X_test=X_test)
        result = self.trainer.eval(y_test=y_test, y_pred=y_pred)
        print(f"[RESULT]: {result}")



