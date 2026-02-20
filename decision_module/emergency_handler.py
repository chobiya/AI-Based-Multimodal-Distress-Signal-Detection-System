import webbrowser
import time

def handle_emergency():
    print("⚠ Emergency Trigger Confirmed.")
    print("📍 Locating and taking action...")

    # Open Google Maps for location (can integrate real-time later)
    latitude = 13.0827
    longitude = 80.2707
    maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"
    webbrowser.open(maps_url)

    # Optional: Simulate alert
    print("📢 Playing alarm sound (simulated)")
    time.sleep(2)
    print("📩 Sending SMS alert (simulated)")

    print("✅ Emergency response actions completed.")

if __name__ == "__main__":
    handle_emergency()