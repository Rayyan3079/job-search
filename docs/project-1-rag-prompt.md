# Prompt for Claude Code: build my portfolio project "DocuMind" (RAG Q&A over technical documents)

Copy everything below the line into a new Claude Code chat.

---

I am a M.Sc. Data Science student (TU Ilmenau, Germany) with a B.S. in Artificial Intelligence. I am applying for working-student roles in AI engineering, data and analytics. I need ONE polished, honest portfolio project on my GitHub that proves I can build a practical LLM application end to end. Build it with me in this session and publish it to my GitHub account at the end.

## Project: DocuMind – ask questions about technical PDF manuals, with sources and an evaluation

A small but production-minded Retrieval-Augmented Generation (RAG) app: the user uploads PDF documents (e.g. product manuals, SAP help guides, technical specs), asks questions in natural language, and gets answers that **cite the exact page and passage** they came from. The project's differentiator is a **built-in evaluation**: a test set of questions with expected answers, and a script that measures retrieval quality, answer quality, latency and cost, so I can show I understand *when a system works, when it fails, and why*.

## Requirements

### Functionality
1. **Ingestion pipeline** (`documind/ingest.py`)
   - Load PDFs from a `data/docs/` folder (use `pypdf`).
   - Clean text, split into chunks (configurable size and overlap, default ~800 characters / 150 overlap), keep metadata: file name, page number, chunk id.
   - Create embeddings with a free local model via `sentence-transformers` (default `all-MiniLM-L6-v2`), so no paid embedding API is needed.
   - Store vectors in a local vector store (ChromaDB, persisted to `data/index/`).
   - Re-running ingestion must be idempotent (skip unchanged files using a content hash).
2. **Retrieval** (`documind/retrieve.py`)
   - Top-k semantic search (default k=5), returning chunks with scores and metadata.
   - Optional: simple keyword (BM25 via `rank_bm25`) + semantic hybrid, switchable by a flag, so the evaluation can compare both.
3. **Answer generation** (`documind/answer.py`)
   - Use the official **Anthropic Python SDK** (`anthropic`) to call Claude. Read the model name from an env var `DOCUMIND_MODEL`; default to Claude Opus 5.5 (`claude-opus-5-5`), and document in the README that Claude Haiku 5.5 (`claude-haiku-5-5`) is a much cheaper option for experiments.
   - Use the claude-api skill / official SDK docs for correct, current API usage (do not guess SDK parameters).
   - The prompt must instruct the model to answer **only from the provided context**, cite sources as `[file, page]`, and say "I could not find this in the documents" when the context does not contain the answer.
   - Return: answer text, list of cited sources, token usage, latency in ms, estimated cost in USD.
   - Read the API key from the `ANTHROPIC_API_KEY` environment variable (`.env` file supported via `python-dotenv`). Never commit keys; add `.env` to `.gitignore` and ship a `.env.example`.
4. **Interfaces**
   - **CLI** (`python -m documind ask "question"` and `python -m documind ingest`), using `typer`.
   - **Web UI** with **Streamlit** (`app.py`): upload PDFs, run ingestion, chat-style Q&A, show the retrieved chunks with page numbers in an expandable "Sources" panel, show latency and cost per answer.
   - **REST API** with **FastAPI** (`documind/api.py`): `POST /ingest`, `POST /ask` returning JSON (answer, sources, usage, latency). Include auto-generated docs at `/docs`.
5. **Evaluation** (`eval/`) – the most important part for my CV
   - Use 2–3 public, freely licensed PDF manuals as the demo corpus (pick openly downloadable documents, record their source URLs and licenses in `data/docs/SOURCES.md`; if a license is unclear, don't commit the PDF itself, add a download script instead).
   - Create `eval/questions.jsonl` with ~25 questions: for each, the question, the expected answer (short), and the page(s) where the answer is found. Include 3–5 questions whose answer is NOT in the documents (to test "I could not find this").
   - `eval/run_eval.py` computes and saves to `eval/results/`:
     - **Retrieval**: hit rate@k and MRR (is the correct page among retrieved chunks?), for semantic vs hybrid retrieval.
     - **Answer quality**: an LLM-as-judge score (correct / partially correct / wrong) comparing the answer to the expected answer, plus a "correct refusal" rate for unanswerable questions.
     - **Latency** (p50/p95) and **total cost**.
   - Print a summary table and write `eval/results/summary.md`. Put the final numbers in the README (real numbers from a real run only, never invented).
6. **Quality**
   - Python 3.11, type hints, docstrings, clean package layout, `pyproject.toml` (or `requirements.txt`).
   - `pytest` unit tests for chunking, idempotent ingestion, retrieval output shape, citation parsing, and the FastAPI endpoints (mock the LLM call in tests so tests need no API key).
   - Logging with the standard `logging` module.
   - A `Dockerfile` that runs the Streamlit app, and a short "Run with Docker" section.
   - GitHub Actions workflow (`.github/workflows/ci.yml`) that installs dependencies and runs `pytest` on every push.

### README (write it for recruiters)
- Title, one-sentence pitch, and a screenshot or GIF of the Streamlit UI (take a real screenshot after running it).
- "What it does", architecture diagram (Mermaid: PDFs → chunking → embeddings → ChromaDB → retrieval → Claude → answer with citations), tech stack.
- Quick start (venv + pip, `.env`, ingest, run UI / CLI / API), Docker.
- **Evaluation results** table with the real numbers and 3–5 honest observations (e.g. where hybrid retrieval beat semantic, which question types failed and why).
- "What I learned" and "Next steps" (e.g. reranking, better chunking, more documents).
- License: MIT.

### Process
1. Ask me first for my GitHub username and check that `git` and the GitHub CLI (`gh`) are installed and that `gh auth status` is logged in; if not, guide me through `gh auth login`.
2. Plan the folder structure, show it to me, then build step by step. Commit after each meaningful step with clear messages (this gives the repo a real history).
3. Ask me for my `ANTHROPIC_API_KEY` only when we first need to call the API, and store it only in `.env`.
4. Run the tests, the ingestion and the full evaluation for real; fix whatever fails.
5. At the end: create a **public** GitHub repository named `documind-rag` with `gh repo create documind-rag --public --source . --push`, add a repository description and topics (`rag`, `llm`, `claude`, `python`, `fastapi`, `streamlit`, `chromadb`, `evaluation`), and confirm the CI run passes.
6. Finally, give me: the repo URL, 3 CV bullet points that describe exactly what I built (with the real evaluation numbers), and a 3–4 sentence explanation of the project I can use in interviews.

Do not fabricate any results, metrics or screenshots. Keep the scope tight and finish a working, well-documented version first; optional extras only if everything else works.
