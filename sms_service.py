from twilio.rest import Client
import os

# Load Twilio credentials (make sure you replaced with real ones in config.py or env vars)
account_sid = "YOUR_TWILIO_ACCOUNT_SID"
auth_token = "YOUR_TWILIO_AUTH_TOKEN"
twilio_number = "YOUR_TWILIO_PHONE_NUMBER"

client = Client(account_sid, auth_token)

def send_sms_to_contacts(contacts, body):
    results = []
    for c in contacts:
        try:
            phone = c["phone"] if isinstance(c, dict) else c
            message = client.messages.create(
                body=body,
                from_=twilio_number,
                to=phone
            )
            results.append({"phone": phone, "status": "sent"})
            print(f"✅ SMS sent to {phone}")
        except Exception as e:
            results.append({"phone": phone, "status": "failed", "error": str(e)})
            print(f"❌ Failed for {phone}: {e}")
    return results
