from abc import ABC, abstractmethod
import pandas as pd

class BaseDataProcessor(ABC):
    @abstractmethod
    def load_data(self, path: str) -> pd.DataFrame:
        ...

    @abstractmethod
    def add_features(self, df: pd.DataFrame) -> pd.DataFrame:
        ...

    @abstractmethod
    def prepare_dataset(self, df: pd.DataFrame) -> tuple:
        ...
