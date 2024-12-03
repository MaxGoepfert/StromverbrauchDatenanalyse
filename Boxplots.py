import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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



def plotBoxplot(data, zeit_spalte, last_spalte, title):
    # clean data and set datetimes as index
    df_verbrauch = cleanData(data, zeit_spalte, last_spalte)

    # dayOfWeek
    """
    df_verbrauch['dayOfWeek'] = df_verbrauch.index.dayofweek
    fig, ax = plt.subplots(figsize=(10,8))
    sns.boxplot(data=df_verbrauch, x='dayOfWeek', y=last_spalte, palette='Blues)
    ax.set_title('Stromverbrauch Wochentage')
    plt.show()
    """
    # month
    df_verbrauch['month'] = df_verbrauch.index.month
    fig, ax = plt.subplots(figsize=(10,8))
    sns.boxplot(data=df_verbrauch, x='month', y=last_spalte, palette='Blues')
    ax.set_title(title)
    plt.show()

def plotJahresdurchschnitt(data, data2,zeit_spalte, last_spalte):

    data_verbrauch = cleanData(data, zeit_spalte, last_spalte)
    data_verbrauch2 = cleanData(data2, zeit_spalte, last_spalte)
    # Jahresdurchschnitt berechnen
    data_verbrauch['Jahr'] = data_verbrauch.index.year
    data_verbrauch2['Jahr'] = data_verbrauch2.index.year

    data_jahresdurchschnitt = data_verbrauch.groupby('Jahr')[last_spalte].mean()
    data_jahresdurchschnitt2 = data_verbrauch2.groupby('Jahr')[last_spalte].mean()

    # Plot
    plt.figure(figsize=(10, 8))
    plt.plot(data_jahresdurchschnitt, label='Jahresdurchschnitt 50Hertz', marker='o', color="blue")
    plt.plot(data_jahresdurchschnitt2, label='Jahresdurchschnitt TransNetBW', marker='s', color="orange")
    plt.title('Jahresdurchschnittlicher Stromverbrauch (2017–2023)')
    plt.xlabel('Jahr')
    plt.ylabel('Verbrauch (MWh)')
    plt.legend(title='ÜNB:', loc='upper right')
    plt.grid()
    plt.tight_layout()
    plt.show()


# call funtion with data
dataPath50Hertz = 'data/Realisierter_Stromverbrauch_2017_2023_Tag_50Hertz.csv'
dataPathBW = 'data/Realisierter_Stromverbrauch_2017_2023_Tag_BW.csv'
data50Hertz = pd.read_csv(dataPath50Hertz, delimiter=';')
dataBW = pd.read_csv(dataPathBW, delimiter=';')
zeit_spalte = 'Datum von'
last_spalte = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'
plotBoxplot(data50Hertz, zeit_spalte, last_spalte, 'Stromverbrauch Monate 50Hertz')
plotBoxplot(dataBW, zeit_spalte, last_spalte, 'Stromverbrauch Monate TransNetBW')
plotJahresdurchschnitt(data50Hertz, dataBW, zeit_spalte, last_spalte)
