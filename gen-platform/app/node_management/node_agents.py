import streamlit as st
from utils.registry_client import RegistryClient
from utils.api import get_node_card
import logging
import requests
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
    logger.info("Rendering AI Agents Hub page")

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

    st.markdown("<h1 class='main-header'>🤖 AI Agent Hub</h1>", unsafe_allow_html=True)

    client = RegistryClient()
    try:
        repositories = client.list_repositories()
        logger.info(f"Found {len(repositories)} repositories")

        if not repositories:
            st.info("ℹ️ No agents found.")
        else:
            # Create a list to store agent information
            agents_info = []

            for repo in repositories:
                tags = client.list_tags(repo)
                if tags:
                    latest_tag = tags[-1]  # Assume the last tag is the latest
                    details = client.get_image_details(repo, latest_tag)
                    
                    # Extract description from labels if available
                    description = "N/A"
                    if 'config' in details and 'config' in details['config'] and 'Labels' in details['config']['config']:
                        labels = details['config']['config']['Labels']
                        if labels and isinstance(labels, dict):
                            description = labels.get("org.gensphere.description", "N/A")
                    
                    agents_info.append({
                        "Repository": repo,
                        "Version": latest_tag,
                        "Description": description
                    })

            # Convert to DataFrame
            df = pd.DataFrame(agents_info)

            # Style the DataFrame
            def style_dataframe(df):
                return df.style.set_properties(**{'text-align': 'left'})\
                    .set_table_styles([
                        {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'left')]},
                        {'selector': 'td', 'props': [('padding', '5px')]},
                    ])

            styled_df = style_dataframe(df)

            st.markdown("<h3 class='sub-header'>🔍 Available Agents</h3>", unsafe_allow_html=True)
            # Display the styled DataFrame without index
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            # Allow users to view details of a specific agent
            st.markdown("<h3 class='sub-header'>📋 Agent Details</h3>", unsafe_allow_html=True)
            
            selected_repo = st.selectbox("📦 Select an agent", repositories)
            
            if selected_repo:
                try:
                    tags = client.list_tags(selected_repo)
                    logger.info(f"Found {len(tags)} tags for repository {selected_repo}")

                    if tags:
                        selected_tag = st.selectbox("🏷️ Select a version", tags)
                        details = client.get_image_details(selected_repo, selected_tag)
                        logger.info(f"Retrieved details for {selected_repo}:{selected_tag}")

                        # Check for labels in the config
                        labels = None
                        if 'config' in details and 'config' in details['config'] and 'Labels' in details['config']['config']:
                            labels = details['config']['config']['Labels']
                        
                        if labels and isinstance(labels, dict):
                            image_full_tag = labels.get("org.gensphere.img-full-tag")
                            if image_full_tag:
                                node_card = get_node_card(image_full_tag)
                                if node_card:
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown(f"**👤 Author:** {node_card['node_card']['author']}")
                                        st.markdown(f"**🖼️ Image:** {node_card['node_card']['image']}")
                                        st.markdown(f"**🏗️ Framework:** {node_card['node_card']['framework']}")
                                    with col2:
                                        st.markdown(f"**🔗 GitHub URL:** [{node_card['node_card']['github_url']}]({node_card['node_card']['github_url']})")
                                        st.markdown(f"**🏗️ Build Date:** {node_card['build_date']}")
                                        st.markdown(f"**🔖 Full Image Tag:** `{image_full_tag}`")
                                    
                                    st.markdown("**📝 Description:**")
                                    st.info(node_card['node_card']['description'])
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown("**📥 Expected Inputs:**")
                                        st.json(node_card['expected_inputs'])
                                    with col2:
                                        st.markdown("**📤 Expected Output:**")
                                        st.json(node_card['expected_output'])

                                    st.markdown("<h3 class='sub-header'>🚀 How to run this Agent</h3>", unsafe_allow_html=True)
                                    st.code(f"gen-cli deploy -r {selected_repo.split('/')[0]} -i {selected_repo.split('/')[1]} -t {selected_tag} -p 8081 -n container_1", language="bash")
                                else:
                                    st.warning("⚠️ Failed to fetch agent card information.")
                            else:
                                st.warning("⚠️ No org.gensphere.img-full-tag label found for this image.")
                        else:
                            st.info("ℹ️ No node card information found for this Agent.")
                            logger.warning(f"No labels found for {selected_repo}:{selected_tag}")
                    else:
                        st.warning("⚠️ No versions found for this agent.")
                        logger.warning(f"No tags found for repository {selected_repo}")

                except Exception as e:
                    error_message = format_error_message(e)
                    st.markdown(f"<p class='error-message'>❌ Error fetching agent details: {error_message}</p>", unsafe_allow_html=True)
                    logger.error(f"Error fetching agent details for agent '{selected_repo}': {str(e)}", exc_info=True)

    except Exception as e:
        error_message = format_error_message(e)
        st.markdown(f"<p class='error-message'>❌ Error fetching agents: {error_message}</p>", unsafe_allow_html=True)
        logger.error(f"Error fetching agents: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()