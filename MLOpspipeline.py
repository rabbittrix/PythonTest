import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib
import time
import pickle
import os

# Mock data generation (for demonstration purposes)
def generate_mock_data():
    data = {
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [5, 4, 3, 2, 1],
        'target': [10, 20, 30, 40, 50]
    }
    return pd.DataFrame(data)

# Step 1: Data Preparation
def prepare_data():
    data = generate_mock_data()

    X = data.drop(columns=['target'])
    y = data['target']

    # Save training and test data to files
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    if not os.path.exists('PythonCode/treining'):
        os.makedirs('PythonCode/treining')
    with open('PythonCode/treining/X_train.pkl', 'wb') as f:
        pickle.dump(X_train, f)
    with open('PythonCode/treining/X_test.pkl', 'wb') as f:
        pickle.dump(X_test, f)
    with open('PythonCode/treining/y_train.pkl', 'wb') as f:
        pickle.dump(y_train, f)
    with open('PythonCode/treining/y_test.pkl', 'wb') as f:
        pickle.dump(y_test, f)

    return X_train, X_test, y_train, y_test

# Step 2: Model Training
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

# Step 3: Model Evaluation
def evaluate_model(model, X_test, y_test):
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    print(f"Mean Squared Error: {mse}")

# Step 4: Model Deployment
def deploy_model(model):
    joblib.dump(model, 'PythonCode/treining/trained_model.pkl')
    print("Model deployed successfully!")

# Step 5: Monitoring and Maintenance (Mocked)
def monitor_and_maintain():
    while True:
        print("Monitoring model...")
        # Simulate monitoring for 5 seconds
        time.sleep(5)

def load_model_and_display():
    try:
        loaded_model = joblib.load('PythonCode/treining/trained_model.pkl')
        coefficients = loaded_model.coef_
        show_model_coefficients(coefficients)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo trained_model.pkl não encontrado!")

def show_model_coefficients(coefficients):
    root = tk.Tk()
    root.title("Coeficientes do Modelo")
    label = tk.Label(root, text="Coeficientes do Modelo:")
    label.pack()
    for idx, coef in enumerate(coefficients):
        label_coef = tk.Label(root, text=f"Coeficiente {idx+1}: {coef}")
        label_coef.pack()
    root.mainloop()

if __name__ == "__main__":
    # Step 1: Data Preparation
    X_train, X_test, y_train, y_test = prepare_data()

    # Step 2: Model Training
    model = train_model(X_train, y_train)

    # Step 3: Model Evaluation
    evaluate_model(model, X_test, y_test)

    # Step 4: Model Deployment
    deploy_model(model)

    # Step 5: Monitoring and Maintenance
    monitor_and_maintain()

    # Step 6: Load and inspect trained model
    loaded_model = joblib.load('PythonCode/treining/trained_model.pkl')
    print("Trained model loaded successfully.")
    print("Model Coefficients:", loaded_model.coef_)

    # Load and inspect data used for training and testing
    with open('PythonCode/treining/X_train.pkl', 'rb') as f:
        loaded_X_train = pickle.load(f)
    with open('PythonCode/treining/X_test.pkl', 'rb') as f:
        loaded_X_test = pickle.load(f)
    with open('PythonCode/treining/y_train.pkl', 'rb') as f:
        loaded_y_train = pickle.load(f)
    with open('PythonCode/treining/y_test.pkl', 'rb') as f:
        loaded_y_test = pickle.load(f)

    print("\nData used for training:")
    print("X_train:", loaded_X_train)
    print("y_train:", loaded_y_train)
    print("\nData used for testing:")
    print("X_test:", loaded_X_test)
    print("y_test:", loaded_y_test)
