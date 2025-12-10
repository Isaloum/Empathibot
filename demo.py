#!/usr/bin/env python3
"""
MindCare Demo Script
Demonstrates the mental health analysis capabilities
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import MentalHealthAnalyzer

def run_demo():
    """Run a demonstration of the mental health analysis"""
    print("🧠 MindCare Mental Health Analysis Demo")
    print("=" * 50)
    
    # Initialize the analyzer
    analyzer = MentalHealthAnalyzer()
    
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
    elif phq9_total > 9 or gad7_total > 9:
        risk_level = "moderate"
    else:
        risk_level = "low"
    
    print(f"⚠️  Overall Risk Level: {risk_level.upper()}")
    
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
        print("• Contact a mental health professional immediately")
        print("• Call National Suicide Prevention Lifeline: 988")
        print("• Reach out to trusted friends or family")
    elif risk_level == "moderate":
        print("• Consider scheduling an appointment with a therapist")
        print("• Practice self-care and stress management")
        print("• Monitor symptoms and take regular assessments")
    else:
        print("• Continue current wellness practices")
        print("• Stay aware of mental health changes")
        print("• Take periodic assessments to track progress")
    
    print("\n" + "=" * 50)
    print("Demo completed! 🎉")
    print("\nTo use the full application:")
    print("1. Configure your .env file with API keys")
    print("2. Run: python app.py")
    print("3. Visit: http://localhost:5000")

if __name__ == "__main__":
    run_demo()