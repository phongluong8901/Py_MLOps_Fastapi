from zenml import pipeline
from steps.ingest_data import ingest_df
from steps.clean_data import clean_df
from steps.model_train import train_model
from steps.evaluation import evaluate_model
from steps.config import ModelNameConfig # Nhớ import class config vào

@pipeline(enable_cache=False)
def training_pipeline(data_path: str):
    # Đọc dữ liệu
    df = ingest_df(data_path)

    # Làm sạch dữ liệu
    X_train, X_test, y_train, y_test = clean_df(df)

    # Khởi tạo config (ví dụ: dùng LinearRegression)
    model_config = ModelNameConfig(model_name="LinearRegression")

    # Gọi step train_model và truyền config vào 👇
    model = train_model(
        X_train=X_train, 
        y_train=y_train, 
        X_test=X_test, 
        y_test=y_test, 
        config=model_config
    )

    # Đánh giá model
    r2_score, rmse = evaluate_model(model, X_test, y_test)