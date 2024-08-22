import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV-Datei einlesen
df = pd.read_csv('gas-data-results.csv')

plt.rcParams["font.family"] = "Times New Roman"

# Farben definieren
colors = {
    "Ethereum": "#008080", #teal
    "Polygon": 'black',
    "Binance": "mediumseagreen",
    "Avalanche": "gray",
    "Gas": "#FF8000" #orange
}

# Manuelle Einstellung des fehlerhaften Werts auf NaN, damit interpolate ihn erkennt
df.at[2, 'AverageGas-EVM'] = np.nan

# Interpolieren des Gasverbrauchs über die ersten 500 Zeilen
df['AverageGas-EVM'] = df['AverageGas-EVM'].interpolate()

# Hinzufügen eines kleinen Werts (epsilon) zu den Durchschnittspreisdaten, um null zu vermeiden
epsilon = 1e-10
df.loc[df['AveragePrice-Ethereum'] == 0, 'AveragePrice-Ethereum'] += epsilon
df.loc[df['AveragePrice-Polygon'] == 0, 'AveragePrice-Polygon'] += epsilon
df.loc[df['AveragePrice-Binance'] == 0, 'AveragePrice-Binance'] += epsilon
df.loc[df['AveragePrice-Avalanche'] == 0, 'AveragePrice-Avalanche'] += epsilon

# Plot erstellen und Größe erhöhen
fig, ax1 = plt.subplots(figsize=(16, 10))  # Plot-Größe erhöhen
#fig, ax1 = plt.subplots()

# Schriftgrößen der Achsen-Ticks
plt.xticks(fontsize=50)
plt.yticks(fontsize=50)

# Erste y-Achse (logarithmisch)
ax1.set_xlabel('Anzahl der Zeilen in 1000 St.', fontsize=55, labelpad=17)
ax1.set_ylabel('Durchschnittspreis pro Transaktion in €', fontsize=55, labelpad=17)
ax1.set_yscale('log')
ax1.plot(df['DataSetSize'] / 1000, df['AveragePrice-Ethereum'], label='Ethereum', color=colors["Ethereum"], linewidth=4)
ax1.plot(df['DataSetSize'] / 1000, df['AveragePrice-Polygon'], label='Polygon', color=colors["Polygon"], linewidth=4)
ax1.plot(df['DataSetSize'] / 1000, df['AveragePrice-Binance'], label='Binance', color=colors["Binance"], linewidth=4)
ax1.plot(df['DataSetSize'] / 1000, df['AveragePrice-Avalanche'], label='Avalanche', color=colors["Avalanche"], linewidth=4)
ax1.tick_params(axis='y', pad=20)
ax1.grid(True, which="both", linestyle='--', linewidth=0.5)

# Setzen der unteren Grenze der linken y-Achse auf den kleinen Wert epsilon
ax1.set_ylim(bottom=epsilon)

# Zweite y-Achse teilen
ax2 = ax1.twinx()
ax2.set_ylabel('Durchschnittlicher Gasverbrauch (EVM) \n in Mio. Einheiten', fontsize=55, labelpad=17)

# Teilen der Werte durch 10^6, um in Millionen Einheiten darzustellen
df['AverageGas-EVM-Millions'] = df['AverageGas-EVM'] / 1e6
ax2.plot(df['DataSetSize'] / 1000, df['AverageGas-EVM-Millions'], label='Gasverbrauch', color=colors["Gas"], linewidth=4)
ax2.tick_params(axis='y', pad=30)

# Maximalen Wert von 'AverageGas-EVM' ermitteln und auf das nächste Vielfache von 200000 aufrunden
max_gas = df['AverageGas-EVM'].max()
max_tick = np.ceil(max_gas / 200000) * 200000

# Ticks von 0 bis max_tick in Schritten von 200000 erstellen und in Millionen umrechnen
ticks = np.arange(0, max_tick + 200000, 200000) / 1e6

# Ticks für die rechte y-Achse setzen
ax2.set_yticks(ticks)

# Beschriftungen für die Ticks generieren und setzen
tick_labels = [f'{tick:.1f}' for tick in ticks]
ax2.set_yticklabels(tick_labels, fontsize=50)

ax2.set_ylim(bottom=0)  # Stelle sicher, dass die rechte y-Achse bei Null beginnt
ax2.grid(False)  # Deaktiviere das Grid für die zweite y-Achse, um Überlappungen zu vermeiden

# Stelle sicher, dass die x-Achse bei Null beginnt
ax1.set_xlim(left=0)

# x-Achse Ticks in 500er Schritten setzen
ax1.set_xlim(left=0, right=4500 / 1000)  # Skaliere x-Achse auf Tausend
ax1.set_xticks(np.arange(0, 4501 / 1000, 500 / 1000))

# Titel und Legenden
# Kombinierte Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=52, markerscale=1.2)

fig.tight_layout()  # sorgt dafür, dass die Achsenbeschriftungen nicht überlappen

# Speichere das Bild, um sicherzustellen, dass alles in den Rahmen passt
plt.savefig('output.png', bbox_inches='tight')

plt.show()
