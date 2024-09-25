import streamlit as st

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
"""         )