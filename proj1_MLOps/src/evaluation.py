import logging
from abc import ABC , abstractmethod
import numpy as np
from sklearn.metrics import mean_squared_error,r2_score

class Evaluation(ABC):
    """
    Abstract class defining strategy for evaluation our models
    """

    @abstractmethod
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculates the socres for the model
        Args
            y_true: True labels
            y_pred: Predicted labels
        returns:
            None
        """
        pass

class MSE(Evaluation):
    """
    Evaluation class for Mean Squared Error
    """
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculates the MSE for the model
        Args:
            y_true: True labels
            y_pred: Predicted labels
        returns:
            None
        """
        try:
            logging.info("Calculating MSE")
            mse = mean_squared_error(y_true, y_pred)
            logging.info(f"MSE: {mse}")
            return mse
        except Exception as e:
            logging.error(f"Error while calculating MSE: {e}")
            raise e

class R2(Evaluation):
    """
    Evaluation class for R2 Score
    """
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculates the R2 Score for the model
        Args:
            y_true: True labels
            y_pred: Predicted labels
        returns:
            None
        """
        try:
            logging.info("Calculating R2 Score")
            r2 = r2_score(y_true, y_pred)
            logging.info(f"R2 Score: {r2}")
            return r2
        except Exception as e:
            logging.error(f"Error while calculating R2 Score: {e}")
            raise e

class RMSE(Evaluation):
    """
    Evaluation class for Root Mean Squared Error
    """
    def calculate_scores(self, y_true: np.ndarray, y_pred: np.ndarray):
        """
        Calculates the RMSE for the model
        Args:
            y_true: True labels
            y_pred: Predicted labels
        returns:
            None
        """
        try:
            logging.info("Calculating RMSE")
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            logging.info(f"RMSE: {rmse}")
            return rmse
        except Exception as e:
            logging.error(f"Error while calculating RMSE: {e}")
            raise e