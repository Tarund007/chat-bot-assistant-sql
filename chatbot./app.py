## Olist D2C AI Analytics Assistant
import base64
import json
import os
import tempfile
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.utilities.sql_database import SQLDatabase
from google.cloud import bigquery
from langchain_groq import ChatGroq
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent

google_form_url = "https://drive.google.com/file/d/1038Z57CcOn1TVn4twxzEuIklskFMBb3D/view?usp=sharing"

@st.cache_resource
def get_db_connection():
    try:
        # Load from Base64 secret on Streamlit Cloud
        if "GCP_CREDENTIALS_BASE64" in st.secrets:
            json_bytes = base64.b64decode(st.secrets["GCP_CREDENTIALS_BASE64"])
            with tempfile.NamedTemporaryFile(mode="wb", delete=False, suffix=".json") as temp:
                temp.write(json_bytes)
                temp_path = temp.name
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = temp_path
            return SQLDatabase.from_uri("bigquery://olist-d2c-analytics/olist_warehouse")

    except Exception as e:
        st.error(f"Cloud DB Connection Error: {e}")

    # Fallback for local execution using local credentials.json file
    try:
        local_creds = r"D:\Data Analytics\Chat D2C\Chatbot\olist-ai-assistant\credentials.json"
        if os.path.exists(local_creds):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = local_creds
            return SQLDatabase.from_uri("bigquery://olist-d2c-analytics/olist_warehouse")
    except Exception as local_err:
        st.error(f"Local DB Connection Error: {local_err}")

    return None
# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Olist D2C AI Analytics Assistant",
    page_icon="🤖",
    layout="wide"
)

