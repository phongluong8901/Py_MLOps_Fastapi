# --- 

# --- setup
cd house_predition_api

- chay powershell admin
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

python -m venv .venv
source venv/bin/activate
.venv\Scripts\Activate.ps1


# --- install
pip install fastapi uvicorn scikit-learn pandas joblib
pip install python-multipart

# --- run
cd house_predition_api

uvicorn explore:app --reload
uvicorn train:app --reload
uvicorn main:app --reload



# --- swagger
http://127.0.0.1:8000/docs

# --- about
http://127.0.0.1:8000/about


# --- tat venv
deactivate

# --- start FE Nextjs
cd proj2_FastApi_ML
cd house_predition_api
cd frontend

npm run dev

# --- full workflow documentation
# Read WORKFLOW.md for detailed architecture & sequence diagrams

