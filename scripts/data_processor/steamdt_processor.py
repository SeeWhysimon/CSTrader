import json
import os
import pandas as pd

from typing import Dict

from scripts.data_processor.base import BaseDataProcessor

class SteamDTDataProcessor(BaseDataProcessor):
    def load_data(self, path) -> pd.DataFrame:
        with open(path, "r", encoding="utf-8") as f:
            json_data = json.load(f)

        data = json_data["data"]
        df = pd.DataFrame(data, columns=["timestamp", "open", "close", "high", "low", "volume", "turnover"])
        df["timestamp"] = pd.to_datetime(df["timestamp"].astype(int), unit='s')
        df = df.sort_values("timestamp")

        df.set_index("timestamp", inplace=True)
        daily_df = df.resample("1D").agg({
            "open": "first",
            "close": "last",
            "high": "max",
            "low": "min",
            "volume": "sum",
            "turnover": "sum"
        })
        daily_df = daily_df.dropna().reset_index()

        return daily_df
    
    def add_features(self, df) -> pd.DataFrame:
        # Add moving avarages
        windows = [7, 14, 21, 42]
        for w in windows:
            df[f"ma{w}"] = df["close"].rolling(window=w).mean()     
        df.dropna(inplace=True)

        return df
    
    def prepare_data(self, df):
        df["next_open"] = df["open"].shift(-1)
        df["next_close"] = df["close"].shift(-1)
        df["next_high"] = df["high"].shift(-1)
        df["next_low"] = df["low"].shift(-1)
        df["next_volume"] = df["volume"].shift(-1)
        df["next_turnover"] = df["turnover"].shift(-1)
        df.dropna(inplace=True)

        features = [
            "open", "close", "high", "low", "volume", "turnover",
            "ma7", "ma14", "ma21", "ma42"
        ]
        targets = ["next_open", "next_close", "next_high", "next_low", "next_volume", "next_turnover"]
        
        return df, features, targets
    
    def append_data(self, json_raw_path: str, json_save_path: str) -> Dict:
        # Step 1: 检查旧数据文件是否存在
        if not os.path.exists(json_save_path):
            print(f"[WARNING] {json_save_path} does not exist. Creating an empty file.")
            # 创建空文件
            with open(json_save_path, "w", encoding="utf-8") as f:
                json.dump({
                    "success": True,
                    "data": [],
                    "errorCode": 0,
                    "errorMsg": None,
                    "errorData": None,
                    "errorCodeStr": None
                }, f, ensure_ascii=False, indent=2)
            return None

        # Step 2: 读取旧数据
        try:
            with open(json_save_path, "r", encoding="utf-8") as f:
                old_data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to read old data from {json_save_path}: {e}")
            return None

        if not old_data.get("success") or "data" not in old_data:
            print(f"[ERROR] Invalid data format in {json_save_path}")
            return None
        
        old_records = old_data["data"]

        # Step 3: 读取新数据
        try:
            with open(json_raw_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to read raw data from {json_raw_path}: {e}")
            return None

        if not raw_data.get("success") or "data" not in raw_data:
            print(f"[ERROR] Invalid data format in {json_raw_path}")
            return None
        
        raw_records = raw_data["data"]

        # Step 4: 比较数据并更新
        new_records = []
        existing_timestamps = {int(record[0]) for record in old_records if isinstance(record, list) and len(record) > 0}

        for record in raw_records:
            try:
                timestamp = int(record[0])
                if timestamp not in existing_timestamps:
                    new_records.append(record)
            except Exception:
                print(f"[WARNING] Invalid timestamp in record: {record}")

        if not new_records:
            print(f"[INFO] No new records to add to {json_save_path}.")
            return None

        # Step 5: 将新记录插入到 old_records 的头部
        new_records.extend(old_records)

        # Step 6: 保存更新后的数据
        try:
            with open(json_save_path, "w", encoding="utf-8") as f:
                json.dump({
                    "success": True,
                    "data": new_records,
                    "errorCode": 0,
                    "errorMsg": None,
                    "errorData": None,
                    "errorCodeStr": None
                }, f, ensure_ascii=False, indent=2)
            print(f"[INFO] Data successfully appended and saved to {json_save_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save updated data to {json_save_path}: {e}")
            return None

        return new_records