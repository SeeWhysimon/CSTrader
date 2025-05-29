import pandas as pd
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
    
    def predict(self, X: pd.DataFrame, steps: int = 1) -> pd.DataFrame:
        preds = []
        last_record = X.copy()

        for _ in range(steps):
            pred = self.model.predict(last_record)[0]
            preds.append(pred)

            last_record = pd.DataFrame([pred], columns=last_record.columns)

        result = pd.DataFrame(preds, columns=X.columns)
        return result

    def eval(self, y_test, y_pred):
        return {
            "mse": mean_squared_error(y_test, y_pred, multioutput='raw_values'),
            "r2": r2_score(y_test, y_pred, multioutput='raw_values')
        }
