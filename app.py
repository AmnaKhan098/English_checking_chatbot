import os
import streamlit as st
import speech_recognition as sr
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Arrays storing essay topics for each plan
essays_30_day_plan = [
    "Discuss a recent technological advancement and its impact on society.",
    # Add more topics up to 30 days
]

essays_45_day_plan = essays_30_day_plan + [
    "How can governments combat the rise of misinformation?",
    # Add more topics up to 45 days
]

essays_60_day_plan = essays_45_day_plan + [
    "The importance of learning foreign languages in a globalized world.",
    # Add more topics up to 60 days
]

# Function to get feedback from Groq API
def get_feedback(user_essay, level):
    # Define the system prompt for essay feedback
    system_prompt = "..."  # Same as before

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": f"{system_prompt}\nEssay:\n{user_essay}\nLevel: {level}"}],
        model="llama3-8b-8192"
    )
    feedback = response.choices[0].message.content
    return feedback

# Function for voice input
def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success("You said: " + text)
        return text
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand the audio.")
    except sr.RequestError:
        st.error("Could not request results from Google Speech Recognition service.")

# Streamlit UI
st.title("Writing Assistant for IELTS/TOEFL/DET Preparation")

# Sidebar for selecting a plan
st.sidebar.title("Select Your Writing Plan")
plan = st.sidebar.radio("Choose a Plan", ("30 Days Plan", "45 Days Plan", "60 Days Plan", "Voice Input"))

# Select the appropriate essay list based on the plan
if plan == "30 Days Plan":
    selected_plan_essays = essays_30_day_plan
elif plan == "45 Days Plan":
    selected_plan_essays = essays_45_day_plan
elif plan == "60 Days Plan":
    selected_plan_essays = essays_60_day_plan
else:
    st.subheader("Voice Input")
    user_voice_input = voice_input()  # Get voice input

# Dropdown to select the current day
if plan != "Voice Input":
    st.subheader("Select your current day:")
    current_day = st.selectbox("Choose the day:", list(range(1, len(selected_plan_essays) + 1)))

    # Display the essay topic for the selected day
    st.write(f"Day {current_day}: {selected_plan_essays[current_day - 1]}")

    # Textbox for the user to input their essay
    user_essay = st.text_area("Write your essay here:", height=300)

    # Dropdown to select proficiency level
    level = st.selectbox("Select your proficiency level:", ["A1 (Beginner)", "A2 (Average)", "B1", "B2", "C1 (Advanced)"])

    # Button to submit essay for feedback
    if st.button("Submit for Feedback"):
        if user_essay.strip():
            st.write("Analyzing your essay...")

            # Get feedback using the get_feedback function
            feedback = get_feedback(user_essay, level)
            
            # Display the feedback provided by the model
            st.subheader("Feedback on your essay:")
            st.write(feedback)
        else:
            st.warning("Please write your essay before submitting!")



