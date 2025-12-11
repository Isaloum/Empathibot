# 🤖 Empathibot - Advanced AI Mental Health Support System

## Overview

Empathibot is a state-of-the-art WhatsApp-based mental health support chatbot that provides 24/7 empathetic, context-aware conversations with advanced crisis detection and intervention capabilities.

## 🌟 Core Features

### 1. Multi-tier Crisis Detection System

Empathibot uses a sophisticated keyword-based crisis detection algorithm with severity scoring:

#### Severity Levels

| Level | Score Range | Example Keywords | Response |
|-------|-------------|------------------|----------|
| **Critical** | 100+ | "suicide", "kill myself", "end my life" | Immediate crisis intervention with 988 hotline |
| **High** | 50-99 | "self harm", "hopeless", "worthless" | Supportive crisis response with resources |
| **Moderate** | 20-49 | "depressed", "anxious", "overwhelmed" | Empathetic support with gentle resources |
| **Low** | <20 | Normal conversation | Standard AI responses |

#### How It Works

```python
# Crisis detection algorithm
severity_score = 0

# Critical keywords: +100 points each
for keyword in critical_keywords:
    if keyword in message:
        severity_score += 100

# High severity: +50 points each
for keyword in high_severity_keywords:
    if keyword in message:
        severity_score += 50

# Moderate: +20 points each
for keyword in moderate_keywords:
    if keyword in message:
        severity_score += 20

# Positive keywords: -10 points (reduces severity)
for keyword in positive_keywords:
    if keyword in message:
        severity_score -= 10
```

### 2. Conversation Memory & Context Management

Empathibot maintains conversation context using LangChain's `ConversationBufferWindowMemory`:

- **Remembers**: Last 5 message exchanges
- **Persists**: Conversation history in Firestore
- **Contextualizes**: Responses based on user history
- **Personalizes**: Uses user name and past interactions

**Example:**
```
User: "I'm feeling depressed"
Bot: "I'm sorry you're feeling this way. Can you tell me more?"

User: "It's been going on for weeks"
Bot: [Remembers depression context] "It sounds like this has been really difficult for you. Have you been able to talk to anyone about this?"
```

### 3. Multilingual Support

Automatic language detection and response generation in 10+ languages:

**Supported Languages:**
- English (en)
- Spanish (es) - "Hola, ¿cómo estás?"
- French (fr) - "Bonjour, comment allez-vous?"
- German (de) - "Hallo, wie geht es Ihnen?"
- Italian (it)
- Portuguese (pt)
- Chinese (zh-cn)
- Japanese (ja)
- Arabic (ar)
- Hindi (hi)

**Crisis resources are automatically localized:**
```python
# English
"National Suicide Prevention Lifeline: 988"

# Spanish
"Línea Nacional de Prevención del Suicídio: 988"
```

### 4. User Session Management

Each WhatsApp user gets a comprehensive profile:

**User Profile Schema:**
```json
{
  "phone_number": "whatsapp:+1234567890",
  "created_at": "2025-12-11T10:00:00Z",
  "last_interaction": "2025-12-11T15:30:00Z",
  "conversation_count": 42,
  "crisis_alerts": 2,
  "preferred_language": "en",
  "check_in_enabled": true,
  "user_profile": {
    "name": "Alice",
    "age": null,
    "timezone": null
  },
  "mental_health_data": {
    "last_assessment": null,
    "risk_level": "moderate",
    "mood_trend": [
      {
        "timestamp": "2025-12-10T14:00:00",
        "sentiment": "positive",
        "crisis_severity": "low"
      }
    ]
  }
}
```

### 5. Automated Wellness Check-ins

**Daily Check-ins** (Scheduled at 10:00 AM):
- Personalized messages using user's name
- Only sent if 24+ hours since last interaction
- Variety of friendly check-in messages

**Example Messages:**
- "Hey Alice 👋 Just checking in - how are you feeling today?"
- "Hi Alice 💙 I wanted to see how you're doing. What's on your mind?"
- "Hello Alice ☀️ How has your day been treating you?"

