import streamlit as st


def run():
    if st.session_state.clear_quiz:
        st.title("Congratulations!")
        st.write("You have finished the quiz!")
        st.write(f"Your score is: {st.session_state.score}")
    else:
        st.title("Sorry, you didn't pass the quiz.")
        st.write("You can click try again.")

    if st.button("Try again"):
        # Clear session state
        st.session_state.clear()

        # Navigate back to the start page
        st.session_state.navigate = "start"


if __name__ == "__main__":
    run()
