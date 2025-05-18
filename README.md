# 🦙 Your Pet Llama

This is a powerful and interactive web application built with [Streamlit](https://streamlit.io/) for retrieving files and images using natural language and visual queries. It leverages [LlamaIndex](https://github.com/jerryjliu/llama_index), OpenAI’s CLIP for multimodal embeddings, and supports vector database integrations with Postgres and Qdrant. Local language model inference is enabled via [Ollama](https://ollama.com/), making the app entirely self-hostable.

## 🚀 Features

- 🔍 Semantic search across documents, files, and images
- 🧩 Multimodal query support using CLIP embeddings
- 🗃️ Built-in support for **Postgres** and **Qdrant** as vector databases
- 🦙 Integration with local LLMs through **Ollama**
- 📊 Intuitive, browser-based UI built with **Streamlit**

## 🛠️ Getting Started

1. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```
2. **Set your OpenAI API key:**

    Open llama_backend.py and locate the line:

    ```python
    os.environ["OPENAI_API_KEY"] = ""
    ```

    Replace the empty string with your actual OpenAI API key.

3. **Launch the application:**

    ```bash
    streamlit run app.py
    ```

