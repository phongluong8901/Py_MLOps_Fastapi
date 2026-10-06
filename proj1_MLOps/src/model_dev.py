import logging
from abc import ABC, abstractmethod
from sklearn.linear_model import LinearRegression

class Model(ABC):
    """
    Abstract class for all models
    """

    @abstractmethod
    def train(self, X_train, y_train):
        """
        Trains the model
        Args:
            X_train: Trainning data
            y_train: Training labels
        returns: None
        """

class LinearRegressionModel(Model):
    """
    Linear Regression Model
    """
    def train(self, X_train, y_train, **kwargs):
        """
        Trains the model
        Args:
            X_train: Trainning data
            y_train: Training labels
            **kwargs: Additional parameters for the model
        returns: None
        """
        try:
            reg = LinearRegression(**kwargs)
            reg.fit(X_train, y_train)
            logging.info("Linear Regression Model trained successfully")
            return reg

        except Exception as e:
            logging.error(f"Error while training Linear Regression Model: {e}")
            raise e

class RandomForestModel(Model):
    """
    Random Forest Model
    """
    def train(self, X_train, y_train, **kwargs):
        """
        Trains the model
        Args:
            X_train: Trainning data
            y_train: Training labels
            **kwargs: Additional parameters for the model
        returns: None
        """
        pass