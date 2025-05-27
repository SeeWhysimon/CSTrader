# scripts/data_collector/buff/buff_collector.py

import requests
import json

from datetime import datetime

from scripts.data_processor.loader import get_json_response, load_config
from scripts.data_processor.cleaner import clean_buff_data
from scripts.data_collector.base import BaseDataCollector

class BuffDataCollector(BaseDataCollector):
    def __init__(self, proxies=None, debug=False):
        self.proxies = proxies or {}
        self.debug = debug

    def run(self, 
            config_path: str, 
            raw_save_path: str, 
            cleaned_save_path: str):
        # Step 1: 获取原始数据
        _, buff_raw_path = self.collect(config_path=config_path, 
                     save_path=raw_save_path)
        
        # Step 2: 清洗BUFF数据
        if cleaned_save_path:
            clean_buff_data(raw_path=buff_raw_path, 
                            save_path=cleaned_save_path)

    def collect(self, config_path: str, save_path: str):
        """从 JSON 配置文件读取参数，采集 BUFF 数据并保存"""

        # Step 1: 加载配置文件
        url, params, headers = load_config(config_path=config_path, 
                                                debug=self.debug)

        # Step 2: 发起请求并解析
        json_data = get_json_response(url=url, 
                          params=params, 
                          headers=headers, 
                          proxies=self.proxies)

        # Step 4: 保存数据，并加上时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        save_path_with_timestamp = f"{save_path}_{timestamp}.json"

        try:
            with open(save_path_with_timestamp, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"[INFO] BUFF data saved: {save_path_with_timestamp}")
        except Exception as e:
            print(f"[ERROR] Failed to save data to {save_path_with_timestamp}: {e}")
            return None

        return json_data, save_path_with_timestamp
        