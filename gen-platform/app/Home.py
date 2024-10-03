import streamlit as st
import logging
import importlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_page(page_name):
    try:
        module = importlib.import_module(f"{page_name.split('/')[0]}.{page_name.split('/')[1]}")
        return getattr(module, "main")
    except Exception as e:
        logger.error(f"Error loading page {page_name}: {str(e)}")
        return None

def home():
    """
    Function to render the home page content of the GenSphere Platform.
    """
    logger.info("Rendering Home page content")

    st.markdown("<h1 class='main-header'>🌐 Welcome to GenSphere!</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>A Hugging Face for AI Agents</p>", unsafe_allow_html=True)

    st.markdown("---")

    st.write("""
    As fellow AI engineers, we felt frustrated by having to re-invent the wheel every time we needed to build something. 
    From agents that can gather data from Yahoo Finance and summarize findings about a public company to agents that can 
    scrape LinkedIn and build a short-list of potential target clients.
    """)

    st.write("""
    It seemed very likely that someone else might have already gone through this hassle. 
    So, what if they could just package and share that? It would save tons of hours 
    of work and make it easier to leverage true expertise from different practitioners.
    """)

    st.markdown("---")

    st.markdown("<h2 class='sub-header'>What is an AI Agent?</h2>", unsafe_allow_html=True)

    st.write("""
    To simply put, agents can be described as a group of tasks that can be sequenced in different ways to solve a problem. 
    These tasks can be anything, but they usually fall into 3 common building blocks: Python functions, LLM calls and other agentic workflows:
    """)

    st.markdown("""
        <figure>
            <img src="app/static/images/agent.png" alt="Agent building blocks" class="small-image">
            <figcaption style="text-align: center;">Agent building blocks</figcaption>
        </figure>
    """, unsafe_allow_html=True)

    st.write("""
    We can think of these blocks as nodes in a graph, linked by edges that represent the sequence they should be executed:
    """)

    st.markdown("""
        <figure>
            <img src="app/static/images/graphs.png" alt="Agents as Graphs" class="small-image">
            <figcaption style="text-align: center;">Agents as Graphs</figcaption>
        </figure>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("<h2 class='sub-header'>Platform Overview</h2>", unsafe_allow_html=True)

    st.write("""
    GenSphere is a hub where developers can build, publish, share and use AI agents. You can quickly build your solution 
    by leveraging existing building blocks from the platform, no more doing it from scratch!
    """)

    # Adjust the image display
    st.markdown("""
        <figure>
            <img src="app/static/images/platform_diagram.png" alt="Platform Architecture" class="small-image-platform">
            <figcaption style="text-align: center;">Platform Architecture</figcaption>
        </figure>
    """, unsafe_allow_html=True)

    st.write("The platform is composed by different services:")

    services = [
        "🏠 **AI agent hub**: Find agents that perform tasks in a variety of segments",
        "🔗 **Agent as a Service (AaaS)**: Publish your agents as APIs through a 1-click deployment",
        "🛒 **Marketplace**: Easily monetize your agents without having to worry about hosting",
        "📊 **Leaderboard**: Compare agents and find the best fit for your need"
    ]

    for service in services:
        st.markdown(f"- {service}")

    st.write("User our open-source tools to get started:")

    tools = [
        "⚬⚬⚬ **gen-graph-sdk**: Python framework to build agentic workflows from first principles, build complex flows using simple blocks",
        "🔌 **gen-node-sdk**: Python framework to easily enable your existing agents (e.g., CrewAI, Autogen) to be published into the platform",
        "🖥️ **gen-cli**: a unified tool to interact with the platform through the terminal"
    ]

    for tool in tools:
        st.markdown(f"- {tool}")

    st.markdown("---")

    st.markdown("<h2 class='sub-header'>Foundational AI Agents Manifest</h2>", unsafe_allow_html=True)

    st.write("""
    Building agents is not an easy task, it's very easy to get caught up in the "my case is truly unique" mindset, 
    which can obfuscate eventual steps that could be generalized and reused in different workflows/contexts with minor adaptations. 
    We call these reusable blocks Foundational AI agents.
    """)
    
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

    st.markdown("<h2 class='sub-header'>Reach Out! We want to hear from you!</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='reach-out'>
        <p>🚀 Ready to revolutionize your AI workflow? We're just a message away!</p>
        <p>Whether you're looking to integrate our platform, contribute to our growing community, or just want to geek out about AI, we'd love to hear from you.</p>
        <p>Drop us a line at <a href="mailto:admin@gensphere.io">admin@gensphere.io</a>, connect with us on <a href="https://www.linkedin.com/company/gen-sphere" target="_blank">LinkedIn</a>, or join our <a href="https://www.reddit.com/r/GenSphere/" target="_blank">Reddit community</a>.</p>
        <p>Let's shape the future of AI together! 🌟</p>
    </div>
    """, unsafe_allow_html=True)

    logger.info("Home page content rendered successfully")
    
def main():
    """
    Main function to set up the GenSphere Platform page.
    """
    logger.info("Setting up GenSphere Platform page")

    st.set_page_config(
        page_title="GenSphere Platform",
        page_icon="🌐",
        layout="wide"
    )

    # Custom CSS for better styling, optimized for light mode
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
            background-color: #F0F8FF;
            border: 1px solid #E0E0E0;
            border-radius: 0.5rem;
            padding: 1rem;
            margin-bottom: 1rem;
            color: #1E1E1E;
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
        .stApp {
            background-color: white;
            color: black;
        }
        
        .small-image {
            max-width: 400px;
            width: 40%;
            margin: auto;
            display: block;
        }
                
        .small-image-platform {
            max-width: 400px;
            width: 60%;
            margin: auto;
            display: block;
        }
        
        .reach-out {
            background-color: #F0F8FF;
            border: 2px solid #4A90E2;
            border-radius: 1rem;
            padding: 1.5rem;
            margin-top: 2rem;
            color: #1E1E1E;
            text-align: center;
        }
        .reach-out p {
            margin-bottom: 1rem;
        }
        .reach-out a {
            color: #4A90E2;
            text-decoration: none;
            font-weight: bold;
        }
        .reach-out a:hover {
            text-decoration: underline;
        }
    </style>
    """, unsafe_allow_html=True)

    # Run the selected page
    pg.run()

    logger.info("GenSphere Platform page setup complete")

# Define your pages
create_node_page = st.Page(load_page("node_management/create_node"), url_path="create_node", title="Create Node", icon="➕")
node_agents_page = st.Page(load_page("node_management/node_agents"), url_path="node_agents", title="Node Agents", icon="🤖")
node_status_page = st.Page(load_page("node_management/node_status"), url_path="node_status", title="Node Status", icon="📋")
create_agent_page = st.Page(load_page("ai_agent/create_agent"), url_path="create_agent", title="Create Agent", icon="➕")
ai_agents_page = st.Page(load_page("ai_agent/ai_agents"), url_path="ai_agents", title="AI Agents", icon="🤖")
getting_started_page = st.Page(load_page("docs/getting_started"), url_path="getting_started", title="Getting Started", icon="📚")

# Set up navigation with section headers
pg = st.navigation({
    "Home": [st.Page(home, title="Home", icon="🏠")],
    "Node Management": [create_node_page, node_status_page, node_agents_page],
    "AI Agents": [create_agent_page, ai_agents_page],
    "Docs": [getting_started_page]
})

if __name__ == "__main__":
    main()