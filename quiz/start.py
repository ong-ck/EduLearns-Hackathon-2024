import streamlit as st
import time


def run():
    st.title("Auto-Math Quiz")
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
            ["addition", "subtraction", "multiplication", "division", "algebra", "fraction"],
            ["algebra"])
        
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
