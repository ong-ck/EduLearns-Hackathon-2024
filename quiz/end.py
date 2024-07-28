import streamlit as st
import base64
from PIL import Image

bg_img_path = "assets/math-curriculum.jpg.webp"

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
    if st.session_state.clear_quiz:
        st.title("Congratulations!")
        st.write("You have finished the quiz!")
        st.write(f"Your score is: {st.session_state.score}")
    else:
        st.title("Sorry, you didn't pass the quiz.")
        st.write("You can click try again.")

    if st.button("Try again"):
        # Clear session state
        # Except for user so that the user is not logged out
        for key in st.session_state:
            if key != "user":
                del st.session_state[key]

        # Navigate back to the start page
        st.session_state.navigate = "start"


if __name__ == "__main__":
    run()
