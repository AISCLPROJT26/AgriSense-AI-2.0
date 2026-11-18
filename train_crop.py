import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. Load your dataset (update filename if yours is named differently)
csv_file = "Crop_recommendation.csv"

if not os.path.exists(csv_file):
    print(f"Error: '{csv_file}' not found in the project folder!")
    exit()

df = pd.read_csv(csv_file)

# 2. Separate features (N, P, K, temperature, humidity, ph, rainfall) and target (label)
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# 3. Split into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Train the Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 5. Evaluate model accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions) * 100
print(f"Model trained successfully! Test Accuracy: {accuracy:.2f}%")

# 6. Save the trained model using standard pickle
os.makedirs("models", exist_ok=True)
model_path = os.path.join("models", "crop_model.pkl")

with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Saved trained model to '{model_path}'")