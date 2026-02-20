import json
import webbrowser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def emergency_response():
    # Read live GPS location
    location_file = "runtime/location.json"
    if not os.path.exists(location_file):
        print("❌ No location found. Run GPS module first.")
        return

    with open(location_file, "r", encoding="utf-8") as f:
        coords = json.load(f)

    lat = coords.get("latitude")
    lon = coords.get("longitude")

    if not lat or not lon:
        print("❌ GPS coordinates missing.")
        return

    maps_link = f"https://maps.google.com/?q={lat},{lon}"
    print(f"📍 Location: {maps_link}")

    # Open in browser
    webbrowser.open(maps_link)

    # Read contacts
    with open("data/contacts.json", "r", encoding="utf-8") as f:
        contacts = json.load(f)

    # Send Email Alerts
    sender_email = "youremail@gmail.com"
    sender_password = "your-app-password"  # Use Gmail App Password

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        for contact in contacts:
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = contact["email"]
            msg["Subject"] = "🚨 Emergency Alert"
            body = f"Help needed! My live location: {maps_link}"
            msg.attach(MIMEText(body, "plain"))
            server.sendmail(sender_email, contact["email"], msg.as_string())
            print(f"✅ Alert sent to {contact['name']} ({contact['email']})")

        server.quit()
    except Exception as e:
        print(f"❌ Failed to send email: {e}")