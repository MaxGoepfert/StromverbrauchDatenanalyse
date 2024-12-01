import pandas as pd
import matplotlib.pyplot as plt

def convert_to_mwh(value):
    #Konvertiert einen Wert von MJ in MWh.
    if pd.notna(value):  # Prüfen, ob der Wert nicht NaN ist
        return value * 0.27778
    return value  # NaN-Werte bleiben NaN


data_Path = "datasetEnergieverbrauchBundesland.csv"
data = pd.read_csv(data_Path, delimiter=';', na_values='.')

# Alle Spalten anzeigen
pd.set_option('display.max_columns', None)

# Alle Zeilen anzeigen
pd.set_option('display.max_rows', None)

# Maximale Breite einer Spalte erhöhen
pd.set_option('display.width', 1000)

#print(data.head())

# Annahme: Spaltennamen sind 'Jahr', 'Bundesland', 'Stromverbrauch'
# Gruppieren der Daten nach Bundesland
bundeslaender = data['Bundesland'].unique()


# Erstellen der Visualisierung
plt.figure(figsize=(12, 10))
# Spalten
zeit_spalte = 'Jahr'
verbrauch_spalte = 'Strom (Tsd. MJ)'

# Integer Werte konvertieren
data[verbrauch_spalte] = pd.to_numeric(data[verbrauch_spalte], errors='raise')
# in MWh konvertieren
data[verbrauch_spalte] = data[verbrauch_spalte].apply(convert_to_mwh)
# Skalieren in Mio. MWh
data[verbrauch_spalte] = data[verbrauch_spalte] / 1e6

for bundesland in bundeslaender:
    subset = data[data['Bundesland'] == bundesland]
    plt.plot(subset[zeit_spalte], subset[verbrauch_spalte], label=bundesland)

# Plot anpassen
plt.title('Stromverbrauch Industrie pro Bundesland über die Jahre')
plt.xlabel('Jahr')
plt.ylabel('Stromverbrauch (Mio. MWh)')
plt.legend(title='Bundesland', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()

# Plot anzeigen
plt.show()

