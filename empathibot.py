"""
Empathibot - Advanced AI Mental Health Support Chatbot
A comprehensive WhatsApp-based mental health support system with:
- Conversation memory and context management
- Advanced crisis detection
- Multilingual support
- Personalized empathetic responses
- Automated wellness check-ins
"""

import os
import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
from langchain.chains import LLMChain
import langdetect
from firebase_admin import firestore


class CrisisDetector:
    """Advanced crisis detection system with severity scoring"""

    def __init__(self):
        # Critical crisis keywords (highest severity)
        self.critical_keywords = [
            'suicide', 'kill myself', 'end my life', 'want to die', 'better off dead',
            'suicide plan', 'overdose', 'jump off', 'hang myself', 'shoot myself',
            'cut myself', 'hurt myself badly', 'end it all', 'no reason to live',
            'suicidio', 'quiero morir', 'me quiero morir', 'me quiero matar',
            'je veux mourir', 'me suicider', 'je veux me tuer'
        ]

        # High severity keywords
        self.high_severity_keywords = [
            'self harm', 'cut', 'cutting', 'harm myself', 'hurt myself',
            'hopeless', 'worthless', 'nothing matters', 'give up', 'can\'t go on',
            'everyone would be better', 'burden to everyone', 'life is meaningless',
            'autolesion', 'desesperado', 'sin esperanza', 'no puedo mas',
            'sans espoir', 'je ne peux plus', 'tout est inutile'
        ]

        # Moderate severity keywords
        self.moderate_keywords = [
            'depressed', 'anxious', 'panic attack', 'can\'t cope', 'overwhelmed',
            'breaking down', 'losing it', 'can\'t handle', 'falling apart',
            'hate myself', 'failure', 'disaster', 'terrible', 'awful day',
            'deprimido', 'ansioso', 'ataque de panico', 'no puedo manejar',
            'deprime', 'anxieux', 'attaque de panique', 'submerge'
        ]

        # Positive/coping keywords (reduce severity)
        self.positive_keywords = [
            'better', 'improving', 'hopeful', 'trying', 'grateful', 'thankful',
            'getting help', 'therapy', 'counselor', 'support', 'family', 'friends'
        ]

        self.negation_words = {
            'not', "don't", 'dont', 'never', 'no', 'without', "isn't", 'isnt',
            "can't", 'cant', "won't", 'wont', "didn't", 'didnt', "doesn't", 'doesnt',
            "wasn't", 'wasnt', "aren't", 'arent'
        }

    def _keyword_pattern(self, keyword: str) -> re.Pattern:
        parts = [re.escape(part) for part in keyword.split()]
        pattern = r"\b" + r"\s+".join(parts) + r"\b"
        return re.compile(pattern)

    def _is_negated(self, text_lower: str, match_start: int) -> bool:
        words = [
            (match.group(0), match.start(), match.end())
            for match in re.finditer(r"[a-z']+", text_lower)
        ]
        preceding_words = [word for word, _, end in words if end <= match_start]
        window = preceding_words[-3:]
        return any(word in self.negation_words for word in window)

    def detect_crisis(self, text: str) -> Dict:
        """
        Analyze text for crisis indicators and return severity assessment

        Returns:
            Dict with 'is_crisis', 'severity', 'matched_keywords', 'confidence'
        """
        text_lower = text.lower()
        severity_score = 0
        matched_keywords = []

        # Check critical keywords (score: 100 each)
        for keyword in self.critical_keywords:
            pattern = self._keyword_pattern(keyword)
            for match in pattern.finditer(text_lower):
                if not self._is_negated(text_lower, match.start()):
                    severity_score += 100
                    matched_keywords.append(keyword)

        # Check high severity keywords (score: 50 each)
        for keyword in self.high_severity_keywords:
            pattern = self._keyword_pattern(keyword)
            for match in pattern.finditer(text_lower):
                if not self._is_negated(text_lower, match.start()):
                    severity_score += 50
                    matched_keywords.append(keyword)

        # Check moderate keywords (score: 20 each)
        for keyword in self.moderate_keywords:
            pattern = self._keyword_pattern(keyword)
            for match in pattern.finditer(text_lower):
                if not self._is_negated(text_lower, match.start()):
                    severity_score += 20
                    matched_keywords.append(keyword)

        # Reduce score for positive keywords (score: -10 each)
        for keyword in self.positive_keywords:
            if keyword in text_lower:
                severity_score = max(0, severity_score - 10)

        # Determine severity level
        if severity_score >= 100:
            severity = "critical"
            is_crisis = True
        elif severity_score >= 50:
            severity = "high"
            is_crisis = True
        elif severity_score >= 20:
            severity = "moderate"
            is_crisis = False
        else:
            severity = "low"
            is_crisis = False

        # Calculate confidence based on number and type of matches
        confidence = min(1.0, len(matched_keywords) * 0.2)

        return {
            "is_crisis": is_crisis,
            "severity": severity,
            "severity_score": severity_score,
            "matched_keywords": matched_keywords,
            "confidence": confidence
        }

    def get_crisis_response(self, severity: str) -> str:
        """Get appropriate crisis response based on severity"""

        if severity == "critical":
            return """🚨 **IMMEDIATE HELP AVAILABLE** 🚨

I'm very concerned about you. Please know that you're not alone and help is available RIGHT NOW:

**Call NOW:**
📞 National Suicide Prevention Lifeline: 988
📞 Crisis Text Line: Text HOME to 741741
📞 Emergency Services: 911

**You matter. Your life has value. These feelings are temporary, but suicide is permanent.**

I'm here to support you, but please reach out to these crisis professionals immediately. Would you like me to help you find additional resources or someone to talk to?"""

        elif severity == "high":
            return """⚠️ **I'm Here For You** ⚠️

I can sense you're going through a really difficult time. Please know that:

✨ You are not alone
✨ These feelings are temporary
✨ Help is available

**Crisis Resources:**
📞 988 - Suicide Prevention Lifeline (24/7)
📱 Text HOME to 741741 - Crisis Text Line
🌐 SAMHSA Helpline: 1-800-662-4357

Please consider reaching out to a mental health professional or one of these crisis resources. I'm here to listen and support you. Would you like to talk about what you're experiencing?"""

        elif severity == "moderate":
            return """💙 **I Hear You** 💙

It sounds like you're struggling right now. That takes courage to share. Remember:

✨ Difficult times don't last forever
✨ You have the strength to get through this
✨ Professional support can make a real difference

If things get worse, please reach out:
📞 988 - Suicide Prevention Lifeline
📱 Crisis Text Line: Text HOME to 741741

I'm here to listen. Would you like to talk about what's troubling you?"""

        else:
            return None


