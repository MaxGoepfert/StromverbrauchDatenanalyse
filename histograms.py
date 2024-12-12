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
    # print(data[zeit_spalte])
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



def plotHistogram(data, zeit_spalte, last_spalte, title):
    data = cleanData(data, zeit_spalte, last_spalte)
    plt.figure(figsize=(10,8))
    sns.histplot(data=data, x=last_spalte, bins=50, kde=True, color='blue', label=title)
    plt.title('Verteilung des Stromverbrauchs in Deutschland (Tageweise)')
    plt.xlabel('Stromverbrauch (in Mio. MWh)')
    plt.ylabel('Häufigkeit')
    plt.legend()
    plt.show()


# call funtion with data
#dataPath50Hertz = 'data/Realisierter_Stromverbrauch_2017_2023_Tag_50Hertz.csv'
#dataPathBW = 'data/Realisierter_Stromverbrauch_2017_2023_Tag_BW.csv'
dataPath_DE = 'data/Realisierter_Stromverbrauch_2017-2024_Tag.csv'
#data50Hertz = pd.read_csv(dataPath50Hertz, delimiter=';')
#dataBW = pd.read_csv(dataPathBW, delimiter=';')
dataDE = pd.read_csv(dataPath_DE, delimiter=';')
zeit_spalte = 'Datum von'
last_spalte = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'
#plotHistogram(data50Hertz,zeit_spalte, last_spalte, '50Hertz')
#plotHistogram(dataBW,zeit_spalte, last_spalte, 'TransNetBW')
plotHistogram(dataDE,zeit_spalte, last_spalte, 'Anzahl Bins: 50')

