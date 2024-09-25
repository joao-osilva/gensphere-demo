import streamlit as st

st.set_page_config(
    page_title="GenSphere Platform",
    page_icon="🌐",
    layout="wide"
)

# Custom CSS for better styling, including dark mode support
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 2rem;
        color: #50C878;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .tagline {
        font-size: 1.5rem;
        color: #FF6B6B;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .principle {
        background-color: rgba(240, 248, 255, 0.1);
        border: 1px solid rgba(240, 248, 255, 0.2);
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .principle-number {
        font-size: 1.2rem;
        font-weight: bold;
        color: #4A90E2;
    }
    .principle-title {
        font-size: 1.1rem;
        font-weight: bold;
        color: #50C878;
    }
    .stApp.light .principle {
        color: #1E1E1E;
    }
    .stApp.dark .principle {
        color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🌐 Welcome to GenSphere Platform!</h1>", unsafe_allow_html=True)
st.markdown("<p class='tagline'>A Hugging Face for AI Agents</p>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<h2 class='sub-header'>Foundational AI Agents Manifest</h2>", unsafe_allow_html=True)

st.write("""
Foundational AI agents are built with the purpose to reduce effort duplication, increase knowledge sharing, 
and unlock a more composable approach to complex AI systems. A set of core design principles can be used to 
steer its implementation:
""")

principles = [
    ("Bounded context", "Single responsibility enables finer-grained and decoupled solutions with more deterministic outcomes"),
    ("Accessible as a service", "Functionalities exposed as services (API) allows easier consumption, hiding implementation details, dependencies and complexities"),
    ("Testable and measurable", "Standardized input/output schema and task decomposition into smaller goals bring order to the chaos and quantifiable progress"),
    ("Built for reuse", "Modularity increases reusability by enabling composition, which can drastically decrease time-to-market")
]

for i, (title, description) in enumerate(principles, 1):
    st.markdown(f"""
    <div class='principle'>
        <span class='principle-number'>{i}.</span> <span class='principle-title'>{title}:</span> {description}
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<h2 class='sub-header'>Get Started</h2>

Explore our AI agents repository and learn how to integrate these powerful tools into your projects. 
Navigate through the pages to discover more about GenSphere Platform and its capabilities.
""", unsafe_allow_html=True)

# You can add more sections or interactive elements here as needed
