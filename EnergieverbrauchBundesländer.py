import pandas as pd
import matplotlib.pyplot as plt

def convert_to_mwh(value):
    #Konvertiert einen Wert von MJ in MWh.
    if pd.notna(value):  # Prüfen, ob der Wert nicht NaN ist
        return value * 0.27778
    return value  # NaN-Werte bleiben NaN


data_Path = "datasetEnergieverbrauchBundesland.csv"
data = pd.read_csv(data_Path, delimiter=';', na_values='.')

# Alle Spalten anzeigen
pd.set_option('display.max_columns', None)

# Alle Zeilen anzeigen
pd.set_option('display.max_rows', None)

# Maximale Breite einer Spalte erhöhen
pd.set_option('display.width', 1000)


# 50 Hertz und BW anschauen
bundeslaenderÜNB = ['Hamburg','Baden-W�rttemberg','Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern'
,'Sachsen', 'Sachsen-Anhalt', 'Th�ringen']

# 50 Hertz und BW anschauen
bundeslaender50Hertz = ['Hamburg', 'Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern'
,'Sachsen', 'Sachsen-Anhalt', 'Th�ringen']

bundeslaenderGesamt = ['Hamburg','Baden-W�rttemberg','Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern'
,'Sachsen', 'Sachsen-Anhalt', 'Th�ringen', 'Schleswig-Holstein', 'Niedersachsen', 'Bremen', 'Hessen', 'Rheinland-Pfalz', 'Bayern', 'Saarland', 'Nordrhein-Westfalen']

print(data['Bundesland'])



dataEinwohner = pd.read_csv('EinwohnerzahlenBundeslaender.csv', delimiter=';')
dataEinwohner['Insgesamt'] = pd.to_numeric(dataEinwohner['Insgesamt'].str.replace(r"\s+", "", regex=True), errors='raise')


# Spalten
zeit_spalte = 'Jahr'
verbrauch_spalte = 'Strom (Tsd. MJ)'

# Integer Werte konvertieren
data[verbrauch_spalte] = pd.to_numeric(data[verbrauch_spalte], errors='raise')
# in MWh konvertieren
data[verbrauch_spalte] = data[verbrauch_spalte].apply(convert_to_mwh)
# Skalieren in Mio. MWh
data[verbrauch_spalte] = data[verbrauch_spalte] / 1e6



def plotBundeslaender(data, bundeslaender, zeit_spalte, verbrauch_spalte):
    plt.figure(figsize=(10, 8))
    for bundesland in bundeslaender:
        subset = data[data['Bundesland'] == bundesland]
        plt.plot(subset[zeit_spalte], subset[verbrauch_spalte], label=bundesland)
    # Plot anpassen

    plt.title('Stromverbrauch Industrie pro Bundesland über die Jahre')
    plt.xlabel('Jahr')
    plt.ylabel('Stromverbrauch (Mio. MWh)')
    plt.legend(title='Bundesland', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Plot anzeigen
    plt.show()

#plotBundeslaender(data,bundeslaenderGesamt, zeit_spalte, verbrauch_spalte)



def plotSum(data, bundeslaender50Hertz, zeit_spalte, verbrauch_spalte):
    # Filter auf die Bundesländer von 50Hertz
    filtered_data = data[data['Bundesland'].isin(bundeslaender50Hertz)]
    subsetBW = data[data['Bundesland'] == 'Baden-W�rttemberg']

    # Gruppieren nach Jahr und Summieren der Verbrauchswerte
    summed_data = filtered_data.groupby(zeit_spalte)[verbrauch_spalte].sum().reset_index()

    # Plot erstellen
    plt.figure(figsize=(10, 8))
    plt.plot(summed_data[zeit_spalte], summed_data[verbrauch_spalte], marker='o', label='50Hertz')
    plt.plot(subsetBW[zeit_spalte], subsetBW[verbrauch_spalte],marker='o', label='BW')
    # Plot anpassen
    plt.title('Gesamtverbrauch Industrie der 50Hertz-Bundesländer und BW über die Jahre')
    plt.xlabel('Jahr')
    plt.ylabel('Gesamtverbrauch (in Mio MWh)')
    plt.grid(True)
    plt.legend(title='ÜNB:', loc='upper right')
    #plt.tight_layout()
    plt.show()

plotSum(data, bundeslaender50Hertz, zeit_spalte, verbrauch_spalte)

