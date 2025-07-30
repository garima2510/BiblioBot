# 📚 BiblioBot - Book Information Chatbot

A Python-based chatbot that helps users find book information and answer questions about books using Azure OpenAI and Google Books API.

## Features

- 🔍 **Book Search**: Search for books by title or author using Google Books API
- 💬 **AI Chat**: Ask natural language questions about books, authors, genres, and ratings
- 🎨 **User-Friendly UI**: Clean Streamlit interface
- 🔐 **Secure**: Environment variables for API key management

## Setup Instructions

### 1. Clone and Setup Environment

```pwsh
# Navigate to project directory
cd c:\_Garima\Projects\BiblioBot

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure API Keys

1. Copy `.env.template` to `.env`
2. Fill in your API credentials:
   - **Google Books API**: Get from [Google Cloud Console](https://console.cloud.google.com/)
   - **Azure OpenAI**: Get from [Azure Portal](https://portal.azure.com/)

```bash
GOOGLE_BOOKS_API_KEY=your_actual_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your_actual_azure_key
AZURE_OPENAI_MODEL=gpt-35-turbo
```

### 3. Run the Application

```pwsh
streamlit run app.py
```

## Usage Examples

### Book Search
- "The Hobbit"
- "Stephen King"
- "Harry Potter"

### AI Questions
- "Who wrote Dune?"
- "What is the Goodreads rating for The Hobbit?"
- "Tell me about sci-fi books from the 1980s"
- "What are some books similar to 1984?"

## Next Steps

This is Step 1 & 2 of a larger project. Future enhancements will include:
- Semantic search capabilities
- AI agents for complex queries
- Semantic Kernel integration
- Caching for better performance
- Azure deployment

## Contributing

This is a learning project. Feel free to fork and experiment!

## License

MIT License
