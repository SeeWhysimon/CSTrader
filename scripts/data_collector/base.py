# scripts/data_collector/base.py

from abc import ABC, abstractmethod

class BaseDataCollector(ABC):
    """
    数据采集器的抽象基类
    所有子类必须实现 collect() 方法
    """

    def __init__(self, proxies=None):
        self.proxies = proxies

    @abstractmethod
    def collect(self, save_path: str, **kwargs):
        """
        实现数据的抓取与保存
        参数：
            save_path: 保存路径
            kwargs: 各平台数据抓取可能需要的参数(如商品ID等)
        """
        pass