class LanguageHandler:
    """Multilingual support with automatic language detection"""

    def __init__(self):
        self.supported_languages = {
            'en': 'English',
            'es': 'Spanish',
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'zh-cn': 'Chinese',
            'ja': 'Japanese',
            'ar': 'Arabic',
            'hi': 'Hindi'
        }

        # Crisis resources in different languages
        self.crisis_resources = {
            'en': "National Suicide Prevention Lifeline: 988 | Crisis Text Line: Text HOME to 741741",
            'es': "Línea Nacional de Prevención del Suicidio: 988 | Línea de Crisis por Texto: Envía HOLA al 741741",
            'fr': "Ligne Nationale de Prévention du Suicide: 988 | Ligne de Crise par SMS: Envoyez MAISON au 741741",
            'de': "Nationale Suizidpräventions-Hotline: 988 | Krisen-SMS-Leitung: Senden Sie HOME an 741741",
            'pt': "Linha Nacional de Prevenção ao Suicídio: 988 | Linha de Crise por Texto: Envie CASA para 741741"
        }

    def detect_language(self, text: str) -> str:
        """Detect language of the input text"""
        try:
            detected = langdetect.detect(text)
            return detected if detected in self.supported_languages else 'en'
        except:
            return 'en'

    def get_crisis_resources(self, language: str) -> str:
        """Get crisis resources in the detected language"""
        return self.crisis_resources.get(language, self.crisis_resources['en'])


