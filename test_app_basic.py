#!/usr/bin/env python3
"""
MindCare Basic Test Version
Run this to test the web interface without external dependencies
"""

from flask import Flask, render_template, request, jsonify, session
import json
import uuid
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'test-secret-key-for-demo')

# In-memory storage for testing (replaces Firebase)
users_db = {}
assessments_db = []

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
        positive_words = ['happy', 'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'joy', 'excited', 'positive', 'better', 'trying']
        negative_words = ['sad', 'bad', 'terrible', 'awful', 'horrible', 'hate', 'depressed', 'anxious', 'worried', 'scared', 'angry', 'struggling', 'difficult']
        
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
        
        if not recommendations:
            recommendations.append("Continue maintaining healthy habits")
            recommendations.append("Stay aware of your mental wellness")
            recommendations.append("Take regular self-assessments")
        
        return recommendations

analyzer = MentalHealthAnalyzer()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assessment")
def assessment():
    return render_template("assessment.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/register", methods=["POST"])
def register_user():
    try:
        data = request.get_json()
        user_id = str(uuid.uuid4())
        
        user_data = {
            "user_id": user_id,
            "email": data.get("email"),
            "name": data.get("name"),
            "age": data.get("age"),
            "created_at": datetime.now().isoformat(),
            "assessments": []
        }
        
        users_db[user_id] = user_data
        session["user_id"] = user_id
        
        return jsonify({"success": True, "user_id": user_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/analyze", methods=["POST"])
def analyze_mental_health():
    try:
        data = request.get_json()
        user_id = session.get("user_id") or data.get("user_id") or str(uuid.uuid4())
        
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
        
        # Calculate risk level
        phq9_total = sum(phq9_scores)
        gad7_total = sum(gad7_scores)
        
        if phq9_total > 19 or gad7_total > 14:
            risk_level = "high"
        elif phq9_total > 9 or gad7_total > 9:
            risk_level = "moderate"
        else:
            risk_level = "low"
        
        # Create comprehensive analysis
        analysis = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "phq9": {
                "scores": phq9_scores,
                "total": phq9_total,
                "result": phq9_result
            },
            "gad7": {
                "scores": gad7_scores,
                "total": gad7_total,
                "result": gad7_result
            },
            "sentiment_analysis": sentiment_analysis,
            "recommendations": recommendations,
            "risk_level": risk_level
        }
        
        # Save to in-memory database
        assessments_db.append(analysis)
        
        print(f"🧠 Assessment completed for user {user_id}")
        print(f"📊 PHQ-9: {phq9_total}/27 ({phq9_result['level']})")
        print(f"📊 GAD-7: {gad7_total}/21 ({gad7_result['level']})")
        print(f"⚠️  Risk Level: {risk_level}")
        
        return jsonify({"success": True, "analysis": analysis})
        
    except Exception as e:
        print(f"Analysis error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/user/<user_id>/history")
def get_user_history(user_id):
    try:
        # Get user's assessment history from in-memory storage
        user_assessments = [a for a in assessments_db if a["user_id"] == user_id]
        user_assessments.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return jsonify({"success": True, "history": user_assessments[:10]})
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

@app.route("/test")
def test_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>MindCare Test Page</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .test-section { background: #f5f5f5; padding: 20px; margin: 20px 0; border-radius: 8px; }
            .button { background: #667eea; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; margin: 5px; }
            .button:hover { background: #5a6fd8; }
            .result { background: white; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; }
        </style>
    </head>
    <body>
        <h1>🧠 MindCare Test Interface</h1>
        
        <div class="test-section">
            <h2>🎯 Quick Tests</h2>
            <button class="button" onclick="testRegistration()">Test Registration</button>
            <button class="button" onclick="testAssessment()">Test Assessment</button>
            <button class="button" onclick="testCrisisResources()">Test Crisis Resources</button>
        </div>
        
        <div class="test-section">
            <h2>📊 Sample Assessment</h2>
            <p>Click to run a sample mental health assessment:</p>
            <button class="button" onclick="runSampleAssessment()">Run Sample Assessment</button>
        </div>
        
        <div id="results"></div>
        
        <div class="test-section">
            <h2>🔗 Navigation</h2>
            <a href="/" class="button">Home Page</a>
            <a href="/assessment" class="button">Take Assessment</a>
            <a href="/dashboard" class="button">Dashboard</a>
        </div>
        
        <script>
            async function testRegistration() {
                const response = await fetch('/api/register', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        name: 'Test User',
                        email: 'test@example.com',
                        age: 25
                    })
                });
                const result = await response.json();
                showResult('Registration Test', result);
            }
            
            async function testAssessment() {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        phq9_scores: [1, 1, 0, 1, 0, 0, 1, 0, 0],
                        gad7_scores: [1, 2, 1, 0, 0, 1, 0],
                        text_input: 'I have been feeling okay lately, some stress but managing well.'
                    })
                });
                const result = await response.json();
                showResult('Assessment Test', result);
            }
            
            async function testCrisisResources() {
                const response = await fetch('/api/crisis-resources');
                const result = await response.json();
                showResult('Crisis Resources Test', result);
            }
            
            async function runSampleAssessment() {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        phq9_scores: [2, 2, 1, 2, 1, 1, 1, 0, 0],
                        gad7_scores: [2, 2, 1, 1, 0, 1, 1],
                        text_input: 'I have been struggling with anxiety about work and feeling down some days. Some days are better than others.'
                    })
                });
                const result = await response.json();
                if (result.success) {
                    const analysis = result.analysis;
                    showResult('Sample Assessment Results', {
                        'PHQ-9 Score': `${analysis.phq9.total}/27 (${analysis.phq9.result.description})`,
                        'GAD-7 Score': `${analysis.gad7.total}/21 (${analysis.gad7.result.description})`,
                        'Risk Level': analysis.risk_level.toUpperCase(),
                        'Sentiment': analysis.sentiment_analysis ? analysis.sentiment_analysis.sentiment : 'N/A',
                        'Recommendations': analysis.recommendations
                    });
                }
            }
            
            function showResult(title, data) {
                const resultsDiv = document.getElementById('results');
                const resultDiv = document.createElement('div');
                resultDiv.className = 'result';
                resultDiv.innerHTML = `<h3>${title}</h3><pre>${JSON.stringify(data, null, 2)}</pre>`;
                resultsDiv.appendChild(resultDiv);
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("🧠 MindCare Basic Test Version")
    print("=" * 40)
    print("🌐 Starting test server...")
    print("📱 Open your browser and go to:")
    print("   • Main app: http://localhost:5000")
    print("   • Test page: http://localhost:5000/test")
    print("   • Assessment: http://localhost:5000/assessment")
    print("=" * 40)
    
    app.run(debug=True, host="0.0.0.0", port=5000)