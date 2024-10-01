import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    logger.info("Rendering Node Status page")

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

    st.markdown("<h1 class='main-header'>📊 Node Creation - Job Status</h1>", unsafe_allow_html=True)

    # Add a refresh button
    if st.button("🔄 Refresh Jobs"):
        logger.info("Refresh button clicked")
        st.rerun()

    try:
        response = requests.get("http://jobs_service:8001/jobs", timeout=10)
        response.raise_for_status()
        jobs = response.json()
        logger.info(f"Retrieved {len(jobs)} jobs")

        if not jobs:
            st.info("ℹ️ No jobs found.")
        else:
            # Convert jobs to a DataFrame for easier display
            df = pd.DataFrame(jobs)
            
            # Select and rename columns
            df = df[['id', 'github_url', 'version', 'author', 'status']]
            df.columns = ['Job ID', 'GitHub URL', 'Version', 'Author', 'Status']

            # Style the DataFrame
            def style_dataframe(df):
                return df.style.apply(lambda x: ['background-color: #90EE90' if v == 'DONE' else 'background-color: #FFB3BA' for v in x], subset=['Status'])\
                    .set_properties(**{'text-align': 'left'})\
                    .set_table_styles([
                        {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'left')]},
                        {'selector': 'td', 'props': [('padding', '5px')]},
                    ])

            styled_df = style_dataframe(df)

            st.markdown("<h3 class='sub-header'>🔍 Job Overview</h3>", unsafe_allow_html=True)
            # Display the styled DataFrame without index
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            # Allow users to view details of a specific job
            st.markdown("<h3 class='sub-header'>📋 Job Details</h3>", unsafe_allow_html=True)
            selected_job_id = st.selectbox("🔎 Select a job to view details:", df['Job ID'].tolist())
            if selected_job_id:
                job = next(job for job in jobs if job['id'] == selected_job_id)
                
                # Display key information
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🔗 GitHub URL:** [{job['github_url']}]({job['github_url']})")
                    st.markdown(f"**👤 Author:** {job['author']}")
                with col2:
                    st.markdown(f"**🏷️ Version:** {job['version']}")
                    st.markdown(f"**🚦 Status:** {job['status']}")

                st.markdown(f"**📝 Description:** {job['description']}")

                # Display the entire job JSON
                with st.expander("🔍 Raw JSON Data", expanded=False):
                    st.json(job)

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Error fetching jobs: {str(e)}")
        logger.error(f"Error fetching jobs: {str(e)}", exc_info=True)

if __name__ == "__main__":
    main()