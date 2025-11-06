# HR Assistant — Demo (Hugging Face Space)

This is a small demo chatbot for HR-related questions built with Gradio — intended for an assignment demonstration.

## Files
- `app.py` — Gradio app (chat UI + FAQ matching)
- `hr_faq.json` — Sample HR Q&A dataset
- `README.md` — This file

## How to deploy on Hugging Face Spaces (Gradio)
1. Create a free account on https://huggingface.co/ (if you don't have one).
2. Go to **Spaces** → **Create new Space**.
   - Name: `hr-assistant-demo` (or `obaid-hr-chatbot`)
   - SDK: **Gradio**
   - Visibility: **Public** (or Private if you prefer)
3. In the new Space repository, upload `app.py`, `hr_faq.json`, and `README.md`.
4. Commit changes. The Space will build and provide a public link, e.g.:
   `https://huggingface.co/spaces/<your-username>/hr-assistant-demo`
5. Open the link and test the chatbot.

## Customization & Next steps (optional)
- Replace the matching logic with an embedding-based retriever (e.g., sentence-transformers + FAISS/Pinecone) and an LLM for generated answers.
- Connect to SSO for internal access.
- Add logging and analytics for the top FAQs.

## Contact
For demo support, contact: hr-support@company.com
