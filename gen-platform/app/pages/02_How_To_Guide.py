import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to render the How-To Guide page.
    """
    logger.info("Rendering How-To Guide page")

    st.set_page_config(page_title="GenSphere - How-To Guide", page_icon="📚")

    st.title("How to Use GenSphere Platform CLI")

    st.markdown("""
    ## Building an Image

    To build a new AI agent image:

    ```bash
    gen-cli build <path_to_dockerfile> -t <repository_name>:<tag>
    ```

    ## Running an Image

    To run an AI agent image:

    ```bash
    gen-cli run <repository_name>:<tag>
    ```
    """)

    logger.info("How-To Guide page rendered successfully")

if __name__ == "__main__":
    main()