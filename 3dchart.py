import matplotlib.pyplot as plt

# Data
categories = [
    "Dons reçus",
    "Revenus des événements (hors concert)",
    "Concert \"Enfances volées\"",
    "Financement réhabilitation psychologique des enfants",
    "Dons en nature (valeur estimée)",
    "Cotisations des membres"
]
values = [20249.26, 19932.57, 24000, 17040, 40500, 240]
colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
explode = (0.1, 0, 0, 0, 0.1, 0)  # Highlighting certain slices

# Create a 3D-like pie chart
fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(values, labels=categories, autopct='%1.1f%%', colors=colors, explode=explode, startangle=140, shadow=True)

# Title
plt.title("Répartition des sources de revenus 2024")

# Display
plt.show()
