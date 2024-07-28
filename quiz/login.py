import streamlit as st
import json
import base64
from PIL import Image

USERS_FILE = "database/users.json"


# Function to load the database
def load_db():
    with open(USERS_FILE, "r") as f:
        return json.load(f)


# Function to save the database
def save_db(db):
    with open(USERS_FILE, "w") as f:
        json.dump(db, f)

bg_img_path = "assets/pngtree-futuristic-shape-abstract-background-chemistry-technology-concept-for-website-image_438818.jpg"

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
        
# Function to handle login
def run():
    st.title("Login")

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
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    back_btn_col, _, _, login_btn_col = st.columns(4)

    with back_btn_col:
        if st.button("Back", use_container_width=True):
            st.session_state.navigate = "start"
            st.rerun()

    with login_btn_col:
        if st.button("Login", use_container_width=True, type="primary"):
            db = load_db()

            if username in db and db[username]["password"] == password:
                st.success("You have successfully logged in")
                st.session_state.user = username
                st.session_state.navigate = "start"
                st.rerun()
            else:
                st.error("Invalid username or password. Please try again.")


if __name__ == '__main__':
    run()
