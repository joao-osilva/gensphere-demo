import streamlit as st
import requests
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False

def main():
    logger.info("Rendering Create Node page")

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
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='main-header'>🚀 Create a Node based on you project</h1>", unsafe_allow_html=True)

    st.markdown("<h3 class='sub-header'>📋 Node Details</h3>", unsafe_allow_html=True)

    # Framework selection
    framework = st.selectbox(
        "🛠️ Select Framework",
        options=["CrewAI"],
        index=0
    )

    # Form inputs
    col1, col2 = st.columns(2)
    with col1:
        github_url = st.text_input(
            "🔗 GitHub Repository URL",
            placeholder="https://github.com/username/repo",
            help="Your project should comply with the template from CrewAI [docs](https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/)"
        )
        author = st.text_input("👤 Author", placeholder="Your Name")
    with col2:
        version = st.text_input("🏷️ Version", placeholder="1.0.0")
        description = st.text_area("📝 Description", placeholder="Describe your AI agent project")

    st.markdown("<h3 class='sub-header'>🔄 Input/Output Configuration</h3>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p class='label-header'>📥 Expected Inputs</p>", unsafe_allow_html=True)
        input_json = st.text_area(
            "Expected Inputs (JSON format)",
            placeholder='''{
    "attribute1_name": "str",
    "attribute2_name": "int",
    "attribute3_name": "float"
}'''
        )
    with col2:
        st.markdown("<p class='label-header'>📤 Expected Outputs</p>", unsafe_allow_html=True)
        output_json = st.text_area(
            "Expected Outputs (JSON format)",
            placeholder='''{
    "attribute1_name": "str",
    "attribute2_name": "list",
    "attribute3_name": "dict"
}'''
        )

    if st.button("🚀 Submit"):
        logger.info("Submit button clicked")
        # Validate all fields
        if not github_url or not author or not description or not input_json or not output_json or not version:
            st.error("❌ All fields are required. Please fill in all the information.")
            logger.warning("Form submission failed: Missing required fields")
            return

        # Validate JSON inputs
        if not is_valid_json(input_json) or not is_valid_json(output_json):
            st.error("❌ Invalid JSON format for inputs or outputs. Please check your JSON syntax.")
            logger.warning("Form submission failed: Invalid JSON format")
            return

        # Prepare the data
        data = {
            "framework": framework,
            "github_url": github_url,
            "author": author,
            "description": description,
            "expected_inputs": json.loads(input_json),
            "expected_outputs": json.loads(output_json),
            "version": version
        }

        # Send the data to the backend
        try:
            response = requests.post("http://jobs_service:8001/create_job", json=data, timeout=10)
            response.raise_for_status()
            st.success("✅ Node created successfully!")
            logger.info("Node created successfully")
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Error creating node: {str(e)}")
            logger.error(f"Error creating node: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()