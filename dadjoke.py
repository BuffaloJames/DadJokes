#Main dad joke app
#Updated 4/21/2025

# === Imports and Setup ===
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
from datetime import datetime, timedelta
import random, os, json
import re
import pyttsx3
import difflib
from joke_charts import plot_category_counts, plot_reaction_scores
from admin_panel import open_admin_panel


engine = pyttsx3.init()
engine.setProperty('rate', 150)

FAVORITES_FILE = "favorites.json"

# === Joke Loading & Deduplication ===
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

def load_reactions():
    if not os.path.exists("joke_reactions.json"):
        return {}
    with open("joke_reactions.json", "r") as f:
        return json.load(f)

def normalize(text):
    return re.sub(r'[^a-z0-9]', '', text.lower())

def remove_duplicates(jokes, fuzzy_threshold=0.9):
    seen = []
    cleaned = []
    for joke in jokes:
        norm_joke = normalize(joke["text"])
        is_duplicate = False
        for seen_joke in seen:
            ratio = difflib.SequenceMatcher(None, norm_joke, seen_joke["norm"]).ratio()
            if ratio >= fuzzy_threshold:
                seen_joke["joke"]["categories"] = list(set(seen_joke["joke"]["categories"] + joke["categories"]))
                is_duplicate = True
                break
        if not is_duplicate:
            seen.append({"norm": norm_joke, "joke": joke})
            cleaned.append(joke)
    return cleaned

def save_jokes(jokes, filename):
    with open(filename, 'w') as f:
        for joke in jokes:
            line = joke["text"]
            for cat in joke["categories"]:
                line += f" %%{cat}"
            f.write(line + '\n')

def run_deduplication_script():
    jokes = load_jokes()
    cleaned_jokes = remove_duplicates(jokes)
    save_jokes(cleaned_jokes, 'cleaned_dadjokeslist.txt')
    messagebox.showinfo("Deduplication Complete", f"{len(jokes) - len(cleaned_jokes)} duplicates removed.")

# === Favorites Persistence ===
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

# --- Seasonal Joke Calculations ---
def calculate_easter(year):
    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1
    return datetime(year, month, day)

def calculate_thanksgiving(year):
    # Fourth Thursday of November
    november = datetime(year, 11, 1)
    # Find the first Thursday
    first_thursday = november + timedelta(days=(3 - november.weekday()) % 7)
    # Add 3 weeks to get the fourth Thursday
    return first_thursday + timedelta(weeks=3)

def calculate_election_day(year):
    # Election Day is the first Tuesday AFTER the first Monday in November.
    november_1st = datetime(year, 11, 1)

    # Find the weekday of November 1st (Monday=0, Sunday=6)
    weekday_nov1 = november_1st.weekday()

    # Calculate days needed to get to the first Monday.
    days_to_monday = (0 - weekday_nov1) % 7

    # Calculate the date of the first Monday
    first_monday = november_1st + timedelta(days=days_to_monday)

    # Election Day is the day after the first Monday (Tuesday)
    election_day = first_monday + timedelta(days=1)

    return election_day

def calculate_fathers_day(year):
    # Father's Day is the third Sunday of June.
    june_1st = datetime(year, 6, 1)
    weekday_june1 = june_1st.weekday()
    days_to_first_sunday = (6 - weekday_june1) % 7
    first_sunday = june_1st + timedelta(days=days_to_first_sunday)
    fathers_day = first_sunday + timedelta(weeks=2)
    return fathers_day

def calculate_mothers_day(year):
    # Mother's Day is the second Sunday of May.
    may_1st = datetime(year, 5, 1)
    weekday_may1 = may_1st.weekday()
    days_to_first_sunday = (6 - weekday_may1) % 7
    first_sunday = may_1st + timedelta(days=days_to_first_sunday)
    mothers_day = first_sunday + timedelta(weeks=1)
    return mothers_day

def calculate_presidents_day(year):
    # Presidents' Day is the third Monday of February.
    february_1st = datetime(year, 2, 1)
    weekday_feb1 = february_1st.weekday()
    days_to_first_monday = (0 - weekday_feb1) % 7
    first_monday = february_1st + timedelta(days=days_to_first_monday)
    presidents_day = first_monday + timedelta(weeks=2)
    return presidents_day

