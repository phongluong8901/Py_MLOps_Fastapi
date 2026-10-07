import streamlit as st
import requests

# Cấu hình trang (Phải đặt ở dòng đầu tiên của Streamlit script)
st.set_page_config(
    page_title="Insurance Premium Predictor",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000/predict"

# --- SIDEBAR: THÔNG TIN & TRẠNG THÁI HỆ THỐNG ---
with st.sidebar:
    st.image("https://img.icons8.com/color/96/health-book.png", width=80)
    st.title("System Status")
    
    # Kiểm tra nhanh kết nối tới FastAPI
    try:
        health_check = requests.get("http://127.0.0.1:8000/")
        if health_check.status_code == 200:
            st.success("🟢 API Server: Connected")
        else:
            st.warning("🟡 API Server: Responding with issues")
    except:
        st.error("🔴 API Server: Offline\n*(Run your FastAPI backend)*")
        
    st.markdown("---")
    st.markdown("### 💡 Hướng dẫn sử dụng")
    st.info("Điền đầy đủ thông tin cá nhân và các chỉ số sức khỏe của bạn vào form bên cạnh, sau đó nhấn **Predict Premium Category** để hệ thống dự đoán.")

# --- MAIN PAGE: TIÊU ĐỀ ---
st.title("🏥 Insurance Premium Predictor")
st.markdown("Hệ thống dự đoán phân khúc gói bảo hiểm y tế thông minh tích hợp **FastAPI** & **Machine Learning**.")
st.markdown("---")

# --- FORM NHẬP LIỆU (CHIA 2 CỘT CHO THOÁNG GIAO DIỆN) ---
with st.form("prediction_form"):
    st.subheader("📝 Nhập thông tin chi tiết")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Tuổi (Age)", min_value=1, max_value=119, value=30, help="Độ tuổi từ 1 đến 119")
        weight = st.number_input("Cân nặng (kg)", min_value=1.0, value=65.0, format="%.1f")
        height = st.number_input("Chiều cao (m)", min_value=0.5, max_value=2.5, value=1.70, format="%.2f")
        income_lpa = st.number_input("Thu nhập hàng năm (LPA)", min_value=0.1, value=10.0, format="%.1f")
        
    with col2:
        smoker = st.selectbox("Bạn có hút thuốc không? (Smoker)", options=[False, True], format_func=lambda x: "Có (Yes)" if x else "Không (No)")
        city = st.text_input("Thành phố sinh sống (City)", value="Mumbai")
        occupation = st.selectbox(
            "Nghề nghiệp (Occupation)",
            options=['private_job', 'government_job', 'business_owner', 'freelancer', 'student', 'retired', 'unemployed'],
            format_func=lambda x: x.replace("_", " ").title()
        )
    
    st.markdown("")
    # Nút submit căn giữa hoặc trải dài
    submitted = st.form_submit_button("🚀 Predict Premium Category", use_container_width=True)

# --- XỬ LÝ KHI NHẤN NÚT ---
if submitted:
    input_data = {
        "age": age,
        "weight": weight,
        "height": height,
        "income_lpa": income_lpa,
        "smoker": smoker,
        "city": city,
        "occupation": occupation
    }

    # Hiệu ứng Loading chuyên nghiệp trong lúc gọi API
    with st.spinner("⏳ Đang phân tích dữ liệu và tính toán từ mô hình ML..."):
        try:
            response = requests.post(API_URL, json=input_data)
            result = response.json()

            if response.status_code == 200:
                prediction_res = result.get("prediction")
                
                st.markdown("---")
                st.success("🎉 Dự đoán thành công!")
                
                if isinstance(prediction_res, dict):
                    predicted_category = prediction_res.get("predicted_category", "N/A")
                    confidence = prediction_res.get("confidence", 0)
                    
                    col_res1, col_res2 = st.columns(2)
                    with col_res1:
                        st.metric(
                            label="🎯 Phân khúc gói bảo hiểm (Predicted Category)", 
                            value=str(predicted_category).upper()
                        )
                    with col_res2:
                        st.metric(
                            label="📊 Độ tin cậy (Confidence)", 
                            value=f"{confidence * 100:.1f}%"
                        )
                else:
                    st.metric(
                        label="🎯 Phân khúc gói bảo hiểm (Predicted Category)", 
                        value=str(prediction_res).upper()
                    )
                
                # Hiển thị dữ liệu đã gửi kèm các trường phái sinh (Computed fields như BMI, City Tier...) bên trong Expander gọn gàng
                with st.expander("🔍 Xem chi tiết thông số & dữ liệu phân tích hệ thống"):
                    st.json(result)

            else:
                st.error(f"⚠️ Lỗi từ hệ thống API (Mã lỗi: {response.status_code})")
                st.json(result)

        except requests.exceptions.ConnectionError:
            st.error("❌ Không thể kết nối tới máy chủ FastAPI! Hãy chắc chắn rằng bạn đã chạy lệnh khởi động backend (`uvicorn main:app --reload`).")