# AI-Based Learning Path Generator

An interactive, multiagent learning assistant powered by **LangChain**, **RAG (Retrieval-Augmented Generation)**, and **FastAPI**. The system analyzes user goals, retrieves curated educational resources from a local RAG vector database, generates a personalized step-by-step roadmap, and dynamically adapts the pathway based on user progress and feedback.

## 🚀 Key Features

* **Multiagent Planning System (LangChain)**:
  * **Goal Analyzer Agent**: Parses learning objectives, duration, hours/week, and style preferences into a series of milestones.
  * **Resource Retriever Agent (RAG)**: Searches the knowledge index using vector embeddings to attach the best courses, videos, and documentation.
  * **Roadmap Generator Agent**: Assembles milestones and resources, appending practical verification projects to each step.
  * **Adaptive Planner Agent**: Automatically updates future roadmap paces, resources, and difficulties when a user struggles or requests adjustments.
* **Dual Execution Modes**:
  * **Demo Mode (Default)**: Out-of-the-box heuristic execution with dynamic timeline adjustment and resource matching—requires no API keys.
  * **Live AI Mode**: Complete AI-agent reasoning using **Gemini 1.5** models and semantic vector searches—activated by entering a Gemini API Key.
* **Modern Glassmorphic Dashboard**: A fully responsive web interface featuring config controls, progress cards, checkbox tracking, timeline visualizations, and a RAG resource catalog browser.

---

## 🛠️ Tech Stack

* **Backend**: FastAPI, Uvicorn, Python 3.11+
* **AI Orchestration**: LangChain, `langchain-google-genai`
* **RAG Vector Search**: LangChain `InMemoryVectorStore` & `GoogleGenerativeAIEmbeddings` (with keyword-based token search fallback)
* **Frontend**: HTML5, Vanilla CSS3 (custom dark/neon theme, glassmorphic layout), Vanilla JavaScript

---

## 📂 Project Structure

```
├── backend/
│   ├── agents.py       # LangChain multiagent reasoning pipelines
│   ├── models.py       # Pydantic data schemas
│   ├── mock_data.py    # Baseline roadmaps for Demo Mode fallback
│   └── rag_store.py    # Knowledge base storage & semantic/keyword search
├── frontend/
│   ├── index.html      # User Interface structural layout
│   ├── styles.css      # Custom styling & animation definitions
│   └── app.js          # DOM manipulation & backend API hooks
├── main.py             # FastAPI server entry point
├── test_app.py         # Automated validation test suite
└── README.md           # Project documentation
```

---

## 💻 Quick Start

### 1. Installation
Install the required packages:
```bash
pip install langchain langchain-community langchain-google-genai fastapi uvicorn pydantic python-dotenv
```

### 2. Run the App
Start the FastAPI server:
```bash
python main.py
```

### 3. Open in Browser
Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

* To run in **Live AI Mode**, click the **Settings Gear (⚙️)** in the top-right corner of the dashboard, enter your `GEMINI_API_KEY`, and save.

---

## 🧪 Verification Tests
To run the local automated test suite that verifies Pydantic schemas, RAG fallback search, and roadmap generators, execute:
```bash
python test_app.py
```
