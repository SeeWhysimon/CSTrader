import json
import os
import pandas as pd

from typing import Dict

from scripts.data_processor.base import BaseDataProcessor

class BuffDataProcessor(BaseDataProcessor):
    def load_data(self, json_path: str) -> pd.DataFrame:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        items = json_data["data"]["items"]
        df = pd.json_normalize(items)

        return df
    
    def clean_data(self, data: pd.DataFrame, save_path: str = None):
        target_cols = ["asset_info.id", # str
                       "asset_info.info.paintindex", # int
                       "asset_info.info.paintseed", # int
                       "asset_info.info.paintwear", # str
                       "price", # str
                       "transact_time"] # str
        cleaned_data = pd.DataFrame(data[target_cols], columns=target_cols)
        
        cleaned_data["asset_info.info.paintwear"] = cleaned_data["asset_info.info.paintwear"].astype(float)
        cleaned_data["price"] = cleaned_data["price"].astype(float)
        cleaned_data["transact_time"] = pd.to_datetime(cleaned_data["transact_time"].astype(int), unit='s')
        
        if save_path:
            cleaned_data.to_csv(save_path, index=False)
        
        return cleaned_data