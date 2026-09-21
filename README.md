# EcoSort AI

## Project Title
EcoSort AI: An Agentic AI Assistant for Intelligent Waste Segregation and Responsible Disposal

## Primary SDG
SDG 12 – Responsible Consumption and Production

## Project Purpose
EcoSort AI helps users identify common waste items, assign them to a practical waste category, retrieve relevant disposal guidance, and provide a clear handling recommendation.

The system is designed as a decision-support and educational tool. Waste-management requirements can differ by location, so users should verify local collection and disposal rules before acting on a recommendation.

## Main Features
- Text-based waste identification
- Optional image-based waste analysis
- Waste-category classification
- Retrieval-augmented guidance from a curated knowledge base
- Agent-based processing workflow
- Responsible handling messages for batteries, e-waste, sanitary waste, and hazardous materials
- Uncertainty handling instead of forced classification
- Streamlit interface
- IBM watsonx.ai / Granite integration
- LangGraph workflow orchestration

## Technology Stack
- Python
- Streamlit
- IBM watsonx.ai
- IBM Granite models
- LangGraph
- scikit-learn
- Pillow
- python-dotenv

## Project Structure

```text
EcoSortAI/
├── app.py
├── agent.py
├── llm.py
├── rag.py
├── requirements.txt
├── .env.example
├── .gitignore
├── LICENSE.txt
├── README.md
│
├── data/
│   └── waste_guidance.json
│
├── docs/
│   ├── BUILD_GUIDE.md
│   ├── PROJECT_BRIEF.md
│   ├── BOB_PROMPTS.txt
│   └── DEMO_CHECKLIST.md
│
└── tests/
    ├── test_rag.py
    └── test_watsonx.py
```

## Important
Never commit `.env` or any API key to GitHub.

## Local Run

1. Create and activate a Python 3.13 virtual environment.
2. Install the packages from `requirements.txt`.
3. Copy `.env.example` to `.env`.
4. Add your own IBM watsonx.ai credentials.
5. Run the test scripts.
6. Start the Streamlit application with:

```powershell
streamlit run app.py
```

The detailed setup sequence is in `docs/BUILD_GUIDE.md`.
