import os
import streamlit as st
from groq import Groq
import speech_recognition as sr
from io import BytesIO

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Function to get feedback from Groq API
def get_feedback(user_essay, level):
    system_prompt = """
    You are an expert academic writer with 40 years of experience in providing concise but effective feedback.
    Provide detailed feedback on any mistakes and present an improved version of the writing.
    """
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": f"{system_prompt}\nEssay:\n{user_essay}\nLevel: {level}"}],
        model="llama3-8b-8192"
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("Writing Assistant for IELTS/TOEFL/DET Preparation")

# Sidebar for selecting a plan
plan = st.sidebar.radio("Choose a Plan", ("30 Days Plan", "45 Days Plan", "60 Days Plan"))

# Essay plans (Add at least 5 essays for each plan)
essays_30_day_plan = [
    "Discuss a recent technological advancement and its impact on society.",
    "How does social media influence mental health in teenagers?",
    "The benefits of reading books in the digital age.",
    "Should homework be banned in schools?",
    "Impact of global warming on biodiversity.",
]

essays_45_day_plan = essays_30_day_plan + [
    "How can governments combat the rise of misinformation?",
    "The role of sports in character building.",
    "The importance of renewable energy sources.",
    "Is it necessary to learn coding in today's world?",
    "Effects of fast food on health.",
]

essays_60_day_plan = essays_45_day_plan + [
    "The significance of cultural exchange in a globalized society.",
    "Should public transport be free for all citizens?",
    "The impact of climate change on agriculture.",
    "How does education shape society?",
    "The influence of technology on modern relationships.",
]

# Selecting essays based on the chosen plan
if plan == "30 Days Plan":
    selected_plan_essays = essays_30_day_plan
elif plan == "45 Days Plan":
    selected_plan_essays = essays_45_day_plan
else:
    selected_plan_essays = essays_60_day_plan

# Dropdown to select the current day
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
        feedback = get_feedback(user_essay, level)
        st.subheader("Feedback on your essay:")
        st.write(feedback)
    else:
        st.warning("Please write your essay before submitting!")

# Voice Input Section
st.subheader("Voice Input for Speaking Practice")

# Upload audio
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
if audio_file is not None:
    # Convert audio to text
    recognizer = sr.Recognizer()
    with sr.AudioFile(BytesIO(audio_file.read())) as source:
        audio_data = recognizer.record(source)
        try:
            spoken_text = recognizer.recognize_google(audio_data)
            st.write(f"You said: {spoken_text}")

            # Get feedback on the spoken text
            feedback = get_feedback(spoken_text, level)
            st.subheader("Feedback on your speaking:")
            st.write(feedback)
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")




