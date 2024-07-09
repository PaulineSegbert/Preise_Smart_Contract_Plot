import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV-Datei einlesen
df = pd.read_csv('gas-data-results.csv')

plt.rcParams["font.family"] = "Times New Roman"

# Farben definieren
colors = {
    "Ethereum": "teal",
    "Polygon": "darkslategray",
    "Binance": "mediumseagreen",
    "Avalanche": "gray",
    "Gas": "orange" 
}

# Konvertiere 'AverageGas-EVM' zu numerischen Werten
df['AverageGas-EVM'] = pd.to_numeric(df['AverageGas-EVM'], errors='coerce')

# Entfernen Sie Zeilen mit NaN-Werten, die nach der Konvertierung entstehen könnten
df = df.dropna(subset=['AverageGas-EVM'])

# Plot erstellen
fig, ax1 = plt.subplots()

# Erste y-Achse (logarithmisch)
ax1.set_xlabel('Anzahl der Zeilen')
ax1.set_ylabel('Durchschnittspreis pro Transaktion in €')
ax1.set_yscale('log')
ax1.plot(df['DataSetSize'], df['AveragePrice-Ethereum'], label='Ethereum', color=colors["Ethereum"], linewidth=2)
ax1.plot(df['DataSetSize'], df['AveragePrice-Polygon'], label='Polygon', color=colors["Polygon"], linewidth=2)
ax1.plot(df['DataSetSize'], df['AveragePrice-Binance'], label='Binance', color=colors["Binance"], linewidth=2)
ax1.plot(df['DataSetSize'], df['AveragePrice-Avalanche'], label='Avalanche', color=colors["Avalanche"], linewidth=2)
ax1.tick_params(axis='y')
ax1.grid(True, which="both", linestyle='--', linewidth=0.5)

# Zweite y-Achse teilen
ax2 = ax1.twinx()
ax2.set_ylabel('Durchschnittlicher Gasverbrauch (EVM)')
ax2.plot(df['DataSetSize'], df['AverageGas-EVM'], label='Gasverbrauch', color=colors["Gas"], linewidth=2)
ax2.tick_params(axis='y')

# Maximalen Wert von 'AverageGas-EVM' ermitteln und auf das nächste Vielfache von 200000 aufrunden
max_gas = df['AverageGas-EVM'].max()
max_tick = np.ceil(max_gas / 200000) * 200000

# Ticks von 0 bis max_tick in Schritten von 200000 erstellen
ticks = np.arange(0, max_tick, 200000)

# Ticks für die rechte y-Achse setzen
ax2.set_yticks(ticks)

# Beschriftungen für die Ticks generieren und setzen
tick_labels = [f'{int(tick)}' for tick in ticks]
ax2.set_yticklabels(tick_labels)

ax2.set_ylim(bottom=0)  # Stelle sicher, dass die rechte y-Achse bei Null beginnt
ax2.grid(False)  # Deaktiviere das Grid für die zweite y-Achse, um Überlappungen zu vermeiden

# Titel und Legenden
# Kombinierte Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
fig.suptitle('Gasverbrauch und Durchschnittspreis pro ausgeführte Smart Contract Methode')

fig.tight_layout()  # sorgt dafür, dass die Achsenbeschriftungen nicht überlappen
plt.show()
