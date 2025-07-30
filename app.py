import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from prompt_template import biblio_prompt
from tools import BookSearchTool

# Load environment variables
load_dotenv()

st.title("📚 BiblioBot - Your AI Book Assistant")
st.markdown("*Ask me anything about books! I can search for books, provide recommendations, and answer questions.*")

# Sidebar for configuration status
with st.sidebar:
    st.header("Configuration Status")
    google_key = os.getenv("GOOGLE_BOOKS_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    azure_key = os.getenv("AZURE_OPENAI_KEY")
    azure_model = os.getenv("AZURE_OPENAI_MODEL")
    
    st.write("📖 Google Books API:", "✅" if google_key else "❌")
    st.write("🤖 Azure OpenAI:", "✅" if all([azure_endpoint, azure_key, azure_model]) else "❌")
    
    if not all([google_key, azure_endpoint, azure_key, azure_model]):
        st.warning("Please configure your API keys in the .env file")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize LangChain Agent
@st.cache_resource
def initialize_agent():
    """Initialize the LangChain agent with tools."""
    try:
        # Initialize Azure OpenAI
        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_KEY"),
            api_version=os.getenv("AZURE_OPENAI_VERSION", "2024-02-01"),
            azure_deployment=os.getenv("AZURE_OPENAI_MODEL"),
            temperature=0.7
        )
        
        # Initialize tools
        tools = [BookSearchTool()]
        
        # Create agent using imported prompt template
        agent = create_openai_tools_agent(llm, tools, biblio_prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
        
        return agent_executor
    
    except Exception as e:
        st.error(f"Failed to initialize agent: {str(e)}")
        return None

# Chat Interface
st.header("💬 Chat with BiblioBot")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input (this appears at the bottom of the page)
if prompt := st.chat_input("Ask me about books, authors, or get recommendations!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get agent response
    with st.chat_message("assistant"):
        with st.spinner("BiblioBot is thinking..."):
            try:
                agent_executor = initialize_agent()
                if agent_executor:
                    response = agent_executor.invoke({
                        "input": prompt,
                        "chat_history": st.session_state.messages[-10:]
                    })
                    assistant_response = response["output"]
                    st.markdown(assistant_response)
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                else:
                    st.error("Failed to initialize BiblioBot. Please check your configuration.")
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
    # Clear the input after sending
    #st.session_state["chat_input"] = ""

# Clear chat button
if st.sidebar.button("Clear Chat History"):
    st.session_state.messages = []
    st.rerun()

# Example queries
with st.sidebar:
    st.header("Example Queries")
    st.markdown("""
    Try asking:
    - "Find me books by Stephen King"
    - "What's the Goodreads rating for Dune?"
    - "Recommend sci-fi books from the 1980s"
    - "Tell me about The Hobbit"
    - "Find fantasy books for beginners"
    """)

# Footer
st.divider()
st.markdown("*BiblioBot v2.0 - Powered by LangChain, Azure OpenAI, and Google Books API*")
