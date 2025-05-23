# scripts/data_collector/buff/buff_collector.py

import requests
import json
import os
from datetime import datetime
from scripts.data_collector.base import BaseDataCollector

class BuffDataCollector(BaseDataCollector):
    def __init__(self, proxies=None, debug=False):
        self.proxies = proxies or {}
        self.debug = debug

    def collect(self, config_path: str, save_path: str):
        """从 JSON 配置文件读取参数，采集 BUFF 数据并保存"""

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
        except Exception as e:
            print(f"[ERROR] Response parsing failed: {e}")
            return None

        # Step 4: 保存数据，并加上时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        save_path_with_timestamp = f"{save_path}_{timestamp}.json"

        try:
            with open(save_path_with_timestamp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"BUFF data saved: {save_path_with_timestamp}")
        except Exception as e:
            print(f"[ERROR] Failed to save data to {save_path_with_timestamp}: {e}")
            return None

        return data, save_path_with_timestamp

    def clean(self, raw_path: str, save_path: str):
        """清洗 BUFF 数据并保存为简化格式，并与现有文件合并"""

        # 检查文件路径是否存在
        if not os.path.exists(raw_path):
            print(f"[ERROR] Raw data file does not exist: {raw_path}")
            return None

        try:
            # 读取原始 JSON 文件
            with open(raw_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to read raw data: {e}")
            return None

        # 提取所需字段
        items = raw_data.get("data", {}).get("items", [])
        result = []

        for item in items:
            asset_info = item.get("asset_info", {})
            info = asset_info.get("info", {})
            phase = info.get("phase_data", {})
            
            entry = {
                "transact_id": asset_info.get("id"),
                "phase_name": phase.get("name"),
                "phase_color": phase.get("color"),
                "paintwear": asset_info.get("paintwear"),
                "transact_time": item.get("transact_time"),
                "price": item.get("price")
            }
            result.append(entry)

        # 读取已保存的数据并合并
        if os.path.exists(save_path):
            try:
                with open(save_path, "r", encoding="utf-8") as f:
                    existing_data = json.load(f)
            except Exception as e:
                print(f"[ERROR] Failed to read existing saved data: {e}")
                existing_data = []

            # 比较新数据与现有数据，以 transact_id 和 transact_time 为标准进行去重
            existing_ids = {(entry["transact_time"], entry["transact_id"]) for entry in existing_data}
            new_entries = [entry for entry in result if (entry["transact_time"], entry["transact_id"]) not in existing_ids]

            # 如果有新的数据，追加到现有数据
            if new_entries:
                existing_data.extend(new_entries)
                print(f"Added {len(new_entries)} new entries to existing data.")
            else:
                print("[INFO] No new entries to add.")

        else:
            # 如果文件不存在，则直接保存清洗后的数据
            existing_data = result
            print("[WARNING] No existing data found. Saving new cleaned data.")

        # 保存合并后的数据
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=2)
            print(f"Cleaned and saved: {save_path}")
        except Exception as e:
            print(f"[ERROR] Failed to save cleaned data to {save_path}: {e}")
            return None

        return existing_data