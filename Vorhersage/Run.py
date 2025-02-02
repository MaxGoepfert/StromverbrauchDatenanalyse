import sys

import pandas as pd
import xgboost as xgb
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import spearmanr
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import Holiday_feature
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

import Seasonality
import Lag_features
from features import feature_engineering
import Klima
import Holiday_feature
import config

import openpyxl

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 2000)

ZEIT_SPALTE = "Datum von"
VERBRAUCH_SPALTE = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

def cleanData(data):
    dataset = data.copy()
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[ZEIT_SPALTE] = pd.to_datetime(dataset[ZEIT_SPALTE], dayfirst=True, errors='raise')
    # Umwandlung Integer
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[VERBRAUCH_SPALTE] = dataset[VERBRAUCH_SPALTE].str.replace(',', '.',
                                                                      regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[VERBRAUCH_SPALTE] = pd.to_numeric(dataset[VERBRAUCH_SPALTE])

    # Prüfen, ob ungültige Werte (NaN) existieren
    # missing_values1 = dataset[ZEIT_SPALTE].isnull().sum()
    # print(f"Fehlende Werte in der Spalte '{ZEIT_SPALTE}': {missing_values1}")
    # Prüfen, ob ungültige Werte (NaN) existieren
    # missing_values2 = dataset[VERBRAUCH_SPALTE].isnull().sum()
    # print(f"Fehlende Werte in der Spalte '{VERBRAUCH_SPALTE}': {missing_values2}")

    # ZEIT_SPALTE als Index setzen
    dataset.set_index(ZEIT_SPALTE, inplace=True)

    return dataset


### Features
def createFeatures(df_verbrauch, zone):
    df_verbrauch = df_verbrauch.copy()
    df_verbrauch = Seasonality.add_seasons(df_verbrauch)
    # Feiertage hinzufügen
    if zone == "50hertz":
        df_verbrauch = Holiday_feature.add_holidays_50Hertz(df_verbrauch)
        print("Feiertage für 50Hertz laden...")
    elif zone == "transnetbw":
        df_verbrauch = Holiday_feature.add_holidays_TransNetBW(df_verbrauch)
        print("Feiertage für TransNetBW laden...")
    elif zone == "de":
        df_verbrauch = Holiday_feature.add_holidays_de(df_verbrauch)
        print("Feiertage für Deutschland laden...")
    else:
        print("Keine Regelzone/Falsche Regelzone ausgewählt: Fortfahren mit Feiertage für Deutschland")
        df_verbrauch = Holiday_feature.add_holidays_de(df_verbrauch)
    df_verbrauch = Lag_features.add_lag(df_verbrauch, VERBRAUCH_SPALTE)

    return df_verbrauch

if __name__ == "__main__":

    ### Benutzereingabe zur Regelzonen-Auswahl
    zone = input("Bitte Regelzone auswählen [DE / TransNetBW / 50Hertz]: \n")
    zone = zone.lower()
    leak = input("Vorhersage auf tagesbasis mithilfe der Daten des Vortags erlauben? (Data Leak!!) [ J / N]: \n")


    ### Einlesen der Datensätze
    if zone == "de":
        data = pd.read_csv(config.DE_STROM_DATA_PATH, delimiter=';')
        print("Datensatz für Deutschland laden...")
    elif zone == "50hertz":
        data = pd.read_csv(config.HERTZ_STROM_DATA_PATH, delimiter=';')
        print("Datensatz für 50Hertz laden...")
    elif zone == "transnetbw":
        data = pd.read_csv(config.BW_STROM_DATA_PATH, delimiter=';')
        print("Datensatz für TransNetBW laden...")
    else:
        print("Keine Regelzone/Falsche Regelzone ausgewählt: Fortfahren mit Datensatz für Deutschland")
        data = pd.read_csv(config.DE_STROM_DATA_PATH, delimiter=';')

    dataset = cleanData(data)
    ### merge
    data_klima = Klima.get_weather_data(zone)
    dataset = pd.merge(dataset, data_klima, left_index=True, right_index=True,
                       how='inner')  # nur gemeinsame Datumswerte zur Sicherheit
    ### Features und Target
    dataset = createFeatures(dataset, zone)

    ### Diese Funktion gibt einige Analysen aus, im Zuge des Feature Engineering
    # Berechnet Korrelationen der Klimadaten und untersucht die Ausreißer im Zusammenhang mit den Feiertagen
    #feature_engineering(dataset)

    holiday_feature = []
    if zone == "50hertz":
        holiday_feature = ['is_holiday_BB', 'is_holiday_BE', 'is_holiday_MV', 'is_holiday_SN', 'is_holiday_ST',
                           'is_holiday_TH', 'is_holiday_HH',
                           ]
    else:
        holiday_feature = ['is_holiday']

    features = [
        *holiday_feature,
        'Weekday', 'Month',
        'Season',
        'Day_of_year',
        'lag_day',
        'lag_week',
        'lag_year',
        'lag_2year',
        'lag_3year',
        'is_weekend',
        'TMK', 'SDK', 'VPM'
    ]

    target = VERBRAUCH_SPALTE
    tss = TimeSeriesSplit(n_splits=4, test_size=365)
    num_split = 0
    all_mape = 0
    all_rmse = 0
    all_mae = 0
    for train_idx, val_idx in tss.split(dataset):
        ### splits
        train = dataset.iloc[train_idx]
        test = dataset.iloc[val_idx]

        # features und target
        x_train = train[features]
        y_train = train[target]
        x_test = test[features]
        y_test = test[target]

        # plot
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(train.index, train[VERBRAUCH_SPALTE], label='Training Set', color='red')
        ax.plot(test.index, test[VERBRAUCH_SPALTE], label='Test Set', color='blue')
        timestmp = "01-01-" + str(2020 + num_split)
        ax.axvline(pd.Timestamp(timestmp), color='black', ls='--', linewidth=2)
        ax.set_title('Test and Train Split')
        plt.ylabel('Stromverbrauch (in MWh)')
        plt.xlabel('Zeit')
        ax.legend(['Training Set', 'Test Set'])
        plt.show()
        """

        # model Deutschland
        model = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=600,
            max_depth=6,
            min_child_weight=10,
            gamma=0.3,
            colsample_bytree=0.8,
            learning_rate=0.01,
            reg_alpha=1,
            reg_lambda=3
        )
        # Array für die Vorhersagen
        predictions = []
        if leak == 'J':
            model.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)],
            verbose=50)
            predictions = model.predict(x_test)
        else:
            ### Rolling Window Methode -> iteratives Vorhersagen und Lag Feature jeweils aktualisiern (lag_day, lag_week)
            model.fit(x_train, y_train, eval_set=[(x_train, y_train)],  # fir nur auf Trainingsdaten
                       verbose=50)
            # Initialisiere mit echten historischen Werten für ersten Tag
            current_input = x_test.iloc[0].copy()  # erste Zeile des Testdatensatzes
            print(f"current input: {current_input}")
            # Iterativer Vorhersagen mit jeweils nächstem Tag
            for i in range(len(x_test)):
                input_pred = current_input.values.reshape(1, -1) # predict() erwartet 2D Matrix statt 1D Array
                # Vorhersage machen und zu predictions hinzufügen
                pred = model.predict(input_pred)[0] # [0] weil return ist sonst ein Array
                predictions.append(pred)
                # Lag-Features für die nächste Vorhersage
                if i + 1 < len(x_test):
                    current_input = x_test.iloc[i + 1].copy()  # Nächster Tag
                    current_input['lag_day'] = pred  # Lag_day wird durch die letzte Vorhersage ersetzt
                    # Ähnlich mit Lag_week -> Entweder historische Daten oder Vorhersage von vor 7 Tagen nehmen
                    if len(predictions) >= 7:
                        current_input['lag_week'] = predictions[-7]

        ### Evaluate
        rmse = np.sqrt(mean_squared_error(y_test, predictions))
        mae = mean_absolute_error(y_test, predictions)
        mape = mean_absolute_percentage_error(y_test, predictions)
        all_mape += mape
        all_rmse += rmse
        all_mae += mae
        num_split += 1
        print(f"Evaluation for the fold: {num_split}:\n")
        print(f"Evaluation: Root mean squared error is: {rmse: .3f}")
        print(f"Evaluation: Mean absolute error is: {mae: .3f}")
        print(f"Evaluation: Mean absolute percentage error is: {mape * 100: .3f} %\n")

    print(f"Overall Evaluation: Root mean squared error is: {all_rmse / num_split: .3f}")
    print(f"Oberall Evaluation: Mean absolute error is: {all_mae / num_split: .3f}")
    print(f"Overall Evaluation: Mean absolute percentage error is: {all_mape * 100 / num_split: .3f} %")

    # Feature Importance Plot
    # xgb.plot_importance(model, importance_type='gain')  # Alternativ: 'gain', 'weight', 'cover'
    # plt.show()

    ### Trainingsdatensatz als Excel abspeichern -> Dafür braucht man das Modul openpyxl!!!
    # trainings_daten = train.copy()
    # trainings_daten = trainings_daten.reset_index()
    # trainings_daten.to_excel('trainings_daten.xlsx', index=False)

    # Plotten
    fig, ax = plt.subplots(figsize=(14, 8))  # Setze die Größe des Plots

    # Plot der Trainingsdaten und Vorhersagen für 2023
    ax.plot(train.index, train[VERBRAUCH_SPALTE], label='Tatsächliche Werte (Trainingsdaten 2017-2023)', color='blue')
    ax.axvline(pd.Timestamp('01-01-2023'), color='black', ls='--', linewidth=2)
    ax.axvline(pd.Timestamp('01-01-2022'), color='black', ls='--', linewidth=2)
    ax.axvline(pd.Timestamp('01-01-2021'), color='black', ls='--', linewidth=2)
    ax.axvline(pd.Timestamp('01-01-2020'), color='black', ls='--', linewidth=2)
    # Plot der Vorhersagen
    ax.plot(test.index, predictions, label='Vorhersagen 2023-2024', color='red')

    # Achsen und Titel
    ax.set_title('Stromverbrauchsdaten mit Vorhersagen für 2023')
    plt.ylabel('Stromverbrauch (in MWh)')
    plt.xlabel('Datum')
    # ax.legend(['Training Set', 'Test Set'])
    # Legende
    plt.legend()
    # Zeige das Diagramm an
    plt.show()

    # plot nur Testdaten 2023 vs. tatsächliche Werte
    plt.figure(figsize=(16, 8))
    plt.plot(test.index, predictions, label="Vorhersage", color="red", linestyle="--")
    plt.plot(test.index, y_test, label="Tatsächliche Werte (Testdaten 2023)", color="blue")
    plt.title('Stromverbrauchsdaten und Vorhersagen für 2023')
    plt.ylabel('Stromverbrauch (in MWh)')
    plt.xlabel('Datum')
    # Legende
    plt.legend()
    # Zeige das Diagramm an
    plt.show()

    ### Save model for later
    # model.save_model(MODEL_PATH)
