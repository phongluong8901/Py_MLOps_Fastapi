# --- source
https://github.com/ayush714/mlops-projects-course/tree/main

# --- setup

cd proj1_MLOps

pip install zenml["server"]

zenml init

zenml downgrade

pip install mlflow

zenml integration install mlflow -y

zenml stack list

zenml stack describe

# --- tich hop mlflow vao zenml
pip install zenml mlflow zenml[mlflow]

zenml integration install mlflow -y

zenml mlflow tracker register my_mlflow_tracker --tracking_uri="http://localhost:5000"

zenml experiment-tracker register my_mlflow_tracker --flavor=mlflow --tracking_uri="file:///d:/A_Self_Proj/learn_mlflow/proj1_MLOps/mlruns"

zenml stack register my_stack -a default -o default -e my_mlflow_tracker --set

zenml stack describe

-- khoi chay zenml
zenml up --blocking

zenml down

# --- run
python run_pipeline.py

# --- zenml
http://127.0.0.1:8237

# --- mlflow
