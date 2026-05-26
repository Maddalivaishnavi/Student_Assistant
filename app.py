import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# --- 0. API Key Loading (Securely) ---
# Load environment variables from .env file (for local development)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Check if the API key is loaded
if not GEMINI_API_KEY:
    st.error("Gemini API key (GEMINI_API_KEY) not found. Please set it in your .env file or Streamlit secrets.")
    st.stop() # Stop the app if no API key is available

# --- 1. Gemini API Client Initialization ---
try:
    client = genai.Client(api_key=GEMINI_API_KEY)
except Exception as e:
    st.error(f"❌ Failed to initialize Gemini Client: {e}")
    st.stop()

# --- 2. Gemini API Call Function ---
@st.cache_data(show_spinner=False) # Cache results to avoid re-calling API for same input
def query_gemini(prompt_instruction, model_name="gemini-2.5-flash"):
    """
    Makes a call to the Gemini API for text generation using the official SDK.

    Args:
        prompt_instruction (str): The instruction/query for the model.
        model_name (str): The Gemini model variant being used.

    Returns:
        str: The generated text from the model or an error message.
    """
    try:
        # Request generation from Gemini
        response = client.models.generate_content(
            model=model_name,
            contents=prompt_instruction,
        )
        
        if response.text:
            return response.text.strip()
        else:
            return "❌ Error: The model returned an empty response."

    except APIError as e:
        # Catch explicit Google API errors (Authentication, quota, etc.)
        return f"❌ Gemini API Error ({e.code}): {e.message}"
    except Exception as e:
        return f"❌ An unexpected error occurred during the API call: {e}"

# --- 3. Streamlit UI ---
st.set_page_config(page_title="AI Student Assistant (Gemini)", page_icon="🎓", layout="wide")
st.title("🤖 AI Student Assistant (Free Tier - Gemini API)")
st.markdown("---")

st.sidebar.header("App Features")
option = st.sidebar.selectbox("Choose a feature", [
    "📚 Summarize Text",
    "💡 Explain Concept",
    "📝 Generate Model Questions",
    "🧠 Generate Quiz Questions"
])

st.subheader("Input Text / Topic")
user_input = st.text_area("Enter your text or topic here:", height=200)

if st.button("Get AI Assistance", use_container_width=True):
    if user_input.strip() == "":
        st.warning("⚠ Please enter some text or a topic.")
    else:
        # Use a spinner for better user experience while AI is processing
        feature_clean_name = option.lower().replace('📚 ', '').replace('💡 ', '').replace('📝 ', '').replace('🧠 ', '')
        with st.spinner(f"Generating {feature_clean_name}..."):
            prompt = ""
            if option == "📚 Summarize Text":
                prompt = f"Summarize the following text concisely and accurately, highlighting the main points:\n\n{user_input}"
            elif option == "💡 Explain Concept":
                prompt = f"Explain the following concept in simple, easy-to-understand terms for a student:\n\nConcept: {user_input}"
            elif option == "📝 Generate Model Questions":
                prompt = f"Generate 5 detailed model exam/essay questions for the topic '{user_input}'. Ensure the questions are open-ended and require analytical answers. Format them as a numbered list."
            elif option == "🧠 Generate Quiz Questions":
                prompt = f"""Create 3 multiple-choice questions (MCQs) with 4 options each, and 2 true/false questions on the topic '{user_input}'.
                For MCQs, clearly indicate the correct option (A, B, C, or D).
                For True/False questions, clearly state 'True' or 'False'.

                Format your output strictly as follows:
                1. MCQ Question 1
                   a) Option A
                   b) Option B
                   c) Option C
                   d) Option D
                   Correct Answer: [Option Letter, e.g., C]

                2. True/False Question 1
                   Answer: [True/False]
                """
            
            # Call the updated Gemini function
            result = query_gemini(prompt)
            st.subheader(f"🧾 Result: {option.replace('📚 ', '').replace('💡 ', '').replace('📝 ', '').replace('🧠 ', '')}")
            st.write(result)

st.markdown("---")
st.caption("Powered by gemini-2.5-flash via Google GenAI SDK.")
