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
        target_cols = ["asset_info.id", 
                       "asset_info.info.paintindex", 
                       "asset_info.info.paintseed", 
                       "asset_info.info.paintwear", 
                       "price", 
                       "transact_time"]
        cleaned_data = pd.DataFrame(data[target_cols], columns=target_cols)
        
        if save_path:
            cleaned_data.to_csv("./data/processed/buff.csv")
        
        return cleaned_data