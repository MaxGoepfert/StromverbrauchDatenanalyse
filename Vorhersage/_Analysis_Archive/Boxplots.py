import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

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



def plotBoxplot(data, zeit_spalte, last_spalte, title):
    # clean data
    df_verbrauch = cleanData(data, zeit_spalte, last_spalte)

    ### Standartisieren für Vergleich
    #scaler = StandardScaler()
    #df_verbrauch['standardized_last_spalte'] = scaler.fit_transform(df_verbrauch[[VERBRAUCH_SPALTE]])
    ###

    # dayOfWeek
    df_verbrauch['Wochentage'] = df_verbrauch.index.dayofweek
    fig, ax = plt.subplots(figsize=(10,8))
    sns.boxplot(data=df_verbrauch, x='Wochentage', y=last_spalte, palette='Blues')
    ax.set_title(title)
    plt.xlabel('Wochentage (Montag-Sonntag)')
    plt.ylabel('Stromverbrauch (in Mio MWh)')
    plt.show()
    ### Analog: Gruppierung nach Monate
    """
    # month
    df_verbrauch['Monat'] = df_verbrauch.index.month
    fig, ax = plt.subplots(figsize=(10,8))
    sns.boxplot(data=df_verbrauch, x='Monat', y='standardized_last_spalte', palette='Blues')
    ax.set_title(title)
    #ax.set_ylim(0, 400000)
    plt.xlabel('Monate (Januar-Dezember)')
    plt.ylabel('Stromverbrauch (standardisiert)')
    plt.show()
    """



# call funtion with data
dataPath50Hertz = '../data/Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv'
dataPathBW = '../data/Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv'
dataPath_DE = '../data/Realisierter_Stromverbrauch_2017-2024_Tag.csv'
data50Hertz = pd.read_csv(dataPath50Hertz, delimiter=';')
dataBW = pd.read_csv(dataPathBW, delimiter=';')
data_DE = pd.read_csv(dataPath_DE, delimiter=';')
zeit_spalte = 'Datum von'
last_spalte = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'
#plotBoxplot(data50Hertz, ZEIT_SPALTE, VERBRAUCH_SPALTE, 'Stromverbrauch der Monate für 50Hertz')
#plotBoxplot(dataBW, ZEIT_SPALTE, VERBRAUCH_SPALTE, 'Stromverbrauch der Monate für TransNetBW')
plotBoxplot(data_DE, zeit_spalte, last_spalte, 'Stromverbrauch der Wochentage in Deutschland')
# monatliche Korrelation

### Klammer fehlt

"""
# Monatsspalte hinzufügen
data_50Hertz['Monat'] = data_50Hertz.index.month
data_TransNetBW['Monat'] = data_TransNetBW.index.month

# Gruppierung nach Monat und Berechnung der Korrelation
korrelationen_monatlich = data_50Hertz.groupby('Monat')[VERBRAUCH_SPALTE].corr(data_TransNetBW[VERBRAUCH_SPALTE])

# Ausgabe
print("Korrelationen pro Monat:")
print(korrelationen_monatlich)

"""
