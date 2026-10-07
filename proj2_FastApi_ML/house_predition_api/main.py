import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from fastapi.responses import StreamingResponse
import io

# Khởi tạo ứng dụng FastAPI
app = FastAPI(title="California House Price Prediction API")

# Cấu hình CORS để cho phép Frontend kết nối
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================================
# 1. TẢI MÔ HÌNH VÀ CẤU HÌNH BAN ĐẦU
# ==========================================================
# Tải mô hình Random Forest đã được huấn luyện và lưu trước đó từ ổ cứng
model = joblib.load("house_model.joblib")

# Tải danh sách tên các đặc trưng (features) đã lưu
features = joblib.load("house_features.joblib")

# ==========================================================
# 2. ĐỊNH NGHĨA SCHEMA DỮ LIỆU ĐẦU VÀO (CHO API /predict)
# ==========================================================
class HouseFeatures(BaseModel):
    MedInc: float = Field(gt=0, description="Median income of Neighbourhood")
    HouseAge: float = Field(ge=0, description="Median age of house in block")
    AveRooms: float = Field(gt=0, description="Average number of rooms")
    AveBedrms: float = Field(gt=0, description="Average number of bedrooms")
    Population: float = Field(gt=0, description="Population")
    AveOccup: float = Field(gt=0, description="Average number of occupants")
    Latitude: float = Field(..., ge=-90, le=90, description="Latitude of house")
    Longitude: float = Field(..., ge=-180, le=180, description="Longitude of house")

# ==========================================================
# 3. CÁC ENDPOINT CƠ BẢN (TRANG CHỦ VÀ HEALTH CHECK)
# ==========================================================
@app.get("/")
def home():
    """Trang chủ API, thông báo trạng thái hoạt động."""
    return {
        "message": "California house prediction api",
        "status": "running",
        "endpoint": "send POST request to /predict"
    }

@app.get("/health")
def health():
    """Endpoint kiểm tra thông tin hệ thống và mô hình."""
    return {
        "status": "running",
        "model": "RandomForestRegressor",
        "features": features,
        "avg_error": "$39,000"
    }

# ==========================================================
# 4. ENDPOINT DỰ ĐOÁN CHO MỘT BẢN GHI (JSON PAYLOAD)
# ==========================================================
@app.post("/predict")
def predict(house: HouseFeatures):
    """Nhận dữ liệu JSON của 1 ngôi nhà và trả về giá dự đoán."""
    try:
        # Chuyển đổi dữ liệu nhận được từ Pydantic model thành DataFrame của Pandas
        input_data = pd.DataFrame([{
            "MedInc": house.MedInc,
            "HouseAge": house.HouseAge,
            "AveRooms": house.AveRooms,
            "AveBedrms": house.AveBedrms,
            "Population": house.Population,
            "AveOccup": house.AveOccup,
            "Latitude": house.Latitude,
            "Longitude": house.Longitude
        }])

        # Đưa dữ liệu vào mô hình để dự đoán (kết quả trả về là mảng, lấy phần tử đầu tiên [0])
        predicted = model.predict(input_data)[0]
        price_usd = predicted * 100000  # Quy đổi ra USD (vì dataset gốc tính theo đơn vị trăm nghìn)

        # Trả về kết quả dự đoán kèm theo khoảng tin cậy
        return {
            "predicted_price": f"${price_usd:,.0f}",
            "predicted_price_short": f"${predicted:.2f} hundred thousands",
            "confidence_range": f"${price_usd - 39000:,.0f} to${price_usd + 39000:,.0f}"
        }
    
    except Exception as e:
        # Bắt lỗi bất ngờ trong quá trình dự đoán và trả về HTTP 400
        raise HTTPException(
            status_code=400,
            detail=f"prediction failed: {str(e)}"
        )

# ==========================================================
# 5. ENDPOINT DỰ ĐOÁN HÀNG LOẠT QUA FILE CSV (BATCH PREDICTION)
# ==========================================================
@app.post("/predict-file")
async def predict_file(file: UploadFile = File(...)):
    """Nhận file CSV chứa nhiều dòng dữ liệu, dự đoán hàng loạt và trả về file CSV kết quả."""
    
    # Kiểm tra xem file tải lên có đúng định dạng .csv không
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a CSV File only"
        )

    # Đọc nội dung thô của file dưới dạng bytes bất đồng bộ (async)
    contents = await file.read()

    try:
        # Đọc dữ liệu từ mảng bytes thành DataFrame của Pandas
        df = pd.read_csv(io.BytesIO(contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV file format")

    # Khai báo danh sách các cột bắt buộc phải có trong file CSV
    required_columns = [
        'MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 
        'Population', 'AveOccup', 'Latitude', 'Longitude'
    ]

    # Kiểm tra xem file CSV thiếu cột nào so với yêu cầu không
    missing_columns = [
        col for col in required_columns
            if col not in df.columns
    ]

    if missing_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Missing columns: {', '.join(missing_columns)}"
        )

    # Kiểm tra xem file CSV có bị rỗng (không có dữ liệu dòng nào) không
    if len(df) == 0:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file has no data rows"
        )

    try:
        # Gọi mô hình dự đoán hàng loạt cho toàn bộ các dòng trong DataFrame
        predictions = model.predict(df[required_columns])
        
        # Gán kết quả dự đoán (đã nhân 100,000 để ra giá trị USD thực tế) vào cột mới của DataFrame
        df["predicted_price_usd"] = [f"${p * 100000:,.0f}" for p in predictions]
        
        # Chuyển đổi DataFrame kết quả thành chuỗi định dạng CSV
        output = df.to_csv(index=False)

        # Trả về file dưới dạng StreamingResponse để client có thể tải xuống tự động
        return StreamingResponse(
            io.StringIO(output), #StringIO đóng vai trò tạo ra một "tệp tin ảo nằm hoàn toàn trong bộ nhớ RAM" (In-memory text stream).
            media_type="text/csv",
            headers={
                "Content-Disposition": "attachment; filename=predictions.csv"
            }
        )

    except Exception as e:
        # Bắt lỗi hệ thống trong quá trình xử lý file và trả về HTTP 500
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )

# ==========================================================
# 6. KHỞI CHẠY SERVER (TÙY CHỌN)
# ==========================================================
# Đoạn code này dùng khi bạn muốn chạy trực tiếp file Python bằng lệnh `python main.py`
# Thông thường, ta hay chạy qua lệnh uvicorn trên terminal: `uvicorn main:app --reload`
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)