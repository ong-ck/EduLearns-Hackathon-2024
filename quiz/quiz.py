import streamlit as st
import random
import sympy
import time
import json
import base64
from PIL import Image

USERS_FILE = "database/users.json"


# TODO: Setup different levels of difficulty (bigger numbers? more algebra variables? Timer?)
# Function to load the database
def load_db():
    with open(USERS_FILE, "r") as f:
        return json.load(f)


# Function to save the database
def save_db(db):
    with open(USERS_FILE, "w") as f:
        json.dump(db, f)


def run_timer(timer_placeholder):
    with timer_placeholder.container():
        st.session_state.time_left = st.session_state.time_left - 1
        st.write(f"Time Left: {st.session_state.time_left:.0f} seconds")
        time.sleep(1)


difficulty_ranges = {
    'Easy': {
        'addition': (1, 20),
        'subtraction': (1, 20),
        'multiplication': (1, 10),
        'division': (1, 20),
        'algebra': (1, 5),
        'fraction': (1, 5)
    },
    'Medium': {
        'addition': (1, 50),
        'subtraction': (1, 50),
        'multiplication': (1, 20),
        'division': (1, 50),
        'algebra': (1, 10),
        'fraction': (1, 10)
    },
    'Hard': {
        'addition': (1, 100),
        'subtraction': (1, 100),
        'multiplication': (1, 50),
        'division': (1, 100),
        'algebra': (1, 15),
        'fraction': (1, 10)
    }
}


# Helper function to generate numbers based on difficulty
def generate_number(difficulty, question_type):
    print(difficulty)
    min_val, max_val = difficulty_ranges[difficulty][question_type]
    print(min_val, max_val)
    return random.randint(min_val, max_val)


# Define the questions and answers
def generate_questions(question_types, difficulty_levels, num_questions=5):
    questions = []
    for _ in range(num_questions):
        difficulty = difficulty_levels  #"Easy"
        question_type = random.choice(question_types)
        question = None
        answer = None

        if question_type == 'addition':
            x = generate_number(difficulty, 'addition')
            y = generate_number(difficulty, 'addition')
            question = f"What is {x} + {y}?"
            answer = str(x + y)

        elif question_type == 'subtraction':
            x = generate_number(difficulty, 'subtraction')
            y = generate_number(difficulty, 'subtraction')
            # Ensure x is always greater than y for valid subtraction
            if x < y:
                x, y = y, x
            question = f"What is {x} - {y}?"
            answer = str(x - y)

        elif question_type == 'multiplication':
            x = generate_number(difficulty, 'multiplication')
            y = generate_number(difficulty, 'multiplication')
            question = f"What is {x} * {y}?"
            answer = str(x * y)

        elif question_type == 'division':
            x = generate_number(difficulty, 'division')
            y = random.randint(1, generate_number(difficulty, 'division'))
            while x % y != 0:  # Ensure division is exact
                x = generate_number(difficulty, 'division')
                y = random.randint(1, generate_number(difficulty, 'division'))
            question = f"What is {x} // {y}?"
            answer = str(x // y)

        elif question_type == 'algebra':
            num1 = generate_number(difficulty, 'algebra')
            num2 = generate_number(difficulty, 'algebra')
            algebra1 = f"{random.randint(1, 10)}*a"
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
            numerator1 = generate_number(difficulty, 'fraction')
            denominator1 = random.randint(
                2, generate_number(difficulty, 'fraction'))
            numerator2 = generate_number(difficulty, 'fraction')
            denominator2 = random.randint(
                2, generate_number(difficulty, 'fraction'))
            question = f"What is {numerator1}/{denominator1} + {numerator2}/{denominator2}?"
            answer = str(
                (numerator1 * denominator2 + numerator2 * denominator1) /
                (denominator1 * denominator2))

        questions.append({'question': question, 'answer': answer})
    return questions


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
    st.title("Quiz Page")
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
    st.markdown(page_bg_img, unsafe_allow_html=True)
    ##################################
    # Populate the questions and answers
    if st.session_state.start_over:
        st.session_state.start_over = False
        st.session_state.questions = generate_questions(
            question_types=st.session_state.question_types,
            difficulty_levels=st.session_state.difficulty_levels,  #"Easy"
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

                ### TODO: start db, get user from db, put users score into db, save db #####
                # db[user]["score"] = st.session_state.score
                # Load user data from user.json
                ##########################################################################
                # 1. Check if user logged in
                if "user" in st.session_state:

                    # 2. Load db (give you a db variable representing the db
                    # Note that this db variable is not going to change the json file until you saved it
                    db = load_db()

                    # 3. Put the score into the db variable (e.g. db[st.session_state.user]["score"] = score)
                    db[st.session_state.user]["score"] = st.session_state.score
                    # 4. Save the db variable (e.g. save_db(db))
                    save_db(db)
                ##########################################################################
                st.session_state.navigate = "end"
                st.rerun()

    print("test")
    with reset_btn_col:
        if st.button("Reset", use_container_width=True, type="primary"):
            # Clear session state
            # Except for user so that the user is not logged out
            for key in st.session_state:
                if key != "user":
                    del st.session_state[key]

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
