# groq.py  (pip install openai)
import config
from openai import OpenAI

GROQ_URL = "https://api.groq.com/openai/v1"
MODELS = getattr(config, "GROQ_MODELS", ["llama-3.1-8b-instant", "mixtral-8x7b-32768"])

def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    key = getattr(config, "GROQ_API_KEY", None)
    if not key:
        return "Error: GROQ_API_KEY missing in config.py"
    c = OpenAI(api_key=key, base_url=GROQ_URL)

    last_err = None
    for m in MODELS:
        try:
            r = c.chat.completions.create(
                model=m,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception as e:
            last_err = e

    return (
        "Groq model failed.\n"
        f"Tried models: {MODELS}\n"
        "Fix:\n"
        "1) Switch to hf by importing hf.py in main.py OR\n"
        "2) Replace Groq model in groq.py (GROQ_MODELS).\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )

#hf.py
import config
from huggingface_hub import InferenceClient

MODELS = getattr(
    config,
    "HF_MODELS",
    ["meta-llama/Llama-3.1-8B-Instruct"],
)

def generate_response(prompt: str, temperature: float = 0.3, max_tokens: int = 512) -> str:
    key = getattr(config, "HF_API_KEY", None)
    if not key:
        return "Error: HF_API_KEY missing in config.py"

    last_err = None
    for m in MODELS:
        try:
            c = InferenceClient(model=m, token=key)
            r = c.chat_completion(
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            return r.choices[0].message.content
        except Exception as e:
            last_err = e

    return (
        "Hugging Face model failed.\n"
        f"Tried models: {MODELS}\n"
        "Fix:\n"
        "1) Switch to Groq by importing groq.py in main.py OR\n"
        "2) Replace HF model in hf.py (HF_MODELS).\n"
        f"Details: {type(last_err).__name__}: {last_err}"
    )
#main.py
# main.py (Streamlit)
# Switch provider by changing the import line:
from groq import generate_response
# from hf import generate_response

import re
import streamlit as st

def looks_incomplete(text: str) -> bool:
    if not text or len(text.strip()) < 10:
        return True
    t = text.strip()
    # common "cut" signs: ends mid-word, mid-markdown, or no closing punctuation
    if t.endswith(("**", "*", "-", "—", ":", ",", "(", "[", "{")):
        return True
    if re.search(r"\d+\.\s*\*\*$", t):  # like "3. **"
        return True
    if not re.search(r"[.!?]\s*$", t):  # no sentence-ending punctuation
        return True
    return False

def complete_answer(question: str, max_rounds: int = 2) -> str:
    # 1) Ask for a clean structured answer (helps avoid unfinished bullets)
    base_prompt = (
        "Answer clearly in numbered points. "
        "Do not cut sentences. Finish each point fully.\n\n"
        f"Question: {question}"
    )

    ans = generate_response(base_prompt, temperature=0.3, max_tokens=1024)

    # 2) If it looks cut, continue from last line without repeating
    rounds = 0
    while rounds < max_rounds and looks_incomplete(ans):
        cont_prompt = (
            "Continue EXACTLY from where you stopped. "
            "Do NOT repeat earlier text. "
            "Finish the incomplete point and complete the answer.\n\n"
            f"Question: {question}\n\n"
            f"Answer so far:\n{ans}\n\nContinue:"
        )
        more = generate_response(cont_prompt, temperature=0.3, max_tokens=1024)
        if not more or more.strip() in ans:
            break
        ans = (ans.rstrip() + "\n" + more.lstrip()).strip()
        rounds += 1

    return ans

def main():
    st.title("AI Teaching Assistant")
    st.write("Welcome! You can ask me anything about various subjects, and I'll provide an answer.")

    user_input = st.text_input("Enter your question here:")

    if user_input:
        st.write(f"**Your question:** {user_input}")
        response = complete_answer(user_input)
        st.write("**AI's answer:**")
        st.markdown(response)  # markdown renders numbered points nicely
    else:
        st.info("Please enter a question to ask.")

if __name__ == "__main__":
    main()
  
#config.py
import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

""" Create " .env " file in your VS Code where there is main.py, config.py, groq.py and hf.py file is present """
#.env
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
HF_API_KEY = "YOUR_HUGGING_FACE_API_KEY"

"""using Streamlit

Streamlit run main.py

After running the code, create a requirements.txt file in the same folder and add the following dependencies

Streamlit
Huggingface_hub
Groq
python-dotenv

Next create .gitignore file and add .env as shown below

"""

'''


If a model doesn’t work, copy another model name from above link and paste it into MODEL_NAME.

MODELS = getattr(

    config,

    "HF_MODELS",

    ["REPLACE_WITH_ANAOTHE_MODEL_FROM_LIST"],

)

meta-llama/Llama-3-8B-Instruct

meta-llama/Llama-3-8B-Instruct

openai/gpt-oss-120b

deepseek-ai/DeepSeek-V3

MiniMaxAI/MiniMax-M1-80k
'''
