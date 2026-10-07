#Api et, post, request, response, json

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class LoanApplication(BaseModel):
    age: int
    income: float
    loan_amount: float
    employee_years: int
    
@app.post("/predict")
def predict_loan(application: LoanApplication):

    #pretend this trained model
    if application.income > 5000 and application.employee_years > 2:
        decision = "approved"
    else:
        decision = "rejected"

    return {
        "application_age": application.age,
        "approved_status": decision
    }

@app.get("/customer/{customer_id}")
def get_customer(customer_id: int):
    return {
        "customer_id": customer_id
    }