import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
from datetime import datetime, timedelta
import random, os, re, json
import pyttsx3

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Load jokes from JSON file
def load_jokes(filename="jokes.json"):
    jokes = []
    if not os.path.exists(filename):
        # Create an empty jokes.json if it doesn't exist
        with open(filename, "w") as f:
            json.dump([], f)
        return jokes
    try:
        with open(filename, "r") as f:
            jokes = json.load(f)
    except json.JSONDecodeError:
        # Handle cases where the file is empty or malformed
        # You might want to log this error or create a default empty list
        with open(filename, "w") as f: # Overwrite/create with empty list
            json.dump([], f)
        return [] # Return empty list if decode error
    return jokes

def save_jokes(jokes, filename="jokes.json"):
    with open(filename, "w") as f:
        json.dump(jokes, f, indent=2)

# Load and save reactions
def load_reactions(filename="joke_reactions.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def save_reactions():
    with open("joke_reactions.json", "w") as f:
        json.dump(reactions, f, indent=2)

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
        "Christmas": datetime(year, 12, 25),
        "Halloween": datetime(year, 10, 31),
        "Valentine's Day": datetime(year, 2, 14),
        "April Fools": datetime(year, 4, 1),
        "Cinco de Mayo": datetime(year, 5, 5),
        "Easter": calculate_easter(year),
        "St. Patrick’s day": datetime(year, 3, 17),
        "Fourth of July": datetime(year, 7, 4),
        "New Years": datetime(year, 1, 1),
        "Birthday": datetime(year, 3, 4),
        "Birthday": datetime(year, 8, 21),
        "Birthday": datetime(year, 6, 25),
        "Star Wars": datetime(year, 5, 4),
        "Groundhog Day": datetime(year, 2, 2),
        "Fathers Day": calculate_fathers_day(year),
        "Mothers Day": calculate_mothers_day(year),
        "Election": calculate_election_day(year),
        "Thanksgiving": calculate_thanksgiving(year),
        "Pi Day": datetime(year, 3, 14),
        "Pirate": datetime(year, 9, 19),
        "Mardi Gras": calculate_mardi_gras(year),
        "Presidents' Day": calculate_presidents_day(year),
        "Earth Day": datetime(year, 4, 22),
        "Talk Like a Pirate Day": datetime(year, 9, 19), # Added for consistency
        "Arbor Day": datetime(year, 4, 26) # Typically last Friday in April, can adjust logic if needed
    }

def get_nearby_event():
    today = datetime.today()
    events = get_seasonal_events()
    for name, date in events.items():
        if abs((date - today).days) <= 7:
            return name
    return None

jokes = load_jokes()
favorites = []
shown_jokes = set()
theme = {"bg": "#f0f0f0", "fg": "black", "button": "lightblue"}
reactions = load_reactions()
current_joke = {} # To store the current joke object

# --- Joke selection functions with weighting ---
def get_joke_weight(joke):
    text = joke["text"]
    react = reactions.get(text, {"Funny": 0, "Confused": 0, "Bad": 0})
    return 1 + 3 * react.get("Funny", 0) + react.get("Confused", 0) - 2 * react.get("Bad", 0)

def get_random_joke():
    remaining = [j for j in jokes if j["text"] not in shown_jokes]
    if not remaining:
        shown_jokes.clear()
        remaining = jokes
    weighted = [(j, get_joke_weight(j)) for j in remaining]
    if not weighted:
        return random.choice(jokes) if jokes else None # Fallback if no reactions yet
    population, weights = zip(*weighted)
    joke = random.choices(population, weights=weights)[0]
    shown_jokes.add(joke["text"])
    return joke

def get_joke_by_category(cat):
    filtered = [j for j in jokes if cat in j["categories"]]
    if not filtered:
        return None
    weighted = [(j, get_joke_weight(j)) for j in filtered]
    if not weighted:
        return random.choice(filtered) if filtered else None # Fallback
    population, weights = zip(*weighted)
    return random.choices(population, weights=weights)[0]

def get_seasonal_joke():
    event = get_nearby_event()
    if not event:
        return {"text": "No seasonal event right now!", "categories": []}
    return get_joke_by_category(event) or {"text": f"No jokes for {event}", "categories": []}

def get_all_categories():
    cats = set()
    for joke in jokes:
        cats.update(joke["categories"])
    return sorted(cats)

# --- Main App ---
root = tk.Tk()
root.title("Dad Joke Generator")

# Apply some root padding
root.configure(bg=theme["bg"], padx=10, pady=10)

# --- TTK Styling ---
style = ttk.Style()
try:
    style.theme_use('clam') # A modern theme
except tk.TclError:
    try:
        style.theme_use('alt') # Fallback
    except tk.TclError:
        style.theme_use('default') # Last resort

# Base font for all ttk widgets (tk widgets might need separate config or inherit)
style.configure('.', font=('Helvetica', 10))

