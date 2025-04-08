import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, colorchooser
from datetime import datetime, timedelta
import random, os
import re
import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Default is usually ~200; try 150 for slower


# Load jokes from file
def load_jokes(filename="dadjokeslist.txt"):
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

def save_jokes(jokes, filename="dadjokeslist.txt"):
    with open(filename, "w") as f:
        for joke in jokes:
            line = joke["text"]
            for cat in joke["categories"]:
                line += f" %%{cat}"
            f.write(line + "\n")

# Easter date calculator
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

def calculate_ElectionDay(year):
    # Election Day is the first Tuesday AFTER the first Monday in November.
    november_1st = datetime(year, 11, 1)
    
    # Find the weekday of November 1st (Monday=0, Sunday=6)
    weekday_nov1 = november_1st.weekday() 
    
    # Calculate days needed to get to the first Monday.
    # If Nov 1st is Monday (0), days_to_monday = 0.
    # If Nov 1st is Sunday (6), days_to_monday = 1.
    # If Nov 1st is Tuesday (1), days_to_monday = 6. 
    # Formula: (0 - weekday_nov1) % 7
    days_to_monday = (0 - weekday_nov1) % 7
    
    # Calculate the date of the first Monday
    first_monday = november_1st + timedelta(days=days_to_monday)
    
    # Election Day is the day after the first Monday (Tuesday)
    election_day = first_monday + timedelta(days=1)
    
    return election_day

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
        "St. Patrick’s day": datetime(year, 3, 14),
        "Fourth of July": datetime(year, 7, 4),
        "New Years": datetime(year, 12, 31),
        "Birthday": datetime(year, 3, 4),
        "Birthday": datetime(year, 8, 21),
        "Birthday": datetime(year, 6, 25),
        "Star Wars": datetime(year, 5, 4),
        "Groundhog Day": datetime(year, 2, 2),
        "Fathers Day": datetime(year, 6, 15),
        "Election": calculate_ElectionDay(year),
        "Thanksgiving": calculate_thanksgiving(year)
    }

def get_nearby_event():
    today = datetime.today()
    events = get_seasonal_events()
    for name, date in events.items():
        if abs((date - today).days) <= 7:
            return name
    return None

def speak(text):
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass  # Fail silently if speech doesn't work

jokes = load_jokes()
favorites = []
shown_jokes = set()
theme = {"bg": "#f0f0f0", "fg": "black", "button": "lightblue"}

# Joke selection functions
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

# UI Functions
def show_joke(joke):
    if not joke:
        messagebox.showinfo("Oops!", "No joke found for this category!")
        return
    joke_text.set(joke["text"])
    current_joke["joke"] = joke

    # Update category label
    if "categories" in joke:
        cat_label_var.set("Categories: " + ", ".join(joke["categories"]))
    else:
        cat_label_var.set("")
    speak(joke["text"])


def add_to_favorites():
    joke = current_joke.get("joke")
    if joke and joke not in favorites:
        favorites.append(joke)
        messagebox.showinfo("Added", "Joke added to favorites!")

def show_favorites():
    if not favorites:
        messagebox.showinfo("Favorites", "No favorites yet!")
        return
    fav_text = "\n\n".join(j["text"] for j in favorites)
    messagebox.showinfo("Favorite Jokes", fav_text)

def react_to_joke(reaction):
    joke = current_joke.get("joke")
    if joke:
        messagebox.showinfo("Reaction Recorded", f"You reacted: {reaction}")

# Define the font - choose family and size
label_font = ("Arial", 18) # Using Arial font, size 14. You can change this!

# --- Main App ---
root = tk.Tk()
root.title("Dad Joke Generator")
root.configure(bg=theme["bg"])

joke_text = tk.StringVar()
current_joke = {}
cat_label_var = tk.StringVar()

joke_label = tk.Label(root, 
    textvariable=joke_text, 
    wraplength=400, 
    bg=theme["bg"], 
    fg=theme["fg"],
    font=label_font)
joke_label.pack(pady=20)

category_var = tk.StringVar()
category_dropdown = ttk.Combobox(root, textvariable=category_var)
category_dropdown['values'] = get_all_categories()
category_dropdown.pack(pady=5)

tk.Button(root, text="Get Joke from Category", command=lambda: show_joke(get_joke_by_category(category_var.get())), bg=theme["button"]).pack(pady=3)


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



cat_label = tk.Label(root, textvariable=cat_label_var, bg=theme["bg"], fg=theme["fg"])
cat_label.pack()

tk.Button(root, text="Random Joke", command=lambda: show_joke(get_random_joke()), bg=theme["button"]).pack(pady=3)
tk.Button(root, text="Seasonal Joke", command=lambda: show_joke(get_seasonal_joke()), bg=theme["button"]).pack(pady=3)
tk.Button(root, text="Add to Favorites", command=add_to_favorites, bg=theme["button"]).pack(pady=3)
tk.Button(root, text="View Favorites", command=show_favorites, bg=theme["button"]).pack(pady=3)

# Reaction Buttons
reaction_frame = tk.Frame(root, bg=theme["bg"])
reaction_frame.pack(pady=5)
tk.Button(reaction_frame, text="😆 Funny!", command=lambda: react_to_joke("Funny"), bg="lightgreen").pack(side="left", padx=5)
tk.Button(reaction_frame, text="🤔 Huh?", command=lambda: react_to_joke("Confused"), bg="lightyellow").pack(side="left", padx=5)
tk.Button(reaction_frame, text="🙄 So Bad", command=lambda: react_to_joke("Bad"), bg="lightcoral").pack(side="left", padx=5)

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

# Themes dropdown
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

#def open_admin_panel():
    #messagebox.showinfo("Admin", "Admin panel is currently not loaded in this preview.")

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

    # --- Add Joke Tab ---
    add_frame = tk.Frame(notebook)
    notebook.add(add_frame, text="Add Joke")

    new_joke_text = tk.Text(add_frame, height=5, width=50)
    new_joke_text.pack(pady=5)
    new_cat_entry = tk.Entry(add_frame)
    new_cat_entry.pack(pady=5)

    def add_new_joke():
        text = new_joke_text.get("1.0", tk.END).strip()
        cats = [c.strip() for c in new_cat_entry.get().split(",") if c.strip()]
        if text:
            jokes.append({"text": text, "categories": cats})
            save_jokes(jokes)
            new_joke_text.delete("1.0", tk.END)
            new_cat_entry.delete(0, tk.END)
            load_page()

    tk.Button(add_frame, text="Add Joke", command=add_new_joke).pack(pady=5)

tk.Button(root, text="Admin Panel", command=open_admin_panel, bg=theme["button"]).pack(pady=3)

def on_exit():
    goodbye_joke = get_joke_by_category("Goodbye")
    if goodbye_joke:
        speak(goodbye_joke["text"])
    root.destroy()

tk.Button(root, text="Close with Exit to hear a goodbye!", command=on_exit, bg=theme["button"], fg=theme["fg"]).pack(pady=3)

show_joke({"text": "Welcome to the Dad Joke Generator!", "categories": []})

root.protocol("WM_DELETE_WINDOW", on_exit)
root.mainloop()