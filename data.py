import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
#plt.use('TkAgg')  # Stabileres Backend für macOS

def plotData(dataset, zeit_spalte, last_spalte, title):
    # Alle Spalten anzeigen
    pd.set_option('display.max_columns', None)

    # Alle Zeilen anzeigen
    pd.set_option('display.max_rows', None)

    # Maximale Breite einer Spalte erhöhen
    pd.set_option('display.width', 1000)

    # Plot erstellen
    plt.figure(figsize=(12, 6))  # Größe des Plots festlegen
    plt.plot(dataset[zeit_spalte], dataset[last_spalte], label="Gesamtlast Strom", color='blue')

    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit (Datum von)")
    plt.ylabel("Gesamtlast Strom (in MWh)")  # Einheit anpassen, falls bekannt
    plt.title(title)

    # Legende und Gitter
    plt.legend()
    plt.grid()
    # Plot anzeigen
    plt.show()

def cleanData(dataset, zeit_spalte, last_spalte):
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[zeit_spalte] = pd.to_datetime(dataset[zeit_spalte], dayfirst=True, errors='raise')
    dataset[last_spalte] = dataset[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[last_spalte] = dataset[last_spalte].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[last_spalte] = pd.to_numeric(dataset[last_spalte])

    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values1 = dataset[zeit_spalte].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{zeit_spalte}': {missing_values1}")
    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values2 = dataset[last_spalte].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{last_spalte}': {missing_values2}")


if __name__ == "__main__":
    dataPath = "Realisierter_Stromverbrauch_201701010000_202301010000_Tag.csv"
    dataPath2 = "Realisierter_Stromverbrauch_2017_2023_Tag_50Hertz.csv"
    dataPath3 = "Realisierter_Stromverbrauch_2017_2023_Tag_BW.csv"

    data = pd.read_csv(dataPath, delimiter=';')
    data_50Hertz = pd.read_csv(dataPath2, delimiter=';')
    data_TransNetBW= pd.read_csv(dataPath3, delimiter=';')
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

    # Clean data
    cleanData(data_50Hertz, zeit_spalte, last_spalte)
    cleanData(data_TransNetBW, zeit_spalte, last_spalte)
    #plotData(data,zeit_spalte, last_spalte, "Gesamt")
    #plotData(data_50Hertz,zeit_spalte, last_spalte, "50Hertz")
    #plotData(data_TransNetBW,zeit_spalte, last_spalte, "TransNetBW")


    varianz = data_50Hertz[last_spalte].var()
    print(f"Die Varianz der Netzlast 50 Hertz beträgt: {varianz}")
    varianz = data_TransNetBW[last_spalte].var()
    print(f"Die Varianz der Netzlast TransNetBW beträgt: {varianz}")

    std_50Hertz = np.std(data_50Hertz[last_spalte])

    std_TransNetBW = np.std(data_TransNetBW[last_spalte])

    mean_50Hertz = np.mean(data_50Hertz[last_spalte])
    mean_TransNetBW = np.mean(data_TransNetBW[last_spalte])

    vk_50Hertz = (std_50Hertz / mean_50Hertz) * 100
    vk_TransNetBW = (std_TransNetBW / mean_TransNetBW) * 100

    print(f"Die Variationskoefizient (in %) der Netzlast 50Hertz beträgt: {vk_50Hertz: .2f}%")
    print(f"Die Variationskoefizient (in %)der Netzlast TransNetBW beträgt: {vk_TransNetBW: .2f}%")

    # Größten Wert in der Zielspalte anzeigen
    max_value = data_50Hertz[last_spalte].max()
    print(f"Der größte Wert in der Spalte {last_spalte} von 50Hertz ist: {max_value}")
    max_value = data_TransNetBW[last_spalte].max()
    print(f"Der größte Wert in der Spalte {last_spalte} von TransNetBW ist: {max_value}")


# TO DO Variationskoeffizent Zusammenhänge: Kovarianz/Korrelation, Korrelationskoeffizient, Anteil Industrie, Anteil Haushalte
