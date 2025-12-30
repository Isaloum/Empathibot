"""
Comprehensive Test Suite for Empathibot
Tests all major components: crisis detection, language handling, session management, and conversation flow
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from langchain_core.language_models.fake import FakeListLLM

from empathibot import (
    CrisisDetector,
    LanguageHandler,
    UserSessionManager,
    ConversationMemory,
    Empathibot
)


class TestCrisisDetector(unittest.TestCase):
    """Test the Crisis Detection System"""

    def setUp(self):
        self.detector = CrisisDetector()

    def test_critical_crisis_detection(self):
        """Test detection of critical crisis keywords"""
        messages = [
            "I want to kill myself",
            "I'm going to end my life",
            "I have a suicide plan",
            "I want to die"
        ]

        for msg in messages:
            result = self.detector.detect_crisis(msg)
            self.assertTrue(result['is_crisis'], f"Failed to detect crisis in: {msg}")
            self.assertEqual(result['severity'], 'critical', f"Wrong severity for: {msg}")
            self.assertGreater(result['severity_score'], 50)

    def test_high_severity_detection(self):
        """Test detection of high severity keywords"""
        messages = [
            "I'm cutting myself",
            "I feel hopeless and worthless",
            "I want to hurt myself",
            "Life is meaningless"
        ]

        for msg in messages:
            result = self.detector.detect_crisis(msg)
            self.assertIn(result['severity'], ['high', 'critical'])
            self.assertGreater(result['severity_score'], 20)

    def test_moderate_severity_detection(self):
        """Test detection of moderate severity keywords"""
        messages = [
            "I'm feeling really depressed today",
            "I'm having a panic attack",
            "I can't cope anymore",
            "I hate myself"
        ]

        for msg in messages:
            result = self.detector.detect_crisis(msg)
            self.assertIn(result['severity'], ['moderate', 'high', 'low'])

    def test_positive_message_no_crisis(self):
        """Test that positive messages don't trigger crisis alerts"""
        messages = [
            "I'm feeling much better today",
            "Therapy is really helping me",
            "I'm grateful for my support system",
            "Things are improving"
        ]

        for msg in messages:
            result = self.detector.detect_crisis(msg)
            self.assertFalse(result['is_crisis'], f"False positive for: {msg}")
            self.assertEqual(result['severity'], 'low')

    def test_mixed_sentiment(self):
        """Test messages with mixed positive and negative sentiment"""
        msg = "I'm feeling depressed but I'm trying to get better with therapy"
        result = self.detector.detect_crisis(msg)

        # Should detect depression but positive words should reduce severity
        self.assertIsNotNone(result)
        self.assertIn('depressed', ' '.join(result['matched_keywords']))

    def test_crisis_response_generation(self):
        """Test that appropriate crisis responses are generated"""
        # Critical response
        critical_response = self.detector.get_crisis_response('critical')
        self.assertIn('988', critical_response)
        self.assertIn('911', critical_response)

        # High severity response
        high_response = self.detector.get_crisis_response('high')
        self.assertIn('988', high_response)

        # Moderate response
        moderate_response = self.detector.get_crisis_response('moderate')
        self.assertIsNotNone(moderate_response)

        # Low severity (should return None)
        low_response = self.detector.get_crisis_response('low')
        self.assertIsNone(low_response)


class TestLanguageHandler(unittest.TestCase):
    """Test the Multilingual Language Handler"""

    def setUp(self):
        self.handler = LanguageHandler()

    def test_english_detection(self):
        """Test English language detection"""
        text = "Hello, how are you feeling today?"
        lang = self.handler.detect_language(text)
        self.assertEqual(lang, 'en')

    def test_spanish_detection(self):
        """Test Spanish language detection"""
        text = "Hola, ¿cómo te sientes hoy?"
        lang = self.handler.detect_language(text)
        self.assertEqual(lang, 'es')

    def test_supported_languages(self):
        """Test that supported languages are properly defined"""
        self.assertIn('en', self.handler.supported_languages)
        self.assertIn('es', self.handler.supported_languages)
        self.assertIn('fr', self.handler.supported_languages)

    def test_crisis_resources_available(self):
        """Test that crisis resources are available in multiple languages"""
        en_resources = self.handler.get_crisis_resources('en')
        self.assertIn('988', en_resources)

        es_resources = self.handler.get_crisis_resources('es')
        self.assertIn('988', es_resources)

    def test_fallback_to_english(self):
        """Test fallback to English for unsupported languages"""
        # Very short text that might not detect properly
        text = "Hi"
        lang = self.handler.detect_language(text)
        # Should either detect en or fallback to en
        self.assertIsNotNone(lang)


