import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from Vorhersage.config import DE_STROM_DATA_PATH, DE_STROM_PROG_DATA_PATH
from matplotlib import pyplot as plt

ZEIT_SPALTE = "Datum von"
VERBRAUCH_SPALTE = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"
def cleanData(data):
    dataset = data.copy()
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[ZEIT_SPALTE] = pd.to_datetime(dataset[ZEIT_SPALTE], dayfirst=True, errors='raise')
    # Umwandlung Integer
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[VERBRAUCH_SPALTE] = pd.to_numeric(dataset[VERBRAUCH_SPALTE])

    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values1 = dataset[ZEIT_SPALTE].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{ZEIT_SPALTE}': {missing_values1}")
    missing_values2 = dataset[VERBRAUCH_SPALTE].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{VERBRAUCH_SPALTE}': {missing_values2}")

    # ZEIT_SPALTE als Index setzen
    dataset.set_index(ZEIT_SPALTE, inplace=True)

    return dataset


if __name__ == "__main__":

    dataReal = pd.read_csv(DE_STROM_DATA_PATH, delimiter=';')
    dataProg = pd.read_csv(DE_STROM_PROG_DATA_PATH, delimiter=';')

    ### Clean data
    datasetReal = cleanData(dataReal)
    datasetProg = cleanData(dataProg)

    datasetReal = datasetReal.loc[datasetReal.index >= '01-01-2023']

    target = VERBRAUCH_SPALTE
    y_real = datasetReal[target]
    y_prog = datasetProg[target]

    rmse = np.sqrt(mean_squared_error(y_real, y_prog))
    mae = mean_absolute_error(y_real, y_prog)
    mape = mean_absolute_percentage_error(y_real, y_prog)
    print(f"Evaluation: Root mean squared error is: {rmse: .3f}")
    print(f"Evaluation: Mean absolute error is: {mae: .3f}")
    print(f"Evaluation: Mean absolute percentage error is: {mape * 100: .3f} %")

    ### Plotten
    plt.figure(figsize=(16, 8))  # Setze die Größe des Plots

    # Plot der tatsächlichen Werte
    plt.plot(datasetReal.index, y_real, label='Tatsächliche Werte', color='blue')

    # Plot der Vorhersagen
    plt.plot(datasetProg.index, y_prog, label='SMARD Vorhersagen', color='red', linestyle='--')

    # Achsen und Titel
    plt.ylim(0.5e6, 2e6)
    plt.xlabel('Datum')
    plt.ylabel('Stromverbrauch (in Mio MWh)')
    plt.title('Tatsächliche Werte vs. SMARD Vorhersagen für 2023')

    # anzeigen
    plt.legend()
    plt.show()