def calculate_mardi_gras(year):
    # Mardi Gras (Fat Tuesday) is 47 days before Easter.
    easter_date = calculate_easter(year)
    mardi_gras = easter_date - timedelta(days=47)
    return mardi_gras

def get_seasonal_events():
    today = datetime.today()
    year = today.year
    return {
        
        "New Years": datetime(year, 1, 1),        
        "Groundhog Day": datetime(year, 2, 2),
        "Valentine's Day": datetime(year, 2, 14),
        "Birthday": datetime(year, 3, 4),
        "Pi Day": datetime(year, 3, 14),
        "St. Patrick’s day": datetime(year, 3, 17),
        "April Fools": datetime(year, 4, 1),
        "Earth Day": datetime(year, 4, 22),
        "Arbor Day": datetime(year, 4, 26), # Typically last Friday in April, can adjust logic if needed
        "Star Wars": datetime(year, 5, 4),
        "Cinco de Mayo": datetime(year, 5, 5),
        "Birthday": datetime(year, 6, 25),
        "Fourth of July": datetime(year, 7, 4),
        "Birthday": datetime(year, 8, 21),
        "Pirate": datetime(year, 9, 19),
        "Halloween": datetime(year, 10, 31),
        "Christmas": datetime(year, 12, 25),
        "Easter": calculate_easter(year),
        "Fathers Day": calculate_fathers_day(year),
        "Mothers Day": calculate_mothers_day(year),
        "Election": calculate_election_day(year),
        "Thanksgiving": calculate_thanksgiving(year),
        "Mardi Gras": calculate_mardi_gras(year),
        "Presidents' Day": calculate_presidents_day(year),
    }

def get_nearby_event():
    today = datetime.today()
    events = get_seasonal_events()
    for name, date in events.items():
        if abs((date - today).days) <= 7:
            return name
    return None

# === Joke Selection Logic ===
jokes = load_jokes()
shown_jokes = set()
theme = {"bg": "#f0f0f0", "fg": "black", "button": "lightblue"}


def get_random_joke():
    remaining = [j for j in jokes if j["text"] not in shown_jokes]
    if not remaining:
        shown_jokes.clear()
        remaining = jokes
    joke = random.choice(remaining)
    shown_jokes.add(joke["text"])
    return joke

def get_joke_by_category(cat):
    filtered = [j for j in jokes if cat in j["categories"]]
    return random.choice(filtered) if filtered else None

# === GUI Setup ===
root = tk.Tk()
root.title("Dad Joke Generator")
root.geometry("500x600")

joke_text = tk.StringVar()
cat_label_var = tk.StringVar()
current_joke = {}

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def show_joke(joke):
    if not joke:
        messagebox.showinfo("Oops!", "No joke found!")
        return
    joke_text.set(joke["text"])
    current_joke["joke"] = joke
    cat_label_var.set("Categories: " + ", ".join(joke["categories"]))
    speak(joke["text"])

def react_to_joke(reaction):
    joke = current_joke.get("joke")
    if joke and reaction == "Funny":
        add_to_favorites(joke)
        messagebox.showinfo("Reaction Recorded", "Added to favorites!")
    elif joke:
        messagebox.showinfo("Reaction Recorded", f"You reacted: {reaction}")

# === Main Widgets ===

joke_label = tk.Label(root, textvariable=joke_text, wraplength=400, bg=theme["bg"], fg=theme["fg"],font=("Helvetica", 16))
joke_label.pack(pady=10)

cat_label = tk.Label(root, textvariable=cat_label_var, bg=theme["bg"], fg=theme["fg"])
cat_label.pack()

# create a horizontal separator
separator = ttk.Separator(root, orient=tk.HORIZONTAL)
separator.pack(side=tk.TOP, fill=tk.X, pady=5)

    # == category dropdown ==
def get_all_categories():
    cats = set()
    for joke in jokes:
        cats.update(joke["categories"])
    return sorted(cats)
    
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var)
category_dropdown['values'] = get_all_categories()
category_dropdown.pack(pady=5)

