# scripts/main.py

import utils
from data_collector import get_collector

def collect_data():
    # BUFF 数据采集
    buff_collector = get_collector("buff")
    _, buff_raw_path = buff_collector.collect(
        config_path="./data_collector/buff/buff_config.json",
        save_path="../data/raw/buff"
    )
    buff_collector.clean(
        raw_path=buff_raw_path, 
        save_path="../data/processed/buff.json"
    )

    # SteamDT 数据采集
    steamdt_collector = get_collector("steamdt")
    _, steamdt_raw_path = steamdt_collector.collect(
        config_path="./data_collector/steamdt/steamdt_config.json",
        save_path="../data/raw/steamdt"
    )
    steamdt_collector.append_data(
        old_path="../data/processed/steamdt.json", 
        raw_path=steamdt_raw_path
    )

    utils.kline_plotter("../data/processed/steamdt.json")

if __name__ == "__main__":
    collect_data()