import streamlit as str
from src.utils import get_welcome_message

# Configure the web page
st.set_page_config(
    page_title="My Python Web App",
    page_icon="🚀",
    layout="centered"
)

# Sidebar navigation is automatically handled by Streamlit because of the 'pages' folder
st.sidebar.success("Select a page above.")

# Main content
st.title("🚀 Welcome to My Python Frontend Application")
st.write("This is a clean, simple web app built entirely in Python.")

# Using a helper function from our src/ directory
message = get_welcome_message()
st.info(message)

# Interactive Widget Example
st.subheader("Interactive Playground")
user_name = st.text_input("What is your name?", placeholder="Type here...")

if user_name:
    st.success(f"Hello, {user_name}! Thanks for checking out this app.")