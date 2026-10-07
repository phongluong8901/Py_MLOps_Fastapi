# --- 

# --- setup
cd proj3_FastApi_ML_2

- chay powershell admin
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

python -m venv .venv
<!-- source venv/bin/activate -->
.venv\Scripts\Activate.ps1


# --- install
pip install fastapi uvicorn 


# --- run
cd proj3_FastApi_ML_2

uvicorn main:app --reload
uvicorn app:app --reload


# --- swagger
http://127.0.0.1:8000/docs

# --- about
http://127.0.0.1:8000/about


# --- tat venv
deactivate

# --- front end
streamlit run frontend.py

# --- tao ra file requirement
pip freeze > requirements.txt