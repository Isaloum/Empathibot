# MindCare - Mental Health Support Platform

A comprehensive mental health support application that combines professional assessment tools, AI-powered analysis, and 24/7 WhatsApp chatbot support to help users monitor and improve their mental wellness.

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

### 💬 24/7 WhatsApp Support
- **Empathibot**: Empathetic AI chatbot available around the clock
- **Instant Support**: Immediate responses to mental health concerns
- **Crisis Intervention**: Automatic detection and response to crisis situations
- **Resource Sharing**: Access to mental health resources and emergency contacts

### 📊 Interactive Dashboard
- **Visual Progress Tracking**: Charts and graphs showing mental health trends
- **Assessment History**: Complete record of all evaluations
- **Personalized Insights**: Data-driven recommendations for improvement
- **Quick Stats**: At-a-glance overview of mental health status

### 🔒 Security & Privacy
- **Data Encryption**: All sensitive data is encrypted and secure
- **HIPAA Compliance**: Following healthcare privacy standards
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

## 🔧 API Endpoints

### User Management
- `POST /api/register` - Register new user
- `GET /api/user/<user_id>/history` - Get user assessment history

### Assessment & Analysis
- `POST /api/analyze` - Submit assessment for analysis
- `GET /api/crisis-resources` - Get crisis support resources

### WhatsApp Integration
- `POST /whatsapp` - Webhook for WhatsApp messages
- `GET /health` - Health check endpoint

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

### Upcoming Features
- [ ] Mobile app (iOS/Android)
- [ ] Integration with wearable devices
- [ ] Machine learning-based mood prediction
- [ ] Therapist matching and booking
- [ ] Group support features
- [ ] Multilingual support
- [ ] Advanced analytics and reporting

### Long-term Goals
- [ ] Clinical validation studies
- [ ] Healthcare provider integration
- [ ] Insurance coverage support
- [ ] Community features and forums
- [ ] AI therapy sessions
- [ ] Medication tracking and reminders

---

**Made with ❤️ for mental health awareness and support**