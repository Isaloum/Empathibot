#!/usr/bin/env python3
"""
MindCare Simple Demo Script
Demonstrates the mental health analysis capabilities without external dependencies
"""

class SimpleMentalHealthAnalyzer:
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

def run_demo():
    """Run a demonstration of the mental health analysis"""
    print("🧠 MindCare Mental Health Analysis Demo")
    print("=" * 50)
    
    # Initialize the analyzer
    analyzer = SimpleMentalHealthAnalyzer()
    
    # Sample PHQ-9 responses (0=Not at all, 1=Several days, 2=More than half the days, 3=Nearly every day)
    sample_phq9_scores = [1, 2, 1, 2, 0, 1, 1, 0, 0]  # Mild depression symptoms
    
    # Sample GAD-7 responses
    sample_gad7_scores = [2, 2, 1, 1, 0, 1, 1]  # Moderate anxiety symptoms
    
    # Sample text input
    sample_text = "I've been feeling quite anxious lately about work and struggling to sleep well. Some days are better than others, but I'm trying to stay positive."
    
    print("📝 Sample Assessment Data:")
    print(f"PHQ-9 Scores: {sample_phq9_scores}")
    print(f"GAD-7 Scores: {sample_gad7_scores}")
    print(f"Text Input: '{sample_text}'")
    print()
    
    # Analyze PHQ-9
    phq9_result = analyzer.analyze_phq9_score(sample_phq9_scores)
    print("📊 PHQ-9 Depression Analysis:")
    print(f"Total Score: {sum(sample_phq9_scores)}/27")
    print(f"Level: {phq9_result['level']}")
    print(f"Description: {phq9_result['description']}")
    print()
    
    # Analyze GAD-7
    gad7_result = analyzer.analyze_gad7_score(sample_gad7_scores)
    print("📊 GAD-7 Anxiety Analysis:")
    print(f"Total Score: {sum(sample_gad7_scores)}/21")
    print(f"Level: {gad7_result['level']}")
    print(f"Description: {gad7_result['description']}")
    print()
    
    # Analyze sentiment
    sentiment_result = analyzer.analyze_text_sentiment(sample_text)
    print("💭 Sentiment Analysis:")
    print(f"Sentiment: {sentiment_result['sentiment']}")
    print(f"Confidence: {sentiment_result['confidence']:.2f}")
    print()
    
    # Generate recommendations
    recommendations = analyzer.generate_recommendations(phq9_result, gad7_result, sentiment_result)
    print("💡 Personalized Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    print()
    
    # Calculate overall risk level
    phq9_total = sum(sample_phq9_scores)
    gad7_total = sum(sample_gad7_scores)
    
    if phq9_total > 19 or gad7_total > 14:
        risk_level = "high"
        risk_color = "🔴"
    elif phq9_total > 9 or gad7_total > 9:
        risk_level = "moderate"
        risk_color = "🟡"
    else:
        risk_level = "low"
        risk_color = "🟢"
    
    print(f"{risk_color} Overall Risk Level: {risk_level.upper()}")
    
    # Risk level descriptions
    risk_descriptions = {
        "low": "Minimal mental health concerns. Continue maintaining healthy habits.",
        "moderate": "Some mental health concerns that may benefit from attention. Consider professional support.",
        "high": "Significant mental health concerns. Strongly recommend seeking professional help."
    }
    
    print(f"📋 Assessment: {risk_descriptions[risk_level]}")
    print()
    
    print("🎯 Next Steps:")
    if risk_level == "high":
        print("🚨 Contact a mental health professional immediately")
        print("📞 Call National Suicide Prevention Lifeline: 988")
        print("👥 Reach out to trusted friends or family")
    elif risk_level == "moderate":
        print("🏥 Consider scheduling an appointment with a therapist")
        print("🧘 Practice self-care and stress management")
        print("📊 Monitor symptoms and take regular assessments")
    else:
        print("✅ Continue current wellness practices")
        print("👀 Stay aware of mental health changes")
        print("📈 Take periodic assessments to track progress")
    
    print("\n" + "=" * 50)
    print("✨ Demo completed! 🎉")
    print("\n🚀 To use the full MindCare application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Configure your .env file with API keys")
    print("3. Run: python app.py")
    print("4. Visit: http://localhost:5000")
    print("\n📱 Features available in the full app:")
    print("• Professional web interface with beautiful UI")
    print("• Interactive dashboard with progress charts")
    print("• 24/7 WhatsApp chatbot support (Empathibot)")
    print("• Secure data storage with Firebase")
    print("• Crisis resources and emergency contacts")
    print("• Assessment history and trend analysis")

if __name__ == "__main__":
    run_demo()