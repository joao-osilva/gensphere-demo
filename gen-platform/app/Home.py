import streamlit as st
from utils.registry_client import RegistryClient

st.set_page_config(
    page_title="GenSphere Platform",
    page_icon="🌐",
    layout="wide"
)

st.title("Welcome to GenSphere Platform")
st.write("Navigate through the pages to explore AI agents and learn how to use the platform.")

st.title("AI Agents Repository")

client = RegistryClient()
repositories = client.list_repositories()

if repositories:
    selected_repo = st.selectbox("Select a repository", repositories)
    tags = client.list_tags(selected_repo)

    if tags:
        selected_tag = st.selectbox("Select a tag", tags)
        details = client.get_image_details(selected_repo, selected_tag)

        st.subheader("Image Details")
        
        # Check for labels in the config
        labels = None
        if 'config' in details and 'config' in details['config'] and 'Labels' in details['config']['config']:
            labels = details['config']['config']['Labels']
        
        if labels and isinstance(labels, dict):
            st.subheader("Labels", divider='gray')
            
            # Create a three-column layout for labels
            cols = st.columns(3)
            
            for i, (key, value) in enumerate(labels.items()):
                with cols[i % 3]:
                    st.markdown(f"**{key}**")
                    st.text(value)
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("No labels found for this image.")

        st.subheader("How to use this image")
        st.code(f"gen-cli run {selected_repo}:{selected_tag}", language="bash")
    else:
        st.warning("No tags found for this repository.")
else:
    st.warning("No repositories found in the registry.")
