import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from Vorhersage.config import DE_STROM_DATA_PATH, DE_STROM_PROG_DATA_PATH
from matplotlib import pyplot as plt

def cleanData(data, zeit_spalte, last_spalte):
    dataset = data.copy()
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[zeit_spalte] = pd.to_datetime(dataset[zeit_spalte], dayfirst=True, errors='raise')
    # Umwandlung Integer
    dataset[last_spalte] = dataset[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[last_spalte] = dataset[last_spalte].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[last_spalte] = pd.to_numeric(dataset[last_spalte])

    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values1 = dataset[zeit_spalte].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{zeit_spalte}': {missing_values1}")
    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values2 = dataset[last_spalte].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{last_spalte}': {missing_values2}")

    # ZEIT_SPALTE als Index setzen
    dataset.set_index(zeit_spalte, inplace=True)

    return dataset

if __name__ == "__main__":
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

    dataReal = pd.read_csv(DE_STROM_DATA_PATH, delimiter=';')
    dataProg = pd.read_csv(DE_STROM_PROG_DATA_PATH, delimiter=';')

    ### Clean data
    datasetReal = cleanData(dataReal, zeit_spalte, last_spalte)
    datasetProg = cleanData(dataProg, zeit_spalte, last_spalte)

    datasetReal =  datasetReal.loc[datasetReal.index >= '01-01-2023']

    target = last_spalte
    y_real = datasetReal[target]
    y_prog = datasetProg[target]

    rmse = np.sqrt(mean_squared_error(y_real, y_prog))
    mae = mean_absolute_error(y_real, y_prog)
    mape = mean_absolute_percentage_error(y_real, y_prog)
    print(f"Evaluation: Root mean squared error is: {rmse: .3f}")
    print(f"Evaluation: Mean absolute error is: {mae: .3f}")
    print(f"Evaluation: Mean absolute percentage error is: {mape * 100: .3f} %")

    # Plotten
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
    # Legende
    plt.legend()
    # Zeige das Diagramm an
    plt.show()



