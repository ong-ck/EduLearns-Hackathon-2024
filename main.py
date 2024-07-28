from keep_alive import keep_alive
keep_alive()

import streamlit as st
from pathlib import Path
import importlib.util

# Dictionary of pages
# We do not name the folder "pages" because it will cause a navigation sidebar to appear - hence we use "quiz" as the folder name
PAGES = {
    "start": "quiz/start.py",
    "quiz": "quiz/quiz.py",
    "end": "quiz/end.py",
    "login": "quiz/login.py",
    "signup": "quiz/signup.py",
    "leaderboard": "quiz/leaderboard.py",
    "chat": "quiz/chat.py"
}


# Function to load a page module and run it
def load_page(page_name):
    file_path = PAGES[page_name]
    spec = importlib.util.spec_from_file_location(page_name, Path(file_path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "start"

# Load and run the current page
page_module = load_page(st.session_state.page)
page_module.run()

# Page navigation logic
if "navigate" in st.session_state:
    st.session_state.page = st.session_state.navigate
    del st.session_state.navigate
    st.rerun()
