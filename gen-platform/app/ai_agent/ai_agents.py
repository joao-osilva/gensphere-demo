import streamlit as st
import requests
import pandas as pd
import logging
import json
import io

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
    logger.info("Rendering AI Agents page")

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

    st.markdown("<h1 class='main-header'>🤖 AI Agents</h1>", unsafe_allow_html=True)

    try:
        response = requests.get("http://agents_service:8002/agents", timeout=10)
        response.raise_for_status()
        agents = response.json()
        logger.info(f"Retrieved {len(agents)} agents")

        if not agents:
            st.info("ℹ️ No agents found.")
        else:
            # Convert agents to a DataFrame for easier display
            df = pd.DataFrame(agents)
            
            # Select and rename columns
            df = df[['agent_name', 'version', 'description']]
            df.columns = ['Agent Name', 'Version', 'Description']

            # Style the DataFrame
            def style_dataframe(df):
                return df.style.set_properties(**{'text-align': 'left'})\
                    .set_table_styles([
                        {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'left')]},
                        {'selector': 'td', 'props': [('padding', '5px')]},
                    ])

            styled_df = style_dataframe(df)

            st.markdown("<h3 class='sub-header'>🔍 Agents</h3>", unsafe_allow_html=True)
            # Display the styled DataFrame without index
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            # Allow users to view details of a specific agent
            st.markdown("<h3 class='sub-header'>📋 Agent Details</h3>", unsafe_allow_html=True)
            
            # Create a list of "Agent Name - Version" for the selectbox
            agent_options = [f"{agent['agent_name']} - {agent['version']}" for agent in agents]
            selected_agent_option = st.selectbox("🔎 Select an agent to view details:", agent_options)
            
            if selected_agent_option:
                try:
                    # Extract agent name and version from the selected option
                    selected_agent_name, selected_agent_version = selected_agent_option.split(" - ")
                    
                    # Find the agent based on the selected name and version
                    selected_agent = next(agent for agent in agents 
                                          if agent['agent_name'] == selected_agent_name 
                                          and agent['version'] == selected_agent_version)
                    selected_agent_id = selected_agent['_id']

                    # Fetch full agent details
                    agent_response = requests.get(f"http://agents_service:8002/agents/{selected_agent_id}", timeout=10)
                    agent_response.raise_for_status()
                    agent = agent_response.json()
                    
                    # Display key information
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"**🤖 Agent Name:** {agent['agent_name']}")
                        st.markdown(f"**👤 Author:** {agent['author']}")
                    with col2:
                        st.markdown(f"**📝 Description:** {agent['description']}")
                        st.markdown(f"**🏷️ Version:** {agent['version']}")                    

                    # Display the agent definition
                    with st.expander("🔧 Agent Definition", expanded=False):
                        st.code(agent['agent_definition'], language='yaml')

                    # Add download button
                    download_url = f"http://agents_service:8002/agents/{selected_agent_id}/download"
                    response = requests.get(download_url)
                    response.raise_for_status()

                    # Create a download button
                    st.download_button(
                        label="📥 Download Agent",
                        data=response.content,
                        file_name=f"{agent['agent_name']}_{agent['version']}.zip",
                        mime="application/zip"
                    )

                except requests.exceptions.RequestException as e:
                    error_message = format_error_message(e)
                    st.markdown(f"<p class='error-message'>❌ Error fetching agent details: {error_message}</p>", unsafe_allow_html=True)
                    logger.error(f"Error fetching agent details for agent '{selected_agent_option}': {str(e)}", exc_info=True)

    except requests.exceptions.RequestException as e:
        error_message = format_error_message(e)
        st.markdown(f"<p class='error-message'>❌ Error fetching agents: {error_message}</p>", unsafe_allow_html=True)
        logger.error(f"Error fetching agents: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()