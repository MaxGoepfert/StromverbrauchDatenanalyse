import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

ZEIT_SPALTE = 'Datum von'
VERBRAUCH_SPALTE = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'
ZEIT_SPALTE_INDUSTRIE = 'Jahr'
VERBRAUCH_SPALTE_INDUSTRIE = 'Strom (Tsd. MJ)'

# 50 Hertz und BW
BUNDESLAENDER_UENB = ['Hamburg', 'Baden-W�rttemberg', 'Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern',
'Sachsen', 'Sachsen-Anhalt', 'Th�ringen']

# 50 Hertz
BUNDESLAENDER_HERTZ = ['Hamburg', 'Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern',
'Sachsen', 'Sachsen-Anhalt', 'Th�ringen']

BUNDESLAENDER_GESAMT = ['Hamburg', 'Baden-W�rttemberg', 'Berlin', 'Brandenburg', 'Mecklenburg-Vorpommern',
'Sachsen', 'Sachsen-Anhalt', 'Th�ringen', 'Schleswig-Holstein', 'Niedersachsen', 'Bremen', 'Hessen', 'Rheinland-Pfalz', 'Bayern', 'Saarland', 'Nordrhein-Westfalen']


# Alle Spalten anzeigen
pd.set_option('display.max_columns', None)

# Alle Zeilen anzeigen
pd.set_option('display.max_rows', None)

# Maximale Breite einer Spalte erhöhen
pd.set_option('display.width', 1000)

def convert_to_mwh(value):
    # Konvertiert einen Wert von MJ in MWh.
    if pd.notna(value):  # Prüfen, ob der Wert nicht NaN ist
        return value * 0.27778
    return value  # NaN-Werte bleiben NaN