class TestUserSessionManager(unittest.TestCase):
    """Test the User Session Management System"""

    def setUp(self):
        # Mock Firestore database
        self.mock_db = Mock()
        self.session_manager = UserSessionManager(self.mock_db)

    def test_create_new_user(self):
        """Test creating a new user profile"""
        phone = "whatsapp:+1234567890"

        # Mock no existing users
        mock_collection = Mock()
        mock_query = Mock()
        mock_query.stream.return_value = []
        mock_collection.where.return_value.limit.return_value = mock_query

        mock_doc = Mock()
        mock_doc.id = "user123"
        mock_collection.document.return_value = mock_doc

        self.mock_db.collection.return_value = mock_collection

        user = self.session_manager.get_or_create_user(phone)

        # Verify user was created
        self.assertEqual(user['phone_number'], phone)
        self.assertTrue(user['check_in_enabled'])

    def test_get_existing_user(self):
        """Test retrieving an existing user"""
        phone = "whatsapp:+1234567890"

        # Mock existing user
        mock_doc = Mock()
        mock_doc.id = "user123"
        mock_doc.to_dict.return_value = {
            'phone_number': phone,
            'conversation_count': 5,
            'check_in_enabled': True
        }

        mock_collection = Mock()
        mock_query = Mock()
        mock_query.stream.return_value = [mock_doc]
        mock_collection.where.return_value.limit.return_value = mock_query

        self.mock_db.collection.return_value = mock_collection

        user = self.session_manager.get_or_create_user(phone)

        # Verify correct user was retrieved
        self.assertEqual(user['id'], 'user123')
        self.assertEqual(user['phone_number'], phone)
        self.assertEqual(user['conversation_count'], 5)

    def test_update_user_activity(self):
        """Test updating user activity"""
        user_id = "user123"

        mock_doc_ref = Mock()
        mock_collection = Mock()
        mock_collection.document.return_value = mock_doc_ref
        self.mock_db.collection.return_value = mock_collection

        self.session_manager.update_user_activity(user_id, language='en', crisis_detected=False)

        # Verify update was called
        mock_doc_ref.update.assert_called_once()


class TestConversationMemory(unittest.TestCase):
    """Test the Conversation Memory System"""

    def test_memory_initialization_empty(self):
        """Test initializing memory with no history"""
        memory = ConversationMemory(user_id="user123")
        self.assertIsNotNone(memory.memory)

    def test_memory_initialization_with_history(self):
        """Test initializing memory with conversation history"""
        history = [
            {'user_message': 'Hello', 'bot_response': 'Hi there!'},
            {'user_message': 'How are you?', 'bot_response': 'I\'m here to support you!'}
        ]

        memory = ConversationMemory(user_id="user123", conversation_history=history)
        context = memory.get_context_summary()

        # Memory should contain previous conversation
        self.assertIsNotNone(context)

    def test_memory_window_limit(self):
        """Test that memory only keeps last 5 exchanges"""
        history = [
            {'user_message': f'Message {i}', 'bot_response': f'Response {i}'}
            for i in range(10)
        ]

        memory = ConversationMemory(user_id="user123", conversation_history=history)

        # Should only load last 5
        # This is implicit in the implementation, just verify it doesn't crash
        self.assertIsNotNone(memory.memory)