# Custom style for TButton for consistent padding
style.configure("TButton", padding=5)

# Custom style for TNotebook tabs
style.configure("TNotebook.Tab", padding=(10, 5), font=('Helvetica', 10, 'bold'))


joke_text = tk.StringVar()
cat_label_var = tk.StringVar()

category_var = tk.StringVar()
# Using ttk.Combobox - should pick up style
category_dropdown = ttk.Combobox(root, textvariable=category_var, font=('Helvetica', 10)) 
category_dropdown['values'] = get_all_categories()
category_dropdown.pack(pady=10, padx=5, fill="x")

# Using tk.Entry, font might need to be set if not inherited, or switch to ttk.Entry
search_entry = tk.Entry(root, font=('Helvetica', 10))
search_entry.pack(pady=5, padx=5, fill="x")

def search_jokes():
    term = search_entry.get().lower()
    results = [j for j in jokes if term in j["text"].lower() or any(term in c.lower() for c in j["categories"])]
    if results:
        show_joke(random.choice(results))
    else:
        messagebox.showinfo("Search", "No jokes matched your search.")

# Using ttk.Button for themed buttons where custom bg isn't paramount
ttk.Button(root, text="Search", command=search_jokes, style="TButton").pack(pady=5, padx=5, fill="x")

# tk.Label - will use theme["bg"], theme["fg"]. Font should be inherited from root or set.
joke_label = tk.Label(root, textvariable=joke_text, wraplength=400, bg=theme["bg"], fg=theme["fg"], font=('Helvetica', 12))
joke_label.pack(pady=10, padx=5)

cat_label = tk.Label(root, textvariable=cat_label_var, bg=theme["bg"], fg=theme["fg"], font=('Helvetica', 9))
cat_label.pack(pady=5, padx=5)

# Button frame for main action buttons
button_action_frame = ttk.Frame(root) # Use ttk.Frame
button_action_frame.pack(pady=10, padx=5, fill="x")

# Using ttk.Button for these as well, custom theme["button"] color might not apply directly with all ttk themes.
# If specific colors are essential, tk.Button might be kept, or style ttk.Button further.
# For now, let's use ttk.Button and rely on the TButton style for padding.
# The 'bg=theme["button"]' will be less effective on ttk.Button for some themes.
# We are prioritizing ttk styling for this pass.
col_weight = 1
button_action_frame.columnconfigure(0, weight=col_weight)
button_action_frame.columnconfigure(1, weight=col_weight)
button_action_frame.columnconfigure(2, weight=col_weight)

ttk.Button(button_action_frame, text="Random Joke", command=lambda: show_joke(get_random_joke()), style="TButton").grid(row=0, column=0, pady=5, padx=2, sticky="ew")
ttk.Button(button_action_frame, text="Seasonal Joke", command=lambda: show_joke(get_seasonal_joke()), style="TButton").grid(row=0, column=1, pady=5, padx=2, sticky="ew")
ttk.Button(button_action_frame, text="Get Joke from Category", command=lambda: show_joke(get_joke_by_category(category_var.get())), style="TButton").grid(row=0, column=2, pady=5, padx=2, sticky="ew")


# Reaction buttons: these have specific colors. Keep as tk.Button for now.
reaction_frame = tk.Frame(root, bg=theme["bg"]) # This is a tk.Frame
reaction_frame.pack(pady=10, padx=5)
tk.Button(reaction_frame, text="😆 Funny!", command=lambda: react_to_joke("Funny"), bg="lightgreen", font=('Helvetica', 10), relief=tk.FLAT, padx=5, pady=2).pack(side="left", padx=5)
tk.Button(reaction_frame, text="🤔 Huh?", command=lambda: react_to_joke("Confused"), bg="lightyellow", font=('Helvetica', 10), relief=tk.FLAT, padx=5, pady=2).pack(side="left", padx=5)
tk.Button(reaction_frame, text="🙄 So Bad", command=lambda: react_to_joke("Bad"), bg="lightcoral", font=('Helvetica', 10), relief=tk.FLAT, padx=5, pady=2).pack(side="left", padx=5)


def show_favorites():
    if not favorites:
        messagebox.showinfo("Favorites", "No favorites yet!")
        return
    fav_text = "\n\n".join(j["text"] for j in favorites)
    messagebox.showinfo("Favorite Jokes", fav_text)

# Management buttons frame
button_mgmt_frame = ttk.Frame(root) # Use ttk.Frame
button_mgmt_frame.pack(pady=10, padx=5, fill="x")
button_mgmt_frame.columnconfigure(0, weight=1) # Allow buttons to expand
button_mgmt_frame.columnconfigure(1, weight=1)


ttk.Button(button_mgmt_frame, text="View Favorites", command=show_favorites, style="TButton").grid(row=0, column=0, pady=5, padx=2, sticky="ew")
ttk.Button(button_mgmt_frame, text="Admin Panel", command=lambda: create_admin_panel(root, jokes, reactions, theme, save_jokes), style="TButton").grid(row=0, column=1, pady=5, padx=2, sticky="ew")


