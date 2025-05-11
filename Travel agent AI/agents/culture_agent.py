import wikipedia
from typing import Optional, Tuple

def get_country_culture(country_name: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Fetch a summary about the culture of a given country from Wikipedia.
    
    Args:
        country_name (str): Name of the country to search for
        
    Returns:
        Tuple[Optional[str], Optional[str]]: A tuple containing:
            - The cultural summary (or None if not found)
            - Error message (or None if successful)
    """
    try:
        # Set language to English
        wikipedia.set_lang("en")
        
        # Search for the country page
        search_results = wikipedia.search(f"{country_name} culture", results=1)
        
        if not search_results:
            return None, f"No Wikipedia page found for {country_name}'s culture"
            
        # Get the page
        page = wikipedia.page(search_results[0], auto_suggest=False)
        
        # Get the summary
        summary = wikipedia.summary(search_results[0], sentences=3)
        
        return summary, None
        
    except wikipedia.DisambiguationError as e:
        # Handle disambiguation pages
        options = e.options[:3]  # Get first 3 options
        return None, f"Multiple matches found. Please be more specific. Options: {', '.join(options)}"
        
    except wikipedia.PageError:
        return None, f"Could not find a Wikipedia page for {country_name}'s culture"
        
    except Exception as e:
        return None, f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Test the function
    country = "Japan"
    summary, error = get_country_culture(country)
    
    if error:
        print(f"Error: {error}")
    else:
        print(f"Cultural summary for {country}:")
        print(summary)
