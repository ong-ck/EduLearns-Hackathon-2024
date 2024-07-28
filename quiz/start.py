import streamlit as st
import time
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
    st.title("Auto-Math Quiz")
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
    #########################################################
    ########### START OF SIDEBAR INTEGRATION ################
    ### TODO: Create a button for signup/login ######
    with st.sidebar:
        # IF USER LOGGED IN - DO THE FOLLOWING:
        if "user" in st.session_state:
            st.write(f"Welcome, {st.session_state.user}!")
            if st.button("Log out", use_container_width=True):
                del st.session_state.user
                st.rerun()

            #################################################
            ### TODO: Create a button for profile ######
            ### NOTE: It should be indented with the 
            ###       and only if signed in
            # if st.button("Profile", use_container_width=True):
            #     # st.session_state.navigate = "profile"
            #     pass

            #################################################
            #################################################
            ### TODO: Create a button for chat/forum ######
            ### NOTE: It should be indented with the 
            ###       and only if signed in
            if st.button("Chat", use_container_width=True):
                st.session_state.navigate = "chat"

            #################################################
        # IF USER NOT LOGGED IN - DO THE FOLLOWING:
        else:
            signup_btn_col, login_btn_col = st.columns(2)
            with signup_btn_col:
                if st.button("Sign Up", use_container_width=True):
                    st.session_state.navigate = "signup"
    
            with login_btn_col:
                if st.button("Log in", use_container_width=True):
                    st.session_state.navigate = "login"

    #################################################
    ### TODO: Create a button for leaderboard ######
    ### NOTE: It should be indented with the sidebar
        if st.button("Leaderboard", use_container_width=True):
            st.session_state.navigate = "leaderboard"

    ########### END OF SIDEBAR INTEGRATION ################
    
    st.write("Please choose your options and click the button below to start the quiz!")

    # Put the options in a container with border
    with st.container(border=True):

        # Slider to choose number of questions
        st.session_state.num_of_questions = st.slider("Choose number of questions:", 1, 20, 5)

        # Input to choose timer duration
        timer_input, timer_select = st.columns([3, 1], vertical_alignment="bottom")
        st.session_state.is_timer_enabled = timer_select.checkbox("Enable Timer")
        st.session_state.time_left = timer_input.number_input("Choose timer duration:", value=20, placeholder="Type a number...", step=1, min_value=1, disabled=not st.session_state.is_timer_enabled, key="timer")
        
        # Multi-select to choose question types
        st.session_state.question_types = st.multiselect(
            "Choose your question types:",
            ["addition", "subtraction", "multiplication", "division", "algebra", "fraction",'angle', 'area', 'geometry'],
            ["algebra"])
        
        # Multi-select to choose question difficulty
        st.session_state.difficulty_levels = st.radio(
            "Select difficulty level:",
            ["Easy", "Medium", "Hard"],
            index=None,
        )

        st.write("You selected:", st.session_state.difficulty_levels)
        
    # If the user clicks the button, navigate to the quiz page
    if st.button("Start Quiz"):
        st.session_state.start_over = True
        st.session_state.navigate = "quiz"
        st.session_state.start_time = time.time()
        st.session_state.time_elapsed = st.session_state.start_time
        st.session_state.start_timer = True
        st.session_state.clear_quiz = False


if __name__ == "__main__":
    run()
