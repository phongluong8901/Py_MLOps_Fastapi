# --- 

# --- setup
cd proj2_FastApi_ML
mkdir fastapi-project
cd fastapi-project

- chay powershell admin
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

python -m venv .venv
source venv/bin/activate
.venv\Scripts\Activate.ps1


# --- install
pip install fastapi uvicorn

# --- run
cd proj2_FastApi_ML

uvicorn main:app --reload
uvicorn loan:app --reload
uvicorn path_p:app --reload
uvicorn query:app --reload
uvicorn pyd:app --reload
uvicorn main_s:app --reload


# --- swagger
http://127.0.0.1:8000/docs

# --- about
http://127.0.0.1:8000/about


# --- tat venv
deactivate