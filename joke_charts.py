#Joke Charts
#Created and Updated 4/21/2025

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict
import tkinter as tk

# === Bar Chart: Number of Jokes Per Category ===
def plot_category_counts(jokes, parent_frame):
    counts = defaultdict(int)
    for joke in jokes:
        for cat in joke["categories"]:
            counts[cat] += 1

    cats = list(counts.keys())
    values = [counts[cat] for cat in cats]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(cats, values, color="skyblue")
    ax.set_title("Jokes per Category")
    ax.set_xlabel("Number of Jokes")

    # Embed in Tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    return canvas  # ✅ RETURN the canvas object

# === Stacked Bar or Average: Reactions by Category ===
def plot_reaction_scores(jokes, reactions, parent_frame):
    # Count reactions per category
    reaction_totals = defaultdict(lambda: {"Funny": 0, "Confused": 0, "Bad": 0, "count": 0})
    for joke in jokes:
        jtext = joke["text"]
        jcats = joke["categories"]
        if jtext in reactions:
            for cat in jcats:
                reaction_totals[cat]["Funny"] += reactions[jtext].get("Funny", 0)
                reaction_totals[cat]["Confused"] += reactions[jtext].get("Confused", 0)
                reaction_totals[cat]["Bad"] += reactions[jtext].get("Bad", 0)
                reaction_totals[cat]["count"] += 1

    # Compute average scores
    cats = sorted(reaction_totals.keys())
    funny_avg = [reaction_totals[cat]["Funny"] / reaction_totals[cat]["count"] for cat in cats]
    confused_avg = [reaction_totals[cat]["Confused"] / reaction_totals[cat]["count"] for cat in cats]
    bad_avg = [reaction_totals[cat]["Bad"] / reaction_totals[cat]["count"] for cat in cats]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(cats, funny_avg, label="Funny 😆", color="green")
    ax.barh(cats, confused_avg, left=funny_avg, label="Confused 🤔", color="gold")
    total_stack = [funny_avg[i] + confused_avg[i] for i in range(len(cats))]
    ax.barh(cats, bad_avg, left=total_stack, label="Bad 🙄", color="red")

    ax.set_title("Avg Emoji Reactions by Category")
    ax.set_xlabel("Avg Reactions per Joke")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    return canvas  # ✅ RETURN the canvas object
