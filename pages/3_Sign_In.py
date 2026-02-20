import streamlit as st
import bcrypt
from auth.db import authenticate_user

st.set_page_config(page_title="Sign In - Alertify", page_icon="🔑", layout="centered")

# CSS
st.markdown("""
    <style>
        .signin-box {
            background: #111827;
            padding: 40px;
            border-radius: 15px;
            color: white;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
        }
        .signin-title {
            text-align: center; 
            font-size: 32px; 
            font-weight: bold; 
            color: #00e0ff;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='signin-box'>", unsafe_allow_html=True)
st.markdown("<h1 class='signin-title'>🔑 Sign In to Alertify</h1>", unsafe_allow_html=True)

with st.form("signin_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Sign In")

    if submitted:
        user = authenticate_user(username)
        if not user:
            st.error("❌ User not found.")
        elif bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success("✅ Login successful! Go to SOS Dashboard.")
        else:
            st.error("❌ Invalid credentials.")

st.markdown("</div>", unsafe_allow_html=True)
