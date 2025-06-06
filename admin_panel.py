import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from joke_utils import remove_duplicate_jokes # Import the deduplication utility
import copy # For deepcopying the list
from collections import Counter

def create_admin_panel(app_root, jokes_list, reactions_data, theme_settings, save_jokes_func):
    """
    Creates and displays the Admin Panel.

    Args:
        app_root: The main application root window.
        jokes_list: The list of joke dictionaries.
        reactions_data: The dictionary of joke reactions.
        theme_settings: The dictionary containing current theme settings.
        save_jokes_func: Callback function to save the jokes list.
    """
    admin = tk.Toplevel(app_root)
    admin.title("Admin Panel")
    admin.geometry("750x550") # Slightly larger for better padding
    admin.configure(padx=10, pady=10) # Add root padding to admin panel

    # Notebook style will be inherited from main app's style.configure("TNotebook.Tab", ...)
    notebook = ttk.Notebook(admin)
    notebook.pack(fill="both", expand=True, padx=5, pady=5)

    # Standard font for tk widgets in admin panel if not covered by ttk styles
    admin_font = ('Helvetica', 10)

    # --- Joke Editor Tab ---
    editor_frame = ttk.Frame(notebook, padding=(10,10)) # Use ttk.Frame and add padding
    notebook.add(editor_frame, text="Edit Jokes")

    per_page = 50
    current_page = tk.IntVar(value=0)

    # Use a frame to hold listbox and its scrollbar
    listbox_frame = ttk.Frame(editor_frame) # Use ttk.Frame
    listbox_frame.pack(side="left", fill="both", expand=True, pady=5, padx=5)

    listbox_scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical")
    listbox_scrollbar.pack(side="right", fill="y")

    listbox = tk.Listbox(listbox_frame, height=15, yscrollcommand=listbox_scrollbar.set, font=admin_font)
    listbox.pack(side="left", fill="both", expand=True)
    listbox_scrollbar.config(command=listbox.yview)
    
    edit_controls_frame = ttk.Frame(editor_frame) # Use ttk.Frame
    edit_controls_frame.pack(side="right", fill="y", padx=(10,5), pady=5)

    cat_entry = ttk.Entry(edit_controls_frame, font=admin_font, width=30) # Use ttk.Entry

        # Joke Text Editor
    ttk.Label(edit_controls_frame, text="Edit Joke Text:", font=admin_font).pack(pady=(10,0), anchor="w")
    joke_text_frame = ttk.Frame(edit_controls_frame)
    joke_text_frame.pack(pady=5, fill="x", expand=False) 

    joke_text_scrollbar = ttk.Scrollbar(joke_text_frame, orient="vertical")
    joke_text_scrollbar.pack(side="right", fill="y")

    joke_text_widget = tk.Text(joke_text_frame, height=7, width=30, yscrollcommand=joke_text_scrollbar.set, font=admin_font, wrap="word")
    joke_text_widget.pack(side="left", fill="x", expand=True)
    joke_text_scrollbar.config(command=joke_text_widget.yview)

    def update_joke_text():
        idx_tuple = listbox.curselection()
        if not idx_tuple:
            messagebox.showinfo("Info", "No joke selected to update.")
            return

        actual_idx = idx_tuple[0]
        joke_idx_in_list = current_page.get() * per_page + actual_idx

        if 0 <= joke_idx_in_list < len(jokes_list):
            new_text = joke_text_widget.get("1.0", "tk.END").strip() # Use "tk.END" as string
            if not new_text:
                messagebox.showerror("Error", "Joke text cannot be empty.")
                return

            jokes_list[joke_idx_in_list]["joke"] = new_text
            save_jokes_func(jokes_list)
            load_page() 
            messagebox.showinfo("Success", "Joke text updated and saved.")
        else:
            messagebox.showerror("Error", "Selected joke index is out of range for updating text.")

        ttk.Button(edit_controls_frame, text="Update Joke Text", command=update_joke_text, style="TButton").pack(pady=5)

    # Existing Categories Selector
    ttk.Label(edit_controls_frame, text="Existing Categories:", font=admin_font).pack(pady=(15,0), anchor="w")
    
    existing_cat_frame = ttk.Frame(edit_controls_frame)
    existing_cat_frame.pack(pady=5, fill="x", expand=False)
    
    existing_cat_scrollbar = ttk.Scrollbar(existing_cat_frame, orient="vertical")
    existing_cat_scrollbar.pack(side="right", fill="y")
    
    existing_categories_listbox = tk.Listbox(existing_cat_frame, height=5, yscrollcommand=existing_cat_scrollbar.set, font=admin_font, exportselection=False)
    existing_categories_listbox.pack(side="left", fill="x", expand=True)
    existing_cat_scrollbar.config(command=existing_categories_listbox.yview)

    def populate_existing_categories_listbox():
        existing_categories_listbox.delete(0, tk.END)
        unique_categories = set()
        # jokes_list is available in this scope from create_admin_panel arguments
        for joke in jokes_list: 
            for category in joke.get("categories", []):
                unique_categories.add(category)
        
        sorted_categories = sorted(list(unique_categories))
        for cat in sorted_categories:
            existing_categories_listbox.insert(tk.END, cat)

    def add_selected_category_to_cat_entry():
        selected_indices = existing_categories_listbox.curselection()
        if not selected_indices:
            messagebox.showinfo("Info", "No category selected from the list.")
            return

        selected_category = existing_categories_listbox.get(selected_indices[0])
        
        # cat_entry is available in this scope
        current_cats_str = cat_entry.get() 
        current_cats_list = [c.strip() for c in current_cats_str.split(',') if c.strip()]
        
        if selected_category not in current_cats_list:
            current_cats_list.append(selected_category)
            cat_entry.delete(0, tk.END)
            cat_entry.insert(0, ", ".join(current_cats_list))
        else:
            messagebox.showinfo("Info", f"Category '{selected_category}' is already in the entry.")

    ttk.Button(edit_controls_frame, text="Add Selected Category", command=add_selected_category_to_cat_entry, style="TButton").pack(pady=5)

    def clear_joke_fields():
        joke_text_widget.delete("1.0", tk.END)
        cat_entry.delete(0, tk.END)
        listbox.selection_clear(0, tk.END)
        # Optionally, set focus to joke_text_widget for new entry
        joke_text_widget.focus_set()

    ttk.Button(edit_controls_frame, text="Clear for New Joke", command=clear_joke_fields, style="TButton").pack(pady=(10,0))

    def save_new_joke():
        new_text = joke_text_widget.get("1.0", tk.END).strip()
        if not new_text:
            messagebox.showerror("Error", "Joke text cannot be empty for a new joke.")
            return

        # Determine new ID - find max current ID and add 1
        new_id = 1
        if jokes_list: # Check if jokes_list is not empty
            new_id = max(joke.get("id", 0) for joke in jokes_list) + 1
        
        cats_str = cat_entry.get()
        # Process categories similar to update_categories, ensuring they are capitalized
        new_categories = sorted(list(set(c.strip().capitalize() for c in cats_str.split(',') if c.strip())))

        new_joke = {
            "id": new_id,
            "joke": new_text,
            "categories": new_categories
        }
        
        jokes_list.append(new_joke)
        save_jokes_func(jokes_list) # Persist changes
        
        # Refresh displays
        load_page() 
        populate_existing_categories_listbox() # Refresh existing categories list
        
        messagebox.showinfo("Success", f"New joke (ID: {new_id}) saved successfully!")
        clear_joke_fields() # Clear fields for next new joke or edit

    ttk.Button(edit_controls_frame, text="Save New Joke", command=save_new_joke, style="TButton").pack(pady=5)

    ttk.Label(edit_controls_frame, text="Edit Categories (comma-separated):", font=admin_font).pack(pady=(10,0), anchor="w") 
    cat_entry.pack(pady=5, fill="x")

    def load_page():
        listbox.delete(0, tk.END)
        start = current_page.get() * per_page
        for i, joke in enumerate(jokes_list[start:start+per_page]):
            # Ensure 'text' key exists, provide default if not (robustness)
            listbox.insert(tk.END, joke.get("joke", "N/A")[:80])


    def update_categories():
        idx_tuple = listbox.curselection()
        if not idx_tuple:
            return
        # listbox.curselection() returns a tuple, e.g., (0,)
        actual_idx = idx_tuple[0] 
        joke_idx_in_list = current_page.get() * per_page + actual_idx
        
        if 0 <= joke_idx_in_list < len(jokes_list):
            cats = [c.strip() for c in cat_entry.get().split(",") if c.strip()]
            jokes_list[joke_idx_in_list]["categories"] = cats
            save_jokes_func(jokes_list)
            # No need to call load_page() if listbox text doesn't change, but categories do.
            # However, if joke text could change or for simplicity, reloading is fine.
            # To refresh categories in view if selected joke is the one edited:
            on_select(None) # Refresh category entry
        else:
            messagebox.showerror("Error", "Selected joke index is out of range.")


    def on_select(event): # event can be None if called manually
        idx_tuple = listbox.curselection()
        if not idx_tuple:
            # If called manually with event=None and nothing is selected, clear cat_entry
            cat_entry.delete(0, tk.END)
            joke_text_widget.delete("1.0", "tk.END")
            
            return
        
        actual_idx = idx_tuple[0]
        joke_idx_in_list = current_page.get() * per_page + actual_idx
        
        if 0 <= joke_idx_in_list < len(jokes_list):
            cat_entry.delete(0, tk.END)
            cat_entry.insert(0, ", ".join(jokes_list[joke_idx_in_list].get("categories", [])))
            joke_text_widget.delete("1.0", "tk.END")
            joke_text_widget.insert("1.0", jokes_list[joke_idx_in_list].get("joke", ""))

        else:
            # This case should ideally not happen if listbox and jokes_list are in sync
            cat_entry.delete(0, tk.END)
            joke_text_widget.delete("1.0", "tk.END")

            messagebox.showwarning("Warning", "Could not find selected joke data.")


    listbox.bind("<<ListboxSelect>>", on_select)
    ttk.Button(edit_controls_frame, text="Update Categories", command=update_categories, style="TButton").pack(pady=10) # Use ttk.Button
    
    page_buttons_frame = ttk.Frame(edit_controls_frame) # Use ttk.Frame, place within controls
    page_buttons_frame.pack(side="bottom", pady=10) 
    ttk.Button(page_buttons_frame, text="Prev", command=lambda: (current_page.set(max(0, current_page.get() - 1)), load_page()), style="TButton").pack(side="left", padx=5)
    ttk.Button(page_buttons_frame, text="Next", command=lambda: (current_page.set(min(current_page.get() + 1, (len(jokes_list)-1)//per_page )), load_page()), style="TButton").pack(side="left", padx=5)
    
    populate_existing_categories_listbox() # Populate the new listbox
    load_page() # Initial load

    # --- Category Count Tab ---
    count_frame = ttk.Frame(notebook, padding=(10,10)) # Use ttk.Frame and add padding
    notebook.add(count_frame, text="Category Counts")

    chart_canvas = tk.Canvas(count_frame, bg="white") # bg likely overridden by theme if this was ttk.Canvas
    chart_canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)

    scrollbar = ttk.Scrollbar(count_frame, orient="vertical", command=chart_canvas.yview)
    scrollbar.pack(side="right", fill="y")
    chart_canvas.configure(yscrollcommand=scrollbar.set)

    def draw_category_chart(event=None):
        chart_canvas.delete("all")
        counts = {}
        for joke in jokes_list:
            for cat in joke.get("categories", []): # Ensure categories exist
                counts[cat] = counts.get(cat, 0) + 1

        if not counts:
            chart_canvas.create_text(10, 10, anchor="nw", text="No categories to display.", font=admin_font)
            return

        sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)
        bar_height = 25
        bar_padding = 8
        label_area_width = 200 # Increased for potentially longer category names
        text_offset_x = 10
        
        canvas_width = chart_canvas.winfo_width()
        if canvas_width <= 1: canvas_width = chart_canvas.master.winfo_width() if chart_canvas.master.winfo_width() > 1 else 600
        
        max_bar_width = canvas_width - label_area_width - text_offset_x - 40 # Increased padding for count
        if max_bar_width < 50: max_bar_width = 50
        max_val_count = sorted_counts[0][1] if sorted_counts else 1

        for i, (category, count) in enumerate(sorted_counts):
            y_position = i * (bar_height + bar_padding) + bar_padding
            # Category Name
            chart_canvas.create_text(text_offset_x, y_position + bar_height / 2, text=category, anchor="w", font=admin_font, width=label_area_width - text_offset_x - 5)
            bar_start_x = label_area_width
            bar_length = (count / max_val_count) * max_bar_width if max_val_count > 0 else 0
            chart_canvas.create_rectangle(bar_start_x, y_position, bar_start_x + bar_length, y_position + bar_height, fill="skyblue", outline="grey") # Softer outline
            # Count Label next to bar
            chart_canvas.create_text(bar_start_x + bar_length + 5, y_position + bar_height / 2, text=str(count), anchor="w", font=admin_font)
        
        total_chart_height = len(sorted_counts) * (bar_height + bar_padding) + bar_padding
        chart_canvas.config(scrollregion=(0, 0, canvas_width, total_chart_height))

    refresh_button = ttk.Button(count_frame, text="Refresh Category Counts", command=draw_category_chart, style="TButton") # Use ttk.Button
    refresh_button.pack(pady=10, side="bottom")
    
    # Bindings for category chart
    # Delay initial draw slightly to allow canvas to size
    admin.after(100, draw_category_chart) # Draw after admin window is surely mapped and sized
    chart_canvas.bind("<Configure>", draw_category_chart)
    # Redraw when tab becomes visible
    def on_tab_selected(event):

        try:

            # Get the widget object of the currently selected tab

            selected_tab_widget_name = notebook.select()

            if not selected_tab_widget_name: # Check if a tab is actually selected

                return

            

            # Assuming 'notebook' is available in the scope where on_tab_selected runs.

            # And 'admin_panel.py' has 'import tkinter as tk'.

            selected_widget = notebook.nametowidget(selected_tab_widget_name)

        

            if selected_widget == count_frame: # Assuming 'count_frame' is available

                # Ensure canvas is ready before drawing, especially if tab was previously hidden

                chart_canvas.update_idletasks() # Assuming 'chart_canvas' is available

                admin.after(50, draw_category_chart) # Assuming 'admin' and 'draw_category_chart' are available

        except tk.TclError as e: # This 'tk' relies on admin_panel.py's import

            # print(f"TclError in on_tab_selected: {e}") 

            pass 

        except Exception as e:

            print(f"Unexpected error in on_tab_selected: {e}", file=sys.stderr)

    notebook.bind("<<NotebookTabChanged>>", on_tab_selected)


    # --- Theme Tab ---
    theme_editor_frame = ttk.Frame(notebook, padding=(10,10)) # Use ttk.Frame and add padding
    notebook.add(theme_editor_frame, text="Theme")

    # Note: The theme change logic here is basic. A full theme application would involve
    # updating ttk styles or having the main app handle theme changes more globally.
    def change_admin_theme_color(): 
        color = colorchooser.askcolor(title="Choose Background Color for Admin Panel")[1]
        if color:
            admin.configure(bg=color) 
            # This is a superficial change for the admin window itself.
            # ttk widgets within are styled by the ttk theme.
            # To change their actual style, one would need to update ttk.Style configurations.
            theme_settings["bg"] = color # Update the shared theme dictionary

    ttk.Button(theme_editor_frame, text="Change Admin Panel Background", command=change_admin_theme_color, style="TButton").pack(pady=10) # Use ttk.Button

    # --- Emoji Reactions Tab ---
    reactions_display_frame = ttk.Frame(notebook, padding=(10,10)) # Use ttk.Frame and add padding
    notebook.add(reactions_display_frame, text="Emoji Reactions")

    reactions_text_frame = ttk.Frame(reactions_display_frame) # Use ttk.Frame
    reactions_text_frame.pack(fill="both", expand=True, padx=5, pady=5)

    reactions_scrollbar = ttk.Scrollbar(reactions_text_frame, orient="vertical")
    reactions_scrollbar.pack(side="right", fill="y")

    reactions_text_widget = tk.Text(reactions_text_frame, wrap="word", yscrollcommand=reactions_scrollbar.set, height=10, font=admin_font)
    reactions_text_widget.pack(side="left", fill="both", expand=True)
    reactions_scrollbar.config(command=reactions_text_widget.yview)

    
    sorted_reacts = sorted(reactions_data.items(), key=lambda x: x[1].get("Funny", 0), reverse=True)
    summary_text = ""
    if not sorted_reacts:
        summary_text = "No reactions yet."
    else:
        for joke_text_val, reacts in sorted_reacts:
             # Ensure 'text' key exists for joke, provide default if not
            joke_display_text = joke_text_val[:50] + "..." if len(joke_text_val) > 50 else joke_text_val
            summary_text += f"{joke_display_text}\n"
            summary_text += f"  😆 Funny: {reacts.get('Funny', 0)} | 😕 Huh?: {reacts.get('Confused', 0)} | 👎 So Bad: {reacts.get('Bad', 0)}\n\n"
    
    reactions_text_widget.insert(tk.END, summary_text)
    reactions_text_widget.config(state="disabled") # Make it read-only

    # --- Utilities Tab ---
    utilities_frame = ttk.Frame(notebook, padding=(10,10)) # Use ttk.Frame and add padding
    notebook.add(utilities_frame, text="Utilities")

    fuzzy_threshold_var = tk.DoubleVar(value=0.9) # Keep as is, for tk.Entry primarily

    def run_deduplication():
        # Make a copy to avoid modifying the original list if the user cancels or if no changes
        original_jokes_copy = copy.deepcopy(jokes_list)
        
        try:
            threshold = fuzzy_threshold_var.get()
        except tk.TclError:
            messagebox.showerror("Error", "Invalid threshold value. Please enter a number (e.g., 0.9).")
            return

        if not (0.0 <= threshold <= 1.0):
            messagebox.showerror("Error", "Fuzzy threshold must be between 0.0 and 1.0.")
            return

        cleaned_jokes_list = remove_duplicate_jokes(original_jokes_copy, fuzzy_threshold=threshold)
        
        num_original = len(jokes_list) # Compare with the live list's current state
        num_cleaned = len(cleaned_jokes_list)
        num_removed = num_original - num_cleaned

        if num_removed > 0:
            # Update the main jokes_list in place
            jokes_list[:] = cleaned_jokes_list 
            save_jokes_func(jokes_list) # Persist changes
            messagebox.showinfo("Deduplication Complete", 
                                f"{num_removed} duplicate joke(s) removed (or merged).\n"
                                f"The joke list has been updated and saved.\n"
                                f"New joke count: {num_cleaned}")
            
            # Adjust current_page in joke editor if it's now out of bounds
            max_page = (len(jokes_list) - 1) // per_page
            if current_page.get() > max_page:
                current_page.set(max(0, max_page)) # Ensure current_page is not negative if list becomes empty

            load_page() # Refresh the joke editor listbox on the "Edit Jokes" tab
            # Also, if category chart is visible, it should be refreshed.
            # Calling draw_category_chart directly might try to draw if tab isn't visible.
            # This is okay, or could be tied to tab visibility.
            draw_category_chart() 
        else:
            messagebox.showinfo("Deduplication Complete", "No duplicate jokes found based on the current threshold.")

    dedup_controls_frame = ttk.Frame(utilities_frame) # Use ttk.Frame
    dedup_controls_frame.pack(pady=10, padx=10, fill="x")
    
    ttk.Label(dedup_controls_frame, text="Fuzzy Match Threshold (0.0-1.0):", font=admin_font).pack(side="left", padx=(0,5)) # Use ttk.Label
    # Using tk.Entry for DoubleVar, or switch to ttk.Entry and manage var differently if needed for pure ttk.
    # ttk.Entry usually works fine with DoubleVar.
    threshold_entry = ttk.Entry(dedup_controls_frame, textvariable=fuzzy_threshold_var, width=5, font=admin_font) # Use ttk.Entry
    threshold_entry.pack(side="left", padx=5)
    ttk.Button(dedup_controls_frame, text="Remove Duplicate Jokes", command=run_deduplication, style="TButton").pack(side="left", padx=5) # Use ttk.Button
    
    # Ensure the admin window is brought to the front and focused
    admin.transient(app_root) # Keep admin window on top of main window
    admin.grab_set()         # Modal behavior: disable other windows until this one is closed
    admin.focus_set()        # Focus on the admin window
    app_root.wait_window(admin) # Wait until admin window is closed

# Example of how this might be called from dadjoke.py:
# from admin_panel import create_admin_panel
# ...
# tk.Button(root, text="Admin Panel", command=lambda: create_admin_panel(root, jokes, reactions, theme, save_jokes)).pack()
