# 🍽️ Restaurant Recommendation System

An AI-powered, multimodal Restaurant Recommendation System built with Retrieval-Augmented Generation (RAG) and a coordinated multi-agent architecture. The system ingests unstructured restaurant data (text + images), structures it with LLMs, indexes it in a multimodal vector store, and serves personalized recommendations through specialized AI agents — all exposed via a chatbot UI and integrated end-to-end using the Model Context Protocol (MCP).

---

## ✨ Features

- **LLM-Powered Data Structuring** — Converts unstructured restaurant descriptions and reviews into structured JSON using prompt-engineered LLM extraction.
- **Multimodal Captioning** — Generates captions for review images using multimodal LLMs and merges them into review data.
- **Multimodal RAG Pipeline** — Builds text + image vector embeddings, performs hybrid similarity search with metadata filtering, and applies late-fusion ranking across modalities.
- **Multi-Agent Recommendation Engine** — Specialized agents (each with defined roles, goals, and tasks) collaborate to generate restaurant and recipe recommendations from a single query.
- **Interactive Chatbot** — A Gradio-based conversational interface for querying restaurants/food and managing records.
- **MCP Integration** — Agent tools, the vector database, and documents are exposed via an MCP server, with a client and an LLM-powered MCP host (GUI) for full tool-augmented interaction.
- **CLI Data Management** — Command-line interface to browse, add, edit, and delete restaurant records, with automatic backups.

---

## 🏗️ Architecture

```
                     ┌───────────────────────┐
                     │   Raw Restaurant Data   │
                     │   (text + images)        │
                     └───────────┬───────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   Data Structuring Layer   │
                    │  LLM extraction + captioning │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   Multimodal RAG Layer      │
                    │  Embeddings · Vector Index   │
                    │  Hybrid Search · Late Fusion │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   Multi-Agent Layer          │
                    │  Restaurant Agent · Recipe Agent │
                    │  Orchestrator (LangGraph)     │
                    └────────────┬─────────────┘
                                 │
                 ┌───────────────┼───────────────┐
                 ▼                               ▼
      ┌─────────────────┐             ┌─────────────────────┐
      │  Gradio Chatbot UI │             │   MCP Server/Client    │
      │                     │             │   + LLM Host (GUI)      │
      └─────────────────┘             └─────────────────────┘
```

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Language | Python 3.10+ |
| Agent Orchestration | LangChain, LangGraph |
| LLM / Multimodal AI | IBM watsonx.ai |
| Vector Search | FAISS |
| Chat Interface | Gradio |
| Integration Protocol | MCP (Model Context Protocol) |
| Data Format | JSON |
| Testing | Pytest |
| Version Control | Git / GitHub |

---

## 📁 Project Structure

```
restaurant-recommendation-system/
├── src/
│   └── restaurant_recsys/
│       ├── __init__.py
│       ├── config.py                  # Env vars, settings, constants
│       │
│       ├── structuring/               # Unstructured -> structured JSON
│       │   ├── __init__.py
│       │   ├── extractor.py           # LLM-based attribute extraction
│       │   └── schema.py              # Data models / JSON schema
│       │
│       ├── captioning/                # Multimodal image captioning
│       │   ├── __init__.py
│       │   └── image_captioner.py
│       │
│       ├── data_manager/              # CRUD + backups for restaurant records
│       │   ├── __init__.py
│       │   ├── repository.py
│       │   └── backup.py
│       │
│       ├── retrieval/                 # Multimodal RAG pipeline
│       │   ├── __init__.py
│       │   ├── embeddings.py          # Text + image embedding generation
│       │   ├── vector_store.py        # FAISS index build/query
│       │   ├── hybrid_search.py       # Similarity + metadata filtering
│       │   └── fusion.py              # Late-fusion ranking
│       │
│       ├── agents/                    # Multi-agent system
│       │   ├── __init__.py
│       │   ├── base_agent.py
│       │   ├── restaurant_agent.py
│       │   ├── recipe_agent.py
│       │   └── orchestrator.py        # LangGraph coordination
│       │
│       ├── mcp/                       # MCP integration
│       │   ├── __init__.py
│       │   ├── server.py              # Exposes tools/data/docs
│       │   ├── client.py
│       │   └── host.py                # LLM-powered MCP host (GUI)
│       │
│       ├── chatbot/                   # Gradio interface
│       │   ├── __init__.py
│       │   └── app.py
│       │
│       └── cli/                       # Command-line interface
│           ├── __init__.py
│           └── main.py
│
├── data/
│   ├── raw/                           # Source descriptions & images
│   ├── structured/                    # Structured JSON records
│   ├── vector_store/                  # Persisted FAISS index
│   └── backups/                       # Auto backups before writes
│
├── tests/
│   ├── test_structuring.py
│   ├── test_retrieval.py
│   ├── test_agents.py
│   └── test_mcp.py
│
├── scripts/
│   ├── build_index.py                 # Standalone index-build entrypoint
│   ├── run_chatbot.py
│   ├── run_mcp_server.py
│   └── run_mcp_host.py
│
├── docs/
│   └── architecture.md
│
├── .env.example
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Git
- An IBM watsonx.ai account (API key + project ID)

### Installation
```bash
git clone https://github.com/<your-username>/restaurant-recommendation-system.git
cd restaurant-recommendation-system

python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Configuration
Copy the example environment file and add your credentials:
```bash
cp .env.example .env
```
```env
WATSONX_API_KEY=your_api_key
WATSONX_PROJECT_ID=your_project_id
WATSONX_URL=your_endpoint_url
VECTOR_STORE_PATH=data/vector_store
```

---

## ▶️ Usage

**1. Structure raw data into JSON**
```bash
python -m restaurant_recsys.structuring.extractor --input data/raw --output data/structured
```

**2. Manage records via CLI**
```bash
python -m restaurant_recsys.cli.main
```

**3. Build the multimodal vector index**
```bash
python scripts/build_index.py
```

**4. Launch the chatbot**
```bash
python scripts/run_chatbot.py
```

**5. Run the MCP server, then client/host**
```bash
python scripts/run_mcp_server.py
python scripts/run_mcp_host.py
```

---

## 🧪 Testing
```bash
pytest tests/ -v
```

---

## 🗺️ Roadmap
- [ ] Data structuring & CLI record management
- [ ] Multimodal embeddings, hybrid search, late-fusion ranking
- [ ] Multi-agent orchestration with LangGraph
- [ ] Gradio chatbot interface
- [ ] MCP server, client, and LLM-powered host
- [ ] Deployment (Docker / cloud hosting)

---

## 🤝 Contributing
Contributions are welcome. Please open an issue to discuss proposed changes, then submit a pull request following the existing project structure and code style.

## 📄 License
Distributed under the MIT License. See `LICENSE` for details.