### 6. Crisis Follow-up System

Automatic follow-ups after crisis alerts (every 4 hours):

**Critical Severity Follow-up:**
```
💙 Checking in after our conversation. I'm still here if you need support.

Please remember:
📞 988 - Available 24/7
📱 Crisis Text Line: Text HOME to 741741

You matter, and people care about you. How are you doing right now?
```

**High Severity Follow-up:**
```
💙 Hi, I wanted to follow up and see how you're feeling now.

Remember that I'm here to listen, and professional support is available if you need it.

How are things going?
```

### 7. Sentiment Analysis

Real-time sentiment analysis to adapt responses:

- **Positive sentiment**: Encouraging, supportive responses
- **Negative sentiment**: Empathetic, validating responses with resources
- **Neutral sentiment**: Standard conversational responses

### 8. Advanced Analytics & Insights

**User Insights Include:**
- Total conversation count
- Number of crisis alerts
- Current risk level
- Mood trend (improving/stable/declining)
- Recent mood history

**Example Insight Response:**
```json
{
  "user_id": "abc123",
  "total_conversations": 25,
  "crisis_alerts": 1,
  "risk_level": "moderate",
  "mood_trend": "improving",
  "mood_score": 0.45,
  "recent_moods": [...]
}
```

## 🏗️ Architecture

### Components

```
┌─────────────────────────────────────────────────┐
│              WhatsApp User                      │
│         (Twilio WhatsApp Business)              │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│         Flask App (/whatsapp endpoint)          │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│            Empathibot Class                     │
│  ┌──────────────────────────────────────────┐  │
│  │  1. UserSessionManager                   │  │
│  │     - Get/create user profile            │  │
│  │                                           │  │
│  │  2. LanguageHandler                      │  │
│  │     - Detect language                    │  │
│  │                                           │  │
│  │  3. CrisisDetector                       │  │
│  │     - Analyze for crisis keywords        │  │
│  │     - Calculate severity score           │  │
│  │                                           │  │
│  │  4. If CRISIS:                           │  │
│  │     - Return crisis response             │  │
│  │     - Log crisis alert                   │  │
│  │     - Update user risk level             │  │
│  │                                           │  │
│  │  5. If NORMAL:                           │  │
│  │     - Load conversation history          │  │
│  │     - Build context                      │  │
│  │     - Generate AI response (LangChain)   │  │
│  │     - Save conversation                  │  │
│  │     - Update mood tracking               │  │
│  └──────────────────────────────────────────┘  │
└────────────────┬────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────┐
│         Firebase Firestore Database             │
│  - whatsapp_users                               │
│  - whatsapp_messages                            │
│  - crisis_alerts                                │
│  - check_in_logs                                │
│  - crisis_follow_ups                            │
└─────────────────────────────────────────────────┘
```

### Message Flow

1. **User sends WhatsApp message** → Twilio webhook triggers `/whatsapp`
2. **Get/create user profile** from Firestore
3. **Detect language** of the message
4. **Check for crisis** keywords and calculate severity
5. **If crisis detected**:
   - Generate crisis intervention response
   - Log crisis alert
   - Update user risk level
   - Schedule follow-up
6. **If normal conversation**:
   - Load conversation history (last 10 messages)
   - Build conversation memory (last 5 exchanges)
   - Create context from user profile + history
   - Generate empathetic AI response using LangChain
   - Analyze sentiment
   - Save conversation to Firestore
   - Update mood tracking
7. **Return response** via Twilio WhatsApp

## 📊 Data Models

### Collections in Firestore

#### 1. `whatsapp_users`
```json
{
  "phone_number": "whatsapp:+1234567890",
  "created_at": "ServerTimestamp",
  "last_interaction": "ServerTimestamp",
  "last_check_in": "ServerTimestamp",
  "conversation_count": 0,
  "crisis_alerts": 0,
  "preferred_language": "en",
  "check_in_enabled": true,
  "user_profile": {
    "name": null,
    "age": null,
    "timezone": null
  },
  "mental_health_data": {
    "last_assessment": null,
    "risk_level": "unknown",
    "mood_trend": []
  }
}
```

