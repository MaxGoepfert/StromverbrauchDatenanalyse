import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from config import WEATHER_DATA_PATH
def get_weather_data():
    data = pd.read_csv(WEATHER_DATA_PATH, delimiter=';')

    zeit_spalte = 'MESS_DATUM'
    temp_avg_spalte = 'TMK' # Tagesdurchschnittstemperatur
    temp_max_spalte = 'TXK' # Tageshöchsttemperatur
    temp_min_spalte = 'TNK' # Tagesniedrigsttemperatur
    sonne_h_spalte = 'SDK' # Sonnenscheindauer (in Stunden)
    niederschlag_spalte = 'RSK' # Menge an Niederschlag in mm
    niederschlag_ordinal_spalte = 'RSKF' # Art/Stärke des Niederschlags 0-9 --> 0 trocken, 9 Extrem-ereignis
    dataset = data.copy()
    dataset.columns = dataset.columns.str.strip()

    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[zeit_spalte] = pd.to_datetime(dataset[zeit_spalte], format='%Y%m%d', errors='raise')

    # zeit_spalte als Index setzen
    dataset.set_index(zeit_spalte, inplace=True)
    # Nur nötigen Zeitraum behalten
    dataset = dataset.loc[dataset.index >= '2017-01-01']
    dataset = dataset[[temp_avg_spalte, temp_max_spalte, temp_min_spalte,
                       sonne_h_spalte, niederschlag_spalte, niederschlag_ordinal_spalte]]

    # Ersetzen von -999 durch NaN
    dataset.replace(-999, np.nan, inplace=True)

    # Identifizieren von NaN-Werten
    missing_values = dataset.isna()

    # Zählen der NaN-Werte
    missing_count_per_column = missing_values.sum()

    print("\nErsetzte fehlende Werte mit NaN und Zählen der NaN-Werte pro Spalte:")
    print(missing_count_per_column)

    outliers = (dataset < -20) | (dataset > 40)

    print("Identifizierte Ausreißer (Werte unter -100 oder über 100):")
    print(outliers.sum())

    return dataset

if __name__ == '__main__':
    df = get_weather_data()
    """
    # Plot erstellen
    plt.figure(figsize=(12, 6))  # Größe des Plots festlegen
    plt.plot(df.index, df['RSK'], color='blue')

    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit (Tage)")
    plt.ylabel("Tagesmitteltemp.")  # Einheit anpassen, falls bekannt
    plt.title('Klima - Tagesmitteltemperaturen DE')

    plt.grid()
    # Plot anzeigen
    plt.show()
    """




