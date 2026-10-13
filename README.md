# Olist D2C Natural Language-to-SQL AI Analytics Assistant

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-SQL%20Agent-green)
![BigQuery](https://img.shields.io/badge/Google-BigQuery-orange)
![Groq](https://img.shields.io/badge/Groq-Qwen%203.8%2027B-purple)

An end-to-end, portfolio-ready D2C analytics platform built on the **Olist
Brazilian E-Commerce dataset**. The project combines a cloud data warehouse,
advanced SQL analytics, an executive dashboard, and a natural-language-to-SQL
assistant for business users.

Stakeholders can ask questions such as:

> What was the retention rate for customers who bought face serum in Q3?

The assistant translates the question into SQL, executes it against BigQuery,
and returns a plain-English answer with strategic recommendations and
technical data-lineage metadata.

## Project outcomes

This project covers the three core layers of a modern analytics product:

1. **Data warehouse and analytics engine** - cleaned Olist data modeled in
   BigQuery with reusable SQL for e-commerce metrics.
2. **Executive BI layer** - a focused D2C performance and cohort dashboard
   designed for daily operational and growth monitoring.
3. **AI product layer** - a Streamlit application that lets users query the
   warehouse using natural language.

## Key features

- Natural-language questions translated into BigQuery SQL
- LangChain SQL Agent connected to the `olist_warehouse` dataset
- Groq-hosted `qwen/qwen3.8-27b` model integration
- Advanced SQL analytics using CTEs and window functions
- Cohort retention matrix based on customers' first purchase month
- Revenue, order-volume, customer, product, payment, and delivery analysis
- Daily and monthly performance tracking
- Executive dashboard with retention and fulfillment views
- Dynamic strategic recommendations generated from query results
- Technical extraction summary showing source tables, warehouse, and execution
  type
- Quick-prompt sidebar for common stakeholder questions
- Cached BigQuery connection for improved Streamlit performance
- Hybrid local and cloud credential handling

## System architecture

```text
 [ Business User / Recruiter ]
             |
             | Natural-language question or quick prompt
             v
 [ Streamlit Executive Analytics App ]
             |
             +--> [ LangChain SQL Agent - ReAct ]
             |             |
             |             +--> [ Groq LLM - qwen/qwen3.8-27b ]
             |             |          |
             |             |          +--> Recommendations and summaries
             |             |
             |             +--> [ SQLAlchemy BigQuery Dialect ]
             |                        |
             v                        v
 [ Plain-English Answer ] <--- [ Google BigQuery ]
                                  olist-d2c-analytics
                                  olist_warehouse
```

## Phase 1: Data warehouse and analytics engine

### Dataset and preparation

The project uses the **Olist Brazilian E-Commerce dataset**, which contains
relational data for orders, customers, products, sellers, payments, reviews,
and delivery dates.

The preparation workflow uses Python, `pandas`, and `numpy` to:

- Clean missing and inconsistent values
- Standardize date and timestamp fields
- Prepare order, customer, product, payment, and review data
- Structure the source files for relational analysis
- Load the cleaned data into BigQuery tables

The main warehouse target is:

```text
Project: olist-d2c-analytics
Dataset: olist_warehouse
```

### Advanced SQL analytics

The analytics layer demonstrates SQL patterns used in real D2C and
e-commerce reporting:

- **Window functions** for product ranking by category and
  week-over-week revenue analysis
- **CTEs** for multi-step business logic
- **Customer Acquisition Cost (CAC)** calculations
- **Customer Lifetime Value (LTV)** calculations
- **Cohort retention analysis** based on first purchase month
- Revenue and order-volume trends
- Customer state and product-category performance
- Payment-method and delivery-status analysis

The cohort retention logic assigns every customer to a first-purchase cohort,
maps later activity to months since acquisition, and produces a retention
matrix that highlights where customers drop off.

## Phase 2: Executive dashboard

The BI layer provides a focused executive view rather than a crowded
collection of charts. It includes:

- Daily order-volume and platform-growth trend
- Order fulfillment and delivery-status view
- Monthly customer retention heat map
- Cohort-based customer activity tracking
- High-level performance indicators and record counts

The dashboard is designed to answer the questions founders and operators
typically ask every morning:

- Is order volume growing?
- Where are customers dropping out of the funnel?
- Are orders being delivered successfully?
- Which customer cohorts retain over time?
- Are performance changes operational or demand-driven?

## Phase 3: AI product layer

The Streamlit app turns the warehouse into a conversational analytics tool.
When a user submits a question:

1. Streamlit receives the question.
2. The LangChain SQL Agent inspects the available BigQuery schema.
3. The Groq model generates an appropriate SQL query.
4. BigQuery executes the query against the Olist warehouse.
5. The result is shown in the chat interface.
6. The model generates concise strategic recommendations.
7. A technical extraction summary describes the data lineage and execution
   type.

Example questions:

- What are the top five product categories by total sales?
- Which customer states generate the highest revenue?
- What is the average order delivery time?
- What is the monthly order and revenue trend for 2018?
- How does payment method share vary across orders?
- How many unique customers made a purchase?

## Technology stack

- **Python** - data preparation and application runtime
- **pandas / numpy** - data cleaning and transformation
- **Jupyter Notebook** - exploratory preparation workflow
- **Google BigQuery Sandbox** - cloud data warehouse
- **SQL** - warehouse transformations and D2C metrics
- **Streamlit** - interactive web application
- **LangChain / LangChain Community** - SQL Agent and database tooling
- **LangChain Groq** - Groq model integration
- **Groq** - LLM inference
- **SQLAlchemy BigQuery dialect** - database connectivity

## Repository structure

```text
Chatbot/
├── README.md
├── requirements.txt
└── olist-ai-assistant/
    ├── sql_agent/                # SQL and analytics work
    └── olist-ai-assistant/
        └── app.py               # Streamlit natural-language analytics app
```

## Prerequisites

Before running the application, make sure you have:

1. Python 3.10 or newer
2. A Google Cloud project with BigQuery access
3. Access to the `olist-d2c-analytics.olist_warehouse` dataset, or an
   equivalent dataset configured in the application
4. A Google Cloud service account with permission to query BigQuery
5. A Groq API key

## Installation

From the repository root, create and activate a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration

### Google Cloud credentials

For local development, set `GOOGLE_APPLICATION_CREDENTIALS` to the absolute
path of a service-account JSON file:

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\credentials.json"
```

For Streamlit Cloud or another deployment environment, configure the
`gcp_service_account` object in Streamlit secrets. The application can map
those secrets to a temporary credentials file at runtime.

Never commit service-account keys, API keys, or other secrets.

### BigQuery connection

The application currently uses:

```text
bigquery://olist-d2c-analytics/olist_warehouse
```

To use another project or dataset, update the `db_uri` in
`olist-ai-assistant/olist-ai-assistant/app.py`.

### Groq API key

Start the app and enter the Groq API key in the sidebar. The key is supplied
to the model at runtime and is not stored in source code.

## Run the Streamlit application

From the repository root:

```powershell
streamlit run .\olist-ai-assistant\olist-ai-assistant\app.py
```

Open the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Security and cost controls

- Do not commit credentials, API keys, or local secret files.
- Use least-privilege, read-only BigQuery permissions where possible.
- Review generated SQL before running expensive queries on large datasets.
- Keep query limits and warehouse cost controls enabled in production.
- Rotate any credential that has been exposed.
- Prefer Streamlit secrets or a managed secret manager for deployment.

## Current limitations

- The assistant is configured for one BigQuery project and dataset by default.
- Chat history is retained only for the current Streamlit session.
- There is no authentication or multi-user access-control layer yet.
- Generated SQL and recommendations depend on schema quality and model output.
- Query results are currently presented as text rather than downloadable
  reports or interactive charts inside the chat.
- Centralized application logging and automated evaluation are not yet
  implemented.

## Future improvements

- Add persistent chat and analytics history
- Add CSV export and chart rendering for query results
- Add authentication and role-based access
- Add query-cost estimation, limits, and SQL approval workflows
- Add automated tests for database connectivity, SQL generation, and metric
  correctness
- Add a production deployment configuration
- Add a Loom walkthrough demonstrating the Streamlit-to-BigQuery flow
