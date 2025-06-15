# For scripts tests
from scripts.data_processor.buff_processor import BuffDataProcessor
from scripts.data_collector.buff.buff_collector import BuffDataCollector

import pandas as pd

if __name__ == "__main__":
    collector = BuffDataCollector()
    _, json_path = collector.collect(config_path="./scripts/data_collector/buff/buff_config.json", 
                                     save_path="./data/raw/buff")

    processor = BuffDataProcessor()
    df = processor.load_raw(json_path=json_path)

    cleaned_df = processor.clean_data(df)

    old_df = processor.load_processed("./data/processed/buff.json")
    all_df = processor.append_data(old_data=old_df, new_data=cleaned_df)
    all_df.to_csv("./data/processed/buff_test.csv", index=False)