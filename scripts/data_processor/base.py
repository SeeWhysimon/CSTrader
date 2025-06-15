from abc import ABC, abstractmethod
import pandas as pd

class BaseDataProcessor(ABC):
    @abstractmethod
    def load_raw(self, path: str) -> pd.DataFrame:
        ...
