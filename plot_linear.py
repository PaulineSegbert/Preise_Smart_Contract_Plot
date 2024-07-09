import pandas as pd
import matplotlib.pyplot as plt

# CSV-Datei einlesen
df = pd.read_csv('gas-data-results.csv')

# Farben definieren
colors = {
    "Ethereum": "teal",
    "Polygon": "darkslategray",
    "Binance": "mediumseagreen",
    "Avalanche": "gray",
    "Gas": "olive"
}

fig, ax1 = plt.subplots()

# Erste y-Achse (linear)
ax1.set_xlabel('Anzahl der Zeilen')
ax1.set_ylabel('Durchschnittspreis pro Transaktion (€)')
line1, = ax1.plot(df['DataSetSize'], df['AveragePrice-Ethereum'], label='Ethereum', color=colors["Ethereum"])
line2, = ax1.plot(df['DataSetSize'], df['AveragePrice-Polygon'], label='Polygon', color=colors["Polygon"])
line3, = ax1.plot(df['DataSetSize'], df['AveragePrice-Binance'], label='Binance', color=colors["Binance"])
line4, = ax1.plot(df['DataSetSize'], df['AveragePrice-Avalanche'], label='Avalanche', color=colors["Avalanche"])
ax1.tick_params(axis='y')
ax1.grid(True, which="both", linestyle='--', linewidth=0.5)

# Zweite y-Achse teilen
ax2 = ax1.twinx()
ax2.set_ylabel('Durchschnittlicher Gasverbrauch (EVM)')
line5, = ax2.plot(df['DataSetSize'], df['AverageGas-EVM'], label='Gasverbrauch', color=colors["Gas"])
ax2.tick_params(axis='y')
ax2.grid(False)  # Deaktiviere das Grid für die zweite y-Achse, um Überlappungen zu vermeiden

# Handles und Labels beider Achsen kombinieren
lines = [line1, line2, line3, line4, line5]
labels = [line.get_label() for line in lines]

# Legende hinzufügen
ax1.legend(lines, labels, loc='upper left')

# Titel und Layout
fig.suptitle('Gasverbrauch und Durchschnittspreis pro Transaktion')
fig.tight_layout()  # sorgt dafür, dass die Achsenbeschriftungen nicht überlappen
plt.show()

