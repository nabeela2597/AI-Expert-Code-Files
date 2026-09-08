
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
# Choose ONE provider by importing it:

#Change groq --> hf to use hugging face API
#Change hf --> groq to use groq API
from groq import generate_response
# from groq import generate_response


def bias_mitigation_activity():
    print("\n=== BIAS MITIGATION ACTIVITY ===\n")
    prompt = input("Enter a prompt to explore bias (e.g., 'Describe the ideal doctor'): ").strip()
    if not prompt:
        print("Please enter a prompt to run the activity.")
        return

    initial_response = generate_response(prompt, temperature=0.3, max_tokens=1024)
    print(f"\nInitial AI Response: {initial_response}")

    modified_prompt = input(
        "Modify the prompt to make it more neutral (e.g., 'Describe the qualities of a doctor'): "
    ).strip()
    if modified_prompt:
        modified_response = generate_response(modified_prompt, temperature=0.3, max_tokens=1024)
        print(f"\nModified AI Response (Neutral): {modified_response}")
    else:
        print("No modified prompt entered. Skipping neutral response.")

def token_limit_activity():
    print("\n=== TOKEN LIMIT ACTIVITY ===\n")
    long_prompt = input(
        "Enter a long prompt (more than 300 words, e.g., a detailed story or description): "
    ).strip()

    if long_prompt:
        long_response = generate_response(long_prompt, temperature=0.3, max_tokens=1024)
        preview = (long_response[:500] + "...") if len(long_response) > 500 else long_response
        print(f"\nResponse to Long Prompt: {preview}")
    else:
        print("No long prompt entered. Skipping long prompt response.")

    short_prompt = input("Now, condense the prompt to be more concise: ").strip()
    if short_prompt:
        short_response = generate_response(short_prompt, temperature=0.3, max_tokens=1024)
        print(f"\nResponse to Condensed Prompt: {short_response}")
    else:
        print("No condensed prompt entered. Skipping condensed prompt response.")

def run_activity():
    print("\n=== AI Learning Activity ===")
    print("Choose an activity:")
    print("1) Bias Mitigation")
    print("2) Token Limits")
    choice = input("> ").strip()

    if choice == "1":
        bias_mitigation_activity()
    elif choice == "2":
        token_limit_activity()
    else:
        print("Invalid choice. Please choose 1 or 2.")

if __name__ == "__main__":
    run_activity()


'''
python main.py
Models for hugging face to replace in hf.py file   

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
