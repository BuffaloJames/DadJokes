import difflib
import re

def normalize_text(text):
    """Lowercase and remove punctuation from text."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    text = re.sub(r'\s+', ' ', text).strip() # Normalize whitespace
    return text

def remove_duplicate_jokes(jokes_list, fuzzy_threshold=0.9):
    """
    Removes duplicate jokes from a list, merging categories.

    Args:
        jokes_list: A list of joke dictionaries. 
                    Each dict is expected to have 'id', 'text', and 'categories'.
        fuzzy_threshold: Similarity threshold for fuzzy matching (0.0 to 1.0).

    Returns:
        A new list of unique joke dictionaries with merged categories.
    """
    if not jokes_list:
        return []

    unique_jokes = []
    # Store normalized text of jokes already added to unique_jokes to avoid re-normalizing
    normalized_unique_texts = [] 

    for joke in jokes_list:
        if not isinstance(joke, dict) or "text" not in joke or "categories" not in joke or "id" not in joke:
            # Skip malformed joke entries, or handle as an error
            print(f"Skipping malformed joke: {joke}")
            continue

        normalized_current_joke_text = normalize_text(joke["text"])
        is_duplicate = False
        
        for i, unique_joke in enumerate(unique_jokes):
            # Compare with normalized text of already added unique jokes
            # No need to re-normalize unique_joke["text"] if we store them
            
            # Using normalized_unique_texts[i] which should correspond to unique_joke
            similarity = difflib.SequenceMatcher(None, normalized_current_joke_text, normalized_unique_texts[i]).ratio()
            
            if similarity >= fuzzy_threshold:
                is_duplicate = True
                # Merge categories: add categories from current joke to the existing unique joke
                # Ensure categories in the unique_joke remain unique
                existing_categories = set(unique_joke["categories"])
                for cat in joke["categories"]:
                    existing_categories.add(cat)
                unique_jokes[i]["categories"] = sorted(list(existing_categories)) # Keep it sorted
                break 
                
        if not is_duplicate:
            unique_jokes.append(joke.copy()) # Add a copy to avoid modifying original list items directly
            normalized_unique_texts.append(normalized_current_joke_text) # Store its normalized form

    return unique_jokes
