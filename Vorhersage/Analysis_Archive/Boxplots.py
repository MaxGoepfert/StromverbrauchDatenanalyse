import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler

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


def plotBoxplot(data, zone):
    # clean data
    df_verbrauch = cleanData(data)

    ### Standartisieren für Vergleich
    if zone == "transnetbw" or zone == "50hertz":
        scaler = StandardScaler()
        df_verbrauch[VERBRAUCH_SPALTE] = scaler.fit_transform(df_verbrauch[[VERBRAUCH_SPALTE]])

    # dayOfWeek
    df_verbrauch['Wochentage'] = df_verbrauch.index.dayofweek
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.boxplot(data=df_verbrauch, x='Wochentage', y=VERBRAUCH_SPALTE, palette='Blues')
    title = f"Stromverbrauch der Wochentage der Zone: {zone.upper()}"
    ax.set_title(title)
    plt.xlabel('Wochentage (Montag-Sonntag)')
    ylabel = "Stromverbrauch (in Mio MWh)"
    if zone == "transnetbw" or zone == "50hertz":
        ylabel = "Stromverbrauch (standardisiert)"
    plt.ylabel(ylabel)
    plt.show()

    ### Analog: Gruppierung nach Monate
    # month
    df_verbrauch['Monat'] = df_verbrauch.index.month
    fig, ax = plt.subplots(figsize=(10,8))
    sns.boxplot(data=df_verbrauch, x='Monat', y=VERBRAUCH_SPALTE, palette='Blues')
    title = f"Stromverbrauch der Monate der Zone: {zone.upper()}"
    ax.set_title(title)
    ax.set_title(title)
    #ax.set_ylim(0, 400000)
    plt.xlabel('Monate (Januar-Dezember)')
    ylabel = "Stromverbrauch (in Mio MWh)"
    if zone == "transnetbw" or zone == "50hertz":
        ylabel = "Stromverbrauch (standardisiert)"
    plt.ylabel(ylabel)
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
    plotBoxplot(data, zone)


