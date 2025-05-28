from abc import ABC, abstractmethod

class BaseTrainer(ABC):
    def __init__(self):
        self.model = None
        self.best_params = None

    @abstractmethod
    def train(self, X_train, y_train):
        ...

    @abstractmethod
    def predict(self, X_test):
        ...

    @abstractmethod
    def evaluate(self, X_test, y_test):
        ...

    def search_params(self, X_train, y_train, param_grid):
        pass