import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# CSV-Datei einlesen
df = pd.read_csv('gas-data-results.csv')

plt.rcParams["font.family"] = "Times New Roman"

# Farben definieren
colors = {
    "Ethereum": "teal",
    "Polygon": 'black',
    "Binance": "mediumseagreen",
    "Avalanche": "gray",
    "Gas": "orange" 
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


# Plot erstellen
fig, ax1 = plt.subplots()

# Schriftgrößen der Achsen-ticks
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Erste y-Achse (logarithmisch)
ax1.set_xlabel('Anzahl der Zeilen', fontsize=20, labelpad=17)
ax1.set_ylabel('Durchschnittspreis pro Transaktion in €', fontsize=20, labelpad=17)
ax1.set_yscale('log')
ax1.plot(df['DataSetSize'], df['AveragePrice-Ethereum'], label='Ethereum', color=colors["Ethereum"], linewidth=2)
ax1.plot(df['DataSetSize'], df['AveragePrice-Polygon'], label='Polygon', color=colors["Polygon"], linewidth=2)
ax1.plot(df['DataSetSize'], df['AveragePrice-Binance'], label='Binance', color=colors["Binance"], linewidth=2)
ax1.plot(df['DataSetSize'], df['AveragePrice-Avalanche'], label='Avalanche', color=colors["Avalanche"], linewidth=2)
ax1.tick_params(axis='y')
ax1.grid(True, which="both", linestyle='--', linewidth=0.5)
# Setzen der unteren Grenze der linken y-Achse auf den kleinen Wert epsilon
ax1.set_ylim(bottom=epsilon)

# Zweite y-Achse teilen
ax2 = ax1.twinx()
ax2.set_ylabel('Durchschnittlicher Gasverbrauch (EVM) in Mio. Einheiten', fontsize=20, labelpad=17)

# Teilen der Werte durch 10^6, um in Millionen Einheiten darzustellen
df['AverageGas-EVM-Millions'] = df['AverageGas-EVM'] / 1e6
ax2.plot(df['DataSetSize'], df['AverageGas-EVM-Millions'], label='Gasverbrauch', color=colors["Gas"], linewidth=2)
ax2.tick_params(axis='y')

# Maximalen Wert von 'AverageGas-EVM' ermitteln und auf das nächste Vielfache von 200000 aufrunden
max_gas = df['AverageGas-EVM'].max()
max_tick = np.ceil(max_gas / 200000) * 200000

# Ticks von 0 bis max_tick in Schritten von 200000 erstellen und in Millionen umrechnen
ticks = np.arange(0, max_tick + 200000, 200000) / 1e6

# Ticks für die rechte y-Achse setzen
ax2.set_yticks(ticks)

# Beschriftungen für die Ticks generieren und setzen
tick_labels = [f'{tick:.1f}' for tick in ticks]
ax2.set_yticklabels(tick_labels, fontsize=14)

ax2.set_ylim(bottom=0)  # Stelle sicher, dass die rechte y-Achse bei Null beginnt
ax2.grid(False)  # Deaktiviere das Grid für die zweite y-Achse, um Überlappungen zu vermeiden

#stelle sicher, dass die x-Achse bei Null beginnt
ax1.set_xlim(left=0)

# x-Achse Ticks in 500er Schritten setzen
ax1.set_xlim(left=0, right=4500)
ax1.set_xticks(np.arange(0, 4501, 500))

# Titel und Legenden
# Kombinierte Legende für beide Achsen
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='best', fontsize=14, markerscale=1.2)

fig.tight_layout()  # sorgt dafür, dass die Achsenbeschriftungen nicht überlappen
plt.show()