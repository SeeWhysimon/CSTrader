# scripts/data_collector/base.py

import json
import requests

from abc import ABC, abstractmethod

class BaseDataCollector(ABC):
    def __init__(self, url=None, params=None, headers=None, proxies=None):
        self.url = url
        self.params = params
        self.headers = headers
        self.proxies = proxies
    
    def load_config(self, config_path: str, debug: bool = False):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"[ERROR] Failed to load config from {config_path}: {e}")
            return None

        self.url = config.get("url")
        self.params = config.get("params", {})
        self.headers = config.get("headers", {})

        if not self.url:
            print("[ERROR] Config missing required field: 'url'")
            return None

        if debug:
            print(f"[DEBUG] URL: {self.url}")
            print(f"[DEBUG] Params: {self.params}")
            print(f"[DEBUG] Headers: {self.headers}")
    
    def get_json_response(self, timeout=10):
        try:
            response = requests.get(url=self.url, 
                                    params=self.params, 
                                    headers=self.headers, 
                                    proxies=self.proxies, 
                                    timeout=timeout)
            response.raise_for_status()
            json_data = response.json()
            if not isinstance(json_data, dict):
                print("[ERROR] Unexpected response format (not a dict)")
                return None
            return json_data
        except Exception as e:
            print(f"[ERROR] Failed to get JSON from {self.url}: {e}")
            return None

    @abstractmethod
    def collect(self, save_path: str, **kwargs):
        pass
