# 🧠 MindCare - Mental Health Support Platform

> Comprehensive mental health assessment platform combining professional tools, AI analysis, and 24/7 WhatsApp support

[![CI/CD Pipeline](https://github.com/Isaloum/empathibot/actions/workflows/ci.yml/badge.svg)](https://github.com/Isaloum/empathibot/actions)
[![codecov](https://codecov.io/gh/Isaloum/empathibot/branch/main/graph/badge.svg)](https://codecov.io/gh/Isaloum/empathibot)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ⚡ Quick Stats


✅ PHQ-9 + GAD-7 Assessments 🤖 AI-Powered Analysis
💬 24/7 WhatsApp Support 🔒 Privacy-Focused Design
📊 Interactive Dashboard 🆘 Crisis Detection


---

## 🌟 Features

### 🔍 Professional Mental Health Assessments
- **PHQ-9 Depression Screening**: Standardized 9-question assessment for depression symptoms
- **GAD-7 Anxiety Assessment**: Professional 7-question evaluation for anxiety disorders
- **Sentiment Analysis**: AI-powered analysis of user text input for emotional insights
- **Risk Level Evaluation**: Comprehensive risk assessment based on multiple factors

### 🧠 AI-Powered Analysis
- **Personalized Recommendations**: Tailored suggestions based on assessment results
- **Progress Tracking**: Monitor mental health trends over time
- **Intelligent Insights**: Advanced algorithms analyze patterns and provide actionable advice
- **Crisis Detection**: Automatic identification of high-risk situations

### 💬 24/7 Enhanced WhatsApp Support (Empathibot)
- **Advanced Conversational AI**: Context-aware responses with conversation memory
- **Multi-tier Crisis Detection**: Automatic severity scoring (critical, high, moderate, low)
- **Multilingual Support**: Automatic language detection and responses in 10+ languages
- **Personalized Interactions**: User profiles with mental health history tracking
- **Intelligent Sentiment Analysis**: Real-time emotion detection and response adaptation
- **Crisis Resources**: Immediate delivery of location-specific emergency contacts
- **Automated Check-ins**: Scheduled wellness monitoring and follow-ups
- **Crisis Follow-ups**: Automatic follow-up after high-severity conversations

### 📊 Interactive Dashboard
- **Visual Progress Tracking**: Charts and graphs showing mental health trends
- **Assessment History**: Complete record of all evaluations
- **Personalized Insights**: Data-driven recommendations for improvement
- **Quick Stats**: At-a-glance overview of mental health status

### 🔒 Security & Privacy
- **Data Encryption**: All sensitive data is encrypted and secure
- **Privacy-Focused Design**: Built with healthcare privacy standards in mind
- **Rate Limiting**: Protection against abuse and spam
- **Secure Authentication**: User data protection with session management

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Firebase account and project
- OpenAI API key
- Twilio account (for WhatsApp integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mindcare-mental-health-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   # Firebase Configuration
   FIREBASE_CONFIG_JSON={"type": "service_account", "project_id": "your-project-id", ...}
   
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   
   # Flask Configuration
   SECRET_KEY=your_secret_key_here
   ENABLE_SCHEDULER=false
   
   # Twilio Configuration (for WhatsApp)
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   ```

4. **Set up Firebase**
   - Create a Firebase project
   - Enable Firestore database
   - Generate service account credentials
   - Add the JSON configuration to your `.env` file

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Web Interface: http://localhost:5000
   - Assessment Tool: http://localhost:5000/assessment
   - Dashboard: http://localhost:5000/dashboard

## 📱 Usage Guide

### Taking an Assessment

1. **Registration**: Create an account with basic information
2. **PHQ-9 Assessment**: Answer 9 questions about depression symptoms
3. **GAD-7 Assessment**: Complete 7 questions about anxiety levels
4. **Text Analysis**: Share your thoughts for sentiment analysis
5. **Results**: Receive comprehensive analysis and recommendations

### Using the Dashboard

- **Quick Stats**: View your mental health metrics at a glance
- **Progress Charts**: Track depression and anxiety scores over time
- **Assessment History**: Review past evaluations and trends
- **Recommendations**: Access personalized mental health advice

### WhatsApp Integration

1. **Setup**: Configure Twilio webhook to `/whatsapp` endpoint
2. **Usage**: Send messages to your WhatsApp business number
3. **Support**: Receive empathetic responses and crisis support
4. **Resources**: Get mental health resources and emergency contacts

## 🏗️ Architecture

### Backend Components
- **Flask Web Framework**: RESTful API and web interface
- **Firebase Firestore**: NoSQL database for user data and assessments
- **LangChain + OpenAI**: AI-powered language processing and responses
- **Twilio**: WhatsApp messaging integration

### Frontend Components
- **Responsive Web Design**: Mobile-first design with Tailwind CSS
- **Interactive Charts**: Chart.js for data visualization
- **Progressive Web App**: Modern web technologies for app-like experience

### Security Features
- **Rate Limiting**: Prevent API abuse and spam
- **Security Headers**: Protection against common web vulnerabilities
- **Data Encryption**: Secure storage of sensitive information
- **Session Management**: Secure user authentication

## 📊 Assessment Scoring

### PHQ-9 Depression Scale
- **0-4**: Minimal depression
- **5-9**: Mild depression
- **10-14**: Moderate depression
- **15-19**: Moderately severe depression
- **20-27**: Severe depression

### GAD-7 Anxiety Scale
- **0-4**: Minimal anxiety
- **5-9**: Mild anxiety
- **10-14**: Moderate anxiety
- **15-21**: Severe anxiety

### Risk Level Calculation
- **Low Risk**: Minimal to mild symptoms
- **Moderate Risk**: Moderate symptoms in either scale
- **High Risk**: Severe symptoms or suicidal ideation

## 🆘 Crisis Resources

The application provides immediate access to crisis resources:

### Immediate Help
- **National Suicide Prevention Lifeline**: 988
- **Crisis Text Line**: Text HOME to 741741
- **Emergency Services**: 911

### Mental Health Resources
- **SAMHSA National Helpline**: 1-800-662-4357
- **National Alliance on Mental Illness**: https://nami.org
- **Mental Health America**: https://mhanational.org

## 🤖 Enhanced Empathibot Features

### Advanced Crisis Detection System
The Empathibot uses a sophisticated multi-tier crisis detection system:

**Crisis Severity Levels:**
- **Critical (100+ points)**: Contains keywords like "suicide", "kill myself", "end my life"
  - Immediate crisis intervention with emergency hotline numbers
  - Automatic alert logging for monitoring
  - Scheduled follow-up within 4 hours

- **High (50-99 points)**: Phrases like "self harm", "hopeless", "worthless"
  - Supportive crisis response with resources
  - Crisis alert logged
  - Follow-up scheduled

- **Moderate (20-49 points)**: Keywords like "depressed", "anxious", "overwhelmed"
  - Empathetic support with coping suggestions
  - Gentle resource recommendations

- **Low (<20 points)**: Normal conversation
  - Standard empathetic AI responses
  - No crisis intervention needed

### Multilingual Capabilities
Empathibot automatically detects and responds in 10+ languages:
- English, Spanish, French, German, Italian
- Portuguese, Chinese, Japanese, Arabic, Hindi
- Crisis resources provided in detected language
- Seamless language switching mid-conversation

### Conversation Memory & Context
- Remembers last 5 message exchanges
- Maintains user context across sessions
- Personalizes responses based on history
- Tracks mood trends over time

### Automated Wellness System
**Daily Check-ins** (10:00 AM):
- Personalized wellness messages
- Customized to user's name and history
- Only sent if 24+ hours since last interaction

**Crisis Follow-ups** (Every 4 hours):
- Automatic follow-up after crisis alerts
- Severity-based messaging
- Ensures ongoing support

### User Session Management
Each WhatsApp user gets:
- Unique profile with conversation history
- Mental health risk assessment
- Mood trend tracking
- Conversation analytics
- Personalized insights

## 🔧 API Endpoints

### User Management
- `POST /api/register` - Register new user
- `GET /api/user/<user_id>/history` - Get user assessment history

### Assessment & Analysis
- `POST /api/analyze` - Submit assessment for analysis
- `GET /api/crisis-resources` - Get crisis support resources

### WhatsApp Integration
- `POST /whatsapp` - Webhook for WhatsApp messages (Enhanced with Empathibot)
- `GET /health` - Health check endpoint

### Enhanced Empathibot Endpoints
- `GET /api/empathibot/user/<phone_number>/insights` - Get user analytics and insights
- `POST /api/empathibot/check-in/<phone_number>` - Trigger wellness check-in
- `GET /api/empathibot/crisis-alerts` - Get recent crisis alerts (monitoring)
- `GET /api/empathibot/conversation/<phone_number>` - Get conversation history
- `GET /api/empathibot/stats` - Get overall system statistics

## 🤝 Contributing

We welcome contributions to improve MindCare! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**Important**: This application is for informational and educational purposes only. It is not intended to replace professional mental health care, diagnosis, or treatment. If you're experiencing a mental health crisis or emergency, please:

- Call 911 immediately
- Contact the National Suicide Prevention Lifeline at 988
- Go to your nearest emergency room
- Contact your mental health professional

Always consult with qualified healthcare providers for proper diagnosis and treatment of mental health conditions.

## 📞 Support

For technical support or questions about the application:
- Create an issue on GitHub
- Contact the development team
- Check the documentation for troubleshooting guides

## 🎯 Roadmap

### ✅ Recently Completed
- [x] **Enhanced Empathibot with Advanced AI** - Multi-tier crisis detection, conversation memory
- [x] **Multilingual Support** - Automatic language detection for 10+ languages
- [x] **Automated Check-in System** - Scheduled wellness monitoring
- [x] **Crisis Follow-up System** - Automatic follow-up after high-risk conversations
- [x] **User Session Management** - Comprehensive user profiles and analytics
- [x] **Advanced Analytics API** - Insights, conversation history, crisis monitoring

### Upcoming Features
- [ ] Mobile app (iOS/Android)
- [ ] Integration with wearable devices
- [ ] Machine learning-based mood prediction models
- [ ] Therapist matching and booking system
- [ ] Group support features and peer connections
- [ ] Voice message support in WhatsApp
- [ ] Integration with assessment system (link WhatsApp users to web assessments)
- [ ] Admin dashboard for crisis monitoring
- [ ] SMS fallback for non-WhatsApp users

### Long-term Goals
- [ ] Clinical validation studies
- [ ] Healthcare provider integration (HIPAA-compliant data sharing)
- [ ] Insurance coverage support
- [ ] Community features and moderated forums
- [ ] Extended AI therapy sessions with structured CBT/DBT protocols
- [ ] Medication tracking and reminders
- [ ] Integration with electronic health records (EHR)
- [ ] Predictive analytics for crisis prevention

---

**Made with ❤️ for mental health awareness and support**
