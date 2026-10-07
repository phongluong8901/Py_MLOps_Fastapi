#Request Body: pydantic model and input validation

from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class LoanApplication(BaseModel):
    name: str
    age: int
    income: float
    loan_amount: float
    employee_years: int

@app.post("predcit")
def predict_loan(application: LoanApplication):
    #model login
    #Nếu tất cả 3 điều kiện trên đều đúng, approved sẽ mang giá trị True
    approved = (
        application.income > 50000 and 
        application.employee_years > 2 and
        application.age >= 21
    )

    return {
        "application name": application.name,
        "loan_amount": application.loan_amount,
        "decision": "appoved" if approved else "rejected",
        "review_income": application.income
    }