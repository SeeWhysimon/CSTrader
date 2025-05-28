# scripts/data_collector/__init__.py

from scripts.DataCollector.buff.buff_collector import BuffDataCollector
from scripts.DataCollector.steamdt.steamdt_collector import SteamDTDataCollector
# 后续你可以继续添加其他数据源

def get_collector(source: str):
    """
    根据用户指定的数据源名称，返回对应的 DataCollector 实例

    参数:
        source (str): 数据源标识，例如 "buff", "steamdt"

    返回:
        BaseDataCollector 的子类实例
    """
    source = source.lower()
    
    if source == "buff":
        return BuffDataCollector()
    elif source == "steamdt":
        return SteamDTDataCollector()
    else:
        raise ValueError(f"Unknown resource: '{source}'. Support: buff, steamdt")
