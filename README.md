# GenAI Learning Lab

A structured, self-directed engineering record moving from core software fundamentals to applied generative AI systems.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B.svg)](https://genai-learning-lab-3aybealefejytfp7kcu24s.streamlit.app/)

> This repository is a public, dated record of my progress through a structured eight-month curriculum. It documents code committed as it is written, not polished after the fact.

---

## Table of Contents

- [About This Repo](#about-this-repo)
- [Why This Exists](#why-this-exists)
- [Projects Completed So Far](#projects-completed-so-far)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Roadmap](#roadmap)
- [How to Run](#how-to-run)
- [License and Contact](#license-and-contact)

---

## About This Repo

This repository tracks my work across an eight-month technical roadmap toward becoming an Applied Arabic Generative AI Engineer. The target focus is enterprise AI systems for UAE government, banking, and energy sectors, where systems integration and regional language support are critical requirements.

The curriculum starts with standard software engineering practices in Python, then progresses through data engineering, API development, Arabic natural language processing, retrieval-augmented generation, sovereign model fine-tuning, and production system serving.

Right now, this repository represents Month 1. The code here covers fundamental programming mechanics, object-oriented design, error handling, API consumption, data manipulation, visualization, interactive web tools, and multi-tier backend architecture. The advanced Arabic AI components come later in the sequence and will appear in future project folders as I build them.

---

## Why This Exists

I started this project because I wanted a verifiable, commit-by-commit record of what I can build. Many portfolios present polished final demos without showing how the engineer got there or whether they understand the underlying layers.

By publishing every project as I complete it, I hold myself to a strict daily building standard. I want potential employers and technical collaborators to inspect the code, trace the architecture decisions, and see steady, deliberate progress across the full eight months.

---

## Projects Completed So Far

| Project | Directory | Status | Description |
| :--- | :--- | :--- | :--- |
| Project 01 | `Projects/Project-01-Personal-Info` | Local | Interactive console script practicing input collection, string formatting, and variable handling. |
| Project 02 | `Projects/Project-02-Guessing-Game` | Local | Number guessing console game implementing control flow, conditional loops, and random value generation. |
| Project 03 | `Projects/Project-03-Calculator` | Local | Command-line arithmetic calculator organized into modular arithmetic functions. |
| Project 04 | `Projects/Project-04-Student-Grade-Tracker` | Local | Grade book script using dictionaries and lists to compute class averages and rank top scores. |
| Project 05 | `Projects/Project-05-Text-Analyzer` | Local | String inspection tool calculating word counts, character frequencies, and sentence lengths. |
| Project 06 | `Projects/Project-06-First-Ai-Tool` | Local | Language model client calling an external LLM endpoint through OpenRouter with environment variable key management. |
| Project 07 | `Projects/Project-07-Calculator-OOP` | Local | Object-oriented calculator class maintaining an in-memory audit history of past operations. |
| Project 08 | `Projects/Project-08-ToDo-List` | Local | Task manager separating task logic, console interaction, and persistent JSON file storage. |
| Project 09 | `Projects/Project-09-Log-Analyzer` | Local | Log parser that aggregates INFO, WARNING, and ERROR counts with custom exception classes and safe file handling. |
| Project 10 | `Projects/Project-10-Password-Generator` | Local | Password generation tool with custom character set rules and regex-based password strength assessment. |
| Project 11 | `Projects/Project-11-Array-Statistics-Tool` | Local | CLI tool using NumPy arrays to calculate means, medians, standard deviations, and min-max boundaries. |
| Project 12 | `Projects/Project-12-Pandas-Data-Analyzer` | Local | Exploratory data analysis on the Titanic passenger dataset covering missing value imputation, grouping, and survival distributions. |
| Project 13 | `Projects/Project-13-News-API-Collector` | Local | Automated news fetcher querying the NewsAPI endpoint over HTTP and persisting structured article records to JSON. |
| Project 14 | `Projects/Project-14-CSV-Data-Analyzer` | Local | Command-line data analysis script computing descriptive statistics and saving Matplotlib bar, line, and pie charts. |
| Project 15 | `Projects/Project-15-CSV-Streamlit-Analyzer` | [Live](https://genai-learning-lab-3aybealefejytfp7kcu24s.streamlit.app/) | Interactive web application for uploading, filtering, and visualizing arbitrary CSV files using dynamic Plotly charts. |
| Project 16 | `Projects/Project-16-Python-API-Database` | Local | Multi-tier bank support system demonstrating clear separation between Streamlit, FastAPI, service logic, SQLAlchemy, and SQLite. |

---

## Tech Stack

The technologies below represent tools currently in use across the existing repository code:

| Layer | Tools Used |
| :--- | :--- |
| Core Language | Python (version 3.10 and newer) |
| Web Frontend | Streamlit |
| API & Transport | FastAPI, Uvicorn, Requests |
| Data Processing | pandas, NumPy |
| Data Visualization | Plotly Express, Matplotlib |
| Database & ORM | SQLite, SQLAlchemy |
| Validation & Configuration | Pydantic, python-dotenv |

---

## Repository Structure

```text
Genai-Learning-Lab/
├── LICENSE
├── README.md
├── requirements.txt
└── Projects/
    ├── Project-01-Personal-Info/
    ├── Project-02-Guessing-Game/
    ├── Project-03-Calculator/
    ├── Project-04-Student-Grade-Tracker/
    ├── Project-05-Text-Analyzer/
    ├── Project-06-First-Ai-Tool/
    ├── Project-07-Calculator-OOP/
    ├── Project-08-ToDo-List/
    ├── Project-09-Log-Analyzer/
    ├── Project-10-Password-Generator/
    ├── Project-11-Array-Statistics-Tool/
    ├── Project-12-Pandas-Data-Analyzer/
    ├── Project-13-News-API-Collector/
    ├── Project-14-CSV-Data-Analyzer/
    ├── Project-15-CSV-Streamlit-Analyzer/
    │   ├── app.py
    │   └── requirements.txt
    └── Project-16-Python-API-Database/
        ├── frontend/
        ├── api/
        ├── services/
        ├── database/
        ├── schemas/
        └── README.md
```

---

## Roadmap

The upcoming stages of this eight-month curriculum move into specialized Arabic natural language processing and production generative AI workflows. Here is what is planned:

1. Arabic Text Processing: Text normalization, morphological analysis, tokenization, and dialect handling across Modern Standard Arabic and Gulf Arabic variants.
2. Retrieval-Augmented Generation: Building vector indexing pipelines, hybrid keyword and dense embedding retrieval, and document grounding for enterprise technical documents.
3. Sovereign Model Fine-Tuning: Parameter-efficient fine-tuning on regional foundation models such as Jais and Falcon, targeting Arabic domain tasks in banking and government workflows.
4. Production Serving & Deployment: Serving containerized inference APIs, implementing latency monitoring, caching, and deploying to cloud infrastructure.

All progress on these topics will be committed to this repository as the code is developed.

---

## How to Run

### Prerequisites
- Python 3.10 or higher installed.
- Git installed.

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/asim-aftab-ai/Genai-Learning-Lab.git
   cd Genai-Learning-Lab
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux or macOS
   # Or on Windows PowerShell:
   # .\.venv\Scripts\Activate.ps1
   ```

3. Install root dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Individual Projects

- Run a standard CLI script (for example, Project 08 To-Do List):
  ```bash
  python Projects/Project-08-ToDo-List/main.py
  ```

- Run the Project 15 Streamlit Web App locally:
  ```bash
  streamlit run Projects/Project-15-CSV-Streamlit-Analyzer/app.py
  ```

- Run the Project 16 Multi-Tier API and Frontend:
  Start the backend:
  ```bash
  cd Projects/Project-16-Python-API-Database
  python -m uvicorn api.main:app --reload --port 8000
  ```
  In a separate terminal, start the frontend:
  ```bash
  cd Projects/Project-16-Python-API-Database
  python -m streamlit run frontend/streamlit_app.py
  ```

---

## License and Contact

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

Maintained by Asim Aftab.  
GitHub Profile: [https://github.com/asim-aftab-ai](https://github.com/asim-aftab-ai)
