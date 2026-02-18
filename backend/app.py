from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import json
import sqlite3

# --- 1. Initialize Flask App ---
app = Flask(__name__)
CORS(app)

# --- 2. Database Setup ---
DB_NAME = '../transactions.db'

def init_db():
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

# --- 3. Load Assets ---
try:
    model = joblib.load('../fraud_detection_model.joblib')
    scaler = joblib.load('../data_scaler.joblib')
    with open('../api_metadata.json', 'r') as f:
        metadata = json.load(f)

    MODEL_COLUMNS = metadata['final_model_columns']
    SCALED_COLS = metadata['scaled_numerical_cols']
    AMOUNT_BINS = metadata['amount_bin_edges']
    AMOUNT_LABELS = metadata['amount_bin_labels']
    
    # Use the balanced threshold
    OPTIMAL_THRESHOLD = 0.2500

    print("✅ Model, scaler, and metadata loaded successfully!")
    init_db()
except FileNotFoundError:
    print("❌ Missing model/scaler/metadata files.")
    model, scaler, metadata = None, None, None

# --- 4. Preprocessing Function (FIXED) ---
def preprocess_input(input_data):
    # Normalize strings (e.g., "visa " -> "Visa")
    normalized_data = {}
    
    # Map Title Case back to the specific casing your model expects
    acronym_fixes = {
        "Pos": "POS",
        "Pin": "PIN",
        "Cvc": "CVC",
        "Usa": "USA",
        "Uae": "UAE",
        "Mastercard": "MasterCard" 
    }

    for key, value in input_data.items():
        if isinstance(value, str):
            # First, apply standard Title Case (e.g., "pos" -> "Pos")
            val = value.strip().title()
            
            # Then, fix specific acronyms if they exist in our map
            if val in acronym_fixes:
                val = acronym_fixes[val]
                
            normalized_data[key] = val
        else:
            normalized_data[key] = value

    df = pd.DataFrame([normalized_data])

    # --- Feature engineering ---
    country_trans = df.get('Country of Transaction', 'Unknown')
    country_res = df.get('Country of Residence', 'Unknown')
    shipping = df.get('Shipping Address', 'Unknown')
    
    df['is_international'] = (country_trans != country_res).astype(int)
    df['shipping_mismatch'] = (shipping != country_res).astype(int)
    df['transaction_frequency'] = 1
    
    # Amount binning
    df['amount_bins'] = pd.cut(
        df['Amount'], 
        bins=AMOUNT_BINS, 
        labels=AMOUNT_LABELS, 
        include_lowest=True
    )
    
    # Risk feature
    df['age_amount_risk'] = np.where(
        (df['Age'] < 20) & (df['amount_bins'].isin(['high_amount', 'very_high_amount'])), 
        1, 0
    )

    # --- Column alignment ---
    final_df = pd.DataFrame(columns=MODEL_COLUMNS)
    final_df.loc[0] = 0

    # Numerical columns
    numerical_map = {
        'Amount': 'Amount',
        'Age': 'Age',
        'transaction_frequency': 'transaction_frequency',
        'is_international': 'is_international',
        'shipping_mismatch': 'shipping_mismatch',
        'age_amount_risk': 'age_amount_risk'
    }
    for input_name, col_name in numerical_map.items():
        if input_name in df.columns and col_name in final_df.columns:
            final_df[col_name] = df[input_name]

    # Categorical columns
    categorical_cols = ['Type of Card', 'Entry Mode', 'Type of Transaction', 'Merchant Group', 
                        'Gender', 'Bank', 'Day of Week', 'amount_bins']
    
    for col in categorical_cols:
        if col in df.columns:
            value = df[col].iloc[0]
            # This matches pandas get_dummies format: "Original Column_Value"
            one_hot_col = f"{col}_{value}"
            
            if one_hot_col in final_df.columns:
                final_df[one_hot_col] = 1
            else:
                print(f"⚠️ Unseen category: {one_hot_col}")

    # Scale numerical features
    final_df[SCALED_COLS] = scaler.transform(final_df[SCALED_COLS])
    
    return final_df

# --- 5. API Endpoints ---
@app.route('/', methods=['GET'])
def hello():
    return "Fraud Detection API is Running"

@app.route('/predict', methods=['POST'])
def predict_fraud():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    try:
        input_data = request.get_json()
        processed_data = preprocess_input(input_data)
        
        probability = model.predict_proba(processed_data)[0][1]
        is_fraudulent = probability >= OPTIMAL_THRESHOLD
        prediction_text = 'Fraudulent' if is_fraudulent else 'Legitimate'

        # Log to DB
        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO transactions (amount, age, bank, merchant_group, is_fraudulent, fraud_probability) VALUES (?, ?, ?, ?, ?, ?)",
                (input_data.get('Amount'), input_data.get('Age'), input_data.get('Bank'), input_data.get('Merchant Group'), is_fraudulent, probability)
            )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB Error: {e}")

        return jsonify({'prediction': prediction_text, 'probability_score': round(probability, 4)})
    
    except Exception as e:
        print(f"Prediction Error: {e}")
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)