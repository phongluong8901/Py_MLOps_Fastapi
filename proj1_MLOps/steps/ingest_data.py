import logging
import pandas as pd
from zenml import step

class IngestData:
    """
    Ingaesting the data from the data_path
    """
    def __init__(self, data_path: str):
        """
        Args:
            data_path (str): The path to the data file
        """
        self.data_path = data_path

    def get_data(self):
        """
        Get the data from the data_path
        Returns:
            pd.DataFrame: The ingested data
        """
        logging.info(f"Ingesting data from {self.data_path}")
        df = pd.read_csv(self.data_path)

        # Debug information
        logging.info(f"DEBUG - Columns: {df.columns.tolist()}")
        logging.info(f"DEBUG - DataFrame shape: {df.shape}")

        return df

@step #Decorator của ZenML: Biến hàm bên dưới thành một "Step" để ZenML có thể quản lý, theo dõi dữ liệu đầu vào/đầu ra
#Kiểu dữ liệu trả về: Ký hiệu -> cho biết hàm này sau khi chạy xong sẽ trả về kết quả thuộc kiểu dữ liệu pd.DataFrame (bảng dữ liệu của thư viện Pandas).
def ingest_df(data_path: str) -> pd.DataFrame:
    """
    Ingest data from the data path
    Args:
        data_path (str): The path to the data file
    Returns:
        pd.DataFrame: The ingested data
    """
    try:
        #Khởi tạo đối tượng IngestData từ class thuần Python ở trên, truyền vào đường dẫn file
        ingest_data = IngestData(data_path)
        #Gọi phương thức get_data() để đọc dữ liệu
        df = ingest_data.get_data()
        return df
    except Exception as e:
        logging.error(f"Error while ingesting data: {e}")
        raise e








        