from typing import Union
import logging
from abc import ABC, abstractmethod

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# Lớp trừu tượng định nghĩa khuôn mẫu chung
class DataStrategy(ABC):
    """
    Abstract class defining strategy for handling data
    """

    @abstractmethod #Khai báo hàm trừu tượng. Mọi class con kế thừa DataStrategy BẮT BUỘC phải viết lại hàm này, nếu không sẽ báo lỗi.
    def handle_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        pass

# Lớp con triển khai (implement) khuôn mẫu
class DataPreProcessingStrategy(DataStrategy):
    """
    Strategy for preprocessing data
    """

    def handle_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess data
        """
        try:
            #Xóa các cột chứa thời gian không cần thiết cho mô hình học máy (chỉ xóa nếu cột tồn tại)
            cols_to_drop_time = [
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date",
                "order_estimated_delivery_date",
                "order_purchase_timestamp",
            ]
            data = data.drop(columns=[col for col in cols_to_drop_time if col in data.columns], errors='ignore')

            #Điền các giá trị bị thiếu (NaN) ở các cột kích thước sản phẩm bằng giá trị trung vị (median) (chỉ điền nếu cột tồn tại)
            for col in ["product_weight_g", "product_length_cm", "product_width_cm", "product_height_cm"]:
                if col in data.columns:
                    data[col] = data[col].fillna(data[col].median())

            #Điền chữ "No review" cho các ô đánh giá bị trống (chỉ điền nếu cột tồn tại)
            if "review_comment_message" in data.columns:
                data["review_comment_message"] = data["review_comment_message"].fillna("No review")

            #Chỉ lọc và giữ lại các cột có kiểu dữ liệu là số
            data = data.select_dtypes(include=[np.number])

            # Xóa thêm một số cột dạng số nhưng không mang lại giá trị dự đoán (chỉ xóa nếu cột tồn tại)
            cols_to_drop = ["customer_zip_prefix", "order_item_id"]
            data = data.drop(columns=[col for col in cols_to_drop if col in data.columns], errors='ignore')

            return data

        except Exception as e:
            #Nếu có lỗi xảy ra trong quá trình tiền xử lý, ghi log lại và ném lỗi ra ngoài
            logging.error(f"Error while preprocessing data: {e}")
            raise e

# Lớp con triển khai chiến lược chia tách dữ liệu
class DataDivideStrategy(DataStrategy):
    """
    Strategy for dividing data into train and test
    """

    # Hàm này có thể trả về kiểu dữ liệu là pd.DataFrame HOẶC kiểu dữ liệu là pd.Series.
    def handle_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, pd.Series]:
        """
        Divide data into train and test
        """

        try:
            target_col = "review_score"
            
            # Kiểm tra xem cột mục tiêu có tồn tại hay không để tránh lỗi KeyError
            if target_col not in data.columns:
                raise KeyError(
                    f"Cột mục tiêu '{target_col}' không tồn tại trong DataFrame. "
                    "Hãy chắc chắn bạn đang sử dụng file dữ liệu tổng hợp (merged dataset) thay vì file đơn lẻ."
                )

            # Tách tập dữ liệu
            X = data.drop([target_col], axis=1)
            y = data[target_col]

            # Chia dữ liệu thành tập Train (80%) và Test (20%)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            return X_train, X_test, y_train, y_test

        except Exception as e:
            logging.error(f"Error while dividing data: {e}")
            raise e

# Lớp DataCleaning (Không đổi)
class DataCleaning:
    """
    Class for cleaning data which processes the data and divides it tinto train and test
    """
    def __init__(self, data: pd.DataFrame, strategy: DataStrategy):
        # Hàm khởi tạo: Nhận vào bảng dữ liệu thô (data) và một "chiến lược" (strategy) bất kỳ (tiền xử lý hoặc chia dữ liệu)
        self.data = data
        self.strategy = strategy

    def handle_data(self) -> Union[pd.DataFrame, pd.Series]:
        """
        Handle data
        """
        try:
            #Thực thi phương thức handle_data dựa trên chiến lược đã được truyền vào ở trên một cách linh hoạt
            return self.strategy.handle_data(self.data)
        except Exception as e:
            logging.error(f"Error while handling data: {e}")
            raise e

# Đoạn code mẫu dùng để test thủ công bên ngoài ZenML nếu cần

# if __name__ == "__main__":
#     data = pd.read_csv("./data/olist_customers_dataset.csv")
#     data_cleaning = DataCleaning(data, DataPreProcessingStrategy())
#     data = data_cleaning.handle_data()