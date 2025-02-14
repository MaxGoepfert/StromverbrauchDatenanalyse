import pandas as pd
import matplotlib.pyplot as plt

ZEIT_SPALTE = 'Datum von'
VERBRAUCH_SPALTE = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'
def cleanData(dataset):

    dataset = dataset.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    dataset[ZEIT_SPALTE] = pd.to_datetime(dataset[ZEIT_SPALTE], dayfirst=True, errors='raise')
    # print(data[ZEIT_SPALTE])
    dataset.set_index(ZEIT_SPALTE, inplace=True)

    # print(data.index)
    # Last Spalte in korrekte numerische Werte konvertieren
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace(',', '.',
                                                                      regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[VERBRAUCH_SPALTE] = pd.to_numeric(dataset[VERBRAUCH_SPALTE])

    # Neuer DataFrame mit nur Index und der Stromverbrauchs Spalte
    df_verbrauch = dataset[[VERBRAUCH_SPALTE]]

    df_verbrauch = df_verbrauch.copy()

    return df_verbrauch

def getJahresdurchschnitt(dataset):
    data_verbrauch = cleanData(dataset)

    data_verbrauch['Jahr'] = data_verbrauch.index.year
    # Jahresdurchschnitt berechnen
    data_jahresdurchschnitt = data_verbrauch.groupby('Jahr')[VERBRAUCH_SPALTE].mean().reset_index()

    # Umbenennen der Spalten für Klarheit
    data_jahresdurchschnitt.rename(columns={VERBRAUCH_SPALTE: 'Jahresdurchschnitt'}, inplace=True)
    return data_jahresdurchschnitt


def plotJahresdurchschnitt(datasetBW, datasetHERTZ):

    # get Jahresdurchschnitt
    datasetBW_AVG = getJahresdurchschnitt(datasetBW)
    datasetHERTZ_AVG = getJahresdurchschnitt(datasetHERTZ)
    # Plot
    plt.figure(figsize=(10, 8))
    plt.plot(datasetBW_AVG['Jahr'], datasetBW_AVG['Jahresdurchschnitt'],
             label='Jahresdurchschnitt der Zone TransnetBW', marker='o', color="blue")
    plt.plot(datasetHERTZ_AVG['Jahr'], datasetHERTZ_AVG['Jahresdurchschnitt'],
             label='Jahresdurchschnitt der Zone 50hertz', marker='s', color="orange")
    plt.title('Jahresdurchschnittlicher Stromverbrauch')
    plt.xlabel('Jahr')
    plt.ylabel('Verbrauch (MWh)')
    plt.legend(title='ÜNB:')
    plt.grid()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    dataPath1 = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"
    data_BW = pd.read_csv(dataPath1, delimiter=';')
    dataPath2 = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
    data_Hertz = pd.read_csv(dataPath2, delimiter=';')
    plotJahresdurchschnitt(data_BW, data_Hertz)



