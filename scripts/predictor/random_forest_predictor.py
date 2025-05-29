import pandas as pd

class RandomForestPredictor():
    def __init__(self, model):
        self.model = model

    def predict_future(self, last_features: pd.Series, steps: int) -> list:
        preds = []

        for _ in range(steps):
            pred = self.model.predict(pd.DataFrame([last_features]))[0]
            preds.append(pred)

            # [ALERT] 更新特征 (需要完善)
            last_features["open"] = pred
            last_features["close"] = pred
            last_features["high"] = pred * 1.01
            last_features["low"] = pred * 0.99
            last_features["volume"] *= 0.95
            last_features["turnover"] *= 0.95

        return preds
