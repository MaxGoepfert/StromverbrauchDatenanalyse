import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


#import matplotlib # for mac
#plt.use('TkAgg')  # Stabileres Backend für macOS
ZEIT_SPALTE = "Datum von"
VERBRAUCH_SPALTE = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"
def plotData(dataset, title):
    # Alle Spalten anzeigen
    pd.set_option('display.max_columns', None)

    # Alle Zeilen anzeigen
    pd.set_option('display.max_rows', None)

    # Maximale Breite einer Spalte erhöhen
    pd.set_option('display.width', 1000)

    # Plot erstellen
    plt.figure(figsize=(12, 6))  # Größe des Plots festlegen
    plt.plot(dataset[ZEIT_SPALTE], dataset[VERBRAUCH_SPALTE], label="Gesamtlast Stromverbrauch", color='blue')

    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit")
    ylabel = "Stromverbrauch (in MWh)"
    if zone == "transnetbw" or zone == "50hertz":
        ylabel = "Stromverbrauch (standardisiert)"
    plt.ylabel(ylabel)
    plt.title(f"Stromverbrauch pro Tag in der Zone {title.upper()}")

    # Legende und Gitter
    plt.legend()
    plt.grid()
    # Plot anzeigen
    plt.show()

def cleanData(dataset):
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[ZEIT_SPALTE] = pd.to_datetime(dataset[ZEIT_SPALTE], dayfirst=True, errors='raise')
    # Umwandlung Integer
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[VERBRAUCH_SPALTE] = pd.to_numeric(dataset[VERBRAUCH_SPALTE])

    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values1 = dataset[ZEIT_SPALTE].isnull().sum()
    #print(f"Fehlende Werte in der Spalte '{ZEIT_SPALTE}': {missing_values1}")
    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values2 = dataset[VERBRAUCH_SPALTE].isnull().sum()
    #print(f"Fehlende Werte in der Spalte '{VERBRAUCH_SPALTE}': {missing_values2}")

### Langfristige Trends |||| Gleitender Durchschnitt
def movingAvg(dataset, title):
    dataset['Gleitender Durchschnitt'] = dataset[VERBRAUCH_SPALTE].rolling(window=30).mean()
    # Plot erstellen
    plt.figure(figsize=(12, 6))  # Größe des Plots festlegen
    plt.plot(dataset[ZEIT_SPALTE], dataset['Gleitender Durchschnitt'], label="Stromverbrauch (30 Tage-Gleitender-Durchschnitt)", color='blue')

    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit (Tage)")
    plt.ylabel("Gesamtlast Strom (in MWh)")
    plt.title(f'Gleitender Durchschnitt der Zone {title.upper()}')

    # Legende und Gitter
    plt.legend()
    plt.grid()
    # Plot anzeigen
    plt.show()


if __name__ == "__main__":

    zone = input("Bitte Regelzone auswählen [DE / TransNetBW / 50Hertz]: \n")
    zone = zone.lower()
    ### Einlesen der Datensätze
    dataPath = ""
    if zone == "de":
        dataPath = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_de.csv"
        print("Datensatz für Deutschland laden...")
    elif zone == "50hertz":
        dataPath = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
        print("Datensatz für 50Hertz laden...")
    elif zone == "transnetbw":
        dataPath = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"
        print("Datensatz für TransNetBW laden...")
    else:
        print("Keine Regelzone/Falsche Regelzone ausgewählt: Fortfahren mit Datensatz für Deutschland")
        dataPath = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_de.csv"

    data = pd.read_csv(dataPath, delimiter=';')

    # Clean data
    cleanData(data)

    varianz = data[VERBRAUCH_SPALTE].var()
    print(f"Die Varianz der Netzlast in der Zone {zone.upper()} beträgt: {varianz: .2f} MWh\n")
    std = np.std(data[VERBRAUCH_SPALTE])
    print(f"Die std-Abweichung der Netzlast in der Zone {zone.upper()} beträgt: {std: .2f} MWh\n")

    mean = np.mean(data[VERBRAUCH_SPALTE])
    print(f"Der Mittelwert der Netzlast in der Zone {zone.upper()} beträgt: {mean: .2f} MWh\n")

    median = np.median(data[VERBRAUCH_SPALTE])
    print(f"Der Median der Netzlast in der Zone {zone.upper()} beträgt: {median: .2f} MWh\n")

    vk = (std / mean) * 100
    print(f"Die Variationskoefizient (in %) der Netzlast in der Zone {zone.upper()} beträgt: {vk: .2f}%\n")

    # Größten Wert in der Zielspalte anzeigen
    max_value = data[VERBRAUCH_SPALTE].max()
    print(f"Der größte Wert in der Spalte {VERBRAUCH_SPALTE} der Zone {zone.upper()} ist: {max_value} MWh\n")

    # Größten Wert in der Zielspalte anzeigen
    min_value = data[VERBRAUCH_SPALTE].min()
    print(f"Der kleinste Wert in der Spalte {VERBRAUCH_SPALTE} der Zone {zone.upper()} ist: {min_value} MWh")

    movingAvg(data, zone)

    ### Standartisieren für Vergleich
    if zone == "transnetbw" or zone == "50hertz":
        scaler = StandardScaler()
        data[VERBRAUCH_SPALTE] = scaler.fit_transform(data[[VERBRAUCH_SPALTE]])

    plotData(data, zone)


