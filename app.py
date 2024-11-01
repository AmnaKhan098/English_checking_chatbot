import os
import streamlit as st
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Arrays storing essay topics for each plan
essays_30_day_plan = [
    "Discuss a recent technological advancement and its impact on society.",
    "How does social media influence mental health in teenagers?",
    "The benefits of reading books in the digital age.",
    "Should homework be banned in schools?",
    "Impact of global warming on biodiversity.",
    "The influence of technology on education.",
    "Should the voting age be lowered to 16?",
    "The importance of arts education in schools.",
    "How can we promote environmental sustainability?",
    "The role of youth in community service."
]

essays_45_day_plan = essays_30_day_plan + [
    "How can governments combat the rise of misinformation?",
    "The role of sports in character building.",
    "The effects of globalization on culture.",
    "Should animals be used for research?",
    "The impact of fast fashion on the environment.",
    "The significance of mental health awareness.",
    "How does climate change affect agriculture?",
    "The benefits of a plant-based diet.",
    "The importance of financial literacy for young adults.",
    "How can technology improve healthcare?"
]

essays_60_day_plan = essays_45_day_plan + [
    "The importance of learning foreign languages in a globalized world.",
    "Should public transport be free for all citizens?",
    "The impact of social media on political movements.",
    "The benefits of remote working for businesses.",
    "How can we bridge the gender gap in STEM fields?",
    "The role of renewable energy in combating climate change.",
    "The effects of digital marketing on consumer behavior.",
    "How can education be made more accessible?",
    "The importance of physical fitness in daily life.",
    "How do cultural festivals promote diversity?"
]

# Function to get feedback from Groq API
def get_feedback(user_essay, level):
    system_prompt = """
    You are an expert academic writer with 40 years of experience in providing concise but effective feedback.
    Instead of asking the student to do this and that, you just say replace this with this to improve in a concise manner.
    You provide concise grammar mistakes, saying replace this with this along with mistake type. 
    You also provide specific replacement sentences for cohesion and abstraction, and you point out all the vocabulary saying replace this word with this.
    You have to analyze the writing for grammar, cohesion, sentence structure, vocabulary, and the use of simple, complex, and compound sentences, as well as the effectiveness of abstraction.
    Provide detailed feedback on any mistakes and present an improved version of the writing.
    Do not use words such as dive, discover, uncover, delve, tailor, equipped, navigate, landscape, delve, magic, comprehensive embrace, well equipped, unleash, cutting edge, harness.
    Strictly follow academic style in writing. Change the sentences according to English standards if needed but do not add any sentences by yourself.
    Give feedback for different levels: A1 for beginners, A2 for average, A3 for advanced, up to C1 level.
    """

    response = client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": f"{system_prompt}\nEssay:\n{user_essay}\nLevel: {level}"
        }],
        model="llama3-8b-8192"
    )
    
    feedback = response.choices[0].message.content
    return feedback

# Streamlit UI
st.set_page_config(page_title="Writing Assistant", layout="wide")
st.title("📝 Writing Assistant for IELTS/TOEFL/DET Preparation")

# Sidebar for selecting a plan
st.sidebar.header("Select Your Writing Plan")
plan = st.sidebar.radio("Choose a Plan", ("30 Days Plan", "45 Days Plan", "60 Days Plan"))

# Select the appropriate essay list based on the plan
selected_plan_essays = []
if plan == "30 Days Plan":
    selected_plan_essays = essays_30_day_plan
elif plan == "45 Days Plan":
    selected_plan_essays = essays_45_day_plan
else:
    selected_plan_essays = essays_60_day_plan

# Dropdown to select the current day
st.subheader("Select Your Current Day:")
current_day = st.selectbox("Choose the day:", list(range(1, len(selected_plan_essays) + 1)))

# Display the essay topic for the selected day
st.markdown(f"### **Day {current_day}:** {selected_plan_essays[current_day - 1]}")

# Dropdown to show the upcoming essay topics
st.subheader("Upcoming Essays:")
upcoming_essays = st.selectbox("Upcoming essay topics:", selected_plan_essays[current_day:])

# Textbox for the user to input their essay
user_essay = st.text_area("✍️ Write your essay here:", height=300)

# Dropdown to select proficiency level
level = st.selectbox("Select Your Proficiency Level:", ["A1 (Beginner)", "A2 (Average)", "B1", "B2", "C1 (Advanced)"])

# Button to submit essay for feedback
if st.button("Submit for Feedback"):
    if user_essay.strip():
        st.write("Analyzing your essay...")
        feedback = get_feedback(user_essay, level)
        
        # Display the feedback provided by the model
        st.subheader("Feedback on Your Essay:")
        st.write(feedback)
    else:
        st.warning("Please write your essay before submitting!")

