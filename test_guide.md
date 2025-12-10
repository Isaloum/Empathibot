# 🧪 MindCare Testing Guide

## Quick Testing Options

### 1. 🚀 Immediate Demo (No Setup Required)
```bash
python3 simple_demo.py
```
This runs a standalone demo showing how the mental health analysis works.

### 2. 🔧 Basic Local Testing (Minimal Setup)
```bash
# Install basic dependencies
pip3 install flask python-dotenv

# Create minimal .env file
echo "SECRET_KEY=test-secret-key-123" > .env

# Run basic version
python3 test_app_basic.py
```

### 3. 🌟 Full Application Testing (Complete Setup)
```bash
# Full setup with all features
python3 setup.py
# Edit .env file with your API keys
python3 app.py
```

## Testing Methods by Complexity

### Level 1: Core Logic Testing ✅
- No external dependencies
- Tests mental health algorithms
- Instant results

### Level 2: Web Interface Testing 🌐
- Basic Flask app
- HTML interface
- Local database simulation

### Level 3: Full Integration Testing 🚀
- Firebase integration
- OpenAI API
- WhatsApp bot
- Complete features

## What Each Test Covers

### ✅ Core Logic Test
- PHQ-9 depression scoring
- GAD-7 anxiety analysis
- Sentiment analysis
- Risk level calculation
- Recommendation generation

### 🌐 Web Interface Test
- Registration flow
- Assessment forms
- Results display
- Dashboard functionality
- Crisis resources

### 🚀 Full Integration Test
- Database storage
- AI-powered responses
- WhatsApp integration
- Real-time analytics
- Security features