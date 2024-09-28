import streamlit as st
from utils.registry_client import RegistryClient
from utils.api import get_agent_card
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to render the Agent Repository page.
    """
    logger.info("Rendering Agent Repository page")

    st.set_page_config(
        page_title="GenSphere - AI Agent Hub",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items=None
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

    st.markdown("<h1 class='main-header'>🤖 AI Agent Hub</h1>", unsafe_allow_html=True)

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

                st.markdown("<h3 class='sub-header'>📋 Agent Card</h3>", unsafe_allow_html=True)
                
                # Check for labels in the config
                labels = None
                if 'config' in details and 'config' in details['config'] and 'Labels' in details['config']['config']:
                    labels = details['config']['config']['Labels']
                
                if labels and isinstance(labels, dict):
                    image_full_tag = labels.get("org.gensphere.img-full-tag")
                    if image_full_tag:
                        agent_card = get_agent_card(image_full_tag)
                        if agent_card:
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown(f"**👤 Author:** {agent_card['agent_card']['author']}")
                                st.markdown(f"**🖼️ Image:** {agent_card['agent_card']['image']}")
                                st.markdown(f"**🏷️ Tag:** {agent_card['agent_card']['tag']}")
                            with col2:
                                st.markdown(f"**🔗 URL:** [{agent_card['agent_card']['url']}]({agent_card['agent_card']['url']})")
                                st.markdown(f"**🏗️ Build Date:** {agent_card['build_date']}")
                                st.markdown(f"**🔖 Full Image Tag:** `{image_full_tag}`")
                            
                            st.markdown("**📝 Description:**")
                            st.info(agent_card['agent_card']['description'])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.markdown("**📥 Expected Inputs:**")
                                st.json(agent_card['expected_inputs'])
                            with col2:
                                st.markdown("**📤 Expected Output:**")
                                st.json(agent_card['expected_output'])
                        else:
                            st.warning("⚠️ Failed to fetch agent card information.")
                    else:
                        st.warning("⚠️ No org.gensphere.img-full-tag label found for this image.")
                else:
                    st.info("ℹ️ No agent card information found for this Agent.")
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
