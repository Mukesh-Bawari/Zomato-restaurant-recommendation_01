from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import sys

# Ensure project root is in path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from phase1.data_loader import load_zomato_dataset
from phase3.logic import filter_restaurants
from phase4.groq_service import get_ai_recommendations

app = Flask(__name__)
CORS(app)

# Global variable to hold the dataset
df = None

@app.before_request
def initialize_dataset():
    global df
    if df is None:
        print("Initial data loading...")
        df = load_zomato_dataset()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    global df
    if df is None:
        return jsonify({"error": "Dataset not loaded yet"}), 503
    
    data = request.json
    location = data.get('location')
    budget = data.get('budget')
    
    if not location or budget is None:
        return jsonify({"error": "Missing location or budget"}), 400
    
    try:
        budget = float(budget)
    except ValueError:
        return jsonify({"error": "Invalid budget format"}), 400
    
    print(f"Web Request: Location={location}, Budget={budget}")
    
    # Existing Phase 3 logic
    filtered_df = filter_restaurants(df, location, budget)
    
    if filtered_df.empty:
        return jsonify({
            "recommendation": "No restaurants found matching your criteria. Try a broader location or increase your budget."
        })

    # Existing Phase 4 logic
    recommendation = get_ai_recommendations(filtered_df, {"location": location, "budget": budget})
    
    return jsonify({"recommendation": recommendation})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