class UserSessionManager:
    """Manage user sessions, conversation history, and profiles"""

    def __init__(self, db, max_history: int = 50):
        self.db = db
        self.sessions = {}  # In-memory session cache
        self.max_history = max_history

    def get_or_create_user(self, phone_number: str) -> Dict:
        """Get existing user or create new user profile"""
        # Check Firestore for existing user
        users_ref = self.db.collection('whatsapp_users')
        query = users_ref.where('phone_number', '==', phone_number).limit(1)

        users = list(query.stream())

        if users:
            user_doc = users[0]
            return {
                'id': user_doc.id,
                **user_doc.to_dict()
            }
        else:
            # Create new user
            new_user = {
                'phone_number': phone_number,
                'created_at': firestore.SERVER_TIMESTAMP,
                'last_interaction': firestore.SERVER_TIMESTAMP,
                'conversation_count': 0,
                'crisis_alerts': 0,
                'preferred_language': 'en',
                'check_in_enabled': True,
                'user_profile': {
                    'name': None,
                    'age': None,
                    'timezone': None
                },
                'mental_health_data': {
                    'last_assessment': None,
                    'risk_level': 'unknown',
                    'mood_trend': []
                }
            }

            doc_ref = users_ref.document()
            doc_ref.set(new_user)

            return {
                'id': doc_ref.id,
                **new_user
            }

    def update_user_activity(self, user_id: str, language: str = None, crisis_detected: bool = False):
        """Update user activity and statistics"""
        user_ref = self.db.collection('whatsapp_users').document(user_id)

        update_data = {
            'last_interaction': firestore.SERVER_TIMESTAMP,
            'conversation_count': firestore.Increment(1)
        }

        if language:
            update_data['preferred_language'] = language

        if crisis_detected:
            update_data['crisis_alerts'] = firestore.Increment(1)
            update_data['mental_health_data.risk_level'] = 'high'

        user_ref.update(update_data)

    def get_conversation_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Retrieve recent conversation history"""
        messages_ref = self.db.collection('whatsapp_messages')
        query = messages_ref.where('user_id', '==', user_id).order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit)

        messages = []
        for msg in query.stream():
            messages.append(msg.to_dict())

        return list(reversed(messages))  # Return in chronological order

    def save_conversation(self, user_id: str, user_message: str, bot_response: str,
                         sentiment: Dict, crisis_info: Dict, language: str):
        """Save conversation to Firestore"""
        self.db.collection('whatsapp_messages').add({
            'user_id': user_id,
            'user_message': user_message,
            'bot_response': bot_response,
            'sentiment': sentiment,
            'crisis_info': crisis_info,
            'language': language,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        self._trim_conversation_history(user_id)

    def _trim_conversation_history(self, user_id: str):
        """Keep only the most recent messages for a user."""
        messages_ref = self.db.collection('whatsapp_messages')
        recent_query = (
            messages_ref.where('user_id', '==', user_id)
            .order_by('timestamp', direction=firestore.Query.DESCENDING)
            .limit(self.max_history)
        )
        recent_docs = list(recent_query.stream())
        if len(recent_docs) < self.max_history:
            return

        last_doc = recent_docs[-1]
        old_query = (
            messages_ref.where('user_id', '==', user_id)
            .order_by('timestamp', direction=firestore.Query.DESCENDING)
            .start_after(last_doc)
        )
        for old_doc in old_query.stream():
            old_doc.reference.delete()


class ConversationMemory:
    """Enhanced conversation memory with context management"""

    def __init__(self, user_id: str, conversation_history: List[Dict] = None):
        self.user_id = user_id
        self.memory = ConversationBufferWindowMemory(k=5)  # Remember last 5 exchanges

        # Load previous conversation history
        if conversation_history:
            for msg in conversation_history[-5:]:  # Load last 5 messages
                self.memory.save_context(
                    {"input": msg.get('user_message', '')},
                    {"output": msg.get('bot_response', '')}
                )

    def get_context_summary(self) -> str:
        """Get a summary of the conversation context"""
        history = self.memory.load_memory_variables({})
        return history.get('history', '')


class Empathibot:
    """
    Advanced AI Mental Health Support Chatbot
    Main class orchestrating all empathibot functionality
    """

    def __init__(self, db, llm: OpenAI):
        self.db = db
        self.llm = llm
        self.crisis_detector = CrisisDetector()
        self.language_handler = LanguageHandler()
        self.session_manager = UserSessionManager(db)

        # Enhanced prompt template for empathetic responses
        self.prompt_template = PromptTemplate(
            input_variables=["history", "input"],
            template="""You are Empathibot, a compassionate and empathetic AI mental health support companion. Your role is to:

