import requests
import os
from typing import Optional, Type
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class BookSearchInput(BaseModel):
    """Input for book search tool."""
    query: str = Field(description="Search query for books (title, author, or keywords)")


class BookSearchTool(BaseTool):
    """Tool for searching books using Google Books API."""

    name: str = "book_search"
    description: str = """
    Search for books using Google Books API. 
    Use this tool when users ask about specific books, authors, or want to find books by topic.
    Input should be a search query like book title, author name, or keywords.
    """
    args_schema: Type[BaseModel] = BookSearchInput

    def _run(self, query: str) -> str:
        """Execute the book search."""
        try:
            api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
            if not api_key:
                return "Google Books API key not configured."
            
            # Add language and country parameters to force English results
            url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}&maxResults=5&langRestrict=en"
            response = requests.get(url)
            data = response.json()
            
            if "items" not in data:
                return f"No books found for '{query}'"
            
            results = []
            for item in data["items"][:3]:  # Limit to top 3 results
                info = item["volumeInfo"]
                book_url = info.get("infoLink", "")
                thumbnail = info.get("imageLinks", {}).get("thumbnail", None)

                book_info = {
                    "title": info.get("title", "Unknown Title"),
                    "authors": ", ".join(info.get("authors", ["Unknown Author"])),
                    "published": info.get("publishedDate", "Unknown"),
                    "pages": info.get("pageCount", "Unknown"),
                    "categories": ", ".join(info.get("categories", ["Unknown"])),
                    "description": info.get("description", "No description available")[:200] + "...",
                    "url": book_url,
                    "thumbnail": thumbnail
                }

                result = f"""
**{book_info['title']}**
- Authors: {book_info['authors']}
- Published: {book_info['published']}
- Pages: {book_info['pages']}
- Categories: {book_info['categories']}
- Description: {book_info['description']}
- [Google Books Link]({book_info['url']})
"""
                if book_info["thumbnail"]:
                    result += f"- ![thumbnail]({book_info['thumbnail']})\n"
                results.append(result)
            
            return "\n".join(results)
        
        except Exception as e:
            return f"Error searching for books: {str(e)}"

    async def _arun(self, query: str) -> str:
        """Async version - not implemented for this simple tool."""
        return self._run(query)