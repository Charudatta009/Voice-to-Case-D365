from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from textblob import TextBlob

app = Flask(__name__)
CORS(app)


POWER_AUTOMATE_URL = os.getenv("POWER_AUTOMATE_URL", "https://cc552f5bc566e779901470aa8ccbed.d7.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/0ab258097fc64362af63c569438539c2/triggers/manual/paths/invoke/?api-version=1&tenantId=tId&environmentName=cc552f5b-c566-e779-9014-70aa8ccbedd7")

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    transcript = data.get('transcript', '')

    # Perform sentiment analysis
    blob = TextBlob(transcript)
    sentiment = blob.sentiment.polarity
    sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

    # Optional priority detection
    priority = "Normal"
    lowered = transcript.lower()
    if "urgent" in lowered or "asap" in lowered or "immediately" in lowered:
        priority = "High"

    # Send to Power Automate
    response = requests.post(POWER_AUTOMATE_URL, json={
        "transcript": transcript,
        "sentiment": sentiment_label,
        "priority": priority
    })

    return jsonify({"message": "Sent to D365", "status": response.status_code})

if __name__ == '__main__':
    app.run(debug=True)
