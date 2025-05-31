from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from textblob import TextBlob

app = Flask(__name__)
CORS(app)

# Hardcoded for now (ideally use os.getenv and environment variables)
TENANT_ID = "cb26282a-9ed2-4db5-be73-ba9a4a76d474"
CLIENT_ID = "9ee7b786-3135-40b9-a43a-7c91af437c24"
CLIENT_SECRET = "OUd8Q~8WFXp_vAVtlXH79b.Y.cgJLT3FnnzjTalb"
POWER_AUTOMATE_URL = "https://cc552f5bc566e779901470aa8ccbed.d7.environment.api.powerplatform.com:443/powerautomate/automations/direct/workflows/0ab258097fc64362af63c569438539c2/triggers/manual/paths/invoke/?api-version=1&tenantId=tId&environmentName=cc552f5b-c566-e779-9014-70aa8ccbedd7"

def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "scope": "https://service.flow.microsoft.com//.default"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]
    
def generate_title(transcript):
    if not transcript.strip():
        return "Voice Case"
    # Take first sentence or first 7 words, whichever feels meaningful
    first_sentence = transcript.split('.')[0]
    words = first_sentence.strip().split()
    return " ".join(words[:7]) + ("..." if len(words) > 7 else "")    

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    transcript = data.get('transcript', '')

    # Sentiment analysis
    blob = TextBlob(transcript)
    sentiment = blob.sentiment.polarity
    sentiment_label = "Positive" if sentiment > 0 else "Negative" if sentiment < 0 else "Neutral"

    # Priority check
    priority = "High" if any(word in transcript.lower() for word in ["urgent", "asap", "immediately"]) else "Normal"
     # Generate title
    title = generate_title(transcript)
    try:
        token = get_access_token()
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "transcript": transcript,
            "sentiment": sentiment_label,
            "priority": priority
        }

        response = requests.post(POWER_AUTOMATE_URL, headers=headers, json=payload)

        # print("Power Automate response:", response.status_code, response.text)

        if response.status_code in [200, 202]:
            return jsonify({
                "message": "✅ Case created in D365",
                "status": response.status_code,
                "sentiment": sentiment_label,
                "priority": priority
            })
        else:
            return jsonify({
                "message": "❌ Failed to trigger flow",
                "status": response.status_code,
                "response": response.text
            }), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "✅ Voice-to-Case-D365 API is running."

if __name__ == '__main__':
    app.run(debug=True)

