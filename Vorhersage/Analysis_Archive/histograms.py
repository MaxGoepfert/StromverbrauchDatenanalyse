import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure

color_pal = sns.color_palette()
ZEIT_SPALTE = 'Datum von'
VERBRAUCH_SPALTE = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'
def cleanData(data):

    data = data.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    data[ZEIT_SPALTE] = pd.to_datetime(data[ZEIT_SPALTE], dayfirst=True, errors='raise')
    # print(data[ZEIT_SPALTE])
    data.set_index(ZEIT_SPALTE, inplace=True)

    # print(data.index)
    # Last Spalte in korrekte numerische Werte konvertieren
    data[VERBRAUCH_SPALTE] = data[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    data[VERBRAUCH_SPALTE] = data[VERBRAUCH_SPALTE].str.replace(',', '.',
                                                                regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    data[VERBRAUCH_SPALTE] = pd.to_numeric(data[VERBRAUCH_SPALTE])

    # Neuer DataFrame mit nur Index und der Stromverbrauchs Spalte
    df_verbrauch = data[[VERBRAUCH_SPALTE]]

    df_verbrauch = df_verbrauch.copy()

    return df_verbrauch


""""
def plotHistogram(data, ZEIT_SPALTE, VERBRAUCH_SPALTE, title):
    data = cleanData(data, ZEIT_SPALTE, VERBRAUCH_SPALTE)
    plt.figure(figsize=(10,8))
    sns.histplot(data=data, x=VERBRAUCH_SPALTE, bins=50, kde=True, color='blue', label=title)
    plt.title('Verteilung des Stromverbrauchs in Deutschland (Tageweise)')
    plt.xlabel('Stromverbrauch (in Mio. MWh)')
    plt.ylabel('Häufigkeit')
    plt.legend()
    plt.show()
"""


def plotHistogram(data, title):
    # Daten vorbereiten
    data = cleanData(data)
    plt.figure(figsize=(10, 8))

    # Histogramm berechnen (um Bin-Breite zu ermitteln)
    counts, bin_edges, _ = plt.hist(data[VERBRAUCH_SPALTE], bins=50, alpha=0)  # Alpha=0, um das Histogramm unsichtbar zu machen

    # Bin-Breite berechnen
    bin_width = bin_edges[1] - bin_edges[0]
    print(f"Bin-Breite: {bin_width: .3f}MWh")

    # Modus berechnen
    max_bin_index = np.argmax(counts)  # Index des Bins mit der höchsten Häufigkeit
    mode = (bin_edges[max_bin_index] + bin_edges[max_bin_index + 1]) / 2 # Mitte des Modus-Bins
    print(f"Modus: {mode: .3f} MWh")
    print(f"Anfangswert des Modus-Bin: {bin_edges[max_bin_index]: .3f} MWh, bis Endwert: {bin_edges[max_bin_index + 1]: .3f} MWh")

    # Median berechnen
    median = np.median(data[VERBRAUCH_SPALTE])

    # Mittelwert berechnen
    mean = np.mean(data[VERBRAUCH_SPALTE])

    # Histogramm zeichnen
    sns.histplot(data=data, x=VERBRAUCH_SPALTE, bins=50, kde=True, color='#5050FF', label='Anzahl Bins: 50')
    plt.axvline(x=mode, color='darkgreen', linestyle='-', linewidth=1.5, label=f'Modus: {mode: .2f}')
    plt.axvline(x=median, color='red', linestyle='-', linewidth=1.5, label=f'Median: {median: .2f}')
    plt.axvline(x=mean, color='orange', linestyle='-', linewidth=1.5, label=f'Mittelwert: {mean: .2f}')
    plt.title(title)
    plt.xlabel('Stromverbrauch (in MWh)')
    plt.ylabel('Häufigkeit')
    plt.legend()
    plt.show()


if __name__ == '__main__':
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

    plotHistogram(data, f'Verteilung des Stromverbrauchs pro Tag für die Zone {zone.upper()}')


