import streamlit as st
import os
from dotenv import load_dotenv
import requests

# --- 0. API Key Loading (Securely) ---
# Load environment variables from .env file (for local development)
load_dotenv()
HF_API_KEY = os.getenv("HF_API_KEY")

# Check if the API key is loaded
if not HF_API_KEY:
    st.error("Hugging Face API key (HF_API_KEY) not found. Please set it in your .env file or Streamlit secrets.")
    st.stop() # Stop the app if no API key is available

# --- 1. Hugging Face Inference API Configuration ---
# CORRECTED: Use the v0.2 model which is generally available
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

# --- 2. Hugging Face API Call Function ---
@st.cache_data(show_spinner=False) # Cache results to avoid re-calling API for same input
def query_huggingface(prompt_instruction, model_name="Mistral-7B-Instruct-v0.2"):
    """
    Makes a call to the Hugging Face Inference API for text generation.
    Uses the recommended chat template for Mistral-Instruct models.

    Args:
        prompt_instruction (str): The instruction/query for the model.
        model_name (str): The name of the model being used (for better error messages).

    Returns:
        str: The generated text from the model or an error message.
    """
    try:
        # Mistral-Instruct models typically use this format for optimal performance
        formatted_prompt = f"<s>[INST] {prompt_instruction} [/INST]"

        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": 512,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.95
            }
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)

        result = response.json()
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            # The model generates text after the prompt. We want the text *after* our instruction.
            # Splitting by "[/INST]" and taking the last part is a common way to get the response.
            generated_text = result[0]["generated_text"]
            # Remove the input prompt part
            if "[/INST]" in generated_text:
                return generated_text.split("[/INST]")[-1].strip()
            else:
                return generated_text.strip() # Fallback if format is unexpected
        else:
            return f"❌ Error: Unexpected API response format: {result}"

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        if status_code == 404:
            return f"❌ Error 404: Model '{model_name}' not found at {API_URL}. Please double-check the model ID and its availability on Hugging Face."
        elif status_code == 401:
            return "❌ Error 401: Unauthorized. Please check your Hugging Face API token (HF_API_KEY)."
        elif status_code == 503:
            return f"❌ Error 503: Service Unavailable. The model '{model_name}' is currently loading or busy. Please try again in a moment."
        else:
            return f"❌ HTTP Error {status_code}: {e.response.text}"
    except requests.exceptions.ConnectionError as e:
        return f"❌ Connection Error: Could not connect to Hugging Face API. Please check your internet connection. Details: {e}"
    except Exception as e:
        return f"❌ An unexpected error occurred during API call: {e}"

# --- 3. Streamlit UI ---
st.set_page_config(page_title="AI Student Assistant (Hugging Face)", page_icon="🎓", layout="wide")
st.title("🤖 AI Student Assistant (Free - Hugging Face)")
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
        with st.spinner(f"Generating {option.lower().replace('📚 ', '').replace('💡 ', '').replace('📝 ', '').replace('🧠 ', '')}..."):
            prompt = ""
            if option == "📚 Summarize Text":
                # Changed to "text" instead of "topic" to be more accurate for summarization
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
            
            result = query_huggingface(prompt)
            st.subheader(f"🧾 Result: {option.replace('📚 ', '').replace('💡 ', '').replace('📝 ', '').replace('🧠 ', '')}")
            st.write(result)

st.markdown("---")
st.caption("Powered by Mistral-7B-Instruct-v0.2 via Hugging Face Inference API.")
