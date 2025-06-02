#Favorites
#Updated 4/21/2025

import difflib
import re
import json
import os
import subprocess

FAVORITES_FILE = "favorites.json"

# Load jokes from file (prioritize cleaned file)
def load_jokes():
    path = "/Users/jamesalcorn/Documents/Jupyter/Dadjokes/cleaned_dadjokeslist.txt" if os.path.exists("/Users/jamesalcorn/Documents/Jupyter/Dadjokes/cleaned_dadjokeslist.txt") else "/Users/jamesalcorn/Documents/Jupyter/Dadjokes/dadjokeslist.txt"
    jokes = []
    with open(path, 'r') as f:
        for line in f:
            parts = line.strip().split("%%")
            text = parts[0].strip()
            categories = [p.strip() for p in parts[1:]]
            jokes.append({"text": text, "categories": categories})
    return jokes

# Normalize joke for comparison (ignore punctuation, casing)
def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

# Remove exact and fuzzy duplicates, preserving categories
def remove_duplicates(jokes, fuzzy_threshold=0.9):
    seen = []
    cleaned = []
    for joke in jokes:
        norm_joke = normalize(joke["text"])
        is_duplicate = False

        for seen_joke in seen:
            ratio = difflib.SequenceMatcher(None, norm_joke, seen_joke["norm"]).ratio()
            if ratio >= fuzzy_threshold:
                # Merge categories if found duplicate
                seen_joke["joke"]["categories"] = list(set(seen_joke["joke"]["categories"] + joke["categories"]))
                is_duplicate = True
                break

        if not is_duplicate:
            seen.append({"norm": norm_joke, "joke": joke})
            cleaned.append(joke)

    return cleaned

# Save cleaned jokes
def save_jokes(jokes, filename):
    with open(filename, 'w') as f:
        for joke in jokes:
            line = joke["text"]
            for cat in joke["categories"]:
                line += f" %%{cat}"
            f.write(line + '\n')

# Persistent favorites management
def load_favorites():
    if not os.path.exists(FAVORITES_FILE):
        return []
    with open(FAVORITES_FILE, "r") as f:
        return json.load(f)

def save_favorites(favorites):
    with open(FAVORITES_FILE, "w") as f:
        json.dump(favorites, f, indent=2)

def add_to_favorites(joke):
    favorites = load_favorites()
    if not any(j["text"] == joke["text"] for j in favorites):
        favorites.append(joke)
        save_favorites(favorites)
        print(f"⭐ Added to favorites: {joke['text'][:60]}...")
    else:
        print(f"✅ Already a favorite: {joke['text'][:60]}...")

# Run deduplication process externally
def run_deduplication_script():
    jokes = load_jokes()
    cleaned_jokes = remove_duplicates(jokes, fuzzy_threshold=0.9)
    save_jokes(cleaned_jokes, 'cleaned_dadjokeslist.txt')
    print(f"✅ Deduplication complete: {len(jokes) - len(cleaned_jokes)} total duplicates removed (exact + fuzzy).")
