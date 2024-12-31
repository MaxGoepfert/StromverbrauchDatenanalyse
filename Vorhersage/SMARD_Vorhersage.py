import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error


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

    # zeit_spalte als Index setzen
    dataset.set_index(zeit_spalte, inplace=True)

    return dataset

if __name__ == "__main__":
    dataPathReal = "/home/maximiliangoepfert/PycharmProjects/StromverbrauchDatenanalyse/data/Realisierter_Stromverbrauch_2017-2024_Tag.csv"
    dataPathProg = "/home/maximiliangoepfert/PycharmProjects/StromverbrauchDatenanalyse/data/Prognostizierter_Stromverbrauch_2023-2024_Tag.csv"
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

    dataReal = pd.read_csv(dataPathReal, delimiter=';')
    dataProg = pd.read_csv(dataPathProg, delimiter=';')

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