# Style frame for theme dropdown - use ttk.Frame
style_controls_frame = ttk.Frame(root) # Renamed from style_frame
style_controls_frame.pack(pady=10, padx=5)

def apply_theme(choice):
    themes = {
        "Default": ("#f0f0f0", "black", "lightblue"),
        "Space": ("#1a1a2e", "white", "#0f3460"),
        "Jungle": ("#dff0d8", "darkgreen", "#4caf50"),
        "Candyland": ("#ffe6f0", "deeppink", "#ff99cc")
    }
    if choice in themes:
        update_theme(*themes[choice])

theme_var = tk.StringVar(value="Default")
# ttk.OptionMenu - should pick up style
theme_menu = ttk.OptionMenu(style_controls_frame, theme_var, "Default", "Default", "Space", "Jungle", "Candyland", command=apply_theme)
theme_menu.pack(pady=5, padx=5)


# Import the admin panel creation function
from admin_panel import create_admin_panel

def on_exit():
    goodbye_joke = get_joke_by_category("goodbye")
    if goodbye_joke:
        speak(goodbye_joke["text"])
    root.destroy()

# Close button - tk.Button to allow specific theme["fg"] color.
# Or, create a specific ttk style for it if that's preferred.
tk.Button(root, text="Close", command=on_exit, bg=theme.get("button", "lightgrey"), fg=theme.get("fg", "black"), font=('Helvetica', 10, 'bold'), relief=tk.FLAT, padx=10, pady=5).pack(pady=20, padx=5)





# --- UI Functions ---
# Make sure messagebox is available if show_joke uses it and is not moved.
# from tkinter import messagebox # Already imported at the top

def show_joke(joke):
    if not joke:
        messagebox.showinfo("Oops!", "No joke found for this category!")
        return
    joke_text.set(joke["text"])
    current_joke["joke"] = joke
    cat_label_var.set("Categories: " + ", ".join(joke.get("categories", [])))
    speak(joke["text"])

def react_to_joke(reaction):
    joke = current_joke.get("joke")
    if joke:
        text = joke["text"]
        if text not in reactions:
            reactions[text] = {"Funny": 0, "Confused": 0, "Bad": 0}
        reactions[text][reaction] += 1
        save_reactions()
        if reaction == "Funny" and joke not in favorites:
            favorites.append(joke)
        messagebox.showinfo("Reaction Recorded", f"You reacted: {reaction}")

style_frame = tk.Frame(root, bg=theme["bg"])
style_frame.pack(pady=5)

def update_theme(bg, fg, button):
    theme["bg"] = bg
    theme["fg"] = fg
    theme["button"] = button
    root.configure(bg=bg)
    for widget in root.winfo_children():
        try:
            # For ttk widgets, changing bg/fg might be theme-dependent.
            # tk widgets will respond to this.
            if isinstance(widget, (ttk.Frame, ttk.Label, ttk.Button, ttk.Combobox, ttk.OptionMenu)):
                 # For ttk widgets, rely more on the ttk theme and style configurations.
                 # Overriding 'background' and 'foreground' directly might not always work as expected
                 # or might make them look inconsistent with the theme.
                 # However, if 'theme' dict is meant to override, this is where it would happen.
                 # We might need to create specific ttk styles for themed elements if this is not enough.
                pass # Let ttk styles handle these mostly.
            widget.configure(bg=bg) # Apply bg to all for consistency if possible
            if not isinstance(widget, (ttk.Combobox, ttk.Entry)): # Avoid changing fg for entry type widgets if it makes text unreadable
                 widget.configure(fg=fg)

        except tk.TclError: # Some widgets might not have bg/fg or specific ones like Combobox list
            pass
    # Ensure main window background is updated
    root.configure(bg=bg)
    # Update specific tk.Labels that use theme colors
    joke_label.config(bg=bg, fg=fg)
    cat_label.config(bg=bg, fg=fg)
    # Update reaction_frame and its tk.Buttons (as they are tk based)
    reaction_frame.config(bg=bg)
    # Note: ttk.Buttons in button_action_frame and button_mgmt_frame will NOT be affected by theme['button'] color here.
    # tk.Button for "Close" will be.

def apply_theme(choice):
    themes = {
        "Default": ("#f0f0f0", "black", "lightblue"), # bg, fg, button_bg
        "Space": ("#1a1a2e", "white", "#0f3460"),
        "Jungle": ("#dff0d8", "darkgreen", "#4caf50"),
        "Candyland": ("#ffe6f0", "deeppink", "#ff99cc")
    }
    if choice in themes:
        update_theme(*themes[choice])



show_joke({"text": "Welcome to the Dad Joke Generator!", "categories": []})

root.mainloop()
