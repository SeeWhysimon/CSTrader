# scripts/main.py

from scripts.utils import kline_plotter
from scripts.data_collector import get_collector
from scripts.data_analyzer.steamdt_analyzer import MachineLearningModel

def collect_data():
    # BUFF 数据采集
    buff_collector = get_collector("buff")
    _, buff_raw_path = buff_collector.collect(
        config_path="./scripts/data_collector/buff/buff_config.json",
        save_path="./data/raw/buff"
    )
    buff_collector.clean(
        raw_path=buff_raw_path, 
        save_path="./data/processed/buff.json"
    )

    # SteamDT 数据采集
    steamdt_collector = get_collector("steamdt")
    _, steamdt_raw_path = steamdt_collector.collect(
        config_path="./scripts/data_collector/steamdt/steamdt_config.json",
        save_path="./data/raw/steamdt"
    )
    steamdt_collector.append_data(
        old_path="./data/processed/steamdt.json", 
        raw_path=steamdt_raw_path
    )

    kline_plotter("./data/processed/steamdt.json")

if __name__ == "__main__":
    collect_data()

    steamdt_analyzer_params = {
        'max_depth': None, 
        'max_features': 19, 
        'min_samples_split': 7, 
        'n_estimators': 50
    }
    
    analyzer = MachineLearningModel(steps=14)
    analyzer.run(data_path="./data/processed/steamdt.json", 
                 params=steamdt_analyzer_params)