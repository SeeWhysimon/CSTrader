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