def plotBundeslaender(data):
    plt.figure(figsize=(10, 8))
    for bundesland in BUNDESLAENDER_GESAMT:
        subset = data[data['Bundesland'] == bundesland]
        plt.plot(subset[ZEIT_SPALTE_INDUSTRIE], (subset[VERBRAUCH_SPALTE_INDUSTRIE] / 1e6), label=bundesland)

    # Plot anpassen
    plt.title('Stromverbrauch Industrie pro Bundesland über die Jahre')
    plt.xlabel('Jahr')
    plt.ylabel('Stromverbrauch (Mio. MWh)')
    plt.legend(title='Bundesland', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    # Plot anzeigen
    plt.show()

def getSumIndustrie(data):
    # Filter auf die Bundesländer von 50Hertz
    filtered_data = data[data['Bundesland'].isin(BUNDESLAENDER_HERTZ)]

    # Gruppieren nach Jahr und Summieren der Verbrauchswerte
    summed_data = filtered_data.groupby(ZEIT_SPALTE_INDUSTRIE)[VERBRAUCH_SPALTE_INDUSTRIE].sum().reset_index()

    return summed_data


def plot_IndustrieVerbrauch_50Hertz_TransNetBW(data):
    # Filter auf die Bundesländer von 50Hertz
    filtered_data = data[data['Bundesland'].isin(BUNDESLAENDER_HERTZ)]
    subsetBW = data[data['Bundesland'] == 'Baden-W�rttemberg']

    # Gruppieren nach Jahr und Summieren der Verbrauchswerte
    summed_data = filtered_data.groupby(ZEIT_SPALTE_INDUSTRIE)[VERBRAUCH_SPALTE_INDUSTRIE].sum().reset_index()

    # Plot erstellen
    plt.figure(figsize=(10, 8))
    plt.plot(summed_data[ZEIT_SPALTE_INDUSTRIE], (summed_data[VERBRAUCH_SPALTE_INDUSTRIE] / 1e6), marker='o', label='50Hertz')
    plt.plot(subsetBW[ZEIT_SPALTE_INDUSTRIE], (subsetBW[VERBRAUCH_SPALTE_INDUSTRIE] / 1e6), marker='o', label='BW')
    # Plot anpassen
    plt.title('Gesamtverbrauch Industrie der Zonen 50Hertz und TransNetBW (2017-2023')
    plt.xlabel('Jahr')
    plt.ylabel('Gesamtverbrauch (in Mio MWh)')
    plt.grid(True)
    plt.legend(title='ÜNB:', loc='upper right')
    #plt.tight_layout()
    plt.show()


def correlation(dataset1, dataset2, title):
    # clean data_industrie (dataset1)
    dataset1 = dataset1.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    dataset1[ZEIT_SPALTE] = pd.to_datetime(dataset1[ZEIT_SPALTE], dayfirst=True, errors='raise')
    dataset1.set_index(ZEIT_SPALTE, inplace=True)
    # Umwandlung Integer
    dataset1[VERBRAUCH_SPALTE] = dataset1[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset1[VERBRAUCH_SPALTE] = dataset1[VERBRAUCH_SPALTE].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset1[VERBRAUCH_SPALTE] = pd.to_numeric(dataset1[VERBRAUCH_SPALTE])

    # same cleaning for dataset2
    dataset2 = dataset2.copy()
    dataset2[ZEIT_SPALTE_INDUSTRIE] = pd.to_datetime(dataset2[ZEIT_SPALTE_INDUSTRIE].astype(str) + '-01-01', errors='raise')
    dataset2 = dataset2.sort_values(by=ZEIT_SPALTE_INDUSTRIE, ascending=True)
    dataset2.set_index(ZEIT_SPALTE_INDUSTRIE, inplace=True)

    dataset1[VERBRAUCH_SPALTE] = dataset1[VERBRAUCH_SPALTE] / 1e6
    dataset2[VERBRAUCH_SPALTE_INDUSTRIE] = dataset2[VERBRAUCH_SPALTE_INDUSTRIE] / 1e6

    # Korrelation berechnen
    correlation = dataset1[VERBRAUCH_SPALTE].corr(dataset2[VERBRAUCH_SPALTE_INDUSTRIE])
    # Ergebnis anzeigen
    print(f"{title}: {correlation: .2f}")

    # Streudiagramm der Stromverbrauchswerte
    plt.figure(figsize=(10, 8))
    plt.scatter(dataset1[VERBRAUCH_SPALTE], dataset2[VERBRAUCH_SPALTE_INDUSTRIE], alpha=0.5, color='blue')
    plt.title(title)
    plt.xlabel("Stromverbrauch Gesamt pro Jahr (in Mio. MWh)")
    plt.ylabel("Stromverbrauch Industrie pro Jahr (in Mio. MWh)")
    plt.grid(True)
    plt.show()




### Anteil des Industriestromverbrauchs an Gesamt
def quotaIndustrie(dataset1, dataset2):
    # clean data_industrie
    dataset1 = dataset1.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    dataset1[ZEIT_SPALTE] = pd.to_datetime(dataset1[ZEIT_SPALTE], dayfirst=True, errors='raise')
    dataset1.set_index(ZEIT_SPALTE, inplace=True)
    # Umwandlung Integer
    dataset1[VERBRAUCH_SPALTE] = dataset1[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset1[VERBRAUCH_SPALTE] = dataset1[VERBRAUCH_SPALTE].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset1[VERBRAUCH_SPALTE] = pd.to_numeric(dataset1[VERBRAUCH_SPALTE])

    # same cleaning for dataset2
    dataset2 = dataset2.copy()
    dataset2[ZEIT_SPALTE_INDUSTRIE] = pd.to_datetime(dataset2[ZEIT_SPALTE_INDUSTRIE].astype(str) + '-01-01', errors='raise')
    dataset2 = dataset2.sort_values(by=ZEIT_SPALTE_INDUSTRIE, ascending=True)
    dataset2.set_index(ZEIT_SPALTE_INDUSTRIE, inplace=True)

    dataset1['Anteil Industriestromverbrauch'] = dataset2[VERBRAUCH_SPALTE_INDUSTRIE] / dataset1[VERBRAUCH_SPALTE]

    return dataset1


if __name__ == '__main__':

    ### Laden und Konvertieren von Industrie Stromverbrauchs Datensatz
    data_Path_industrie = "Vorhersage/data/datasetEnergieverbrauchBundesland.csv"
    data_industrie = pd.read_csv(data_Path_industrie, delimiter=';', na_values='.')
    # Integer Werte konvertieren
    data_industrie[VERBRAUCH_SPALTE_INDUSTRIE] = pd.to_numeric(data_industrie[VERBRAUCH_SPALTE_INDUSTRIE], errors='raise')
    # in MWh konvertieren
    data_industrie[VERBRAUCH_SPALTE_INDUSTRIE] = data_industrie[VERBRAUCH_SPALTE_INDUSTRIE].apply(convert_to_mwh)


    dataEinwohner = pd.read_csv('Vorhersage/data/EinwohnerzahlenBundeslaender.csv', delimiter=';')
    dataEinwohner['Insgesamt'] = pd.to_numeric(dataEinwohner['Insgesamt'].str.replace(r"\s+", "", regex=True), errors='raise')

    # Plotten der Industriestromverbrauchswerte pro Jahr aller Bundesländer
    plotBundeslaender(data_industrie)
    # Plotten von Industriestromverbrauch der Zone 50Hertz und TransNetBW
    plot_IndustrieVerbrauch_50Hertz_TransNetBW(data_industrie)

    ### Korrelation
    dataPath50Hertz = 'Vorhersage/data/Realisierter_Stromverbrauch_2017-2023_Jahr_50Hertz.csv'
    dataPathBW = 'Vorhersage/data/Realisierter_Stromverbrauch_2017-2023_Jahr_TransNetBW.csv'
    data50Hertz = pd.read_csv(dataPath50Hertz, delimiter=';')
    dataBW = pd.read_csv(dataPathBW, delimiter=';')

    # Industrie Jahreswert 50Hertz
    data_Industrie50Hertz = getSumIndustrie(data_industrie)

    mean_Industrie_50Hertz = np.mean(data_Industrie50Hertz[VERBRAUCH_SPALTE_INDUSTRIE])
    print(f"Durchschnitt Stromverbrauch der Industrie in Regelzone 50Hertz: {mean_Industrie_50Hertz / 1e6: .2f} Mio. MWh")
    # Industrie Jahreswert TransNetBW
    subsetBW = data_industrie[data_industrie['Bundesland'] == 'Baden-W�rttemberg'].reset_index()
    mean_Industrie_TransNetBW = np.mean(subsetBW[VERBRAUCH_SPALTE_INDUSTRIE])
    print(f"Durchschnitt Stromverbrauch der Industrie in Regelzone TransNetBW: {mean_Industrie_TransNetBW / 1e6: .2f} Mio. MWh")

    # Korrelation berechnen und plotten
    correlation(data50Hertz, data_Industrie50Hertz, "Korrelation des Jahresstromverbrauchs zwischen 50Hertz und Industrie")
    correlation(dataBW, subsetBW, "Korrelation des Jahresstromverbrauchs zwischen TransNetBW und Industrie")

    # Industriestromverbrauchs-Anteile beider Regelzonen berechnen
    dataAnteilIndustrieBW = quotaIndustrie(dataBW, subsetBW)
    dataAnteilIndustrie50Hertz = quotaIndustrie(data50Hertz, data_Industrie50Hertz)

    # Diagramm der Stromverbrauchswerte
    plt.figure(figsize=(10, 8))
    plt.plot(dataAnteilIndustrieBW.index, dataAnteilIndustrieBW['Anteil Industriestromverbrauch'], color='blue',
             label='Anteil Industriestromverbrauch TransNetBW')
    plt.plot(dataAnteilIndustrie50Hertz.index, dataAnteilIndustrie50Hertz['Anteil Industriestromverbrauch'], color='red',
             label='Anteil Industriestromverbrauch 50Hertz')
    # Diagrammtitel und Achsenbeschriftungen
    plt.title("Anteil Industriestromverbrauch in den Regelzonen")
    plt.xlabel('Jahr')
    plt.ylabel('Anteil des Industriestromverbrauchs')

    # Raster und Legende
    plt.grid(True)
    plt.legend()

    # Diagramm anzeigen
    plt.tight_layout()
    plt.show()

