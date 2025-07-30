import streamlit as st
import requests
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("📚 BiblioBot - Your Book Information Assistant")
st.markdown("*Find book information and ask questions about books using AI*")

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

# Basic Book Search Section
st.header("🔍 Search for Books")
book_query = st.text_input("Enter a book title or author:", placeholder="e.g., The Hobbit, Stephen King")

if book_query and os.getenv("GOOGLE_BOOKS_API_KEY"):
    with st.spinner("Searching for books..."):
        try:
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
            url = f"https://www.googleapis.com/books/v1/volumes?q={book_query}&key={api_key}&maxResults=5"
            resp = requests.get(url)
            data = resp.json()
            
            if "items" in data:
                st.success(f"Found {len(data['items'])} results:")
                for i, item in enumerate(data["items"][:3], 1):
                    info = item["volumeInfo"]
                    
                    with st.expander(f"📖 {info.get('title', 'No Title')}"):
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            # Display thumbnail if available
                            if "imageLinks" in info and "thumbnail" in info["imageLinks"]:
                                st.image(info["imageLinks"]["thumbnail"], width=120)
                        
                        with col2:
                            st.write("**Authors:**", ", ".join(info.get("authors", ["Unknown"])))
                            st.write("**Published:**", info.get("publishedDate", "Unknown"))
                            if "categories" in info:
                                st.write("**Categories:**", ", ".join(info["categories"]))
                            if "pageCount" in info:
                                st.write("**Pages:**", info["pageCount"])
                        
                        # Description
                        description = info.get("description", "No description available")
                        if len(description) > 300:
                            description = description[:300] + "..."
                        st.write("**Description:**", description)
            else:
                st.warning("No results found. Try a different search term.")
        except Exception as e:
            st.error(f"Error searching books: {str(e)}")
elif book_query and not os.getenv("GOOGLE_BOOKS_API_KEY"):
    st.error("Google Books API key not configured. Please add it to your .env file.")

# Divider
st.divider()

# Natural Language Query Section
st.header("💬 Ask BiblioBot Anything")
st.markdown("Ask questions in natural language about books, authors, genres, or even Goodreads ratings!")

user_question = st.text_input(
    "Your question:", 
    placeholder="e.g., Who wrote Dune? What is the Goodreads rating for The Hobbit? Tell me about sci-fi books."
)

if user_question and all([os.getenv("AZURE_OPENAI_ENDPOINT"), os.getenv("AZURE_OPENAI_KEY"), os.getenv("AZURE_OPENAI_MODEL")]):
    with st.spinner("BiblioBot is thinking..."):
        try:
            # Initialize Azure OpenAI client
            client = AzureOpenAI(
                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                api_key=os.getenv("AZURE_OPENAI_KEY"),
                api_version=os.getenv("AZURE_OPENAI_VERSION")
            )

            response = client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_MODEL"),
                messages=[
                    {
                        "role": "system", 
                        "content": """You are BiblioBot, a helpful assistant specializing in book information. 
                        You have extensive knowledge about books, authors, genres, publication dates, and literary analysis.
                        When asked for Goodreads ratings or reviews, provide information based on your knowledge.
                        Be conversational, informative, and enthusiastic about books.
                        If you don't know something specific, be honest about it."""
                    },
                    {"role": "user", "content": user_question}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            # Display response in a nice format
            st.markdown("### 🤖 BiblioBot's Response:")
            st.markdown(response.choices[0].message.content)
            
        except Exception as e:
            st.error(f"Error getting AI response: {str(e)}")
            st.info("Please check your Azure OpenAI configuration in the .env file.")
            
elif user_question and not all([os.getenv("AZURE_OPENAI_ENDPOINT"), os.getenv("AZURE_OPENAI_KEY"), os.getenv("AZURE_OPENAI_MODEL")]):
    st.error("Azure OpenAI not configured. Please add your credentials to the .env file.")

# Footer
st.divider()
st.markdown("---")
st.markdown("*BiblioBot v1.0 - Powered by Google Books API and Azure OpenAI*")
