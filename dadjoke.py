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

# Load jokes from file
def load_jokes(filename="dadjokeslist.txt"): #Update with link to your joke file
    jokes = []
    if not os.path.exists(filename):
        return jokes
    with open(filename, "r") as f:
        for line in f:
            parts = line.strip().split("%%")
            text = parts[0].strip()
            categories = [p.strip() for p in parts[1:]]
            jokes.append({"text": text, "categories": categories})
    return jokes

def save_jokes(jokes, filename="dadjokeslist.txt"): #Update with link to your joke file
    with open(filename, "w") as f:
        for joke in jokes:
            line = joke["text"]
            for cat in joke["categories"]:
                line += f" %%{cat}"
            f.write(line + "\n")

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
root.configure(bg=theme["bg"])

joke_text = tk.StringVar()
cat_label_var = tk.StringVar()

category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var)
category_dropdown['values'] = get_all_categories()
category_dropdown.pack(pady=5)

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

joke_label = tk.Label(root, textvariable=joke_text, wraplength=400, bg=theme["bg"], fg=theme["fg"])
joke_label.pack(pady=10)

cat_label = tk.Label(root, textvariable=cat_label_var, bg=theme["bg"], fg=theme["fg"])
cat_label.pack()

tk.Button(root, text="Random Joke", command=lambda: show_joke(get_random_joke()), bg=theme["button"]).pack(pady=3)
tk.Button(root, text="Seasonal Joke", command=lambda: show_joke(get_seasonal_joke()), bg=theme["button"]).pack(pady=3)
tk.Button(root, text="Get Joke from Category", command=lambda: show_joke(get_joke_by_category(category_var.get())), bg=theme["button"]).pack(pady=3)

reaction_frame = tk.Frame(root, bg=theme["bg"])
reaction_frame.pack(pady=5)
tk.Button(reaction_frame, text="😆 Funny!", command=lambda: react_to_joke("Funny"), bg="lightgreen").pack(side="left", padx=5)
tk.Button(reaction_frame, text="🤔 Huh?", command=lambda: react_to_joke("Confused"), bg="lightyellow").pack(side="left", padx=5)
tk.Button(reaction_frame, text="🙄 So Bad", command=lambda: react_to_joke("Bad"), bg="lightcoral").pack(side="left", padx=5)

def show_favorites():
    if not favorites:
        messagebox.showinfo("Favorites", "No favorites yet!")
        return
    fav_text = "\n\n".join(j["text"] for j in favorites)
    messagebox.showinfo("Favorite Jokes", fav_text)

tk.Button(root, text="View Favorites", command=show_favorites, bg=theme["button"]).pack(pady=3)

style_frame = tk.Frame(root, bg=theme["bg"])
style_frame.pack(pady=5)

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
theme_menu = ttk.OptionMenu(style_frame, theme_var, "Default", *["Default", "Space", "Jungle", "Candyland"], command=apply_theme)
theme_menu.pack()

def on_exit():
    goodbye_joke = get_joke_by_category("goodbye")
    if goodbye_joke:
        speak(goodbye_joke["text"])
    root.destroy()

