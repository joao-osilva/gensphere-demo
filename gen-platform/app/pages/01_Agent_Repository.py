import streamlit as st
from utils.registry_client import RegistryClient

st.set_page_config(
    page_title="GenSphere - Agent Repository",
    page_icon="🤖",
    layout="wide"
)

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
        background-color: rgba(240, 248, 255, 0.1);
        border: 1px solid rgba(240, 248, 255, 0.2);
    }
    .stApp.light .info-box {
        color: #1E1E1E;
    }
    .stApp.dark .info-box {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🤖 AI Agents Repository</h1>", unsafe_allow_html=True)

client = RegistryClient()
repositories = client.list_repositories()

if repositories:
    selected_repo = st.selectbox("📦 Select a repository", repositories)
    tags = client.list_tags(selected_repo)

    if tags:
        selected_tag = st.selectbox("🏷️ Select a tag", tags)
        details = client.get_image_details(selected_repo, selected_tag)

        st.markdown("<h3 class='sub-header'>📋 Details</h3>", unsafe_allow_html=True)
        
        # Check for labels in the config
        labels = None
        if 'config' in details and 'config' in details['config'] and 'Labels' in details['config']['config']:
            labels = details['config']['config']['Labels']
        
        if labels and isinstance(labels, dict):
            st.markdown("---")
            
            # Create a three-column layout for labels
            cols = st.columns(3)
            
            for i, (key, value) in enumerate(labels.items()):
                with cols[i % 3]:
                    st.markdown(f"**{key}**")
                    st.markdown(f"<div class='info-box'>{value}</div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("ℹ️ No details found for this Agent.")

        st.markdown("<h3 class='sub-header'>🚀 How to use this Agent</h3>", unsafe_allow_html=True)
        st.code(f"gen-cli run {selected_repo}:{selected_tag}", language="bash")
    else:
        st.warning("⚠️ No tags found for this repository.")
else:
    st.warning("⚠️ No repositories found in the registry.")