#### 2. `whatsapp_messages`
```json
{
  "user_id": "user123",
  "user_message": "I'm feeling down today",
  "bot_response": "I'm sorry to hear that...",
  "sentiment": {
    "sentiment": "negative",
    "score": 2
  },
  "crisis_info": {
    "is_crisis": false,
    "severity": "low",
    "severity_score": 15,
    "matched_keywords": ["down"]
  },
  "language": "en",
  "timestamp": "ServerTimestamp"
}
```

#### 3. `crisis_alerts`
```json
{
  "user_id": "user123",
  "phone_number": "whatsapp:+1234567890",
  "message": "I want to end it all",
  "severity": "critical",
  "severity_score": 150,
  "matched_keywords": ["end my life", "suicide"],
  "timestamp": "ServerTimestamp",
  "response_sent": "🚨 IMMEDIATE HELP AVAILABLE..."
}
```

#### 4. `check_in_logs`
```json
{
  "user_id": "user123",
  "phone_number": "whatsapp:+1234567890",
  "message": "Hey Alice 👋 Just checking in...",
  "status": "sent",
  "twilio_sid": "SM1234567890",
  "timestamp": "ServerTimestamp"
}
```

## 🔌 API Reference

### Enhanced Empathibot Endpoints

#### Get User Insights
```http
GET /api/empathibot/user/<phone_number>/insights
```

**Response:**
```json
{
  "success": true,
  "insights": {
    "user_id": "user123",
    "total_conversations": 42,
    "crisis_alerts": 2,
    "risk_level": "moderate",
    "mood_trend": "improving",
    "mood_score": 0.35,
    "recent_moods": [...]
  }
}
```

#### Trigger Check-in
```http
POST /api/empathibot/check-in/<phone_number>
```

**Response:**
```json
{
  "success": true,
  "message": "Hey Alice 👋 Just checking in - how are you feeling today?",
  "note": "Check-in message generated. Integrate with Twilio to send."
}
```

#### Get Crisis Alerts
```http
GET /api/empathibot/crisis-alerts
```

**Response:**
```json
{
  "success": true,
  "alerts": [
    {
      "id": "alert123",
      "user_id": "user123",
      "phone_number": "whatsapp:+1234567890",
      "severity": "critical",
      "severity_score": 150,
      "matched_keywords": ["suicide", "end my life"],
      "timestamp": "2025-12-11T15:30:00Z"
    }
  ],
  "count": 1
}
```

#### Get Conversation History
```http
GET /api/empathibot/conversation/<phone_number>?limit=20
```

**Response:**
```json
{
  "success": true,
  "messages": [
    {
      "user_message": "Hello",
      "bot_response": "Hi! I'm here to support you...",
      "sentiment": {"sentiment": "neutral", "score": 0},
      "crisis_info": {"severity": "low"},
      "language": "en",
      "timestamp": "2025-12-11T14:00:00Z"
    }
  ],
  "count": 20
}
```

#### Get System Statistics
```http
GET /api/empathibot/stats
```

**Response:**
```json
{
  "success": true,
  "stats": {
    "total_users": 1250,
    "total_conversations": 15430,
    "total_crisis_alerts": 47,
    "active_users_7d": 0,
    "system_status": "operational"
  }
}
```

## 🧪 Testing

Run the comprehensive test suite:

```bash
python test_empathibot.py
```

**Test Coverage:**
- Crisis detection (critical, high, moderate, low)
- Language detection
- User session management
- Conversation memory
- Sentiment analysis
- Full conversation flow integration

## 🚀 Deployment

### Environment Variables

Add to `.env`:
```env
# Existing variables
FIREBASE_CONFIG_JSON={"type": "service_account", ...}
OPENAI_API_KEY=your_openai_key
SECRET_KEY=your_secret_key

# Twilio for WhatsApp
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
```

