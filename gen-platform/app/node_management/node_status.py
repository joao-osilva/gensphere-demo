import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def main():
    st.title("Jobs")

    # Add a refresh button
    if st.button("Refresh Jobs"):
        st.rerun()

    try:
        response = requests.get("http://jobs_service:8001/jobs", timeout=10)
        response.raise_for_status()
        jobs = response.json()

        if not jobs:
            st.info("No jobs found.")
        else:
            # Convert jobs to a DataFrame for easier display
            df = pd.DataFrame(jobs)
            
            # Select and rename columns
            df = df[['id', 'github_url', 'author', 'status']]
            df.columns = ['Job ID', 'GitHub URL', 'Author', 'Status']

            # Style the DataFrame
            def style_dataframe(df):
                return df.style.apply(lambda x: ['background-color: #90EE90' if v == 'DONE' else 'background-color: #FFB3BA' for v in x], subset=['Status'])\
                    .set_properties(**{'text-align': 'left'})\
                    .set_table_styles([
                        {'selector': 'th', 'props': [('font-weight', 'bold'), ('text-align', 'left')]},
                        {'selector': 'td', 'props': [('padding', '5px')]},
                    ])

            styled_df = style_dataframe(df)

            # Display the styled DataFrame without index
            st.dataframe(styled_df, use_container_width=True, hide_index=True)

            # Allow users to view details of a specific job
            selected_job_id = st.selectbox("Select a job to view details:", df['Job ID'].tolist())
            if selected_job_id:
                job = next(job for job in jobs if job['id'] == selected_job_id)
                
                # Display the entire job JSON
                with st.expander("Raw JSON Data", expanded=True):
                    st.json(job)

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching jobs: {str(e)}")

if __name__ == "__main__":
    main()