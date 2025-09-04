import firebase_admin
from firebase_admin import credentials, firestore

from flask import Flask, request, render_template, jsonify, session
from flask_cors import CORS
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
import os
import json
import datetime
from datetime import timedelta
import re
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

# Firebase setup
firebase_json = os.getenv("FIREBASE_CONFIG_JSON")
cred = credentials.Certificate(json.loads(firebase_json))
firebase_admin.initialize_app(cred)
db = firestore.client()

# LLM setup
llm = OpenAI(temperature=0.7)

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')

# Mental Health Assessment Tools
class MentalHealthAnalyzer:
    def __init__(self):
        self.phq9_questions = [
            "Little interest or pleasure in doing things",
            "Feeling down, depressed, or hopeless",
            "Trouble falling or staying asleep, or sleeping too much",
            "Feeling tired or having little energy",
            "Poor appetite or overeating",
            "Feeling bad about yourself or that you are a failure",
            "Trouble concentrating on things",
            "Moving or speaking slowly, or being fidgety/restless",
            "Thoughts that you would be better off dead or hurting yourself"
        ]
        
        self.gad7_questions = [
            "Feeling nervous, anxious, or on edge",
            "Not being able to stop or control worrying",
            "Worrying too much about different things",
            "Trouble relaxing",
            "Being so restless that it is hard to sit still",
            "Becoming easily annoyed or irritable",
            "Feeling afraid as if something awful might happen"
        ]
    
    def analyze_phq9_score(self, scores):
        total = sum(scores)
        if total <= 4:
            return {"level": "minimal", "description": "Minimal depression symptoms"}
        elif total <= 9:
            return {"level": "mild", "description": "Mild depression symptoms"}
        elif total <= 14:
            return {"level": "moderate", "description": "Moderate depression symptoms"}
        elif total <= 19:
            return {"level": "moderately_severe", "description": "Moderately severe depression symptoms"}
        else:
            return {"level": "severe", "description": "Severe depression symptoms"}
    
    def analyze_gad7_score(self, scores):
        total = sum(scores)
        if total <= 4:
            return {"level": "minimal", "description": "Minimal anxiety symptoms"}
        elif total <= 9:
            return {"level": "mild", "description": "Mild anxiety symptoms"}
        elif total <= 14:
            return {"level": "moderate", "description": "Moderate anxiety symptoms"}
        else:
            return {"level": "severe", "description": "Severe anxiety symptoms"}
    
    def analyze_text_sentiment(self, text):
        # Simple sentiment analysis using keywords
        positive_words = ['happy', 'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'joy', 'excited']
        negative_words = ['sad', 'bad', 'terrible', 'awful', 'horrible', 'hate', 'depressed', 'anxious', 'worried', 'scared', 'angry']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return {"sentiment": "positive", "confidence": min(0.9, (positive_count / max(len(text.split()), 1)) * 10)}
        elif negative_count > positive_count:
            return {"sentiment": "negative", "confidence": min(0.9, (negative_count / max(len(text.split()), 1)) * 10)}
        else:
            return {"sentiment": "neutral", "confidence": 0.5}
    
    def generate_recommendations(self, phq9_result, gad7_result, sentiment_analysis):
        recommendations = []
        
        if phq9_result["level"] in ["moderate", "moderately_severe", "severe"]:
            recommendations.append("Consider speaking with a mental health professional")
            recommendations.append("Practice daily self-care activities")
            recommendations.append("Maintain a regular sleep schedule")
        
        if gad7_result["level"] in ["moderate", "severe"]:
            recommendations.append("Try relaxation techniques like deep breathing")
            recommendations.append("Consider mindfulness or meditation practices")
            recommendations.append("Limit caffeine intake")
        
        if sentiment_analysis["sentiment"] == "negative":
            recommendations.append("Engage in activities you enjoy")
            recommendations.append("Connect with supportive friends or family")
            recommendations.append("Consider journaling your thoughts")
        
        return recommendations

analyzer = MentalHealthAnalyzer()

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        incoming_msg = request.form.get("Body", "").strip()
        sender = request.form.get("From", "")  # 🆕 Who sent the message?

        response = llm.invoke(f"Respond empathetically to this message: {incoming_msg}")

        # 🆕 Save full context to Firestore
        db.collection("messages").add({
            "text": incoming_msg,
            "response": str(response),  # ✅ Save bot’s reply too
            "sender": sender,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        print(f"User ({sender}): {incoming_msg}")
        print(f"Empathibot: {response}")

        twilio_response = MessagingResponse()
        twilio_response.message(str(response))
        return str(twilio_response)

    except Exception as e:
        # 🛑 Log errors in Firestore
        db.collection("errors").add({
            "error": str(e),
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        print(f"[ERROR] {e}")
        return "Internal server error", 500

# ✅ Health check route
@app.route("/health", methods=["GET"])
def health():
    return "Empathibot is alive!", 200

# ✅ Required for Render
if __name__ == "__main__":
    print("✅ Flask app is starting properly on Render...")
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
