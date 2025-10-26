# Assignment 1

This is a chat application that lets you upload your own `.txt` and `.pdf` files and ask questions about them.

It uses a RAG (Retrieval-Augmented Generation) pipeline to find answers directly from your documents. You can upload multiple files at once and have a conversation, including follow-up questions.

---

## How to Run

This app is designed to run in the provided GitHub Codespace.

1.  **Set API Key:** In the Codespace terminal, set your API key:
    ```bash
    export API_KEY="your-api-key-goes-here"
    ```
2.  **Run App:** In the same terminal, run Streamlit:
    ```bash
    streamlit run chat_with_pdf.py
    ```
3.  **View App:** A URL will appear in the terminal. Open this link in your browser.

---

## Project Configuration

* **`requirements.txt`**: Added `numpy==1.26.4` to fix a `ValueError: numpy.dtype size changed` incompatibility error in the base environment.
* All other configurations (`.devcontainer/` files) are used as-provided.