tk.Button(root, text="Get Joke from Category", command=lambda: show_joke(get_joke_by_category(category_var.get())), bg=theme["button"]).pack(pady=3)

# create a horizontal separator
separator = ttk.Separator(root, orient=tk.HORIZONTAL)
separator.pack(side=tk.TOP, fill=tk.X, pady=5)

    #search function ==
search_entry = tk.Entry(root)
search_entry.pack(pady=3)

def search_jokes():
    term = search_entry.get().lower()
    results = [j for j in jokes if term in j["text"].lower() or any(term in c.lower() for c in j["categories"])]
    if results:
        show_joke(random.choice(results))
    else:
        messagebox.showinfo("Search", "No jokes matched your search.")

tk.Button(root, text="Search", command=search_jokes, bg=theme["button"]).pack(pady=2)

# create a horizontal separator
separator = ttk.Separator(root, orient=tk.HORIZONTAL)
separator.pack(side=tk.TOP, fill=tk.X, pady=5)


tk.Button(root, text="Random Joke", command=lambda: show_joke(get_random_joke())).pack(pady=5)
tk.Button(root, text="Seasonal Joke", command=lambda: show_joke(get_seasonal_joke()), bg=theme["button"]).pack(pady=5)


# === Reaction Buttons ===
reaction_frame = tk.Frame(root)
reaction_frame.pack(pady=5)
tk.Button(reaction_frame, text="😆 Funny", command=lambda: react_to_joke("Funny")).pack(side="left", padx=5)
tk.Button(reaction_frame, text="🤔 Huh?", command=lambda: react_to_joke("Confused")).pack(side="left", padx=5)
tk.Button(reaction_frame, text="🙄 So Bad", command=lambda: react_to_joke("Bad")).pack(side="left", padx=5)

# === Joke Sharing Functions ===
import webbrowser
import urllib.parse

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Required on macOS
    messagebox.showinfo("Copied", "Joke copied to clipboard!")

def export_joke_to_file(text):
    with open("shared_joke.txt", "w") as f:
        f.write(text)
    messagebox.showinfo("Exported", "Joke saved to shared_joke.txt!")

def email_joke(text):
    subject = urllib.parse.quote("Check out this Dad Joke!")
    body = urllib.parse.quote(text)
    mailto_link = f"mailto:?subject={subject}&body={body}"
    webbrowser.open(mailto_link)

# === Sharing Buttons ===

share_frame = tk.Frame(root)
share_frame.pack(pady=5)

tk.Button(share_frame, text="📋 Copy", command=lambda: copy_to_clipboard(joke_text.get())).pack(side="left", padx=5)
tk.Button(share_frame, text="💾 Export", command=lambda: export_joke_to_file(joke_text.get())).pack(side="left", padx=5)
tk.Button(share_frame, text="✉️ Email", command=lambda: email_joke(joke_text.get())).pack(side="left", padx=5)


# === View Favorites ===
def show_favorites():
    favs = load_favorites()
    if not favs:
        messagebox.showinfo("Favorites", "No favorites yet!")
        return
    fav_text = "\n\n".join(j["text"] for j in favs)
    messagebox.showinfo("Favorites", fav_text)

tk.Button(root, text="View Favorites", command=show_favorites).pack(pady=5)

# == Admin Panel ==

def launch_admin_panel():
    try:
        messagebox.showinfo("Debug", "Launching admin panel...")

        jokes_data = load_jokes()
        reactions = load_reactions()

        open_admin_panel(
            jokes=jokes_data,
            reactions=reactions,
            save_jokes_callback=lambda jokes: save_jokes(jokes, "cleaned_dadjokeslist.txt"),
            run_deduplication_callback=run_deduplication_script
        )
    except Exception as e:
        messagebox.showerror("Error", f"Admin panel launch failed:\n{e}")




tk.Button(root, text="Admin Panel", command=launch_admin_panel, bg=theme["button"]).pack(pady=5)




# === Exit Button ===
def on_exit():
    goodbye = get_joke_by_category("Goodbye")
    if goodbye:
        speak(goodbye["text"])
    root.destroy()

tk.Button(root, text="Close", command=on_exit).pack(pady=5)

show_joke({"text": "Welcome to the Dad Joke Generator!", "categories": []})
root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()