def open_admin_panel():
    admin = tk.Toplevel(root)
    admin.title("Admin Panel")
    admin.geometry("700x500")

    notebook = ttk.Notebook(admin)
    notebook.pack(fill="both", expand=True)

    # --- Joke Editor Tab ---
    editor_frame = tk.Frame(notebook)
    notebook.add(editor_frame, text="Edit Jokes")

    per_page = 50
    current_page = tk.IntVar(value=0)

    listbox = tk.Listbox(editor_frame, height=20)
    listbox.pack(side="left", fill="y")

    edit_frame = tk.Frame(editor_frame)
    edit_frame.pack(side="right", fill="both", expand=True)

    cat_entry = tk.Entry(edit_frame)
    cat_entry.pack(pady=5)

    def load_page():
        listbox.delete(0, tk.END)
        start = current_page.get() * per_page
        for i, joke in enumerate(jokes[start:start+per_page]):
            listbox.insert(tk.END, joke["text"][:80])

    def update_categories():
        idx = listbox.curselection()
        if not idx:
            return
        joke_idx = current_page.get() * per_page + idx[0]
        cats = [c.strip() for c in cat_entry.get().split(",") if c.strip()]
        jokes[joke_idx]["categories"] = cats
        save_jokes(jokes)
        load_page()

    def on_select(event):
        idx = listbox.curselection()
        if not idx:
            return
        joke_idx = current_page.get() * per_page + idx[0]
        cat_entry.delete(0, tk.END)
        cat_entry.insert(0, ", ".join(jokes[joke_idx]["categories"]))

    listbox.bind("<<ListboxSelect>>", on_select)
    tk.Button(edit_frame, text="Update Categories", command=update_categories).pack(pady=2)
    tk.Button(editor_frame, text="Prev", command=lambda: (current_page.set(max(0, current_page.get() - 1)), load_page())).pack()
    tk.Button(editor_frame, text="Next", command=lambda: (current_page.set(current_page.get() + 1), load_page())).pack()
    load_page()

    # --- Category Count Tab ---
    count_frame = tk.Frame(notebook)
    notebook.add(count_frame, text="Category Counts")

    def show_category_counts():
        counts = {}
        for j in jokes:
            for cat in j["categories"]:
                counts[cat] = counts.get(cat, 0) + 1
        if not counts:
            messagebox.showinfo("No Categories", "There are no categories to count.")
            return

        counts_win = tk.Toplevel(root)
        counts_win.title("Category Counts")
        counts_win.geometry("400x400")

        canvas = tk.Canvas(counts_win)
        scrollbar = ttk.Scrollbar(counts_win, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for cat, count in sorted(counts.items()):
            tk.Label(scroll_frame, text=f"{cat}: {count}", anchor="w").pack(anchor="w", padx=10)

    tk.Button(count_frame, text="Show Category Counts", command=show_category_counts).pack(pady=10)

    # --- Theme Tab ---
    theme_frame = tk.Frame(notebook)
    notebook.add(theme_frame, text="Theme")

    def change_theme():
        color = colorchooser.askcolor(title="Choose Background Color")[1]
        if color:
            theme["bg"] = color
            root.configure(bg=color)
            for widget in root.winfo_children():
                widget.configure(bg=color)

    tk.Button(theme_frame, text="Change Background Color", command=change_theme).pack(pady=10)

    # --- Emoji Reactions Tab ---
    reaction_frame = tk.Frame(notebook)
    notebook.add(reaction_frame, text="Emoji Reactions")

    sorted_reacts = sorted(reactions.items(), key=lambda x: x[1].get("Funny", 0), reverse=True)
    summary = ""
    for joke, reacts in sorted_reacts:
        summary += f"\n{joke[:50]}...\n  Funny: {reacts.get('Funny', 0)} | Huh: {reacts.get('Confused', 0)} | Bad: {reacts.get('Bad', 0)}\n"
    tk.Label(reaction_frame, text=summary or "No reactions yet.", justify="left", anchor="w").pack(padx=10, pady=10, fill="both", expand=True)

tk.Button(root, text="Admin Panel", command=open_admin_panel, bg=theme["button"]).pack(pady=3)
tk.Button(root, text="Close", command=on_exit, bg=theme["button"], fg=theme["fg"]).pack(pady=3) # Modified close button





# --- UI Functions ---
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
            widget.configure(bg=bg, fg=fg)
        except:
            pass

def apply_theme(choice):
    themes = {
        "Default": ("#f0f0f0", "black", "lightblue"),
        "Space": ("#1a1a2e", "white", "#0f3460"),
        "Jungle": ("#dff0d8", "darkgreen", "#4caf50"),
        "Candyland": ("#ffe6f0", "deeppink", "#ff99cc")
    }
    if choice in themes:
        update_theme(*themes[choice])



show_joke({"text": "Welcome to the Dad Joke Generator!", "categories": []})

root.mainloop()
