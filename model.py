import joblib
import warnings


warnings.filterwarnings("ignore", message="Some specific warning message")

def predict(symptoms):
    model = joblib.load('disease_prediction_model.joblib')
    # new_symptoms = ["fever", "bodypain"]
    new_predictions = model.predict(symptoms)
    print("Predicted diseases for new symptoms:", new_predictions)
    return new_predictions