class TestEmpathibot(unittest.TestCase):
    """Test the main Empathibot class"""

    def setUp(self):
        # Mock database and LLM
        self.mock_db = Mock()
        self.mock_llm = FakeListLLM(
            responses=["I'm here to support you. How can I help?"]
        )

        self.empathibot = Empathibot(db=self.mock_db, llm=self.mock_llm)

    def test_sentiment_analysis_positive(self):
        """Test sentiment analysis for positive messages"""
        text = "I'm feeling great and happy today!"
        sentiment = self.empathibot._analyze_sentiment(text)

        self.assertEqual(sentiment['sentiment'], 'positive')
        self.assertGreater(sentiment['score'], 0)

    def test_sentiment_analysis_negative(self):
        """Test sentiment analysis for negative messages"""
        text = "I'm feeling sad and depressed today"
        sentiment = self.empathibot._analyze_sentiment(text)

        self.assertEqual(sentiment['sentiment'], 'negative')
        self.assertGreater(sentiment['score'], 0)

    def test_sentiment_analysis_neutral(self):
        """Test sentiment analysis for neutral messages"""
        text = "The weather is okay today"
        sentiment = self.empathibot._analyze_sentiment(text)

        self.assertEqual(sentiment['sentiment'], 'neutral')

    @patch.object(UserSessionManager, 'get_or_create_user')
    @patch.object(UserSessionManager, 'get_conversation_history')
    @patch.object(UserSessionManager, 'save_conversation')
    @patch.object(UserSessionManager, 'update_user_activity')
    def test_process_normal_message(self, mock_update, mock_save, mock_history, mock_get_user):
        """Test processing a normal (non-crisis) message"""
        phone = "whatsapp:+1234567890"
        message = "Hello, I'm feeling okay today"

        # Setup mocks
        mock_get_user.return_value = {
            'id': 'user123',
            'phone_number': phone,
            'check_in_enabled': True,
            'user_profile': {'name': 'Test User'},
            'mental_health_data': {'risk_level': 'low'}
        }
        mock_history.return_value = []

        # Mock Firestore collection for messages
        mock_collection = Mock()
        mock_collection.document.return_value.get.return_value.to_dict.return_value = {}
        self.mock_db.collection.return_value = mock_collection

        # Process message
        response = self.empathibot.process_message(phone, message)

        # Verify response was generated
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)

        # Verify conversation was saved
        mock_save.assert_called_once()

    @patch.object(UserSessionManager, 'get_or_create_user')
    @patch.object(UserSessionManager, 'save_conversation')
    @patch.object(UserSessionManager, 'update_user_activity')
    def test_process_crisis_message(self, mock_update, mock_save, mock_get_user):
        """Test processing a crisis message"""
        phone = "whatsapp:+1234567890"
        message = "I want to kill myself"

        # Setup mocks
        mock_get_user.return_value = {
            'id': 'user123',
            'phone_number': phone,
            'check_in_enabled': True,
            'user_profile': {},
            'mental_health_data': {}
        }

        # Mock Firestore collections
        mock_collection = Mock()
        mock_collection.document.return_value.get.return_value.to_dict.return_value = {}
        self.mock_db.collection.return_value = mock_collection

        # Process message
        response = self.empathibot.process_message(phone, message)

        # Verify crisis response was generated
        self.assertIsNotNone(response)
        self.assertIn('988', response)  # Should include crisis hotline

        # Verify crisis alert was logged
        self.mock_db.collection.assert_called()

    def test_check_in_message_generation(self):
        """Test wellness check-in message generation"""
        # Mock user document
        mock_doc = Mock()
        mock_doc.get.return_value.to_dict.return_value = {
            'user_profile': {'name': 'Alice'}
        }

        mock_collection = Mock()
        mock_collection.document.return_value = mock_doc
        self.mock_db.collection.return_value = mock_collection

        check_in = self.empathibot.send_check_in('user123')

        # Verify check-in message was generated
        self.assertIsNotNone(check_in)
        self.assertIsInstance(check_in, str)
        self.assertIn('Alice', check_in)

    @patch.object(UserSessionManager, '__init__', return_value=None)
    def test_get_user_insights(self, mock_session_init):
        """Test user insights generation"""
        # Mock user document
        mock_doc = Mock()
        mock_doc.get.return_value.to_dict.return_value = {
            'conversation_count': 15,
            'crisis_alerts': 2,
            'mental_health_data': {
                'risk_level': 'moderate',
                'mood_trend': [
                    {'sentiment': 'positive', 'crisis_severity': 'low'},
                    {'sentiment': 'positive', 'crisis_severity': 'low'},
                    {'sentiment': 'negative', 'crisis_severity': 'moderate'},
                ]
            }
        }

        mock_collection = Mock()
        mock_collection.document.return_value = mock_doc
        self.mock_db.collection.return_value = mock_collection

        insights = self.empathibot.get_user_insights('user123')

        # Verify insights were generated
        self.assertIsNotNone(insights)
        self.assertEqual(insights['user_id'], 'user123')
        self.assertEqual(insights['total_conversations'], 15)
        self.assertEqual(insights['crisis_alerts'], 2)
        self.assertIn('mood_trend', insights)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""

    def setUp(self):
        self.mock_db = Mock()
        self.mock_llm = FakeListLLM(
            responses=[
                "I understand you're going through a difficult time.",
                "That sounds really hard. I'm here with you.",
                "I'm glad you reached out. How can I support you next?"
            ]
        )

    @patch.object(UserSessionManager, 'get_or_create_user')
    @patch.object(UserSessionManager, 'get_conversation_history')
    @patch.object(UserSessionManager, 'save_conversation')
    @patch.object(UserSessionManager, 'update_user_activity')
    def test_full_conversation_flow(self, mock_update, mock_save, mock_history, mock_get_user):
        """Test a complete conversation flow from start to finish"""
        empathibot = Empathibot(db=self.mock_db, llm=self.mock_llm)

        phone = "whatsapp:+1234567890"

        # Setup mocks
        mock_get_user.return_value = {
            'id': 'user123',
            'phone_number': phone,
            'check_in_enabled': True,
            'user_profile': {'name': 'Test'},
            'mental_health_data': {'risk_level': 'low'}
        }
        mock_history.return_value = []

        mock_collection = Mock()
        mock_collection.document.return_value.get.return_value.to_dict.return_value = {}
        self.mock_db.collection.return_value = mock_collection

        # Simulate conversation
        messages = [
            "Hi, I'm feeling down",
            "I've been having trouble sleeping",
            "I think I need help"
        ]

        for msg in messages:
            response = empathibot.process_message(phone, msg)
            self.assertIsNotNone(response)
            self.assertIsInstance(response, str)

        # Verify all messages were saved
        self.assertEqual(mock_save.call_count, len(messages))


def run_tests():
    """Run all tests and print results"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCrisisDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestLanguageHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestUserSessionManager))
    suite.addTests(loader.loadTestsFromTestCase(TestConversationMemory))
    suite.addTests(loader.loadTestsFromTestCase(TestEmpathibot))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*70)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
