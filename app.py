# app.py
import json
import difflib
import gradio as gr
from typing import List, Tuple

# Config
HR_CONTACT = "hr-support@company.com"
FALLBACK_THRESHOLD = 0.55  # similarity threshold to accept an answer

# Load HR FAQ dataset
with open("hr_faq.json", "r", encoding="utf-8") as f:
    HR_FAQ = json.load(f)

# Helper: find best matching FAQ entry using difflib SequenceMatcher
def find_best_answer(query: str, top_k: int = 3) -> Tuple[List[Tuple[float,str,str]], float]:
    scores = []
    q = query.lower()
    for item in HR_FAQ:
        text_candidates = " ".join([item.get("question",""), item.get("answer","")]).lower()
        score = difflib.SequenceMatcher(None, q, text_candidates).ratio()
        scores.append((score, item.get("question",""), item.get("answer","")))
    scores.sort(key=lambda x: x[0], reverse=True)
    best_score = scores[0][0] if scores else 0.0
    return scores[:top_k], best_score

# Generate reply: either precise answer, top suggestions, or fallback
def generate_reply(user_message: str, history: List[List[str]] = None) -> Tuple[List[List[str]], str]:
    if history is None:
        history = []
    matches, best_score = find_best_answer(user_message, top_k=3)
    if best_score >= FALLBACK_THRESHOLD:
        # Return best match as answer, and also show related suggestions
        best = matches[0]
        answer = best[2]
        suggestions = "\n\nIf this doesn't fully answer your question, related topics you can try:\n"
        for s in matches[1:]:
            suggestions += f"- {s[1]}\n"
        final_answer = answer + suggestions
    else:
        # low confidence -> provide fallback guidance
        final_answer = (
            "I couldn't find an exact answer in the HR knowledge base. "
            f"Please contact HR at {HR_CONTACT} for case-specific help, or ask a clearer question (e.g., 'How many sick leaves per year?')."
        )
    # Append to history and return
    history = history + [["Employee", user_message], ["HR-Bot", final_answer]]
    return history, final_answer

# Simple small-talk handler
def is_small_talk(q: str) -> bool:
    s = q.lower().strip()
    small = ["hi", "hello", "hey", "thanks", "thank you", "good morning", "good evening", "bye"]
    return any(s.startswith(item) for item in small)

def small_talk_reply(q: str):
    low = q.lower()
    if "hi" in low or "hello" in low or "hey" in low:
        return "Hello! I'm HR Assistant Bot. How can I help you today?"
    if "thank" in low:
        return "You're welcome! Anything else I can help with?"
    if "bye" in low:
        return "Goodbye — have a great day!"
    return "How can I help with HR today? Ask about leave, reimbursements, or benefits."

# Gradio UI
with gr.Blocks(theme=gr.themes.Default()) as demo:
    gr.Markdown("## 🤖 HR Assistant — Demo\nAsk about leave policy, reimbursements, benefits, and more. (Demo dataset)")
    chat_history = gr.State([])  # stores conversation list pairs
    chatbot = gr.Chatbot(elem_id="chatbot").style(height=400)
    txt = gr.Textbox(show_label=False, placeholder="Ask about leave policy, reimbursements, etc. Press Enter to send.")
    submit_btn = gr.Button("Send")

    def user_submit(message, history):
        if not message or not message.strip():
            return history, ""
        # handle small talk
        if is_small_talk(message):
            reply = small_talk_reply(message)
            history = history + [["Employee", message], ["HR-Bot", reply]]
            return history, ""
        history, answer = generate_reply(message, history)
        return history, ""

    txt.submit(user_submit, [txt, chat_history], [chat_history, txt])
    submit_btn.click(user_submit, [txt, chat_history], [chat_history, txt])

    gr.Markdown("**Demo notes:** This demo uses a small local HR FAQ dataset. For production, integrate a vector store and an LLM for retrieval + generation. Contact HR: " + HR_CONTACT)

if __name__ == "__main__":
    demo.launch()
