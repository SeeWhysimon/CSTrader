import pandas as pd

from typing import Tuple
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.multioutput import MultiOutputRegressor

class RandomForestPredictor():
    def __init__(self, params=None):
        self.base_model = RandomForestRegressor()
        self.model = MultiOutputRegressor(self.base_model)
        self.best_params = params

    def search_params(self, X_train, y_train, param_grid=None):
        if param_grid is None:
            param_grid = {
                'estimator__n_estimators': [50, 100, 200], 
                'estimator__max_depth': [None, 10, 20], 
                'estimator__min_samples_split': [2, 5, 7], 
                'estimator__max_features': [7, 11, 13, 19]
            }
        grid = GridSearchCV(self.model, param_grid, cv=3, scoring='neg_mean_squared_error')
        print("[INFO] Searching for best parameters...")
        grid.fit(X_train, y_train)
        print("[INFO] Parameters found.")
        self.best_params = grid.best_params_
        print(self.best_params)
        self.model.set_params(**self.best_params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self.model

    def predict(self, X: pd.DataFrame, y: pd.DataFrame, steps: int = 1) -> Tuple[pd.DataFrame, pd.DataFrame]:
        X_history = X.copy()
        y_history = y.copy()

        label_to_feature = {
            'next_open': 'open',
            'next_high': 'high',
            'next_low': 'low',
            'next_close': 'close',
            'next_volume': 'volume',
            'next_turnover': 'turnover'
        }

        for _ in range(steps):
            ma = pd.DataFrame([{
                "ma7": y_history["next_close"].tail(7).mean(),
                "ma14": y_history["next_close"].tail(14).mean(),
                "ma21": y_history["next_close"].tail(21).mean(),
                "ma42": y_history["next_close"].tail(42).mean()
            }])

            current_y = y_history.iloc[[-1]].copy()
            print(current_y)
            current_y.rename(columns=label_to_feature, inplace=True)
            current = pd.concat([current_y.reset_index(drop=True), ma], axis=1)

            pred = self.model.predict(current)
            pred_df = pd.DataFrame(pred, columns=y.columns)
            X_history = pd.concat([X_history, current], axis=0, ignore_index=True)
            y_history = pd.concat([y_history, pred_df], axis=0, ignore_index=True)

        return X_history[-steps:], y_history[-steps:]

    def eval(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        return {
            "mse": mean_squared_error(y_test, y_pred, multioutput='raw_values'),
            "r2": r2_score(y_test, y_pred, multioutput='raw_values')
        }
