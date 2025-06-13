# Descriptive QA System with DeepSeek R1 via Ollama (cleaned output version)

import streamlit as st
import ollama
import re

def clean_output(text):
    """
    Cleans filler phrases and removes <think>...</think> blocks.
    """
    import re

    # Remove <think>...</think> blocks completely
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # Remove common assistant-style filler phrases
    patterns_to_remove = [
        r"^(Sure|Certainly|Of course|Let me explain|Here's|Here is|As an AI.*?)[:,\-]\s*",
        r"^I'm an AI.*?\.\s*",
        r"^Let's dive in.*?\.\s*",
        r"^Here’s (what|how|a|an).*?:\s*"
    ]
    for pattern in patterns_to_remove:
        text = re.sub(pattern, "", text, flags=re.IGNORECASE | re.MULTILINE)

    # Clean up extra blank lines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    return text.strip()


# ----------------------------------
# Streamlit UI Setup
# ----------------------------------
st.set_page_config(page_title="DeepSeek QA System", layout="centered")
st.title("🧠 DeepSeek Descriptive QA System (Ollama)")

with st.expander("📘 Instructions", expanded=False):
    st.markdown("""
    - This app uses DeepSeek R1 running locally with Ollama.
    - Select a prompt style and enter your question.
    - The model output is automatically cleaned of assistant-style phrases.
    - **Ensure Ollama is running** with:
      ```
      ollama run deepseek-r1:1.5b
      ```
    """)

# ----------------------------------
# Prompt Style Selection
# ----------------------------------
style = st.selectbox("Select Prompt Style", ["Descriptive", "Concise", "Story-like"])
question = st.text_input("Ask your question", placeholder="e.g., What is Artificial Intelligence?")

# ----------------------------------
# Format Prompt
# ----------------------------------
def format_prompt(q, style):
    if style == "Descriptive":
        return f"Please provide a detailed and informative explanation for the following:\n{q}"
    elif style == "Concise":
        return f"Give a short and clear answer to:\n{q}"
    elif style == "Story-like":
        return f"Explain this with a short story or real-life example:\n{q}"

# ----------------------------------
# Get DeepSeek R1 Response via Ollama
# ----------------------------------
def get_deepseek_response(prompt):
    try:
        response = ollama.chat(
            model="deepseek-r1:1.5b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['message']['content']
    except Exception as e:
        return f"⚠️ Error: {e}"

# ----------------------------------
# Generate Answer
# ----------------------------------
if st.button("Generate Answer") and question:
    with st.spinner("Generating response from DeepSeek R1..."):
        final_prompt = format_prompt(question, style)
        raw_answer = get_deepseek_response(final_prompt)
        cleaned_answer = clean_output(raw_answer)

        st.success("Answer generated!")
        st.markdown("### ✅ Answer")
        st.write(cleaned_answer)

        st.markdown("### 📌 Prompt Used")
        st.code(final_prompt)

# ----------------------------------
# Save Q&A History for Manual Comparison
# ----------------------------------
st.markdown("---")
st.markdown("## 🔍 Compare with ChatGPT / Gemini Manually")

if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

if st.button("Save this Q&A for Comparison"):
    if question:
        st.session_state.qa_history.append({
            "question": question,
            "style": style,
            "prompt": format_prompt(question, style)
        })
        st.success("Saved for manual comparison with ChatGPT and Gemini.")
    else:
        st.warning("Please enter a question first.")

if st.session_state.qa_history:
    st.markdown("### 📄 Saved Prompts")
    for idx, item in enumerate(st.session_state.qa_history, 1):
        st.markdown(f"**{idx}. Prompt Style: {item['style']}**")
        st.code(item['prompt'])

