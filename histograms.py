import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.pyplot import figure

color_pal = sns.color_palette()

def cleanData(data, zeit_spalte, last_spalte):

    data = data.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    data[zeit_spalte] = pd.to_datetime(data[zeit_spalte], dayfirst=True, errors='raise')
    # print(data[ZEIT_SPALTE])
    data.set_index(zeit_spalte, inplace=True)

    # print(data.index)
    # Last Spalte in korrekte numerische Werte konvertieren
    data[last_spalte] = data[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    data[last_spalte] = data[last_spalte].str.replace(',', '.',
                                                      regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    data[last_spalte] = pd.to_numeric(data[last_spalte])

    # Neuer DataFrame mit nur Index und der Stromverbrauchs Spalte
    df_verbrauch = data[[last_spalte]]

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


def plotHistogram(data, zeit_spalte, last_spalte, title):
    # Daten vorbereiten
    data = cleanData(data, zeit_spalte, last_spalte)
    plt.figure(figsize=(10, 8))

    # Histogramm berechnen (um Bin-Breite zu ermitteln)
    counts, bin_edges, _ = plt.hist(data[last_spalte], bins=50, alpha=0)  # Alpha=0, um das Histogramm unsichtbar zu machen

    # Bin-Breite berechnen
    bin_width = bin_edges[1] - bin_edges[0]
    print(f"Bin-Breite: {bin_width: .3f}MWh")

    # Modus berechnen
    max_bin_index = np.argmax(counts)  # Index des Bins mit der höchsten Häufigkeit
    mode = (bin_edges[max_bin_index] + bin_edges[max_bin_index + 1]) / 2 # Mitte des Modus-Bins
    print(f"Modus: {mode / 1e6: .3f} Mio. MWh")
    print(f"Anfangswert des Modus-Bin: {bin_edges[max_bin_index] / 1e6: .3f}Mio. MWh, bis Endwert: {bin_edges[max_bin_index + 1] / 1e6: .3f}Mio. MWh")

    # Median berechnen
    median = np.median(data[last_spalte])

    # Mittelwert berechnen
    mean = np.mean(data[last_spalte])

    # Histogramm zeichnen
    sns.histplot(data=data, x=last_spalte, bins=50, kde=True, color='#5050FF', label='Anzahl Bins: 50')
    plt.axvline(x=mode, color='darkgreen', linestyle='-', linewidth=1.5, label=f'Modus: {mode:.2f}')
    plt.axvline(x=median, color='red', linestyle='-', linewidth=1.5, label=f'Median: {median:.2f}')
    plt.axvline(x=mean, color='orange', linestyle='-', linewidth=1.5, label=f'Mittelwert: {mean:.2f}')
    plt.title(title)
    plt.xlabel('Stromverbrauch (in MWh)')
    plt.ylabel('Häufigkeit')
    plt.legend()
    plt.show()


# call funtion with data
dataPath50Hertz = 'data/Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv'
dataPathBW = 'data/Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv'
dataPath_DE = 'data/Realisierter_Stromverbrauch_2017-2024_Tag.csv'
data50Hertz = pd.read_csv(dataPath50Hertz, delimiter=';')
dataBW = pd.read_csv(dataPathBW, delimiter=';')
dataDE = pd.read_csv(dataPath_DE, delimiter=';')
zeit_spalte = 'Datum von'
last_spalte = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'
plotHistogram(data50Hertz,zeit_spalte, last_spalte, 'Verteilung des Stromverbrauchs 50Hertz (Tageweise)')
plotHistogram(dataBW,zeit_spalte, last_spalte, 'Verteilung des Stromverbrauchs TransNetBW (Tageweise)')
#plotHistogram(dataDE,ZEIT_SPALTE, VERBRAUCH_SPALTE, 'Verteilung des Stromverbrauchs in Deutschland (Tageweise)')

