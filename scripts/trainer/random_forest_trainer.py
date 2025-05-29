from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score

class RandomForestTrainer():
    def __init__(self):
        self.model = RandomForestRegressor()
        self.best_params = None

    def search_params(self, X_train, y_train, param_grid=None):
        if param_grid is None:
            param_grid = {
                'n_estimators': [50, 100, 200], 
                'max_depth': [None, 10, 20], 
                'min_samples_split': [2, 5, 7], 
                'max_features': [7, 11, 13, 19]
            }
        grid = GridSearchCV(self.model, param_grid, cv=3, scoring='neg_mean_squared_error')
        grid.fit(X_train, y_train)
        self.best_params = grid.best_params_
        self.model.set_params(**self.best_params)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)
        return self.model

    def predict(self, X_test):
        return self.model.predict(X_test)

    def eval(self, y_test, y_pred):
        return {
            "mse": mean_squared_error(y_test, y_pred),
            "r2": r2_score(y_test, y_pred)
        }
