import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def recommend_crop(N, P, K, temperature, humidity, ph, rainfall):
    """
    Predict best crop based on soil and weather parameters.
    Falls back to heuristic rules if the ML model pickle isn't found.
    """
    model_path = BASE_DIR / "models" / "crop_model.pkl"
    
    if model_path.exists():
        try:
            model = joblib.load(model_path)
            prediction = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])
            return prediction[0]
        except Exception as e:
            print(f"[Crop Model Error] Failed to load trained model: {e}")

    # Robust heuristic fallback engine for testing & demonstration
    if rainfall > 200 and humidity > 75:
        return "Rice"
    elif temperature > 28 and rainfall < 90:
        return "Cotton"
    elif ph < 6.0:
        return "Tea / Coffee"
    elif N > 80 and P > 40 and K > 40:
        return "Maize / Wheat"
    elif temperature > 24 and humidity > 60:
        return "Vegetables (Tomato / Chili)"
    else:
        return "Watermelon"