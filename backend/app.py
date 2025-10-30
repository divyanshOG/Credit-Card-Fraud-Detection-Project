from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
import json
import sqlite3 # Import the database library

# --- 1. Initialize Flask App ---
app = Flask(__name__)

# --- Database Setup ---
DB_NAME = '../transactions.db' # The database file will be saved in your main project folder

def init_db():
    """Creates the database table if it doesn't exist."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        # This is the SQL schema we designed earlier
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
# --- End of DB Setup ---


# --- 2. Load All Assets ---
try:
    model = joblib.load('../fraud_detection_model.joblib')
    
    with open('../api_metadata.json', 'r') as f:
        metadata = json.load(f)
    
    MODEL_COLUMNS = metadata['final_model_columns']
    AMOUNT_BINS = metadata['amount_bin_edges']
    AMOUNT_LABELS = metadata['amount_bin_labels']
    OPTIMAL_THRESHOLD = 0.6500

    print("✅ Model and metadata loaded successfully!")
    
    # Initialize the database when the app starts
    init_db()

except FileNotFoundError:
    print("❌ Error: Missing a .joblib or .json file. Please check file paths.")
    model = None
    metadata = None

# --- 3. Preprocessing Function ---
def preprocess_input(input_data):
    """
    Takes the raw JSON input from the frontend and prepares it
    into the exact DataFrame format the model was trained on.
    """
    
    df = pd.DataFrame([input_data])
    
    # Feature Engineering
    df['is_international'] = (df['Country of Transaction'] != df['Country of Residence']).astype(int)
    df['shipping_mismatch'] = (df['Shipping Address'] != df['Country of Residence']).astype(int)
    df['transaction_frequency'] = 1 
    
    df['amount_bins'] = pd.cut(
        df['Amount'], 
        bins=AMOUNT_BINS, 
        labels=AMOUNT_LABELS, 
        include_lowest=True
    )
    
    # One-Hot Encoding & Column Alignment
    final_df = pd.DataFrame(columns=MODEL_COLUMNS)
    final_df.loc[0] = 0
    
    numerical_cols = ['Amount', 'Age', 'transaction_frequency']
    for col in numerical_cols:
        if col in df.columns:
            final_df[col] = df[col]
            
    for col in df.columns:
        if col in ['Type of Card', 'Entry Mode', 'Type of Transaction', 'Merchant Group', 
                   'Gender', 'Bank', 'Day of Week', 'amount_bins', 'shipping_mismatch', 
                   'is_international']:
            
            one_hot_col = f"{col}_{df[col].iloc[0]}"
            if one_hot_col in final_df.columns:
                final_df[one_hot_col] = 1

    return final_df

# --- 4. API Endpoints ---
@app.route('/', methods=['GET'])
def hello():
    return "Hello, world! The fraud detection API is running and all models are loaded."

@app.route('/predict', methods=['POST'])
def predict_fraud():
    if model is None:
        return jsonify({'error': 'Model is not loaded!'}), 500

    try:
        input_data = request.get_json()
        processed_data = preprocess_input(input_data)
        
        # Make a prediction
        probability = model.predict_proba(processed_data)[0][1] 
        is_fraudulent = probability >= OPTIMAL_THRESHOLD
        
        prediction_text = 'Fraudulent' if is_fraudulent else 'Legitimate'
        
        # --- NEW: Save to Database ---
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

# --- 5. Run the App ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)