# --- Custom CSS Styling for a Sleek Enterprise Look ---
st.markdown("""
    <style>
        .main {
            background-color: #0e1117;
        }
        h1 {
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
        }
        .stTextInput input {
            border-radius: 8px;
            border: 1px solid #30363d;
            background-color: #161b22;
            color: #ffffff;
        }
        .metric-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Title Header & Description ---
st.title("🤖 Olist D2C Natural Language-to-SQL Assistant")
st.markdown("Query your Brazilian E-Commerce BigQuery data warehouse instantly using natural language.")
st.markdown("---")

# --- Sidebar Configuration & Interactive Prompts ---
with st.sidebar:
    st.header("⚙️ Configuration")
    groq_api_key = st.text_input("Enter Groq API Key:", type="password")
    
    # --- API Key & Free Tier Notice Addon ---
    st.markdown("---")
    st.markdown("### ℹ️ API Key & Usage Limits")
    st.markdown(
        """
        <div style="
            background-color: #161b22; 
            border: 1px solid #30363d; 
            padding: 15px; 
            border-radius: 10px; 
            margin-bottom: 10px;
            font-family: 'Segoe UI', sans-serif;
            color: #c9d1d9;
            font-size: 13.5px;
            line-height: 1.5;
        ">
            <strong style="color: #ffffff; font-size: 14px;">⚡ Groq Free Tier Guidelines:</strong><br><br>
            <b style="color: #58a6ff;">Use the Groq API key <a href="{https://drive.google.com/file/d/1038Z57CcOn1TVn4twxzEuIklskFMBb3D/view?usp=sharing}" target="_blank" style="color: #58a6ff;">View Key</a></b><br>
            Enter a valid key above. Do not share it with others.<br><br>
            • <b>Rate Limits:</b> Subject to ~30 requests/min and token caps.<br>
            • <b>Reset / Refresh:</b> If you encounter a rate limit error, simply wait 1 minute or re-enter/refresh your key!
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.markdown("---")
    st.markdown("### 💡 Quick Portfolio Prompts")
    st.markdown("*(Click an idea to copy or test)*")
    
    if "selected_prompt" not in st.session_state:
        st.session_state.selected_prompt = ""

    prompts = [
        "What are the top 5 product categories by total sales and average price?",
        "Which customer states have the highest order volume and delivery times?",
        "What is the order fulfillment status breakdown (delivered vs canceled)?",
        "What is the monthly cohort retention trend from Month 0 to Month 3?",
        "What is the average product weight and physical dimension per product category?",
        "Which sellers handle the highest order item volume across orders?"
    ]
    
    for p in prompts:
        if st.button(p, use_container_width=True):
            st.session_state.selected_prompt = p

    st.markdown("---")
    st.markdown("### 📊 Warehouse Status")
    st.markdown("🟢 **BigQuery**: Connected (`olist_warehouse`)")
    st.markdown("⚡ **LLM**: Groq (`qwen/qwen3.8-27b`)")
    
    

# --- Check API Key and Initialize Agent ---
if not groq_api_key:
    st.warning("⚠️ Please enter your free Groq API key in the sidebar to initialize the AI agent.")
else:
    try:
        db = get_db_connection()
        
        llm = ChatGroq(
            model="qwen/qwen3.8-27b", 
            groq_api_key=groq_api_key, 
            temperature=0.1,
            max_tokens=800
            
        )
        
        agent_executor = create_sql_agent(
            llm=llm,
            db=db,
            verbose=True,
            agent_type="zero-shot-react-description",
            agent_executor_kwargs={"handle_parsing_errors": True}
        )
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # --- Display Historical Messages & Persistent Expanders ---
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant":
                    if "recommendations" in message:
                        with st.expander("💡 Strategic Business Recommendations"):
                            st.markdown(message["recommendations"])
                    if "summary" in message:
                        with st.expander("📊 View Data Extraction Summary"):
                            st.markdown(message["summary"])

        chat_placeholder = "Ask a data question..."
        prompt = st.chat_input(chat_placeholder)
        
        if st.session_state.selected_prompt:
            prompt = st.session_state.selected_prompt
            st.session_state.selected_prompt = ""

        if prompt:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("🔍 Inspecting schema, writing BigQuery SQL, and executing..."):
                    try:
                        response = agent_executor.run(prompt)
                        st.markdown(response)
                        
                        # Dynamically generate tailored strategic recommendations
                        with st.spinner("Generating strategic business insights..."):
                            recommendation_prompt = f"""
                            Based on this data query result: "{response}"
                            Provide 2 short, highly tailored strategic business or operational recommendations for an e-commerce platform like Olist. Keep it concise, specific, and actionable.
                            """
                            dynamic_recommendations = llm.invoke(recommendation_prompt).content

                        with st.expander("💡 Strategic Business Recommendations"):
                            st.markdown(dynamic_recommendations)

                        # Dynamically generate the Data Extraction Summary using the LLM
                        with st.spinner("Extracting query metadata..."):
                            summary_prompt = f"""
                            Based on the user's question "{prompt}" and the query result "{response}", provide a concise technical summary in bullet points covering:
                            - **Source Tables Queried:** (e.g. cleaned_orders, cleaned_customers, cleaned_order_items, etc. based on the data)
                            - **Warehouse Provider:** Google BigQuery (olist_warehouse)
                            - **Execution Type:** (e.g. Real-time multi-table relational join, time-series aggregation, grouping, etc.)
                            Keep it clean and formatted in markdown bullet points.
                            """
                            dynamic_summary = llm.invoke(summary_prompt).content

                        with st.expander("📊 View Data Extraction Summary"):
                            st.markdown(dynamic_summary)

                        # --- SAVE TO SESSION STATE ONCE (No duplication) ---
                        st.session_state.messages.append({
                            "role": "assistant", 
                            "content": response,
                            "recommendations": dynamic_recommendations,
                            "summary": dynamic_summary
                        })
                        
                    except Exception as e:
                        error_msg = f"An error occurred while executing the query: {e}"
                        st.error(error_msg)

    except Exception as e:
        st.error(f"Failed to connect to BigQuery database. Check your credentials: {e}")
