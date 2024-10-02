import streamlit as st
import requests
import yaml
import logging
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_valid_yaml(yaml_string):
    try:
        yaml.safe_load(yaml_string)
        return True
    except yaml.YAMLError:
        return False

def format_error_message(error):
    if isinstance(error, requests.exceptions.HTTPError):
        try:
            error_json = error.response.json()
            if 'detail' in error_json:
                return f"Error: {error_json['detail']}"
        except json.JSONDecodeError:
            pass
    return str(error)

def main():
    logger.info("Rendering Create Agent page")

    # Custom CSS for better styling, including dark mode support
    st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #4A90E2;
        }
        .sub-header {
            font-size: 1.8rem;
            color: #50C878;
        }
        .label-header {
            font-size: 1.2rem;
            color: #FF6B6B;
        }
        .info-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #F0F8FF;
            border: 1px solid #E0E0E0;
            color: #1E1E1E;
        }
        .stApp {
            background-color: white;
            color: black;
        }
        .error-message {
            color: #FF4136;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            background-color: #FFECEC;
            border: 1px solid #FF4136;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>🤖 Create an AI Agent</h1>", unsafe_allow_html=True)

    st.markdown("<h3 class='sub-header'>📋 Agent Details</h3>", unsafe_allow_html=True)

    # Form inputs
    col1, col2 = st.columns(2)
    with col1:
        agent_name = st.text_input("🏷️ Agent Name", placeholder="MyAwesomeAgent", key="agent_name")
        author = st.text_input("👤 Author", placeholder="Your Name", key="author")
    with col2:
        version = st.text_input("🔢 Version", placeholder="1.0.0", key="version")
        description = st.text_area("📝 Description", placeholder="Describe your AI agent", key="description")

    st.markdown("<h3 class='sub-header'>🔧 Agent Definition</h3>", unsafe_allow_html=True)
    agent_definition = st.text_area(
        "Agent Definition (YAML format)",
        placeholder="""name: MyAgent
role: Assistant
goals:
  - Help users with their queries
  - Provide accurate information
tools:
  - name: web_search
    description: Search the web for information
  - name: calculator
    description: Perform mathematical calculations
""",
        height=300,
        key="agent_definition"
    )

    st.markdown("<h3 class='sub-header'>📁 Dependency Files</h3>", unsafe_allow_html=True)
    uploaded_files = st.file_uploader("Upload dependency files (e.g., functions.py, requirements.txt)", accept_multiple_files=True, type=['py', 'txt'], key="uploaded_files")

    if st.button("🚀 Create Agent"):
        logger.info("Create Agent button clicked")
        
        # Validate all fields
        if not agent_name or not author or not description or not version or not agent_definition:
            st.markdown("<p class='error-message'>❌ All fields are required. Please fill in all the information.</p>", unsafe_allow_html=True)
            logger.warning("Form submission failed: Missing required fields")
            return

        # Validate YAML input
        if not is_valid_yaml(agent_definition):
            st.markdown("<p class='error-message'>❌ Invalid YAML format for agent definition. Please check your YAML syntax.</p>", unsafe_allow_html=True)
            logger.warning("Form submission failed: Invalid YAML format")
            return

        # Prepare the data
        data = {
            "agent_name": agent_name,
            "author": author,
            "description": description,
            "version": version,
            "agent_definition": agent_definition,
        }

        files = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                file_content = uploaded_file.read()
                files.append(('files', (uploaded_file.name, file_content, 'application/octet-stream')))

        # Send the data to the backend
        try:
            response = requests.post(
                "http://agents_service:8002/create_agent",
                data=data,
                files=files,
                timeout=10
            )
            response.raise_for_status()
            result = response.json()
            st.success(f"✅ Agent '{agent_name}' created successfully! Agent ID: {result['agent_id']}")
            logger.info(f"Agent '{agent_name}' created successfully with ID: {result['agent_id']}")
        except requests.exceptions.RequestException as e:
            error_message = format_error_message(e)
            st.markdown(f"<p class='error-message'>❌ Error creating agent: {error_message}</p>", unsafe_allow_html=True)
            logger.error(f"Error creating agent '{agent_name}': {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()