# pages/4_SOS_Dashboard.py
import json
from pathlib import Path
import time
import os

import streamlit as st
from streamlit_js_eval import get_geolocation
import geocoder
import folium
from streamlit_folium import st_folium

from sms_service import send_sms_to_contacts
from emergency_module.emergency_alert import emergency_response

st.set_page_config(page_title="SOS Dashboard", layout="wide")

# -------------------- Helpers --------------------
CONTACTS_FILE = Path("contacts.json")
RUNTIME_FILE = Path("runtime/location.json")

def load_contacts():
    """Load and normalize contacts from contacts.json"""
    if not CONTACTS_FILE.exists():
        return []

    with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Case 1: {"contacts": [...]}
    if isinstance(data, dict) and "contacts" in data:
        raw_list = data["contacts"]
    # Case 2: plain list
    elif isinstance(data, list):
        raw_list = data
    else:
        return []

    normalized = []
    for item in raw_list:
        if isinstance(item, str):  # e.g. ["+911234..."]
            normalized.append({"name": item, "phone": item})
        elif isinstance(item, dict) and "phone" in item:
            normalized.append({
                "name": item.get("name", item["phone"]),
                "phone": item["phone"]
            })

    return normalized
def save_runtime_location(lat, lon):
    RUNTIME_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RUNTIME_FILE, "w", encoding="utf-8") as f:
        json.dump({"latitude": lat, "longitude": lon, "timestamp": int(time.time())}, f, indent=2)

def get_best_location():
    # 1) Browser geolocation
    loc = get_geolocation()
    if loc and isinstance(loc, dict):
        coords = loc.get("coords") or {}
        lat = coords.get("latitude")
        lon = coords.get("longitude")
        if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
            return float(lat), float(lon), "browser"

    # 2) Cached
    if RUNTIME_FILE.exists():
        try:
            obj = json.loads(RUNTIME_FILE.read_text(encoding="utf-8"))
            return float(obj["latitude"]), float(obj["longitude"]), "cached"
        except Exception:
            pass

    # 3) IP-based fallback
    try:
        g = geocoder.ip("me")
        if g.ok and g.latlng:
            return float(g.latlng[0]), float(g.latlng[1]), "ip"
    except Exception:
        pass

    return None, None, None

def show_map(lat, lon):
    m = folium.Map(location=[lat, lon], zoom_start=16, control_scale=True)
    folium.Marker([lat, lon], tooltip="You are here").add_to(m)
    st_folium(m, width=900, height=450)

def format_maps_link(lat, lon):
    return f"https://www.google.com/maps?q={lat},{lon}"

def trigger_emergency_flow(trigger_source: str):
    """Shared function for Voice, Gesture, and Text"""
    with st.spinner(f"Getting location for {trigger_source}…"):
        lat, lon, source = get_best_location()

    if lat is not None and lon is not None:
        save_runtime_location(lat, lon)
        st.success(f"🚨 Emergency triggered via {trigger_source}! Location source: {source}")
        st.write(f"**Lat:** {lat:.6f} | **Lon:** {lon:.6f}")
        show_map(lat, lon)

        maps_url = format_maps_link(lat, lon)
        contacts = load_contacts()
        if not contacts:
            st.warning("⚠️ No contacts found in contacts.json")
        else:
            body = f"🚨 EMERGENCY: I need help.\nTriggered by: {trigger_source}\nLocation: {maps_url}\n(Lat {lat:.6f}, Lon {lon:.6f})"
            results = send_sms_to_contacts(contacts, body)
            st.subheader("📤 SMS Status")
            for r in results:
                if r["status"] == "sent":
                    st.success(f"Sent to {r['phone']} ✅")
                else:
                    st.error(f"Failed for {r['phone']}: {r['error']}")
        # also call your existing emergency flow
        emergency_response()
    else:
        st.error("❌ Could not get location. Please click **Allow** when browser asks.")

# -------------------- UI --------------------
st.title("🚨 Distress SOS System")
st.markdown("Choose how you want to trigger an emergency response.")

option = st.selectbox("Select input method:", ["Voice Trigger", "Gesture Trigger", "Text Trigger"])

# ---- Voice Trigger ----
if option == "Voice Trigger":
    st.warning("🎙 Listening for help keywords...")
    if st.button("Start Voice Detection"):
        os.system("python voice_module/voice_trigger.py")
        trigger_emergency_flow("Voice")

# ---- Gesture Trigger ----
elif option == "Gesture Trigger":
    st.info("📷 Activating camera for gesture detection...")
    if st.button("Start Gesture Detection"):
        os.system("python gesture_module/gesture_detector.py")
        trigger_emergency_flow("Gesture")

# ---- Text Trigger ----
elif option == "Text Trigger":
    st.subheader("📝 Text Trigger")
    code = st.text_input("Enter your secret code (example: HELP123)", type="password")

    if st.button("Trigger SOS via Text", type="primary"):
        if (code or "").strip().lower() == "help123":
            trigger_emergency_flow("Text")
        else:
            st.error("❌ Wrong secret code.")
