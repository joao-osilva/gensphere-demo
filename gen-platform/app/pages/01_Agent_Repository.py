import streamlit as st
from utils.registry_client import RegistryClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to render the Agent Repository page.
    """
    logger.info("Rendering Agent Repository page")

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
    try:
        repositories = client.list_repositories()
        logger.info(f"Found {len(repositories)} repositories")

        if repositories:
            selected_repo = st.selectbox("📦 Select a repository", repositories)
            tags = client.list_tags(selected_repo)
            logger.info(f"Found {len(tags)} tags for repository {selected_repo}")

            if tags:
                selected_tag = st.selectbox("🏷️ Select a tag", tags)
                details = client.get_image_details(selected_repo, selected_tag)
                logger.info(f"Retrieved details for {selected_repo}:{selected_tag}")

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
                    logger.warning(f"No labels found for {selected_repo}:{selected_tag}")

                st.markdown("<h3 class='sub-header'>🚀 How to run this Agent</h3>", unsafe_allow_html=True)
                st.code(f"gen-cli deploy -r {selected_repo.split('/')[0]} -i {selected_repo.split('/')[1]} -t {selected_tag} -p 8081 -n container_1", language="bash")
            else:
                st.warning("⚠️ No tags found for this repository.")
                logger.warning(f"No tags found for repository {selected_repo}")
        else:
            st.warning("⚠️ No repositories found in the registry.")
            logger.warning("No repositories found in the registry")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"An error occurred while rendering the Agent Repository page: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()
