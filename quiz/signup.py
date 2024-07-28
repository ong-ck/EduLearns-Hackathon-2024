import streamlit as st
import json
import base64
from PIL import Image

USERS_FILE = "database/users.json"

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
        
def run():
    st.title("Sign Up")

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
    
    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    # Load database
    with open(USERS_FILE, "r") as f:
        db = json.load(f)

    back_btn_col, _, _, signup_btn_col = st.columns(4)
    with back_btn_col:
        if st.button("Back", use_container_width=True):
            st.session_state.navigate = "start"
            st.rerun()

    with signup_btn_col:
        if st.button("Sign Up", use_container_width=True, type="primary"):
            # If username already exists, show error message
            if new_user in db.keys():
                st.error(
                    "Username already exists. Please choose a different username."
                )
            else:
                db[new_user] = {"password": new_password}

                # Save database to db.json
                with open("db.json", "w") as f:
                    json.dump(db, f)

                st.success("You have successfully created an account")
                st.session_state.user = new_user
                st.session_state.navigate = "start"
                st.rerun()


if __name__ == '__main__':
    run()
