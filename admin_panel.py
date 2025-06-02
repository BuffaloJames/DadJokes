#Admin Panel
#Created and updated on 4/21/2025

import tkinter as tk
from tkinter import ttk, messagebox
from joke_charts import plot_category_counts, plot_reaction_scores
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def open_admin_panel(jokes, reactions, save_jokes_callback, run_deduplication_callback):

#    messagebox.showinfo("Debug", "Entered open_admin_panel")

    admin_win = tk.Toplevel()
    admin_win.title("Admin Panel")
    admin_win.geometry("600x500")

#    messagebox.showinfo("Debug", "Created admin window")

    tab_control = ttk.Notebook(admin_win)

    # === Tab 1: Edit Jokes ===
    edit_tab = ttk.Frame(tab_control)
    tab_control.add(edit_tab, text="Edit Jokes")

    text_frame = tk.Frame(edit_tab)
    text_frame.pack(fill="x", pady=5)

    joke_text_editor = tk.Text(text_frame, height=4)
    joke_text_editor.pack(fill="x", padx=10)

    category_entry = tk.Entry(edit_tab)
    category_entry.pack(pady=5)

    def update_selected_joke():
        global selected_joke_index
        if selected_joke_index is not None:
            new_text = joke_text_editor.get("1.0", tk.END).strip()
            new_cats = [c.strip() for c in category_entry.get().split(",") if c.strip()]
            jokes[selected_joke_index]["text"] = new_text
            jokes[selected_joke_index]["categories"] = new_cats
            refresh_list()
            save_jokes_callback(jokes, 'cleaned_dadjokeslist.txt')

    def refresh_list():
        joke_list.delete(0, tk.END)
        for joke in jokes:
            joke_list.insert(tk.END, joke["text"][:80])

    def on_select(event):
        global selected_joke_index
        selected = joke_list.curselection()
        if selected:
            index = selected[0]
            selected_joke_index = index
            joke_text_editor.delete("1.0", tk.END)
            joke_text_editor.insert(tk.END, jokes[index]["text"])
            category_entry.delete(0, tk.END)
            category_entry.insert(0, ", ".join(jokes[index]["categories"]))

    joke_list = tk.Listbox(edit_tab)
    joke_list.pack(expand=True, fill="both", pady=5)
    joke_list.bind('<<ListboxSelect>>', on_select)
    refresh_list()

    tk.Button(edit_tab, text="Update Joke", command=update_selected_joke).pack(pady=5)

#    messagebox.showinfo("Debug", "Finished setting up Edit Jokes tab")

    # === Tab 2: Category Counts ===
    count_tab = ttk.Frame(tab_control)
    tab_control.add(count_tab, text="Category Chart")

    canvas_frame = tk.Frame(count_tab)
    canvas_frame.pack(fill="both", expand=True)

    canvas = tk.Canvas(canvas_frame)
    scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Plot and pack the chart
    category_canvas = plot_category_counts(jokes, scrollable_frame)
    if category_canvas:
        category_canvas.get_tk_widget().pack(fill="both", expand=True)

    # === Tab 3: Emoji Reactions ===
    reaction_tab = ttk.Frame(tab_control)
    tab_control.add(reaction_tab, text="Reactions")

    reaction_fig = plot_reaction_scores(jokes, reactions, reaction_tab)
    if reaction_fig:
        reaction_fig.get_tk_widget().pack(in_=reaction_tab)


#    messagebox.showinfo("Debug", "Finished Reactions tab")

    # === Tab 4: Deduplication ===
    dedupe_tab = ttk.Frame(tab_control)
    tab_control.add(dedupe_tab, text="Deduplicate")
    tk.Button(dedupe_tab, text="Run Deduplication", command=run_deduplication_callback).pack(pady=20)

    tab_control.pack(expand=True, fill="both")

#    messagebox.showinfo("Debug", "All tabs loaded successfully")