### Enable Automated Scheduler

In `app.py`, uncomment:
```python
# Start the scheduler in background
scheduler.start_scheduler()
```

This will enable:
- Daily check-ins at 10:00 AM
- Crisis follow-ups every 4 hours

### Twilio Webhook Setup

1. Go to Twilio Console → WhatsApp Sandbox
2. Set webhook URL: `https://your-domain.com/whatsapp`
3. Method: `POST`
4. Save configuration

## 🎯 Best Practices

### Crisis Management

1. **Always prioritize safety**: Crisis responses include immediate hotline numbers
2. **Log all crisis alerts**: For monitoring and follow-up
3. **Never replace professionals**: Always recommend professional help
4. **Follow up**: Automated follow-ups ensure ongoing support

### Conversation Quality

1. **Be empathetic**: Use warm, validating language
2. **Keep it concise**: 2-4 sentences per response
3. **Ask questions**: Encourage user to share more
4. **Provide resources**: When appropriate, share coping strategies

### Data Privacy

1. **Encrypt sensitive data**: Use Firestore security rules
2. **Limit data access**: Only authorized personnel see crisis alerts
3. **HIPAA awareness**: Follow healthcare privacy guidelines
4. **Anonymize when possible**: Use user IDs instead of phone numbers in logs

## 📈 Monitoring & Analytics

### Key Metrics to Track

- **Crisis alert rate**: % of conversations triggering crisis detection
- **Response time**: Average time to generate responses
- **User engagement**: Conversation frequency and length
- **Mood trends**: Overall sentiment changes over time
- **Language distribution**: Most common languages used

### Firestore Queries for Analytics

```python
# Get high-risk users
high_risk_users = db.collection('whatsapp_users')\
    .where('mental_health_data.risk_level', '==', 'high')\
    .stream()

# Get crisis alerts in last 24 hours
from datetime import datetime, timedelta
yesterday = datetime.now() - timedelta(days=1)
recent_crises = db.collection('crisis_alerts')\
    .where('timestamp', '>=', yesterday)\
    .stream()

# Get most active users
# (Note: Requires composite index)
active_users = db.collection('whatsapp_users')\
    .order_by('conversation_count', direction=firestore.Query.DESCENDING)\
    .limit(10)\
    .stream()
```

## 🔧 Customization

### Adding New Crisis Keywords

In `empathibot.py` → `CrisisDetector`:

```python
self.critical_keywords = [
    'suicide', 'kill myself',
    # Add your keywords here
    'new critical keyword'
]
```

### Customizing Check-in Messages

In `empathibot.py` → `Empathibot.send_check_in()`:

```python
check_in_messages = [
    f"Hey {name} 👋 Just checking in - how are you feeling today?",
    # Add your custom messages here
    f"Hi {name}, hope you're having a good day!"
]
```

### Adjusting Conversation Memory Window

In `empathibot.py` → `ConversationMemory`:

```python
# Change k=5 to your desired number
self.memory = ConversationBufferWindowMemory(k=5)  # Last 5 exchanges
```

## 🆘 Troubleshooting

### Common Issues

**Issue**: Bot not responding to WhatsApp messages
- Check Twilio webhook configuration
- Verify `/whatsapp` endpoint is accessible
- Check Firestore connection

**Issue**: Crisis detection not working
- Verify keywords are lowercase in messages
- Check crisis detector initialization
- Review Firestore permissions

**Issue**: Language detection errors
- Install `langdetect`: `pip install langdetect`
- Check for very short messages (may not detect properly)
- Default fallback to English should still work

**Issue**: Memory/context not persisting
- Verify Firestore writes are successful
- Check `whatsapp_messages` collection
- Ensure user ID is correctly passed

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Twilio WhatsApp API](https://www.twilio.com/docs/whatsapp)
- [Firebase Firestore](https://firebase.google.com/docs/firestore)
- [Crisis Intervention Best Practices](https://suicidepreventionlifeline.org/)

---

**Built with ❤️ for mental health support**
