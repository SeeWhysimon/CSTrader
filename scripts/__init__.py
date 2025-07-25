# scripts/data_collector/__init__.py

from scripts.data_collector.buff.buff_collector import BuffDataCollector
from scripts.data_collector.steamdt.steamdt_collector import SteamDTDataCollector

def get_collector(source: str):
    source = source.lower()
    
    if source == "buff":
        return BuffDataCollector()
    elif source == "steamdt":
        return SteamDTDataCollector()
    else:
        raise ValueError(f"Unknown resource: '{source}'. Support: buff, steamdt")
