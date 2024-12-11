import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def search_domains(query, **kwargs):
    url = "https://domainr.p.rapidapi.com/v2/search"
    
    headers = {
        "x-rapidapi-key": os.getenv('RAPIDAPI_KEY'),
        "x-rapidapi-host": os.getenv('RAPIDAPI_HOST')
    }
    
    # Base params with query
    params = {"query": query}
    
    # Add optional parameters if provided
    optional_params = ['defaults', 'registrar', 'location']
    for param in optional_params:
        if param in kwargs and kwargs[param]:
            params[param] = kwargs[param]
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def main():
    # Example search with no optional parameters
    results = search_domains("takin")
    
    if results:
        print("Domain Search Results:")
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
