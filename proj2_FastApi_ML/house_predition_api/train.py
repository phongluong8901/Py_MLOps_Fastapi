# ==========================================
# 1. KHAI BÁO THƯ VIỆN
# ==========================================
from sklearn.datasets import fetch_california_housing  # Tải bộ dữ liệu giá nhà California mẫu
from sklearn.ensemble import RandomForestRegressor      # Mô hình học máy dạng Rừng ngẫu nhiên (Hồi quy)
from sklearn.model_selection import train_test_split    # Hàm chia dữ liệu thành tập Train và Test
from sklearn.metrics import mean_absolute_error, r2_score # Các hàm đo lường độ chính xác của mô hình

import pandas as pd  # Thư viện xử lý dữ liệu dạng bảng (DataFrame)
import joblib        # Thư viện lưu mô hình và danh sách cột ra ổ cứng

# ==========================================
# 2. TẢI VÀ CHUẨN BỊ DỮ LIỆU
# ==========================================
print("loading datasets")
data = fetch_california_housing()

# Tách dữ liệu thành 2 phần độc lập:
# - X: Các đặc trưng đầu vào (thu nhập, số phòng, tuổi nhà,...)
# - y: Nhãn mục tiêu đầu ra (giá nhà trung bình cần dự đoán)
X = pd.DataFrame(data.data, columns=data.feature_names)
y = data.target

print(f"total recors: {X.shape[0]}") # In ra tổng số dòng dữ liệu (hơn 20,600 dòng)

# Chia dữ liệu: 80% để huấn luyện (train), 20% để kiểm tra (test)
# random_state=42 giúp kết quả chia ngẫu nhiên luôn cố định ở mọi lần chạy
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 3. HUẤN LUYỆN MÔ HÌNH (TRAINING)
# ==========================================
print("Training model...")
# Khởi tạo mô hình Random Forest với 100 cây quyết định (n_estimators=100)
model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

# Cho mô hình "học" từ tập huấn luyện (X_train và y_train)
model.fit(X_train, y_train)

# ==========================================
# 4. DỰ ĐOÁN VÀ ĐÁNH GIÁ (EVALUATION)
# ==========================================
# Dùng mô hình đã học để dự đoán giá nhà trên tập kiểm tra (X_test)
y_pred = model.predict(X_test)

# Tính toán các chỉ số đánh giá sai số và độ chính xác
mae = mean_absolute_error(y_test, y_pred) # Sai số tuyệt đối trung bình
r2 = r2_score(y_test, y_pred)             # Hệ số xác định R² (độ phù hợp, càng gần 1 càng tốt)

print(f"average error: {mae:.2f}")
print(f"value average error: {mae * 100000:.0f}") # Quy đổi ra tiền thực tế (đơn vị gốc tính theo trăm ngìn USD)
print(f"Accuracy (R2): {r2:.2f}")

# ==========================================
# 5. LƯU MÔ HÌNH VÀO Ổ CỨNG (SERIALIZATION)
# ==========================================
# Lưu mô hình đã train thành file để sau này tích hợp vào API (FastAPI)
joblib.dump(model, "house_model.joblib")

# Lưu lại danh sách tên các cột đặc trưng để đảm bảo sau này dữ liệu gửi lên API phải khớp thứ tự
joblib.dump(list(X.columns), "house_features.joblib")
print("Model and features saved successfully!")