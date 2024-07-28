import streamlit as st
import json
import pandas as pd
import base64
from PIL import Image

USERS_FILE = "database/users.json"

bg_img_path = "assets/images.jpeg"

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
    st.title("Leaderboard")
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

    # Load user data from JSON file
    with open(USERS_FILE, 'r') as f:
        db = json.load(f)

    # Sort users by points in descending order
    sorted_users = sorted(db.items(), key=lambda x: x[1].get('score', 0), reverse=True)

    # Prepare data for the table with index starting from 1
    table_data = [(i + 1, user, info.get('score', 0)) for i, (user, info) in enumerate(sorted_users)]

    # Convert to a Pandas DataFrame
    df = pd.DataFrame(table_data, columns=['Rank', 'User', 'Score'])
    df = df.set_index('Rank') 

    # Display leaderboard in a dataframe with headers
    st.dataframe(df, use_container_width=True)
    
    with st.sidebar:
        if st.button("Back", use_container_width=True):
            # Clear session state
            # Except for user so that the user is not logged out
            for key in st.session_state:
                if key != "user":
                    del st.session_state[key]
            st.session_state.navigate = "start"
            st.rerun()
if __name__ == '__main__':
    run()
