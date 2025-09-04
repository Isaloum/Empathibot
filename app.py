import firebase_admin
from firebase_admin import credentials, firestore

from flask import Flask, request, render_template, jsonify, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
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

# Rate limiting for security
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Security headers
@app.after_request
def after_request(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

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

# Web Interface Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/assessment")
def assessment():
    return render_template("assessment.html")

# API Routes for Mental Health Analysis
@app.route("/api/register", methods=["POST"])
@limiter.limit("5 per minute")
def register_user():
    try:
        data = request.get_json()
        user_id = str(uuid.uuid4())
        
        user_data = {
            "user_id": user_id,
            "email": data.get("email"),
            "name": data.get("name"),
            "age": data.get("age"),
            "created_at": firestore.SERVER_TIMESTAMP,
            "assessments": []
        }
        
        db.collection("users").document(user_id).set(user_data)
        session["user_id"] = user_id
        
        return jsonify({"success": True, "user_id": user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/analyze", methods=["POST"])
@limiter.limit("10 per hour")
def analyze_mental_health():
    try:
        data = request.get_json()
        user_id = session.get("user_id") or data.get("user_id")
        
        if not user_id:
            return jsonify({"success": False, "error": "User ID required"}), 400
        
        # Analyze PHQ-9 (Depression)
        phq9_scores = data.get("phq9_scores", [])
        phq9_result = analyzer.analyze_phq9_score(phq9_scores)
        
        # Analyze GAD-7 (Anxiety)
        gad7_scores = data.get("gad7_scores", [])
        gad7_result = analyzer.analyze_gad7_score(gad7_scores)
        
        # Analyze text sentiment if provided
        text_input = data.get("text_input", "")
        sentiment_analysis = analyzer.analyze_text_sentiment(text_input) if text_input else None
        
        # Generate recommendations
        recommendations = analyzer.generate_recommendations(phq9_result, gad7_result, sentiment_analysis or {"sentiment": "neutral"})
        
        # Create comprehensive analysis
        analysis = {
            "user_id": user_id,
            "timestamp": firestore.SERVER_TIMESTAMP,
            "phq9": {
                "scores": phq9_scores,
                "total": sum(phq9_scores),
                "result": phq9_result
            },
            "gad7": {
                "scores": gad7_scores,
                "total": sum(gad7_scores),
                "result": gad7_result
            },
            "sentiment_analysis": sentiment_analysis,
            "recommendations": recommendations,
            "risk_level": "high" if (phq9_result["level"] in ["moderately_severe", "severe"] or 
                                   gad7_result["level"] == "severe") else "moderate" if (
                                   phq9_result["level"] == "moderate" or gad7_result["level"] == "moderate") else "low"
        }
        
        # Save to Firestore
        db.collection("assessments").add(analysis)
        
        # Update user's assessment history
        user_ref = db.collection("users").document(user_id)
        user_ref.update({
            "last_assessment": firestore.SERVER_TIMESTAMP,
            "assessments": firestore.ArrayUnion([analysis])
        })
        
        return jsonify({"success": True, "analysis": analysis})
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/user/<user_id>/history")
def get_user_history(user_id):
    try:
        # Get user's assessment history
        assessments = db.collection("assessments").where("user_id", "==", user_id).order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10).stream()
        
        history = []
        for assessment in assessments:
            data = assessment.to_dict()
            history.append(data)
        
        return jsonify({"success": True, "history": history})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/crisis-resources")
def get_crisis_resources():
    resources = {
        "immediate_help": [
            {"name": "National Suicide Prevention Lifeline", "phone": "988", "description": "24/7 crisis support"},
            {"name": "Crisis Text Line", "text": "HOME to 741741", "description": "24/7 text-based crisis support"},
            {"name": "Emergency Services", "phone": "911", "description": "For immediate emergency situations"}
        ],
        "mental_health_resources": [
            {"name": "SAMHSA National Helpline", "phone": "1-800-662-4357", "description": "Treatment referral and information service"},
            {"name": "National Alliance on Mental Illness", "website": "https://nami.org", "description": "Support and education"},
            {"name": "Mental Health America", "website": "https://mhanational.org", "description": "Mental health resources and screening tools"}
        ]
    }
    return jsonify(resources)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    try:
        incoming_msg = request.form.get("Body", "").strip()
        sender = request.form.get("From", "")

        # Enhanced response with mental health awareness
        sentiment = analyzer.analyze_text_sentiment(incoming_msg)
        
        if sentiment["sentiment"] == "negative" and sentiment["confidence"] > 0.7:
            prompt = f"Respond empathetically to this message with mental health awareness: {incoming_msg}. The person seems to be struggling. Provide supportive, caring response and suggest professional help if appropriate."
        else:
            prompt = f"Respond empathetically to this message: {incoming_msg}"
        
        response = llm.invoke(prompt)

        # Save enhanced context to Firestore
        db.collection("messages").add({
            "text": incoming_msg,
            "response": str(response),
            "sender": sender,
            "sentiment_analysis": sentiment,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

        print(f"User ({sender}): {incoming_msg}")
        print(f"Sentiment: {sentiment}")
        print(f"Empathibot: {response}")

        twilio_response = MessagingResponse()
        twilio_response.message(str(response))
        return str(twilio_response)

    except Exception as e:
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
