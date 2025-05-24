# scripts/data_collector/steamdt/steamdt_collector.py

import requests
import json
import os
from datetime import datetime
from scripts.data_collector.base import BaseDataCollector

class SteamDTDataCollector(BaseDataCollector):
    def __init__(self, proxies=None, debug=False):
        self.proxies = proxies or {}
        self.debug = debug

    def collect(self, config_path: str, save_path: str):
        """从配置文件中读取url/params/headers进行采集"""

        # Step 1: 加载配置文件
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to read config: {e}")
            return None

        url = config.get("url")
        params = config.get("params", {})
        headers = config.get("headers", {})

        if not url:
            print("[ERROR] Config missing required field: 'url'")
            return None

        if self.debug:
            print(f"[DEBUG] URL: {url}")
            print(f"[DEBUG] Params: {params}")
            print(f"[DEBUG] Headers: {headers}")

        # Step 2: 发起请求
        try:
            response = requests.get(url, params=params, headers=headers, proxies=self.proxies)
            response.raise_for_status()
        except Exception as e:
            print(f"[ERROR] Request failed: {e}")
            return None

        # Step 3: 解析响应
        try:
            data = response.json()
            if not isinstance(data, dict):
                print("[ERROR] Unexpected response format (not a dict)")
                return None

            # 转换时间戳字段为 int
            if "data" in data and isinstance(data["data"], list):
                for record in data["data"]:
                    if isinstance(record, list) and len(record) > 0:
                        try:
                            record[0] = int(record[0])
                        except Exception:
                            print(f"[WARNING] Invalid timestamp format: {record[0]}")

        except Exception as e:
            print(f"[ERROR] Response parsing failed: {e}")
            return None

        # Step 4: 保存数据
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        save_path_with_timestamp = f"{save_path}_{timestamp}.json"

        try:
            with open(save_path_with_timestamp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"SteamDT data saved: {save_path_with_timestamp}")
        except Exception as e:
            print(f"[ERROR] Failed to save data to {save_path_with_timestamp}: {e}")
            return None

        return data, save_path_with_timestamp

    def append_data(self, old_path: str, raw_path: str):
        # Step 1: 检查旧数据文件是否存在
        if not os.path.exists(old_path):
            print(f"[WARNING] {old_path} does not exist. Creating an empty file.")
            # 创建空文件
            with open(old_path, "w", encoding="utf-8") as f:
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
            with open(old_path, "r", encoding="utf-8") as f:
                old_data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to read old data from {old_path}: {e}")
            return None

        if not old_data.get("success") or "data" not in old_data:
            print(f"[ERROR] Invalid data format in {old_path}")
            return None
        
        old_records = old_data["data"]

        # Step 3: 读取新数据
        try:
            with open(raw_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to read raw data from {raw_path}: {e}")
            return None

        if not raw_data.get("success") or "data" not in raw_data:
            print(f"[ERROR] Invalid data format in {raw_path}")
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
            print(f"[INFO] No new records to add to {old_path}.")
            return None

        # Step 5: 将新记录插入到 old_records 的头部
        new_records.extend(old_records)

        # Step 6: 保存更新后的数据
        try:
            with open(old_path, "w", encoding="utf-8") as f:
                json.dump({
                    "success": True,
                    "data": new_records,
                    "errorCode": 0,
                    "errorMsg": None,
                    "errorData": None,
                    "errorCodeStr": None
                }, f, ensure_ascii=False, indent=2)
            print(f"Data successfully appended and saved to {old_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save updated data to {old_path}: {e}")
            return None

        return new_records
