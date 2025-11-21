# search_tool.py - mock search tool returning curated links or performing HTTP searches if configured.
import os, requests

def search(query, top_k=5):
    # If a real SEARCH_API_KEY provided, implement web lookup here.
    # For demo we return curated results.
    results = [
        {'title': 'Free Frontend Course - Example', 'url': 'https://example.com/frontend', 'snippet': 'A beginner-friendly frontend course.'},
        {'title': 'Top DSA Course - Example', 'url': 'https://example.com/dsa', 'snippet': 'Learn data structures.'},
    ]
    return results[:top_k]
