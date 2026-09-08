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
# main_part1 (Streamlit) 
import io, re
from io import BytesIO
import streamlit as st
from huggingface_hub import InferenceClient
import config
# Switch provider by changing the import line:
from groq import generate_response
# from hf import generate_response 

MATH_SYSTEM = """You are a Math Mastermind.
Solve with clear step-by-step reasoning, correct notation, and a final answer.
Verify when possible; mention an alternative method briefly if relevant."""

CHAT_CSS = """
<style>
.wrap {max-height: 520px; overflow-y: auto; padding-right: 6px;}
.card{border:1px solid #e6e6e6;background:#fff;border-radius:10px;padding:14px 16px;margin:10px 0;
box-shadow:0 1px 2px rgba(0,0,0,0.04);}
.q{font-weight:700;color:#0a6ebd;margin-bottom:8px;}
.meta{display:inline-block;background:#FF9800;color:#fff;padding:2px 8px;border-radius:12px;font-size:12px;margin-left:8px}
.a{white-space:pre-wrap;color:#333;line-height:1.5;}
</style>
"""

def export_txt(history):
    txt = "".join([f"Q{i}: {h['question']}\nA{i}: {h['answer']}\n\n" for i, h in enumerate(history, 1)])
    bio = io.BytesIO(txt.encode("utf-8")); bio.seek(0); return bio

def teaching_answer(q: str) -> str:
    return generate_response(q, temperature=0.3, max_tokens=1024)

def math_answer(q: str, level: str) -> str:
    prompt = f"{MATH_SYSTEM}\n\nDifficulty: {level}\nMath Problem: {q}"
    return generate_response(prompt, temperature=0.1, max_tokens=1024)

def run_ai_teaching_assistant():
    st.title("🤖 AI Teaching Assistant")
    st.session_state.setdefault("history_ata", [])
    c1, c2 = st.columns([1, 2])
    if c1.button("🧹 Clear", key="c_ata"): st.session_state.history_ata = []; st.rerun()
    if st.session_state.history_ata:
        c2.download_button("📄 Export", export_txt(st.session_state.history_ata),
                           "AI_Teaching_Assistant_Conversation.txt", "text/plain")
    q = st.text_input("Enter your question:", key="q_ata")
    if st.button("Ask", key="a_ata"):
        if not q.strip(): st.warning("⚠️ Enter a question.")
        else:
            with st.spinner("Thinking..."):
                st.session_state.history_ata.append({"question": q.strip(), "answer": teaching_answer(q.strip())})
            st.rerun()

    if not st.session_state.history_ata: return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html = '<div class="wrap">'
    for i, qa in enumerate(st.session_state.history_ata, 1):
        html += f'<div class="card"><div class="q">Q{i}: {qa["question"]}</div><div class="a">{qa["answer"]}</div></div>'
    st.markdown(html + "</div>", unsafe_allow_html=True)

def run_math_mastermind():
    st.title("🧮 Math Mastermind")
    st.session_state.setdefault("history_mm", [])
    st.session_state.setdefault("k_mm", 0)
    c1, c2 = st.columns([1, 2])
    if c1.button("🧹 Clear", key="c_mm"): st.session_state.history_mm = []; st.rerun()
    if st.session_state.history_mm:
        c2.download_button("📄 Export", export_txt(st.session_state.history_mm),
                           "Math_Mastermind_Solutions.txt", "text/plain")
    with st.form("mm_form", clear_on_submit=True):
        q = st.text_area("Math problem:", height=100, key=f"mm_{st.session_state.k_mm}")
        a, b = st.columns([3, 1])
        go = a.form_submit_button("Solve", use_container_width=True)
        lvl = b.selectbox("Level", ["Basic", "Intermediate", "Advanced"], index=1)
        if go:
            if not q.strip(): st.warning("⚠️ Enter a problem.")
            else:
                with st.spinner("Solving..."):
                    ans = math_answer(q.strip(), lvl)
                st.session_state.history_mm.insert(0, {"question": q.strip(), "answer": ans, "difficulty": lvl})
                st.session_state.k_mm += 1; st.rerun()

    if not st.session_state.history_mm: return
    st.markdown(CHAT_CSS, unsafe_allow_html=True)
    html = '<div class="wrap">'
    for i, qa in enumerate(st.session_state.history_mm, 1):
        html += (f'<div class="card"><div class="q">Q{i}: {qa["question"]}'
                 f'<span class="meta">{qa["difficulty"]}</span></div>'
                 f'<div class="a">{qa["answer"]}</div></div>')
    st.markdown(html + "</div>", unsafe_allow_html=True)




# ---- Part 2: paste this function into Part 1 (replace placeholder) ----
def run_safe_ai_image_generator():
    FILTER_API_URL = "https://filters-zeta.vercel.app/api/filter"

    # fallback model if needed: "black-forest-labs/FLUX.1-schnell"
    IMG_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
    img_client = InferenceClient(provider="hf-inference", api_key=config.HF_API_KEY)

    st.title("🖼️ Safe AI Image Generator")

    def is_prompt_safe(prompt: str):
        try:
            response = requests.post(
                FILTER_API_URL,
                json={"text": prompt},
                timeout=15
            )

            if response.status_code != 200:
                return False, f"Filter API failed with status {response.status_code}: {response.text}"

            data = response.json()

            if data.get("ok") is True:
                return True, None
            return False, data.get("reason", "⚠️ Unsafe prompt.")

        except Exception as e:
            return False, f"Filter API error: {e}"

    def generate_image(prompt: str):
        safe, err = is_prompt_safe(prompt)
        if not safe:
            return None, err

        try:
            image = img_client.text_to_image(prompt=prompt, model=IMG_MODEL)
            return image, None
        except Exception as e:
            return None, f"Error during image generation: {e}"

    with st.form("img_form"):
        p = st.text_area("Image description:", height=120)
        ok = st.form_submit_button("Generate Image")

    if ok:
        if not p.strip():
            st.warning("⚠️ Enter a description.")
        else:
            with st.spinner("Generating image..."):
                im, err = generate_image(p.strip())

            if err:
                st.error(err)
            else:
                st.image(im, use_container_width=True)
                st.session_state.generated_image = im

    im = st.session_state.get("generated_image")
    if im:
        buf = BytesIO()
        im.save(buf, format="PNG")
        st.download_button(
            "📥 Download",
            buf.getvalue(),
            "ai_generated_image.png",
            "image/png"
        )

def main():
    st.sidebar.title("Choose AI Feature")
    opt = st.sidebar.selectbox("", ["AI Teaching Assistant", "Math Mastermind", "Safe AI Image Generator"])
    if opt == "AI Teaching Assistant": run_ai_teaching_assistant()
    elif opt == "Math Mastermind": run_math_mastermind()
    else: run_safe_ai_image_generator()

if __name__ == "__main__":
    main()


'''Step 3: Create "config.py" file in your VS Code where there is main.py and hf.py file is present 
config.py code: 

import os
from dotenv import load_dotenv

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY", "")

Step 4: Create " .env " file in your VS Code where there is main.py, config.py and hf.py file is present 

HF_API_KEY = "YOUR_HUGGING_FACE_API_KEY"

Run the main.py code:

Streamlit run main.py

After running the code, create a requirements.txt file in the same folder and add the following dependencies.
Streamlit
Huggingface_hub
python-dotenv

Next, push your code to GitHub and deploy the app by following the deployment instructions provided in Activity 2.

Models for hugging face to replace in hf.py file  

MODELS = getattr(
    config,
    "HF_MODELS",
    ["REPLACE_WITH_ANAOTHE_MODEL_FROM_LIST"],
)