1. Listen actively and validate feelings
2. Provide emotional support and encouragement
3. Suggest healthy coping strategies
4. Recognize when professional help is needed
5. Be warm, non-judgmental, and supportive

Previous conversation:
{history}

Current message: {input}

Guidelines for your response:
- Be warm, empathetic, and genuine
- Validate their feelings without judgment
- Ask thoughtful follow-up questions
- Suggest coping strategies when appropriate
- Keep responses concise (2-4 sentences)
- Use emojis sparingly and appropriately
- NEVER diagnose or replace professional therapy
- Encourage professional help for serious concerns

Your empathetic response:"""
        )

    def process_message(self, phone_number: str, message: str) -> str:
        """
        Main message processing pipeline

        Args:
            phone_number: User's WhatsApp phone number
            message: Incoming message text

        Returns:
            str: Bot response to send back
        """
        # 1. Get or create user profile
        user = self.session_manager.get_or_create_user(phone_number)
        user_id = user['id']

        # 2. Detect language
        language = self.language_handler.detect_language(message)

        # 3. Crisis detection
        crisis_info = self.crisis_detector.detect_crisis(message)

        # 4. If crisis detected, handle immediately
        if crisis_info['is_crisis']:
            crisis_response = self.crisis_detector.get_crisis_response(crisis_info['severity'])

            # Update user profile with crisis alert
            self.session_manager.update_user_activity(user_id, language, crisis_detected=True)

            # Log crisis incident
            self.db.collection('crisis_alerts').add({
                'user_id': user_id,
                'phone_number': phone_number,
                'message': message,
                'severity': crisis_info['severity'],
                'severity_score': crisis_info['severity_score'],
                'matched_keywords': crisis_info['matched_keywords'],
                'timestamp': firestore.SERVER_TIMESTAMP,
                'response_sent': crisis_response
            })

            # Save conversation
            sentiment = {"sentiment": "negative", "confidence": 0.9}
            self.session_manager.save_conversation(
                user_id, message, crisis_response, sentiment, crisis_info, language
            )

            return crisis_response

        # 5. Get conversation history and build memory
        conversation_history = self.session_manager.get_conversation_history(user_id)
        memory = ConversationMemory(user_id, conversation_history)

        # 6. Build context
        context_parts = []
        if user.get('user_profile', {}).get('name'):
            context_parts.append(f"User's name: {user['user_profile']['name']}")

        if user.get('mental_health_data', {}).get('risk_level'):
            context_parts.append(f"Risk level: {user['mental_health_data']['risk_level']}")

        if crisis_info['severity'] in ['moderate', 'low'] and crisis_info['matched_keywords']:
            context_parts.append(f"User is experiencing: {', '.join(crisis_info['matched_keywords'][:3])}")

        context = " | ".join(context_parts) if context_parts else "New conversation"

        # 7. Generate empathetic response using LangChain
        conversation_chain = LLMChain(
            llm=self.llm,
            memory=memory.memory,
            prompt=self.prompt_template,
            verbose=False
        )

        # Generate response
        combined_input = f"Context: {context}\n\nUser message: {message}"
        ai_response = conversation_chain.predict(input=combined_input)

        # 8. Post-process response
        # Add crisis resources if moderate severity detected
        if crisis_info['severity'] == 'moderate':
            ai_response += f"\n\n💙 Remember, if you need immediate support: {self.language_handler.get_crisis_resources(language)}"

        # 9. Sentiment analysis (basic)
        sentiment = self._analyze_sentiment(message)

        # 10. Update user activity
        self.session_manager.update_user_activity(user_id, language, crisis_detected=False)

        # 11. Save conversation
        self.session_manager.save_conversation(
            user_id, message, ai_response, sentiment, crisis_info, language
        )

        # 12. Update mood tracking
        self._update_mood_tracking(user_id, sentiment, crisis_info)

        return ai_response

    def _analyze_sentiment(self, text: str) -> Dict:
        """Basic sentiment analysis"""
        positive_words = ['happy', 'good', 'great', 'better', 'excellent', 'wonderful',
                         'love', 'joy', 'grateful', 'thankful', 'blessed', 'excited']
        negative_words = ['sad', 'bad', 'terrible', 'awful', 'horrible', 'hate',
                         'depressed', 'anxious', 'worried', 'scared', 'angry', 'upset']

        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)

        if positive_count > negative_count:
            return {"sentiment": "positive", "score": positive_count}
        elif negative_count > positive_count:
            return {"sentiment": "negative", "score": negative_count}
        else:
            return {"sentiment": "neutral", "score": 0}

    def _update_mood_tracking(self, user_id: str, sentiment: Dict, crisis_info: Dict):
        """Update user's mood trend for analytics"""
        user_ref = self.db.collection('whatsapp_users').document(user_id)

        mood_entry = {
            'timestamp': datetime.now().isoformat(),
            'sentiment': sentiment['sentiment'],
            'crisis_severity': crisis_info['severity']
        }

        # Keep last 30 mood entries
        user_data = user_ref.get().to_dict() or {}
        mood_trend = user_data.get('mental_health_data', {}).get('mood_trend', [])
        mood_trend.append(mood_entry)
        trimmed_trend = mood_trend[-30:]
        user_ref.update({
            'mental_health_data.mood_trend': trimmed_trend
        })

    def send_check_in(self, user_id: str) -> str:
        """Generate a wellness check-in message"""
        user_ref = self.db.collection('whatsapp_users').document(user_id)
        user = user_ref.get().to_dict()

        name = user.get('user_profile', {}).get('name', 'friend')

        check_in_messages = [
            f"Hey {name} 👋 Just checking in - how are you feeling today?",
            f"Hi {name} 💙 I wanted to see how you're doing. What's on your mind?",
            f"Hello {name} ☀️ How has your day been treating you?",
            f"Hey {name} 🌟 Just thinking of you. How are things going?",
        ]

        import random
        return random.choice(check_in_messages)

    def get_user_insights(self, user_id: str) -> Dict:
        """Get analytics and insights for a user"""
        user_ref = self.db.collection('whatsapp_users').document(user_id)
        user = user_ref.get().to_dict()

        mood_trend = user.get('mental_health_data', {}).get('mood_trend', [])

        # Analyze mood trend
        recent_moods = mood_trend[-7:] if len(mood_trend) >= 7 else mood_trend

        positive_count = sum(1 for m in recent_moods if m['sentiment'] == 'positive')
        negative_count = sum(1 for m in recent_moods if m['sentiment'] == 'negative')

        if len(recent_moods) > 0:
            mood_score = (positive_count - negative_count) / len(recent_moods)
        else:
            mood_score = 0

        return {
            'user_id': user_id,
            'total_conversations': user.get('conversation_count', 0),
            'crisis_alerts': user.get('crisis_alerts', 0),
            'risk_level': user.get('mental_health_data', {}).get('risk_level', 'unknown'),
            'mood_trend': 'improving' if mood_score > 0.3 else 'declining' if mood_score < -0.3 else 'stable',
            'mood_score': mood_score,
            'recent_moods': recent_moods
        }
