import os
from typing import List
from unittest import result
from urllib import response
from dotenv import load_dotenv
from tavily import TavilyClient

load_dotenv()

client = TavilyClient(api_key= os.getenv("TAVILY_API_KEY"))

def search(query : str, max_results : int = 5):
    
    try:
        
        response = client.search(query=query, max_results= max_results,search_depth="advanced")
        
        results = response.get("results", [])
        
        if not results:
            return "No results were found"
        
        formatted_results = []
        
        for result in results:
            
            formatted_results.append(
                f"Source: {result.get('url', 'unknown')}\n"
                f"Title: {result.get('title', '')}\n"
                f"Content: {result.get('content', '')}\n"   
            )
            
            return "\n---\n".join(formatted_results)
        
    except Exception as e:
        return f"Search failed : {str(e)}"
    
    
def search_multiple_queries(queries: List[str]):
    
    results = {}
    for query in queries:
        result = search(query)
        results[query] = result
        
    return results
        