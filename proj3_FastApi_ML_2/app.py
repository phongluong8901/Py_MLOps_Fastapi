from schema.prediction_response import PredictionResponse
from model.predict import predict_output
from model.predict import model, MODEL_VERSION
from schema.user_input import UserInput
from fastapi import FastAPI
import pandas as pd
from fastapi.responses import JSONResponse

app = FastAPI()

#human reable
@app.get('/')
def home():
    return {
        'message': 'Insurance Premium Prediction APi'
    }

#machine reable
@app.get('/health')
def health_check():
    return {
        "status": "OK",
        "model": MODEL_VERSION,
        "version": model is not None
    }

@app.post('/predict', response_model=PredictionResponse)
def predict_premium(data: UserInput):
    try:
        # Đưa các trường dữ liệu đã qua tính toán tự động (computed fields) vào DataFrame để đưa vào mô hình ML
        user_input = pd.DataFrame([{
            'bmi': data.bmi,
            'age_group': data.age_group,
            'lifestyle_risk': data.lifestyle_risk,
            'city_tier': data.city_tier,
            'income_lpa': data.income_lpa,
            'occupation': data.occupation
        }])

        # Dự đoán kết quả từ model
        prediction = predict_output(user_input=user_input)
        
        return JSONResponse(
            status_code=200,
            content={
                "prediction": prediction,
                "message": "Premium predicted successfully",
                "data": data.model_dump() 
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "prediction": None,
                "message": "Premium predicted failed",
                "error": str(e),
                "data": None
            }
        )

# {
#   "age": 30,
#   "weight": 70.5,
#   "height": 1.75,
#   "income_lpa": 12.5,
#   "smoker": false,
#   "city": "Mumbai",
#   "occupation": "private_job"
# }