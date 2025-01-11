import xgboost as xgb
from matplotlib import pyplot as plt
import pandas as pd
from config import BW_STROM_DATA_PATH, HERTZ_STROM_DATA_PATH, DE_STROM_DATA_PATH, MODEL_PATH
from forecastingModelXGB import cleanData, get_weather_data, createFeatures

zeit_spalte = "Datum von"
last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"
target = last_spalte
features = ['Weekday', 'Month', 'Season', 'Day_of_year',
            'lag_year', 'lag_week', 'lag_day_before',
            'is_holiday', 'is_weekend',
            'rolling_mean', 'rolling_mean_week',
            'TMK', 'SDK']


if __name__ == "__main__":
    model_new = xgb.XGBRegressor()
    model_new.load_model(MODEL_PATH)

    data = pd.read_csv(DE_STROM_DATA_PATH, delimiter=';')
    #data_50Hertz = pd.read_csv(HERTZ_STROM_DATA_PATH, delimiter=';')
    #data_TransNetBW = pd.read_csv(BW_STROM_DATA_PATH, delimiter=';')

    ### Clean data
    # dataset = cleanData(data_50Hertz, zeit_spalte, last_spalte)
    # dataset = cleanData(data_TransNetBW, zeit_spalte, last_spalte)
    dataset = cleanData(data, zeit_spalte, last_spalte)

    ### merge
    data_klima = get_weather_data()
    # DataFrames: dataset1, dataset2
    dataset = pd.merge(dataset, data_klima, left_index=True, right_index=True,
                       how='inner')  # nur gemeinsame Datumswerte zur Sicherheit
    print(dataset.head())
    dataset = createFeatures(dataset)

    test = dataset.loc[dataset.index >= '2023-01-01']
    x_test = test[features]
    y_test = test[target]
    y_pred = model_new.predict(x_test)

    # Plotten
    plt.figure(figsize=(10, 8))  # Setze die Größe des Plots

    # Plot der tatsächlichen Werte
    plt.plot(test.index, y_test, label='Tatsächliche Werte', color='blue')

    # Plot der Vorhersagen
    plt.plot(test.index, y_pred, label='Vorhersagen', color='red', linestyle='--')

    # Achsen und Titel
    plt.xlabel('Datum')
    plt.ylabel('Stromverbrauch')
    plt.title('Tatsächliche Werte vs. Vorhersagen für 2023')
    # Legende
    plt.legend()
    # Zeige das Diagramm an
    plt.show()

