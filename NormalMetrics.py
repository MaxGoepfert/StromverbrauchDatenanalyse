import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler


#import matplotlib # for mac
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
    plt.plot(dataset[zeit_spalte], dataset[last_spalte], label="Gesamtlast Stromverbrauch", color='blue')

    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit")
    plt.ylabel("Gesamtlast Strom (standardisiert)")  # Einheit anpassen, falls bekannt
    plt.title(f"Stromverbrauch pro Tag in der Regelzone {title}")

    # Legende und Gitter
    plt.legend()
    plt.grid()
    # Plot anzeigen
    plt.show()

def cleanData(dataset, zeit_spalte, last_spalte):
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[zeit_spalte] = pd.to_datetime(dataset[zeit_spalte], dayfirst=True, errors='raise')
    # Umwandlung Integer
    dataset[last_spalte] = dataset[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[last_spalte] = dataset[last_spalte].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[last_spalte] = pd.to_numeric(dataset[last_spalte])

    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values1 = dataset[zeit_spalte].isnull().sum()
    #print(f"Fehlende Werte in der Spalte '{zeit_spalte}': {missing_values1}")
    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values2 = dataset[last_spalte].isnull().sum()
    #print(f"Fehlende Werte in der Spalte '{last_spalte}': {missing_values2}")

### Langfristige Trends |||| Gleitender Durchschnitt
def movingAvg(dataset, zeit_spalte, last_spalte, title):
    dataset['Gleitender Durchschnitt'] = dataset[last_spalte].rolling(window=30).mean()
    # Plot erstellen
    plt.figure(figsize=(12, 6))  # Größe des Plots festlegen
    plt.plot(dataset[zeit_spalte], dataset['Gleitender Durchschnitt'], label="Stromverbrauch (30 Tage-Gleitender-Durchschnitt)", color='blue')

    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit (Tage)")
    plt.ylabel("Gesamtlast Strom (in MWh)")  # Einheit anpassen, falls bekannt
    plt.title(title)

    # Legende und Gitter
    plt.legend()
    plt.grid()
    # Plot anzeigen
    plt.show()


if __name__ == "__main__":
    dataPath = "data/Realisierter_Stromverbrauch_2017-2024_Tag.csv"
    dataPath2 = "data/Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
    dataPath3 = "data/Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"

    data = pd.read_csv(dataPath, delimiter=';')
    data_50Hertz = pd.read_csv(dataPath2, delimiter=';')
    data_TransNetBW= pd.read_csv(dataPath3, delimiter=';')
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"
    print(data_50Hertz.columns)

    # Clean data
    cleanData(data_50Hertz, zeit_spalte, last_spalte)
    cleanData(data_TransNetBW, zeit_spalte, last_spalte)


    ### Standartisieren für Vergleich
    scaler = StandardScaler()
    data_50Hertz['standardized_last_spalte'] = scaler.fit_transform(data_50Hertz[[last_spalte]])
    data_TransNetBW['standardized_last_spalte'] = scaler.fit_transform(data_TransNetBW[[last_spalte]])
    ###
    standard_spalte = 'standardized_last_spalte'

    #cleanData(data, zeit_spalte, last_spalte)
    #plot data
    #plotData(data,zeit_spalte, last_spalte, "Stromverbrauch Deutschland 2017-2023")
    plotData(data_50Hertz,zeit_spalte, standard_spalte, "50Hertz")
    plotData(data_TransNetBW,zeit_spalte, standard_spalte, "TransNetBW")

    #movingAvg(data_50Hertz, zeit_spalte, last_spalte, 'Gleitender Durchschnitt 50Hertz')
    #movingAvg(data_TransNetBW, zeit_spalte, last_spalte, 'Gleitender Durchschnitt TransNetBW')
    #movingAvg(data, zeit_spalte, last_spalte, 'Gleitender Durchschnitt Deutschland')
    """
    varianz = data[last_spalte].var()
    print(f"Die Varianz der Netzlast in DE beträgt: {varianz}\n")
    std_DE = np.std(data[last_spalte])
    print(f"Die std-Abweichung der Netzlast in DE beträgt: {std_DE}\n")

    mean_DE = np.mean(data[last_spalte])
    print(f"Der Mittelwert der Netzlast in DE beträgt: {mean_DE: .2f} \n")

    median_DE = np.median(data[last_spalte])
    print(f"Der Median der Netzlast in DE beträgt: {median_DE: .2f}\n")

    vk_DE = (std_DE / mean_DE) * 100
    print(f"Die Variationskoefizient (in %) der Netzlast in DE beträgt: {vk_DE: .2f}%\n")

    # Größten Wert in der Zielspalte anzeigen
    max_value = data[last_spalte].max()
    print(f"Der größte Wert in der Spalte {last_spalte} von DE ist: {max_value}\n")

    # Größten Wert in der Zielspalte anzeigen
    min_value = data[last_spalte].min()
    print(f"Der kleinste Wert in der Spalte {last_spalte} von DE ist: {min_value}")

    """
    #    50 Hertz und TransNetBW
    varianz = data_50Hertz[last_spalte].var()
    print(f"Die Varianz der Netzlast 50 Hertz beträgt: {varianz}")
    varianz = data_TransNetBW[last_spalte].var()
    print(f"Die Varianz der Netzlast TransNetBW beträgt: {varianz}\n")

    std_50Hertz = np.std(data_50Hertz[last_spalte])

    std_TransNetBW = np.std(data_TransNetBW[last_spalte])

    mean_50Hertz = np.mean(data_50Hertz[last_spalte])
    mean_TransNetBW = np.mean(data_TransNetBW[last_spalte])
    print(f"Der Mittelwert der Netzlast 50Hertz beträgt: {mean_50Hertz: .2f}")
    print(f"Der Mittelwert der Netzlast TransNetBW beträgt: {mean_TransNetBW: .2f} \n")

    median_50Hertz = np.median(data_50Hertz[last_spalte])
    median_TransNetBW = np.median(data_TransNetBW[last_spalte])
    print(f"Der Median der Netzlast 50Hertz beträgt: {median_50Hertz: .2f}")
    print(f"Der Median der Netzlast TransNetBW beträgt: {median_TransNetBW: .2f}\n")

    vk_50Hertz = (std_50Hertz / mean_50Hertz) * 100
    vk_TransNetBW = (std_TransNetBW / mean_TransNetBW) * 100

    print(f"Die Variationskoefizient (in %) der Netzlast 50Hertz beträgt: {vk_50Hertz: .2f}%")
    print(f"Die Variationskoefizient (in %)der Netzlast TransNetBW beträgt: {vk_TransNetBW: .2f}%\n")

    # Größten Wert in der Zielspalte anzeigen
    max_value = data_50Hertz[last_spalte].max()
    print(f"Der größte Wert in der Spalte {last_spalte} von 50Hertz ist: {max_value}")
    max_value = data_TransNetBW[last_spalte].max()
    print(f"Der größte Wert in der Spalte {last_spalte} von TransNetBW ist: {max_value} \n")

    # Größten Wert in der Zielspalte anzeigen
    min_value = data_50Hertz[last_spalte].min()
    print(f"Der kleinste Wert in der Spalte {last_spalte} von 50Hertz ist: {min_value}")
    min_value = data_TransNetBW[last_spalte].min()
    print(f"Der kleinste Wert in der Spalte {last_spalte} von TransNetBW ist: {min_value}")



