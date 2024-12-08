import pandas as pd
import matplotlib.pyplot as plt

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

def getJahresdurchschnitt(data, zeit_spalte, last_spalte):
    data_verbrauch = cleanData(data, zeit_spalte, last_spalte)

    data_verbrauch['Jahr'] = data_verbrauch.index.year
    # Jahresdurchschnitt berechnen
    data_jahresdurchschnitt = data_verbrauch.groupby('Jahr')[last_spalte].mean().reset_index()

    # Umbenennen der Spalten für Klarheit
    data_jahresdurchschnitt.rename(columns={last_spalte: 'Jahresdurchschnitt'}, inplace=True)
    return data_jahresdurchschnitt


def plotJahresdurchschnitt(data, data2,zeit_spalte, last_spalte):

    # get Jahresdurchschnitt
    data = getJahresdurchschnitt(data, zeit_spalte, last_spalte)
    data2 = getJahresdurchschnitt(data2, zeit_spalte, last_spalte)

    # Plot
    plt.figure(figsize=(10, 8))
    plt.plot(data, label='Jahresdurchschnitt 50Hertz', marker='o', color="blue")
    plt.plot(data2, label='Jahresdurchschnitt TransNetBW', marker='s', color="orange")
    plt.title('Jahresdurchschnittlicher Stromverbrauch (2017–2023)')
    plt.xlabel('Jahr')
    plt.ylabel('Verbrauch (MWh)')
    plt.legend(title='ÜNB:')
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
print(getJahresdurchschnitt(data50Hertz, zeit_spalte, last_spalte).columns)

#print(getJahresdurchschnitt(dataBW, zeit_spalte, last_spalte))
#plotJahresdurchschnitt(data50Hertz, dataBW, zeit_spalte, last_spalte)
