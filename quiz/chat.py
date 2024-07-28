import streamlit as st
import json
import os
import time
import datetime
import base64
from PIL import Image

CHAT_FILE = "database/chat.json"


# Function to load chat history from the JSON file
def load_chat():
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            return json.load(f)
    return {"messages": []}


# Function to save chat history to the JSON file
def save_chat(chat_history):
    db = load_chat()
    with open(CHAT_FILE, "w") as f:
        db["messages"] = chat_history
        json.dump(db, f)


# Function to get the last modification time of the chat file
def get_last_mod_time(file_path):
    return os.path.getmtime(file_path) if os.path.exists(file_path) else 0

bg_img_path = "assets/social-media-sketch-vector-seamless-600nw-1660950727.jpg.webp"

# https://www.youtube.com/watch?v=pyWqw5yCNdo
@st.cache_data
def get_img_as_base64_with_opacity(file, opacity):
    # Open the image file
    with Image.open(file) as img:
        # Ensure image has an alpha channel
        img = img.convert("RGBA")

        # Modify the alpha channel
        alpha = img.split()[3]
        alpha = alpha.point(lambda p: p * opacity)

        # Merge the image with the new alpha channel
        img.putalpha(alpha)

        # Save the modified image to a bytes buffer
        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # Encode the bytes buffer to base64
        data = buffer.read()
        return base64.b64encode(data).decode()

def run():
    # Initialize chat history and last modification time
    # if "message_db" not in st.session_state:
    st.session_state.message_db = load_chat()["messages"]

    st.title("Chatting Area")
    ### Add background image #################################
    img = get_img_as_base64_with_opacity(bg_img_path, 0.2)
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url('data:image/png;base64,{img}');
        background-size: cover;
    }}

    [data-testid="stHeader"] {{
    background-color: rgba(0,0,0,0);
    }}
    </style>
    """
    st.markdown(page_bg_img ,unsafe_allow_html=True)
    ##################################
    # Sidebar to add back button
    with st.sidebar:
        if st.button("Back", use_container_width=True):
            # Clear session state
            # Except for user so that the user is not logged out
            for key in st.session_state:
                if key != "user":
                    del st.session_state[key]
            st.session_state.navigate = "start"
            st.rerun()

    # Display chat messages from history on app rerun
    for message in st.session_state.message_db:
        if message["sender"] == st.session_state.user:
            with st.chat_message("user"):
                st.markdown("<b>" + "You" + "</b>" + ": " + message["content"], unsafe_allow_html=True)
                st.markdown(f'<div style="text-align: right;">{message["timestamp"]}</div>', unsafe_allow_html=True)
        else:
            with st.chat_message(message["sender"]):
                st.markdown("<b>" + message["sender"] + "</b>" + ": " + message["content"], unsafe_allow_html=True)
                # Note: padding-right is set to 16px to align the timestamps together
                st.markdown(f'<div style="text-align: right; padding-right: 16px">{message["timestamp"]}</div>', unsafe_allow_html=True)
                
    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        st.chat_message("user").markdown(st.session_state.user + ": " + prompt)
        # Add user message to chat history
        st.session_state.message_db.append({"sender": st.session_state.user, "content": prompt, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        save_chat(st.session_state.message_db)  # Save chat history
        st.rerun()

    # Poll for updates to the chat file
    time.sleep(1)  # Add a small delay to avoid excessive polling
    st.rerun()


if __name__ == "__main__":
    run()
