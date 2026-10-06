# --- source
https://github.com/ayush714/mlops-projects-course/tree/main

# --- setup

cd proj1_MLOps

pip install zenml["server"]

zenml init

zenml downgrade

-- khoi chay zenml
zenml up --blocking

# --- run
python run_pipeline.py

# --- zenml
http://127.0.0.1:8237