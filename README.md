🧠 MindMap Live: AI-Powered Research Portal
MindMap Live is a full-stack research knowledge management system designed to automate the transition from unstructured academic literature to structured, interconnected knowledge representations. Built to streamline the research workflow, the portal focuses on Relational Machine Learning and Natural Language Processing (NLP).

🚀 Core Functionalities
LLM-Based Synthesis: Leverages the Gemini 3 Flash model to perform cross-document analysis, generating "Connection Insights" that identify theoretical overlaps between separate research papers.

Dynamic Knowledge Graphing: Implements a radial-layout visualization that maps entities and concepts (e.g., Transformer Models, Tensor Factorization) to reveal latent dependencies.

Automated Research Briefings: A background processing engine that compiles recent discoveries and dispatches structured summaries via SMTP-secured email protocols.

Persistent Research Timeline: A database-driven timeline that maintains the provenance of findings, tracking source metadata, methodology, and core contributions over time.
 
![Dashboard Screenshot]
<img width="1881" height="883" alt="image" src="https://github.com/user-attachments/assets/25a14442-ac0e-4b5e-8c01-2d31e169dbef" />

🛠️ Technical Architecture
Backend: Python (Flask / Gradio)

LLM Integration: Google Generative AI API (Gemini 1.5/3 Flash)

Graph Theory: NetworkX for modeling relational data structures

Data Visualization: D3.js-inspired radial layout for complex entity mapping

OCR & Extraction: Automated PDF processing for metadata and methodology extraction

📖 Research Alignment (LLM-OCR-D)
This project is architected to address challenges similar to those in the LLM-OCR-D initiative at ScaDS.AI:

Post-Correction & Quality Assurance: Using generative models to refine extracted data.

Structured Preparation: Organizing disparate findings into Knowledge Graphs for scholarly reuse.

Intelligent Workflows: Automating the selection and execution of text transformation tasks.

⚙️ Installation & Setup
Clone the repository:

Bash
git clone https://github.com/Monisha2181998/mindmap-live.git
Install dependencies:

Bash
pip install -r requirements.txt
Configure Environment:

Add your Gemini API Key in llm_connector.py.

Update SMTP credentials in notifier.py.

Run the Portal:

Bash
python app.py
