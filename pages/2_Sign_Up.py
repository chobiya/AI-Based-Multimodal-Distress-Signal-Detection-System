import streamlit as st
import bcrypt
from auth.db import create_user

st.set_page_config(page_title="Sign Up - Alertify", page_icon="🆕", layout="centered")

# CSS
st.markdown("""
    <style>
        .signup-box {
            background: #111827;
            padding: 40px;
            border-radius: 15px;
            color: white;
            box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
        }
        .signup-title {
            text-align: center; 
            font-size: 32px; 
            font-weight: bold; 
            color: #00e0ff;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='signup-box'>", unsafe_allow_html=True)
st.markdown("<h1 class='signup-title'>🚀 Join Alertify</h1>", unsafe_allow_html=True)

with st.form("signup_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    submitted = st.form_submit_button("Create Emergency Account")

    if submitted:
        if password != confirm_password:
            st.error("❌ Passwords do not match.")
        elif not username or not password:
            st.warning("⚠ Please fill in all fields.")
        else:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            create_user(username, hashed_pw, first_name, last_name)
            st.success("✅ Account created successfully! Please go to Sign In.")

st.markdown("</div>", unsafe_allow_html=True)
