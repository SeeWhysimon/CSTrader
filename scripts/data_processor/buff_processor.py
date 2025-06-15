import json
import os
import pandas as pd

from typing import Dict

from scripts.data_processor.base import BaseDataProcessor

class BuffDataProcessor(BaseDataProcessor):
    def load_raw(self, json_path: str) -> pd.DataFrame:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        items = json_data["data"]["items"]
        df = pd.json_normalize(items)

        return df
    
    def load_processed(self, json_path: str) -> pd.DataFrame:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        df = pd.DataFrame(json_data)
        df["transact_time"] = pd.to_datetime(df["transact_time"].astype(int), unit='ms')

        return df
        
    def clean_data(self, data: pd.DataFrame) -> pd.DataFrame:
        origin_cols = ["asset_info.id",                 # str
                       "asset_info.info.paintindex",    # int
                       "asset_info.info.paintseed",     # int
                       "asset_info.paintwear",          # str
                       "price",                         # str
                       "transact_time"]                 # int
        target_cols = ["transact_id", "paint_index", "paint_seed", "paint_wear", "price", "transact_time"]

        cleaned_data = data[origin_cols].rename(columns=dict(zip(origin_cols, target_cols)))

        # 格式转换
        cleaned_data["paint_wear"] = cleaned_data["paint_wear"].astype(float)
        cleaned_data["price"] = cleaned_data["price"].astype(float)
        cleaned_data["transact_time"] = pd.to_datetime(cleaned_data["transact_time"].astype(int), unit='s')
        cleaned_data.to_json("./data/processed/buff.json", orient="records", force_ascii=False, indent=2)

        return cleaned_data

    def append_data(self, old_data: pd.DataFrame, new_data: pd.DataFrame):
        old_len = len(old_data)
        new_data = new_data[~new_data["transact_id"].isin(old_data["transact_id"])]
        
        df = pd.concat([old_data, new_data], ignore_index=True)
        df.sort_values(by="transact_time", inplace=True)
        
        new_len = len(df)
        print(f"[INFO] {new_len - old_len} entries added.")
        return df