import joblib
import numpy as np
import pandas as pd
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 入力データのスキーマ定義
class InputData(BaseModel):
    values: List[int]

@app.post("/predict/")
def predict(data: InputData):
    results = {}
    current_time = datetime.datetime.now()

    # 予測用データフレームを作成
    future_df = pd.DataFrame({
        "ds": [current_time],
        "hour": [current_time.hour],
        "weekday": [current_time.weekday()]
    })

    for value in data.values:
        model_path = f"models/model_{value}.joblib"
        try:
            # モデルとマッピングをロード
            model, pattern_mapping = joblib.load(model_path)
            
            # 予測
            forecast = model.predict(future_df)

            # 予測結果の取得
            prediction = round(forecast["yhat"].iloc[0])  # Prophetはyhatが予測値

            # 数値から pattern_id に変換
            prediction_label = pattern_mapping.get(prediction, "Unknown")

            results[value] = prediction_label
        except FileNotFoundError:
            results[value] = f"Error: Model file '{model_path}' not found"
        except Exception as e:
            results[value] = f"Error: {str(e)}"

    return {
        "input": data.values,
        "timestamp": current_time.isoformat(),
        "predictions": results  # `results` をそのまま返す
    }