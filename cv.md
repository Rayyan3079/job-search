# CV -- Muhammad Rayyan Ahmed

**Location:** Ilmenau, Germany
**Email:** muhammad-rayyan.ahmed@tu-ilmenau.de
**Phone:** +49 179 6991596
**LinkedIn:** linkedin.com/in/rayyan--ahmed
**Kaggle:** kaggle.com/rayyan123z

## Professional Summary

M.Sc. Data Science student at TU Ilmenau with professional experience in SAP data modelling, SAP Datasphere, SAP Analytics Cloud and ABAP CDS views, and a background in Python and machine learning.

## Work Experience

### Tapal Tea (Pvt.) Ltd. -- Karachi, Pakistan

**Business Analyst**
Apr 2026 - Sep 2026

- Built a quality inspection dashboard in SAP Analytics Cloud on a data model built from ABAP CDS view data sources and joins, replacing a manual process in which users opened an SAP report per material for thousands of materials and compiled defect status in Excel
- Built an employee expense reimbursement dashboard in SAP Analytics Cloud
- Handled daily support tickets and user queries for around 30 SAP Analytics Cloud dashboards across HR, finance, supply chain and procurement, including dashboards built by others
- Performed SQL analysis, ABAP CDS view validation and data reconciliation to support reporting accuracy
- Translated business requirements into KPI-based reporting
- Wrote complete documentation for the dashboards I built, covering data sources, calculations, the dashboard and the resulting numbers
- Built a simple Power BI dashboard for the CEO comparing current-month sales with the fiscal-year sales plan, used to track performance and adjust strategy

### SAP Authorized Training Program -- Karachi, Pakistan

**SAP Young Professionals Program (YPP)**
Aug 2025 - Sep 2025

- Selected as one of 10 participants from Pakistan for the SAP Young Professionals Program
- Completed intensive training on SAP S/4HANA Cloud Public Edition implementation, covering end-to-end business processes and system configuration
- Gained hands-on exposure to SAP Activate methodology, Fit-to-Standard workshops and cloud-based best practices
- Studied SAP Cloud Integration (CPI) concepts including message mappings, iFlows and integration scenarios
- Earned SAP Certified Associate: SAP S/4HANA Cloud Public Edition, Implementation Consultant, and SAP Certified Associate: Integration Developer

### TallyMarks Consulting (TMC) -- Karachi, Pakistan

**Management Trainee Officer, Data Planning & Analytics**
Jun 2025 - Apr 2026

- Part of a team migrating a textile manufacturer's 42 SAP Analytics Cloud dashboards from an SAP BW backend to SAP Datasphere
- Independently built the spinning dashboard end to end: investigated sources and dependencies, rebuilt the datasets in SAP Datasphere and rebuilt the SAP Analytics Cloud dashboard
- Dashboard KPIs: Overall Equipment Effectiveness (OEE), machine efficiency and utilization, downtime and yield
- Designed and implemented SAP Datasphere data pipelines connecting the required sources
- Prepared and presented a client presentation on SAP Analytics Cloud; the client subsequently purchased it

### Tapal Tea (Pvt.) Ltd. -- Karachi, Pakistan

**SAP Data Analyst Intern**
Jun 2024 - Aug 2024

- Analyzed company purchase data from SAP reports to uncover key trends and insights, improving procurement decision-making
- Developed interactive dashboards in SAP Analytics Cloud (SAC) and Power BI, enabling real-time visualization of purchasing data and faster report generation
- Collected and refined user stories from employees to design customized dashboards that streamlined operational workflows and reduced manual data processing
- Wrote complex SQL queries to integrate company-wide data with SAC, enabling seamless data updates and minimizing reliance on manual extraction

## Projects

- **DocuMind: RAG Q&A over technical PDF manuals** (Python, FastAPI, Streamlit, ChromaDB, sentence-transformers, BM25, Claude API, pytest, Docker, GitHub Actions) -- Personal project, github.com/Rayyan3079/documind-rag. Built a retrieval-augmented generation system that answers questions about PDF manuals with page-level citations, served through a CLI, a FastAPI REST API and a Streamlit UI. Answered 20 of 22 answerable test questions correctly (91%) and refused all 4 unanswerable questions, at 3.3 s median latency. Implemented hybrid retrieval (BM25 + semantic search merged with Reciprocal Rank Fusion), raising MRR from 0.748 (semantic only) to 0.898 and evidence-page hit rate@5 from 91% to 100% (BM25 alone reached MRR 0.894, so most of the gain came from keyword search). Designed an evaluation harness with retrieval metrics (hit rate, MRR) and an LLM-as-judge; a full evaluation run cost $0.44. 37 offline unit tests, GitHub Actions CI, Docker. Used the evaluation to trace both wrong answers to chunk boundaries
- **Retinal OCT Scan Classification** (PyTorch, EfficientNet-B0, OpenCV) -- 4-class classifier on a pretrained EfficientNet-B0; 94.11% accuracy on a 968-image test set. Preprocessing and augmentation: denoising, resizing, rotation, cropping, flipping
- **Automated Cricket Highlights Generation** (PyTorch, OpenCV, EfficientNet-B0, EasyOCR, FFmpeg) -- B.S. final-year thesis, team project. My part: created training data, evaluated and tuned the EfficientNet-B0 model, tested EasyOCR configurations for scoreboard extraction, and built the video extraction and highlight assembly pipeline aligning detected events with timestamps
- **Kaggle notebooks** (Python) -- Exploratory data analysis and visualization notebooks: Spotify Top Songs, Obesity EDA & Predictions, Heart Attack EDA & Prediction (kaggle.com/rayyan123z)
- **Knowledge Graph Construction & Clustering from Reddit Text** (Python, spaCy, NetworkX, Node2Vec, BERT, GPT-2) -- Team project on a professor-provided dataset. Extracted subject-relation-object triples; compared graph-based and language-model embeddings with K-Means and HDBSCAN

## Education

- **M.Sc. Data Science**, Technische Universität Ilmenau, Oct 2026 - present. Current courses: Bayesian Data Assimilation, Research Skills, Sequential Decision Making, Theoretical Foundations of Data Management
- **B.S. Artificial Intelligence**, FAST-NUCES, Karachi, Sep 2021 - Jun 2025. CGPA 3.49/4.00 (German grade equivalent: 1.7, converted). Final-year thesis: Automated Cricket Highlights Generation

## Certifications

- SAP Certified Associate: SAP Analytics Cloud (Data Analyst)
- SAP Certified Associate: SAP Business Data Cloud
- SAP Certified Associate: SAP S/4HANA Cloud Public Edition, Implementation Consultant
- SAP Certified Associate: SAP Integration Developer
- Earned via the SAP Young Professionals Program (2025)

## Skills

- **SAP & Analytics:** SAP Analytics Cloud, SAP Datasphere, ABAP CDS views, SAP Business Data Cloud, data modelling, ETL / data transformation, data pipelines, SQL
- **Programming & ML:** Python, Pandas, NumPy, scikit-learn, PyTorch, OpenCV, EasyOCR, FFmpeg, spaCy, NetworkX, Node2Vec, BERT, GPT-2
- **LLM apps & engineering (project experience):** RAG, Claude API, ChromaDB, sentence-transformers, BM25, FastAPI, Streamlit, pytest, Docker, Git/GitHub, GitHub Actions
- **Visualization & Office:** SAP Analytics Cloud, Matplotlib, Power BI (basic), Excel (pivot tables, formulas), PowerPoint
- **Languages:** English (fluent, IELTS 8.0 / C1), German (A1, currently learning)
