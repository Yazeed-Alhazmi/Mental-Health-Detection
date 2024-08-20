import streamlit as st
import openai

st.set_page_config(page_title="FARAH", page_icon="👩‍⚕️", layout="centered")

st.markdown( """ <style> .st-emotion-cache-janbn0 { flex-direction: row-reverse; text-align: right; } </style> """, unsafe_allow_html=True, ) 
st.markdown("<h1 style='text-align: center; color: white;'>👩‍⚕️ فرح</h1>", unsafe_allow_html=True)
# st.markdown("<h1 style='text-align: center; color: white;'>FARAH 👩‍⚕️</h1>", unsafe_allow_html=True)
# ---------- Openai
# Opeai API Key
client = openai.OpenAI( api_key=st.secrets["OPENAI_API_KEY"])
# ChatGPT Model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# st.title("👩‍⚕️ فرح") # ChatBot Title

# Chat History
if "texts" not in st.session_state:
    st.session_state.texts = []

# Initial system message to set the context
if not st.session_state.texts:
    st.session_state.texts.append({
        "role": "system",
        "content": """You are a respectful and helpful therapist, here to support patients and listen carefully to their concerns and feelings using your knowledge.
       Your responses should always be only in colloquia Saudi Hijazi Arabic.
        You are the user's friend. so please speak like a helpful friend.
        Ensure that your responses are unbiased and positive in nature.
        If a question does not make sense or is not factually coherent, explain why instead of providing an incorrect answer.
        If you don't know the answer to a question, do not share false information.
        Make sure you make the user in the most comfortable space to speak and engage.
        Speak with love and empathy.
        Your goal is to provide psychological support, help patients deal with their emotions and concerns in a respectful and supportive manner, and act as a therapist during the conversation.
        Engage with patients in a conversational manner, asking questions to understand their symptoms and feelings better, and provide guidance and support as a therapist would.
        Embed PHQ-9 rating scale within stories and conversations, because we are going to diagnose the patient based on their answers.
        Your name is فرح"""
    })

# Display History on each rerun
for text in st.session_state.texts[1:]:
    with st.chat_message(text["role"]):
        st.markdown(text["content"])

prompt = st.chat_input("كيف اقدر اساعدك؟")
if prompt:
    # Display User Input
    with st.chat_message("user"):
        st.markdown(prompt)
    # add user input to history
    st.session_state.texts.append({"role": "user", "content": prompt})

    # #Assistant:  
    with st.chat_message("assistant"):
        stream =  client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages = [{"role": m["role"], "content":m["content"]} for m in st.session_state.texts],
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.texts.append({"role":"assistant","content":response})