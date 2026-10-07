from sklearn.base import RegressorMixin
import logging
from zenml import step
import pandas as pd
from src.evaluation import MSE, R2, RMSE
from typing_extensions import Annotated
from typing import Tuple
import mlflow


# Tuple[...]: Khai báo hàm này sẽ trả về một bộ gồm nhiều giá trị.

# Annotated[float, "r2_score"] & Annotated[float, "rmse"]:

# Kiểu dữ liệu thực tế trả về của cả hai phần tử đều là số thực (float).

from zenml.client import Client

experiment_tracker = Client().active_stack.experiment_tracker

@step(experiment_tracker=experiment_tracker.name)
def evaluate_model(model: RegressorMixin,
    X_test: pd.DataFrame,
    y_test: pd.DataFrame,
) -> Tuple[
    Annotated[float, "r2_score"],
    Annotated[float, "rmse"]
]:
    """
    Evaluate the model on the ingeted data
    Args:
        df: the ingested data
    """
    try:
        prediction = model.predict(X_test)

        mse_class= MSE()
        mse = mse_class.calculate_scores(y_test, prediction)
        mlflow.log_metric("mse", mse)

        r2_class = R2()
        r2 = r2_class.calculate_scores(y_test, prediction)
        mlflow.log_metric("r2", r2)

        rmse_class = RMSE()
        rmse = rmse_class.calculate_scores(y_test, prediction)
        mlflow.log_metric("rmse", rmse)

        return r2, rmse
    except Exception as e:
        logging.error(f"Error while evaluating model: {e}")
        raise e