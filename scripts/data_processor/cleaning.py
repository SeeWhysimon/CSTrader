import json
import os
from scripts.utils import load_json

def clean_buff_data(raw_path: str, 
                    save_path: str):
    """清洗 BUFF 数据并保存为简化格式，并与现有文件合并"""

    # 检查文件路径是否存在
    if not os.path.exists(raw_path):
        print(f"[ERROR] Raw data file does not exist: {raw_path}")
        return None

    raw_data = load_json(raw_path)

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
            print(f"[INFO] Added {len(new_entries)} new entries to existing data.")
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
        print(f"[INFO] Cleaned and saved: {save_path}")
    except Exception as e:
        print(f"[ERROR] Failed to save cleaned data to {save_path}: {e}")
        return None

    return existing_data