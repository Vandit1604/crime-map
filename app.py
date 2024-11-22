from flask import Flask, render_template, jsonify, request
import pandas as pd
import requests
import os

# Initialize Flask application
app = Flask(__name__)

# Load initial crime data from CSV
crime_data_path = 'tamil_nadu_crime_data.csv'
crime_data = pd.read_csv(crime_data_path)

# OpenAI API key (replace 'YOUR_OPENAI_API_KEY' with your actual key)
openai_api_key = os.getenv('YOUR_OPENAI_API_KEY')

def analyze_crime_data(text):
    """
    Analyzes crime data text using the OpenAI GPT API.
    """
    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {openai_api_key}'
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": text}],
            "temperature": 0.5
        }
    )
    return response.json()

@app.route('/')
def index():
    # Render the main HTML page with Google Maps
    return render_template('index.html')

@app.route('/crime-data')
def get_crime_data():
    # Convert crime data to JSON format for frontend
    data = crime_data.to_dict(orient='records')
    return jsonify(data)

@app.route('/crime-summary')
def get_crime_summary():
    """
    Summarizes crime data for plotting
    """
    # Group by city and crime type for summary
    summary = crime_data.groupby(['city', 'crime_type']).size().reset_index(name='count')
    summary_dict = summary.to_dict(orient='records')
    return jsonify(summary_dict)

@app.route('/crime-counts')
def get_crime_counts():
    """
    Aggregates crime data by city for displaying count markers
    """
    counts = crime_data.groupby(['city', 'latitude', 'longitude']).size().reset_index(name='count')
    counts_dict = counts.to_dict(orient='records')
    return jsonify(counts_dict)

@app.route('/upload-data', methods=['POST'])
def upload_data():
    """
    Endpoint to upload new crime data.
    """
    file = request.files['file']
    if file:
        global crime_data
        file_path = os.path.join('data/', file.filename)
        file.save(file_path)
        crime_data = pd.read_csv(file_path)  # Reload the data
        return jsonify({"message": "File uploaded successfully."}), 200
    return jsonify({"error": "File not uploaded."}), 400

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint to analyze crime data using OpenAI's GPT.
    Accepts a JSON body with 'text' field.
    """
    text = request.json.get('text')
    if text:
        analysis_result = analyze_crime_data(text)
        return jsonify(analysis_result)
    return jsonify({"error": "No text provided"}), 400

@app.route('/crime-details')
def get_crime_details():
    """
    Retrieves detailed crime data by city.
    """
    data = crime_data.to_dict(orient='records')
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
