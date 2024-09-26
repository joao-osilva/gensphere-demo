import streamlit as st
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Main function to render the home page of the GenSphere Platform.
    """
    logger.info("Rendering Home page")

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

    st.markdown("<h1 class='main-header'>🌐 Welcome to GenSphere!</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>A Hugging Face for AI Agents</p>", unsafe_allow_html=True)

    st.markdown("---")

    # New section: Platform Architecture and Components
    st.markdown("<h2 class='sub-header'>Platform Architecture and Components</h2>", unsafe_allow_html=True)

    st.write("""
    We are a hub where developers can build, publish, share and use AI agents. You can quickly build your solution 
    by leveraging existing building blocks from the platform, no more doing it from scratch!
    """)

    #st.image("../imgs/platform_diagram.svg", caption="Platform Architecture Diagram", use_column_width=True)

    st.write("Our platform is composed by different services:")

    services = [
        "**AI agent hub**: Find agents that perform tasks in a variety of segments",
        "**Agent as a Service (AaaS)**: Publish your agents as APIs through a 1-click deployment",
        "**Marketplace**: Easily monetize your agents without having to worry about hosting",
        "**Leaderboard**: Compare agents and find the best fit for your need"
    ]

    for service in services:
        st.markdown(f"- {service}")

    st.write("You can get started by using our open-source tools:")

    tools = [
        "**gen-flow-sdk**: Python framework to build agentic workflows from first principles, build complex flows using simple blocks",
        "**gen-pod-sdk**: Python framework to easily enable your existing agents (e.g., CrewAI, Autogen) to be published into the platform",
        "**gen-cli**: a unified tool to interact with the platform through the terminal"
    ]

    for tool in tools:
        st.markdown(f"- {tool}")

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

    logger.info("Home page rendered successfully")

if __name__ == "__main__":
    main()
