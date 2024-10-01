import streamlit as st
import requests
import json

def is_valid_json(json_string):
    try:
        json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False

def main():
    st.title("Create a Node from an existing AI Agent project")

    # Framework selection
    framework = st.selectbox(
        "Select Framework",
        options=["CrewAI"],
        index=0
    )

    # Form inputs
    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repo",
        help="Your project should comply with the template from CrewAI [docs](https://docs.crewai.com/getting-started/Start-a-New-CrewAI-Project-Template-Method/)"
    )
    author = st.text_input("Author", placeholder="Your Name")
    description = st.text_area("Description", placeholder="Describe your AI agent project")
    
    # Expected inputs
    st.subheader("Expected Inputs")
    input_json = st.text_area(
        "Expected Inputs (JSON format)",
        placeholder='''{
    "attribute1_name": "str",
    "attribute2_name": "int",
    "attribute3_name": "float"
}'''
    )
    
    # Expected outputs
    st.subheader("Expected Outputs")
    output_json = st.text_area(
        "Expected Outputs (JSON format)",
        placeholder='''{
    "attribute1_name": "str",
    "attribute2_name": "list",
    "attribute3_name": "dict"
}'''
    )
    
    version = st.text_input("Version", placeholder="1.0.0")

    if st.button("Submit"):
        # Validate all fields
        if not github_url or not author or not description or not input_json or not output_json or not version:
            st.error("All fields are required. Please fill in all the information.")
            return

        # Validate JSON inputs
        if not is_valid_json(input_json) or not is_valid_json(output_json):
            st.error("Invalid JSON format for inputs or outputs. Please check your JSON syntax.")
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
            st.success("Job created successfully!")
        except requests.exceptions.RequestException as e:
            st.error(f"Error creating job: {str(e)}")

if __name__ == "__main__":
    main()