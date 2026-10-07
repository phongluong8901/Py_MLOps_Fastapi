#Path and Quey parameters (Path, Query & Optional Params)
from fastapi import FastAPI

app = FastAPI()

all_customers = [
    {"id": 101, "name": "pg", "city": "hcm", "risk": "low"},
    {"id": 102, "name": "pg2", "city": "hcm", "risk": "high"},
    {"id": 103, "name": "pg3", "city": "hcm", "risk": "medium"},
    {"id": 104, "name": "pg4", "city": "hcm", "risk": "medium"},
]

#thông báo cho FastAPI rằng hàm phía dưới sẽ xử lý phương thức HTTP GET khi có yêu cầu truy cập vào đường dẫn /customers.
@app.get("/customers")
def get_customers(city: str, risk: str): #Query Parameters (tham số truy vấn trên URL, ví dụ: /customers?city=hcm&risk=low)
    #Chỉ giữ lại những khách hàng có city khớp với tham số city được truyền vào URL và risk khớp với tham số risk được truyền vào.
    filtered = [
        c for c in all_customers
            if c["city"] == city and c["risk"] == risk
    ]

    return {
        "city": city,
        "risk": risk,
        "count": len(filtered),
        "results": filtered
    }