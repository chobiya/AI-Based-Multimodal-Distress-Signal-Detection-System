import streamlit as st
from auth.db import init_db

# Import the geolocation component
from streamlit_geolocation import streamlit_geolocation

init_db()
st.set_page_config(page_title="Alertify - Home", layout="wide")

# Custom CSS for Alertify Look
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #000428, #004e92);
            color: white;
        }
        .big-title {
            text-align: center; 
            font-size: 55px; 
            font-weight: bold; 
            color: #00e0ff; 
            text-shadow: 0px 0px 15px #00e0ff;
        }
        .subtitle {
            text-align: center; 
            font-size: 20px; 
            margin-bottom: 40px; 
            color: #ddd;
        }
        .feature-card {
            padding: 25px; 
            border-radius: 15px; 
            background: #111827; 
            color: white; 
            text-align: center; 
            box-shadow: 0 6px 15px rgba(0,0,0,0.5);
            transition: transform 0.3s, background 0.3s;
        }
        .feature-card:hover {
            transform: scale(1.05);
            background: #1f2937;
        }
        .footer {
            text-align: center; 
            color: gray; 
            margin-top: 50px;
        }
        button {
            border-radius: 20px !important;
            padding: 10px 20px !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("<h1 class='big-title'>🚨 Welcome to Alertify</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Personal Safety Assistant - Voice, Gesture & Real-Time SOS Alerts</p>", unsafe_allow_html=True)

# CTA Buttons
col1, col2 = st.columns(2)
with col1:
    if st.button("👉 Get Started"):
        st.experimental_set_query_params(page="2_Sign_Up")
        st.experimental_rerun()
with col2:
    if st.button("🔑 Sign In"):
        st.experimental_set_query_params(page="3_Sign_In")
        st.experimental_rerun()

st.markdown("---")

# Features Section
st.subheader("✨ Features")
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='feature-card'>🎙<br><b>Voice Alerts</b><br>Say 'Help Me' to trigger instant alerts.</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='feature-card'>🖐<br><b>Gesture Detection</b><br>Silent hand gestures activate SOS mode.</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='feature-card'>📍<br><b>Live Location</b><br>Shares your GPS location with emergency contacts.</div>", unsafe_allow_html=True)

col4, col5, col6 = st.columns(3)
with col4:
    st.markdown("<div class='feature-card'>📲<br><b>Instant SMS</b><br>Emergency alerts are sent to your contacts.</div>", unsafe_allow_html=True)
with col5:
    st.markdown("<div class='feature-card'>👥<br><b>Contact Management</b><br>Add & manage trusted emergency contacts.</div>", unsafe_allow_html=True)
with col6:
    st.markdown("<div class='feature-card'>🔒<br><b>Privacy & Security</b><br>Your data is encrypted and safe.</div>", unsafe_allow_html=True)

st.markdown("---")

# Location Section (using browser-assisted location, which uses WiFi if available)
st.subheader("📍 Your Current Location (via WiFi / Browser)")

location = streamlit_geolocation()
if location and location.get("latitude") and location.get("longitude"):
    lat = location["latitude"]
    lon = location["longitude"]
    st.success(f"Latitude: {lat}, Longitude: {lon}")
    maps_url = f"https://www.google.com/maps/@{lat},{lon},15z"
    st.markdown(f"🌍 [Open in Google Maps]({maps_url})", unsafe_allow_html=True)
    st.components.v1.iframe(maps_url, width=700, height=450)
else:
    st.warning("Unable to fetch your location. Please allow location access in your browser and connect to WiFi for best results.")

# Footer
st.markdown("<p class='footer'>© 2025 Alertify Emergency Alert System | Built with ❤ for your safety.</p>", unsafe_allow_html=True)
