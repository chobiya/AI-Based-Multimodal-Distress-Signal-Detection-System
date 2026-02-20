import speech_recognition as sr
import webbrowser
import geocoder

# Trigger phrase
TRIGGER_PHRASE = "help me"

def get_location_url():
    try:
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            lat, lon = g.latlng
            print(f"📍 Your Location: Latitude = {lat}, Longitude = {lon}")
            return f"https://www.google.com/maps/search/{lat},{lon}"
        else:
            print("⚠ Could not fetch location from IP")
            return "https://www.google.com/maps"
    except Exception as e:
        print(f"❌ Error while fetching location: {e}")
        return "https://www.google.com/maps"

def listen_for_trigger():
    print("✅ voice_trigger.py is running... Listening for trigger phrase.")
    recognizer = sr.Recognizer()

    try:
        mic = sr.Microphone()
    except OSError as e:
        print("❌ Microphone not accessible:", e)
        return

    print("🎙 Speak now...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio).lower()
        print(f"🗣 You said: {text}")

        if TRIGGER_PHRASE in text:
            print("🚨 Emergency Trigger Detected!")
            map_url = get_location_url()
            print(f"🗺 Opening map at: {map_url}")
            webbrowser.open(map_url)
        else:
            print("❌ Trigger phrase not detected.")

    except sr.UnknownValueError:
        print("😕 Could not understand your speech")
    except sr.RequestError as e:
        print(f"🌐 API Error: {e}")

if  __name__ == "__main__":
    try:
        listen_for_trigger()
    except Exception as err:
        print(f"❌ Unexpected Error: {err}")