"""
Automated Check-In Scheduler for Empathibot
Handles scheduled wellness check-ins and follow-ups
"""

import os
from datetime import datetime, timedelta
from typing import List, Dict
from firebase_admin import firestore
from twilio.rest import Client
import schedule
import time
import threading


class CheckInScheduler:
    """Manages automated wellness check-ins for users"""

    def __init__(self, db, empathibot, twilio_account_sid=None, twilio_auth_token=None, twilio_whatsapp_number=None):
        self.db = db
        self.empathibot = empathibot

        # Twilio setup for sending messages
        self.twilio_account_sid = twilio_account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = twilio_auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_whatsapp_number = twilio_whatsapp_number or os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

        if self.twilio_account_sid and self.twilio_auth_token:
            self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
        else:
            self.twilio_client = None
            print("⚠️ Twilio credentials not found. Check-ins will be logged but not sent.")

    def get_users_for_check_in(self) -> List[Dict]:
        """Get list of users who should receive check-ins"""
        users_ref = self.db.collection('whatsapp_users')

        # Get users who have check-ins enabled
        query = users_ref.where('check_in_enabled', '==', True)

        eligible_users = []
        for user_doc in query.stream():
            user_data = user_doc.to_dict()
            user_data['id'] = user_doc.id

            # Check if enough time has passed since last check-in
            last_check_in = user_data.get('last_check_in')

            # Send check-in if:
            # 1. Never received one before, OR
            # 2. Last check-in was more than 24 hours ago
            should_send = True

            if last_check_in:
                # Convert Firestore timestamp to datetime if needed
                if hasattr(last_check_in, 'timestamp'):
                    last_check_in = datetime.fromtimestamp(last_check_in.timestamp())

                time_since_last = datetime.now() - last_check_in
                if time_since_last < timedelta(hours=24):
                    should_send = False

            if should_send:
                eligible_users.append(user_data)

        return eligible_users

    def send_check_in_message(self, user: Dict):
        """Send a check-in message to a specific user"""
        try:
            user_id = user['id']
            phone_number = user['phone_number']

            # Generate personalized check-in message
            check_in_message = self.empathibot.send_check_in(user_id)

            # Send via Twilio if available
            if self.twilio_client:
                message = self.twilio_client.messages.create(
                    body=check_in_message,
                    from_=self.twilio_whatsapp_number,
                    to=phone_number
                )

                print(f"✅ Check-in sent to {phone_number}: {message.sid}")

                # Update user's last check-in time
                user_ref = self.db.collection('whatsapp_users').document(user_id)
                user_ref.update({
                    'last_check_in': firestore.SERVER_TIMESTAMP
                })

                # Log the check-in
                self.db.collection('check_in_logs').add({
                    'user_id': user_id,
                    'phone_number': phone_number,
                    'message': check_in_message,
                    'status': 'sent',
                    'twilio_sid': message.sid,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })

                return True
            else:
                # Just log it
                print(f"📝 Check-in generated for {phone_number}: {check_in_message}")

                self.db.collection('check_in_logs').add({
                    'user_id': user_id,
                    'phone_number': phone_number,
                    'message': check_in_message,
                    'status': 'generated_not_sent',
                    'timestamp': firestore.SERVER_TIMESTAMP
                })

                return False

        except Exception as e:
            print(f"❌ Error sending check-in to {user.get('phone_number')}: {e}")

            # Log error
            self.db.collection('check_in_errors').add({
                'user_id': user.get('id'),
                'phone_number': user.get('phone_number'),
                'error': str(e),
                'timestamp': firestore.SERVER_TIMESTAMP
            })

            return False

    def run_daily_check_ins(self):
        """Run daily check-ins for all eligible users"""
        print("🔄 Running daily check-ins...")

        eligible_users = self.get_users_for_check_in()
        print(f"📊 Found {len(eligible_users)} users eligible for check-in")

        sent_count = 0
        for user in eligible_users:
            if self.send_check_in_message(user):
                sent_count += 1
            # Small delay to avoid rate limiting
            time.sleep(1)

        print(f"✅ Daily check-ins completed: {sent_count}/{len(eligible_users)} sent")

        return {
            'eligible_users': len(eligible_users),
            'sent_count': sent_count,
            'timestamp': datetime.now().isoformat()
        }

    def send_crisis_follow_up(self, user_id: str, severity: str):
        """Send follow-up after a crisis alert"""
        try:
            user_ref = self.db.collection('whatsapp_users').document(user_id)
            user = user_ref.get().to_dict()

            if not user:
                print(f"❌ User {user_id} not found for crisis follow-up")
                return False

            phone_number = user['phone_number']

            # Different follow-up messages based on severity
            if severity == 'critical':
                follow_up = """💙 Checking in after our conversation. I'm still here if you need support.

Please remember:
📞 988 - Available 24/7
📱 Crisis Text Line: Text HOME to 741741

You matter, and people care about you. How are you doing right now?"""

            elif severity == 'high':
                follow_up = """💙 Hi, I wanted to follow up and see how you're feeling now.

Remember that I'm here to listen, and professional support is available if you need it.

How are things going?"""

            else:
                follow_up = """💙 Just checking in on you. How are you feeling today?

I'm here if you want to talk about anything."""

            # Send via Twilio if available
            if self.twilio_client:
                message = self.twilio_client.messages.create(
                    body=follow_up,
                    from_=self.twilio_whatsapp_number,
                    to=phone_number
                )

                print(f"✅ Crisis follow-up sent to {phone_number}: {message.sid}")

                # Log the follow-up
                self.db.collection('crisis_follow_ups').add({
                    'user_id': user_id,
                    'phone_number': phone_number,
                    'severity': severity,
                    'message': follow_up,
                    'status': 'sent',
                    'twilio_sid': message.sid,
                    'timestamp': firestore.SERVER_TIMESTAMP
                })

                return True
            else:
                print(f"📝 Crisis follow-up generated for {phone_number}")

                self.db.collection('crisis_follow_ups').add({
                    'user_id': user_id,
                    'phone_number': phone_number,
                    'severity': severity,
                    'message': follow_up,
                    'status': 'generated_not_sent',
                    'timestamp': firestore.SERVER_TIMESTAMP
                })

                return False

        except Exception as e:
            print(f"❌ Error sending crisis follow-up: {e}")
            return False

    def schedule_crisis_follow_ups(self):
        """Check for recent crisis alerts and schedule follow-ups"""
        print("🔄 Checking for crisis alerts needing follow-up...")

        # Get crisis alerts from the last 24 hours that haven't been followed up
        alerts_ref = self.db.collection('crisis_alerts')

        # Get recent alerts
        recent_alerts = []
        for alert_doc in alerts_ref.stream():
            alert_data = alert_doc.to_dict()

            # Check if timestamp is within last 24 hours
            timestamp = alert_data.get('timestamp')
            if hasattr(timestamp, 'timestamp'):
                alert_time = datetime.fromtimestamp(timestamp.timestamp())
                time_since = datetime.now() - alert_time

                if time_since < timedelta(hours=24) and time_since > timedelta(hours=4):
                    # Check if follow-up already sent
                    follow_ups_ref = self.db.collection('crisis_follow_ups')
                    existing_follow_up = follow_ups_ref.where('user_id', '==', alert_data.get('user_id')).limit(1).stream()

                    if not list(existing_follow_up):
                        recent_alerts.append(alert_data)

        print(f"📊 Found {len(recent_alerts)} crisis alerts needing follow-up")

        sent_count = 0
        for alert in recent_alerts:
            if self.send_crisis_follow_up(alert.get('user_id'), alert.get('severity')):
                sent_count += 1
            time.sleep(1)

        print(f"✅ Crisis follow-ups completed: {sent_count}/{len(recent_alerts)} sent")

        return {
            'alerts_needing_followup': len(recent_alerts),
            'sent_count': sent_count,
            'timestamp': datetime.now().isoformat()
        }

    def start_scheduler(self):
        """Start the background scheduler"""
        # Schedule daily check-ins at 10 AM
        schedule.every().day.at("10:00").do(self.run_daily_check_ins)

        # Schedule crisis follow-ups every 4 hours
        schedule.every(4).hours.do(self.schedule_crisis_follow_ups)

        print("✅ Scheduler started")
        print("   - Daily check-ins: 10:00 AM")
        print("   - Crisis follow-ups: Every 4 hours")

        # Run in background thread
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute

        scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
        scheduler_thread.start()

        return scheduler_thread


# Standalone script for testing
if __name__ == "__main__":
    from dotenv import load_dotenv
    import firebase_admin
    from firebase_admin import credentials
    from langchain_community.llms import OpenAI
    from empathibot import Empathibot
    import json

    load_dotenv()

    # Firebase setup
    firebase_json = os.getenv("FIREBASE_CONFIG_JSON")
    cred = credentials.Certificate(json.loads(firebase_json))
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    # LLM setup
    llm = OpenAI(temperature=0.7, max_tokens=250)

    # Initialize Empathibot
    empathibot = Empathibot(db=db, llm=llm)

    # Initialize scheduler
    scheduler = CheckInScheduler(db=db, empathibot=empathibot)

    # Run check-ins immediately for testing
    print("Running test check-ins...")
    result = scheduler.run_daily_check_ins()
    print(f"Result: {result}")
