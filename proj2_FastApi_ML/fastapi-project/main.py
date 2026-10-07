from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "myfirst API i working"}

@app.get("/about")
def about():
    return {"project": "loan risk model", "version": "1.0.0"}

# http://127.0.0.1:8000/customer?customer_id=01
@app.get("/customer")
def get_customer(customer_id: int):
    return {
        "customer_id": customer_id,
        "Name": "pg",
        "status": "active"
    }