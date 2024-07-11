import streamlit as st
import random
from streamlit.runtime.state import session_state_proxy
import sympy
import time


def run_timer(timer_placeholder):
    with timer_placeholder.container():
        st.session_state.time_left = st.session_state.time_left - 1
        st.write(f"Time Elapsed: {st.session_state.time_left:.0f} seconds")
        time.sleep(1)


# Define the questions and answers
def generate_questions(question_types, num_questions=5):
    questions = []
    for _ in range(num_questions):
        question_type = random.choice(question_types)
        question = None
        answer = None

        if question_type == 'addition':
            x, y = random.randint(1, 100), random.randint(1, 100)
            question = f"What is {x} + {y}?"
            answer = str(x + y)

        elif question_type == 'subtraction':
            x, y = random.randint(1, 100), random.randint(1, 100)
            question = f"What is {x} - {y}?"
            answer = str(x - y)

        elif question_type == 'multiplication':
            x, y = random.randint(1, 10), random.randint(1, 10)
            question = f"What is {x} * {y}?"
            answer = str(x * y)

        elif question_type == 'division':
            x, y = random.randint(1, 100), random.randint(1, 10)
            while x % y != 0:  # Ensure division is exact
                x, y = random.randint(1, 100), random.randint(1, 10)
            question = f"What is {x} // {y}?"
            answer = str(x // y)

        elif question_type == 'algebra':
            num1 = random.randint(1, 10)
            algebra1 = f"{random.randint(1, 10)}*a"
            num2 = random.randint(1, 10)
            algebra2 = f"{random.randint(1, 10)}*a"

            # Prevent algebra1 and algebra2 from having the same variable
            while algebra1 == algebra2:
                algebra1 = f"{random.randint(1, 10)}*a"
                algebra2 = f"{random.randint(1, 10)}*a"

            lhs = f"{num1} + {algebra1}"
            rhs = f"{num2} + {algebra2}"
            question = f"Solve the equation: {lhs} = {rhs}"
            equation = sympy.Eq(sympy.sympify(lhs), sympy.sympify(rhs))
            answer = str(sympy.solve(equation)[0])

        elif question_type == 'fraction':
            numerator1, denominator1 = random.randint(1, 10), random.randint(
                2, 10)
            numerator2, denominator2 = random.randint(1, 10), random.randint(
                2, 10)
            while denominator1 == 1 or denominator2 == 1:  # Ensure denominators are not 1
                denominator1 = random.randint(2, 10)
                denominator2 = random.randint(2, 10)
            question = f"What is {numerator1}/{denominator1} + {numerator2}/{denominator2}?"
            answer = str(
                (numerator1 * denominator2 + numerator2 * denominator1) /
                (denominator1 * denominator2))

        questions.append({'question': question, 'answer': answer})
    return questions


def run():
    st.title("Quiz Page")

    # Populate the questions and answers
    if st.session_state.start_over:
        st.session_state.start_over = False
        st.session_state.questions = generate_questions(
            question_types=st.session_state.question_types,
            num_questions=st.session_state.num_of_questions)
        print(st.session_state.questions)

    # Setup session_state to contain the index of question
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0

    # Setup session_state to contain a list to store the user's answers
    if "answers" not in st.session_state:
        st.session_state.answers = list(range(len(st.session_state.questions)))

    # Set the session_state to the index of the current question
    current_question_index = st.session_state.current_question
    current_question = st.session_state.questions[current_question_index]

    # Creates container to store timer only if enabled
    if st.session_state.is_timer_enabled:
        timer_placeholder = st.empty()

    # Display the current question
    st.write(
        f"Question {current_question_index + 1}/{len(st.session_state.questions)}"
    )

    # Put question and answer box in a container
    with st.container(border=True):
        st.write(current_question["question"])
        user_answer = st.text_input("Your answer",
                                    key=f"answer_{current_question_index}")

    # Empty cols to give space between the buttons
    next_btn_col, _, _, reset_btn_col = st.columns(4)

    with next_btn_col:
        # When user clicks next, store the answer in the session_state.answers list. Increments the current_question_index until it reaches the length of the questions list. Then calculate the score and navigate to the end page.
        if st.button("Next", use_container_width=True):
            # Store the user's answer for current question in the session_state.answers list
            st.session_state.answers[current_question_index] = user_answer
            if current_question_index + 1 < len(st.session_state.questions):
                st.session_state.current_question += 1
                st.rerun()
            else:
                st.session_state.clear_quiz = True  # Quiz cleared before timer ran out
                st.session_state.start_timer = False  # Stop timer
                print(st.session_state.answers)  # To debug
                # Calculate the score
                st.session_state.score = sum(
                    1 for i, q in enumerate(st.session_state.questions) if
                    st.session_state.answers[i].strip().lower() == q["answer"])
                st.session_state.navigate = "end"
                st.rerun()

    with reset_btn_col:
        if st.button("Reset", use_container_width=True, type="primary"):
            # Clear session state
            st.session_state.clear()

            # Navigate back to the start page
            st.session_state.navigate = "start"
            st.rerun()

    # Only if timer is enabled and started, run the timer
    if st.session_state.start_timer and st.session_state.is_timer_enabled:
        if st.session_state.time_left > 0:
            run_timer(timer_placeholder)
            st.rerun()
        else:
            st.session_state.start_timer = False  # Stop timer
            st.session_state.clear_quiz = False  # Quiz not cleared
            st.session_state.navigate = "end"
            st.rerun()


if __name__ == "__main__":
    run()
