# scripts/data_collector/buff/buff_collector.py

import json

from datetime import datetime

from scripts.data_collector.base import BaseDataCollector

class BuffDataCollector(BaseDataCollector):
    def collect(self, config_path: str, save_path: str, debug: bool = False):
        """从 JSON 配置文件读取参数，采集 BUFF 数据并保存"""

        # Step 1: 加载配置文件
        self.load_config(config_path=config_path, debug=debug)

        # Step 2: 发起请求并解析
        json_data = self.get_json_response()

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
        