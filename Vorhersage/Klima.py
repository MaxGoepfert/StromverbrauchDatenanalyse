import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import WEATHER_DATA_PATH

def convertDatasets(dataset):
    zeit_spalte = 'MESS_DATUM'
    temp_avg_spalte = 'TMK' # Tagesdurchschnittstemperatur
    sonne_h_spalte = 'SDK' # Sonnenscheindauer (in Stunden)
    dampfdruck_spalte = 'VPM' # in hPa
    # folgende Spalten sind interessant aber werden später nicht als Features genutzt
    temp_max_spalte = 'TXK' # Tageshöchsttemperatur
    temp_min_spalte = 'TNK' # Tagesniedrigsttemperatur
    niederschlag_spalte = 'RSK' # Menge an Niederschlag in mm
    niederschlag_ordinal_spalte = 'RSKF' # Art/Stärke des Niederschlags 0-9 --> 0 trocken, 9 Extrem-ereignis
    luftfeuchtigkeit_spalte = 'UPM' # Relative Luftfeuchtigkeit (in %)
    luftdruck_spalte = 'PM' # in hPa

    dataset = dataset.copy()
    dataset.columns = dataset.columns.str.strip()

    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[zeit_spalte] = pd.to_datetime(dataset[zeit_spalte], format='%Y%m%d', errors='raise')

    # ZEIT_SPALTE als Index setzen
    dataset.set_index(zeit_spalte, inplace=True)
    # Nur nötigen Zeitraum behalten
    dataset = dataset.loc[dataset.index >= '2017-01-01']
    dataset = dataset[[temp_avg_spalte,
                       temp_max_spalte, temp_min_spalte,
                       sonne_h_spalte,
                       niederschlag_spalte, niederschlag_ordinal_spalte,
                       luftfeuchtigkeit_spalte, luftdruck_spalte, dampfdruck_spalte
                       ]]

    # Ersetzen von -999 durch NaN und dann mit Mittelwerten auffüllen
    dataset.replace(-999, np.nan, inplace=True)
    dataset = dataset.apply(lambda col: col.fillna(col.mean()), axis=0)

    # Identifizieren von NaN-Werten
    #missing_values = dataset.isna()
    # Zählen der NaN-Werte -> Sollte jetzt 0 sein
    #missing_count_per_column = missing_values.sum()

    #print("Ersetzte fehlende Werte mit NaN und Zählen der NaN-Werte pro Spalte:")
    #print(missing_count_per_column)

    return dataset

def get_weather_data(zone):
    # Wetterstationen werden aggregiert -> Hauptstädte der Bundesländer (mit Ausnahme Hessen->Frankfurt statt Wiesbaden)
    # TransNetBW: Stuttgart Wetterstation (recht zentral)
    # 50Hertz: Hamburg, Berlin, Magdeburg, Dresden, Schwerin, Erfurt, Potsdam
    # Deutschland: Hamburg, Berlin, Magdeburg, Dresden, Schwerin, Erfurt, Potsdam, Stuttgart,
    #              München, Mainz, Saarbrücken, Wiesbaden/Frankfurt, Düsseldorf, Hannover, Bremen, Kiel
    if zone == "50hertz":
        states = ["Hamburg", "Berlin", "Magdeburg", "Dresden", "Schwerin", "Erfurt", "Potsdam"]
        print("Wetterdaten der Regelzone 50Hertz laden:")
    elif zone == "transnetbw":
        states = ["Stuttgart"]
        print("Wetterdaten der Regelzone TransNetBW laden:")
    elif zone == "de":
        states = ["Hamburg", "Berlin", "Magdeburg", "Dresden", "Schwerin", "Erfurt", "Potsdam", "Stuttgart",
                      "Muenchen", "Mainz", "Saarbruecken", "Frankfurt", "Duesseldorf", "Hannover", "Bremen", "Kiel"]
        print("Wetterdaten für Deutschland laden:")
    else:
        print("Keine Regelzone/Falsche Regelzone ausgewählt: Fortfahren mit Wetterdaten für Deutschland")
        states = ["Hamburg", "Berlin", "Magdeburg", "Dresden", "Schwerin", "Erfurt", "Potsdam", "Stuttgart",
                      "Muenchen", "Mainz", "Saarbruecken", "Frankfurt", "Duesseldorf", "Hannover", "Bremen", "Kiel"]

    datasets = []
    for state in states:
        file_path = f"{WEATHER_DATA_PATH}/tageswerte_{state}/Wetterdaten.txt"
        try:
            # Datei laden
            data = pd.read_csv(file_path, delimiter=';')
            print(f"Lade Daten von Wetterstation {state}... ")
            data = convertDatasets(data) # Bereinigen und Konvertieren/Selektieren der Spalten
            datasets.append(data)  # Füge den geladenen DataFrame der Liste hinzu
        except FileNotFoundError:
            print(f"Datei nicht gefunden: {file_path}")
        except Exception as e:
            print(f"Fehler beim Laden von {file_path}: {e}")
    # Kombiniere die Datensätze und berechne den Durchschnitt
    kombiniert = pd.concat(datasets)
    dataset = kombiniert.groupby(kombiniert.index).mean()  # Gruppiere nach Index und Durchschnitt aller Spalten berechnen
    return dataset

if __name__ == '__main__':
    zone = input("Regelzone? [ DE / TransNetBW / 50Hertz]: \n")
    zone = zone.lower()
    df = get_weather_data(zone)

    # Plot erstellen
    plt.figure(figsize=(12, 6))
    plt.plot(df.index, df['TMK'], color='blue')
    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit (Tage)")
    plt.ylabel("Tagesmitteltemp.")
    plt.title('Klima - Tagesmitteltemperaturen')
    plt.grid()
    # Plot anzeigen
    plt.show()





