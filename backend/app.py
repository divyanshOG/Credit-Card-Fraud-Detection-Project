from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import json
import sqlite3

# --- 1. Initialize Flask App ---
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# --- 2. Database Setup ---
DB_NAME = '../transactions.db' # The database file

def init_db():
    """Creates the database table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            amount FLOAT,
            age FLOAT,
            bank VARCHAR(100),
            merchant_group VARCHAR(100),
            is_fraudulent BOOLEAN,
            fraud_probability FLOAT
        );
        ''')
        conn.commit()
        conn.close()
        print("✅ Database table created successfully.")
    except Exception as e:
        print(f"❌ Error creating database: {str(e)}")

# --- 3. Load All Assets ---
try:
    # Load the model and metadata (NO SCALER)
    model = joblib.load('../fraud_detection_model.joblib')
    
    with open('../api_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    # Get our "rules" from the metadata file
    MODEL_COLUMNS = metadata['final_model_columns']
    AMOUNT_BINS = metadata['amount_bin_edges']
    AMOUNT_LABELS = metadata['amount_bin_labels']
    OPTIMAL_THRESHOLD = 0.6500 # Your champion threshold

    print("✅ Model and metadata loaded successfully!")
    
    # Initialize the database when the app starts
    init_db()

except FileNotFoundError:
    print("❌ Error: Missing a .joblib or .json file. Please check file paths.")
    model = None
    metadata = None

# --- 4. Preprocessing Function (CORRECTED) ---
def preprocess_input(input_data):
    """
    Takes the raw JSON input from the frontend and prepares it
    into the exact DataFrame format the model was trained on.
    """
    
    # Create a single-row DataFrame from the input JSON
    df = pd.DataFrame([input_data])
    
    # --- Feature Engineering (must match notebook) ---
    df['is_international'] = (df['Country of Transaction'] != df['Country of Residence']).astype(int)
    df['shipping_mismatch'] = (df['Shipping Address'] != df['Country of Residence']).astype(int)
    df['transaction_frequency'] = 1 # Default for a new transaction
    
    df['amount_bins'] = pd.cut(
        df['Amount'], 
        bins=AMOUNT_BINS, 
        labels=AMOUNT_LABELS, 
        include_lowest=True
    )
    
    # --- One-Hot Encoding & Column Alignment ---
    
    # Create an empty DataFrame with all model columns, filled with 0s
    final_df = pd.DataFrame(columns=MODEL_COLUMNS)
    final_df.loc[0] = 0
    
    # (FIXED) Fill in the numerical values, INCLUDING 'is_international'
    numerical_cols = ['Amount', 'Age', 'transaction_frequency', 'is_international']
    for col in numerical_cols:
        if col in df.columns:
            final_df[col] = df[col]
            
    # (FIXED) Create the one-hot columns, REMOVING 'is_international'
    categorical_inputs = ['Type of Card', 'Entry Mode', 'Type of Transaction', 'Merchant Group', 
                          'Gender', 'Bank', 'Day of Week', 'amount_bins', 'shipping_mismatch']
    
    for col in categorical_inputs:
        value = df[col].iloc[0]
        one_hot_col = f"{col}_{value}"
        if one_hot_col in final_df.columns:
            final_df[one_hot_col] = 1

    # --- NO SCALING STEP ---
    
    return final_df

# --- 5. API Endpoints ---
@app.route('/', methods=['GET'])
def hello():
    return "Hello, world! The fraud detection API is running and all models are loaded."

@app.route('/predict', methods=['POST'])
def predict_fraud():
    if model is None:
        return jsonify({'error': 'Model is not loaded!'}), 500

    try:
        input_data = request.get_json()

        # Input validation
        required_keys = [
            'Amount', 'Age', 'Type of Card', 'Entry Mode', 'Type of Transaction',
            'Merchant Group', 'Bank', 'Day of Week', 'Gender', 
            'Country of Transaction', 'Country of Residence', 'Shipping Address'
        ]
        missing_keys = [key for key in required_keys if key not in input_data]
        if missing_keys:
            return jsonify({'error': f'Missing input data for: {", ".join(missing_keys)}'}), 400
        
        processed_data = preprocess_input(input_data)
        
        # Make a prediction
        probability = model.predict_proba(processed_data)[0][1] 
        is_fraudulent = probability >= OPTIMAL_THRESHOLD
        
        prediction_text = 'Fraudulent' if is_fraudulent else 'Legitimate'
        
        # --- Save to Database ---
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (amount, age, bank, merchant_group, is_fraudulent, fraud_probability) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    input_data.get('Amount'),
                    input_data.get('Age'),
                    input_data.get('Bank'),
                    input_data.get('Merchant Group'),
                    is_fraudulent,
                    probability
                )
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error saving to database: {str(e)}")
        # --- End of DB save ---

        response = {
            'prediction': prediction_text,
            'probability_score': round(probability, 4)
        }
        return jsonify(response)
    
    except Exception as e:
        print(f"❌ Error during prediction: {str(e)}")
        return jsonify({'error': f'An error occurred: {str(e)}'}), 400

# --- 6. Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)