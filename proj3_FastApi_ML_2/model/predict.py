import pickle
import pandas as pd

# Mlflow
MODEL_VERSION = '1.0.0'

# Load mô hình Machine Learning đã được train
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Get class labels from model (important for matching probabilities to class names)
class_labels = model.classes_.tolist()

def predict_output(user_input):
    if isinstance(user_input, pd.DataFrame):
        df = user_input
    elif isinstance(user_input, dict):
        df = pd.DataFrame([user_input])
    else:
        df = pd.DataFrame(user_input)

    # Predict the class
    predicted_class = model.predict(df)[0]

    # Get probabilities for all classes
    probabilities = model.predict_proba(df)[0]
    confidence = float(max(probabilities))
    
    # Create mapping: {class_name: probability}
    class_probs = {
        str(cls): float(round(prob, 4))
        for cls, prob in zip(class_labels, probabilities)
    }

    return {
        "predicted_category": str(predicted_class),
        "confidence": round(confidence, 4),
        "class_probabilities": class_probs
    }