import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import config
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
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].replace("-", np.nan) # Es gibt einen Null Wert in Regelzone TransNetBW/50Hertz
    dataset[VERBRAUCH_SPALTE] = pd.to_numeric(dataset[VERBRAUCH_SPALTE])
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].ffill()

    #dataset = dataset.apply(lambda col: col.fillna(col.mean()), axis=0) # NaN Wert(e) mit Mittelwert auffüllen

    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values1 = dataset[ZEIT_SPALTE].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{ZEIT_SPALTE}': {missing_values1}")
    missing_values2 = dataset[VERBRAUCH_SPALTE].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{VERBRAUCH_SPALTE}': {missing_values2}")

    # ZEIT_SPALTE als Index setzen
    dataset.set_index(ZEIT_SPALTE, inplace=True)

    return dataset


if __name__ == "__main__":
    zone = input("Regelzone oder DE? [de / bw / hertz]\n")
    dataReal = []
    dataProg = []
    if zone == "de":
        dataReal = pd.read_csv(config.DE_STROM_DATA_PATH, delimiter=';')
        dataProg = pd.read_csv(config.DE_STROM_PROG_DATA_PATH, delimiter=';')

    elif zone == "bw":
        dataReal = pd.read_csv(config.BW_STROM_DATA_PATH, delimiter=';')
        dataProg = pd.read_csv(config.BW_STROM_PROG_DATA_PATH, delimiter=';')
    elif zone == "hertz":
        dataReal = pd.read_csv(config.HERTZ_STROM_DATA_PATH, delimiter=';')
        dataProg = pd.read_csv(config.HERTZ_STROM_PROG_DATA_PATH, delimiter=';')
    else:
        dataReal = pd.read_csv(config.DE_STROM_DATA_PATH, delimiter=';')
        dataProg = pd.read_csv(config.DE_STROM_PROG_DATA_PATH, delimiter=';')

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

    plt.xlabel('Datum')
    plt.ylabel('Stromverbrauch (in Mio MWh)')
    plt.title(f'Tatsächliche Werte vs. SMARD Vorhersagen für 2023 (zone: {zone})')

    # anzeigen
    plt.legend()
    plt.show()
