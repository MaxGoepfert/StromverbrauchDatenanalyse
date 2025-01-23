import pandas as pd
import xgboost as xgb
import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import holidays
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

from Klima import get_weather_data
from config import BW_STROM_DATA_PATH, HERTZ_STROM_DATA_PATH, DE_STROM_DATA_PATH, MODEL_PATH

import openpyxl

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 2000)


def cleanData(data, zeit_spalte, last_spalte):
    dataset = data.copy()
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[zeit_spalte] = pd.to_datetime(dataset[zeit_spalte], dayfirst=True, errors='raise')
    # Umwandlung Integer
    dataset[last_spalte] = dataset[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[last_spalte] = dataset[last_spalte].str.replace(',', '.',
                                                            regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[last_spalte] = pd.to_numeric(dataset[last_spalte])

    # Prüfen, ob ungültige Werte (NaN) existieren
    #missing_values1 = dataset[zeit_spalte].isnull().sum()
    #print(f"Fehlende Werte in der Spalte '{zeit_spalte}': {missing_values1}")
    # Prüfen, ob ungültige Werte (NaN) existieren
    #missing_values2 = dataset[last_spalte].isnull().sum()
    #print(f"Fehlende Werte in der Spalte '{last_spalte}': {missing_values2}")

    # zeit_spalte als Index setzen
    dataset.set_index(zeit_spalte, inplace=True)

    return dataset


# Lags hinzufügen
def add_lag(df, leak):
    dictOfLastSpalte = df[last_spalte].to_dict()
    # zieht von Datum ein Jahr ab und gibt Wert von diesem Datum zurück
    if leak == "J":
        print("Laden der Daten des Vortages...")
        df['lag_day'] = (df.index - pd.Timedelta('1 days')).map(dictOfLastSpalte)
        df['lag_week'] = (df.index - pd.Timedelta('7 days')).map(dictOfLastSpalte)
    df['lag_year'] = (df.index - pd.Timedelta('364 days')).map(dictOfLastSpalte)
    df['lag_2year'] = (df.index - pd.Timedelta('728 days')).map(dictOfLastSpalte)
    df['lag_3year'] = (df.index - pd.Timedelta('1092 days')).map(dictOfLastSpalte)

    """
    ###  Standartisierung (optional)
    lag_features = df[['lag_year', 'lag_2year', 'lag_3year']]
    # Standardisierung der Lag-Features
    scaler = StandardScaler()
    scaled_lag_features = scaler.fit_transform(lag_features)

    # DataFrame umwandeln
    scaled_lag_df = pd.DataFrame(
        scaled_lag_features,
        index=lag_features.index,
        columns=['lag_year', 'lag_2year', 'lag_3year']
    )
    # Lag-Features kombinieren
    df[['lag_year', 'lag_2year', 'lag_3year']] = scaled_lag_df
    """
    return df


# Feiertage hinzufügen
def add_holidays(df):
    de_holidays = holidays.Germany()
    # Feature: Ist der Tag ein Feiertag?
    df['is_holiday'] = df.index.to_series().apply(lambda x: x in de_holidays)
    df['is_holiday'] = df['is_holiday'].astype(int)
    return df


def add_holidays_50Hertz(df):
    for states in ["BB", "BE", "MV", "SN", "ST", "TH", "HH"]:
        holiday_states = holidays.Germany(state=states)
        df['is_holiday_' + states] = df.index.to_series().apply(lambda x: x in holiday_states)
        df['is_holiday_' + states] = df['is_holiday_' + states].astype(int)
    return df


def add_holidays_TransNetBW(df):
    de_holidays = holidays.Germany(state="BW")
    # Feature: Ist der Tag ein Feiertag?
    df['is_holiday'] = df.index.to_series().apply(lambda x: x in de_holidays)
    df['is_holiday'] = df['is_holiday'].astype(int)
    return df


# Jahreszeiten hinzufügen (ungefähr per Monate)
def add_seasons(month):
    if month in [12, 1, 2]:
        return 1  # winter
    elif month in [3, 4, 5]:
        return 2  # Frühling
    elif month in [6, 7, 8]:
        return 3  # Sommer
    else:
        return 4  # Herbst


### Features
def createFeatures(df_verbrauch, zone, leak):
    df_verbrauch = df_verbrauch.copy()
    df_verbrauch['Day_of_year'] = df_verbrauch.index.day_of_year
    df_verbrauch['Weekday'] = df_verbrauch.index.weekday
    df_verbrauch['Month'] = df_verbrauch.index.month
    df_verbrauch['Season'] = df_verbrauch.index.month.map(add_seasons)
    df_verbrauch['is_weekend'] = df_verbrauch.index.weekday.isin([5, 6])  # Samstag (5) und Sonntag (6)
    df_verbrauch['is_weekend'] = df_verbrauch['is_weekend'].astype(int)
    # Feiertage hinzufügen
    if zone == "50hertz":
        df_verbrauch = add_holidays_50Hertz(df_verbrauch)
        print("Feiertage für 50Hertz laden...")
    elif zone == "transnetbw":
        df_verbrauch = add_holidays_TransNetBW(df_verbrauch)
        print("Feiertage für TransNetBW laden...")
    elif zone == "de":
        df_verbrauch = add_holidays(df_verbrauch)
        print("Feiertage für Deutschland laden...")
    else:
        print("Keine Regelzone/Falsche Regelzone ausgewählt: Fortfahren mit Feiertage für Deutschland")
        df_verbrauch = add_holidays(df_verbrauch)
    df_verbrauch = add_lag(df_verbrauch, leak)
    return df_verbrauch


if __name__ == "__main__":

    ### Benutzeriengabe zur Regelzonen-Auswahl
    zone = input("Bitte Regelzone auswählen [DE / TransNetBW / 50Hertz]: \n")
    zone = zone.lower()
    leak = input("Vorhersage auf tagesbasis mithilfe der Daten des Vortags erlauben? (Data Leak!!) [ J / N]: \n")




    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

    ### Einlesen der Datensätze
    if zone == "de":
        data = pd.read_csv(DE_STROM_DATA_PATH, delimiter=';')
        print("Datensatz für Deutschland laden...")
    elif zone == "50hertz":
        data = pd.read_csv(HERTZ_STROM_DATA_PATH, delimiter=';')
        print("Datensatz für 50Hertz laden...")
    elif zone == "transnetbw":
        data = pd.read_csv(BW_STROM_DATA_PATH, delimiter=';')
        print("Datensatz für TransNetBW laden...")
    else:
        print("Keine Regelzone/Falsche Regelzone ausgewählt: Fortfahren mit Datensatz für Deutschland")
        data = pd.read_csv(DE_STROM_DATA_PATH, delimiter=';')

    dataset = cleanData(data, zeit_spalte, last_spalte)
    ### merge
    data_klima = get_weather_data(zone)
    dataset = pd.merge(dataset, data_klima, left_index=True, right_index=True,
                       how='inner')  # nur gemeinsame Datumswerte zur Sicherheit
    ### Features und Target
    dataset = createFeatures(dataset, zone, leak)

    holiday_feature = []
    if zone == "50hertz":
        holiday_feature = ['is_holiday_BB', 'is_holiday_BE', 'is_holiday_MV', 'is_holiday_SN', 'is_holiday_ST',
                           'is_holiday_TH', 'is_holiday_HH',
                           ]
    else:
        holiday_feature = ['is_holiday']

    leak_lags = []
    if leak == "J":
        leak_lags = ['lag_day', 'lag_week']
    else:
        print("Ohne Data Leak starten (Daten vom Vortag)...")
    features = [
        *holiday_feature,
        'Weekday', 'Month',
        'Season',
        'Day_of_year',
        *leak_lags,
        'lag_year',
        'lag_2year',
        'lag_3year',
        'is_weekend',
        'TMK', 'SDK',
        ]

    target = last_spalte
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
        ax.plot(train.index, train[last_spalte], label='Training Set', color='red')
        ax.plot(test.index, test[last_spalte], label='Test Set', color='blue')
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
            max_depth=6,  # 8
            min_child_weight=5,  # 10
            gamma=0.3,
            subsample=0.8,
            colsample_bytree=0.8,  # 0.7
            learning_rate=0.01,  # 0.005
            n_estimators=4000,
            reg_alpha=1,
            reg_lambda=3,
            early_stopping_rounds=50,
            objective='reg:squarederror'
        )
        # fit
        model.fit(x_train, y_train,
                  eval_set=[(x_train, y_train), (x_test, y_test)],
                  verbose=50)

        ### Evaluate
        y_pred = model.predict(x_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mae = mean_absolute_error(y_test, y_pred)
        mape = mean_absolute_percentage_error(y_test, y_pred)
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
    #xgb.plot_importance(model, importance_type='gain')  # Alternativ: 'gain', 'weight', 'cover'
    #plt.show()

    ### Trainingsdatensatz als Excel abspeichern -> Dafür braucht man das Modul openpyxl!!!
    #trainings_daten = train.copy()
    #trainings_daten = trainings_daten.reset_index()
    #trainings_daten.to_excel('trainings_daten.xlsx', index=False)

    # Plotten
    fig, ax = plt.subplots(figsize=(14, 8))  # Setze die Größe des Plots

    # Plot der tatsächlichen Werte
    ax.plot(train.index, train[last_spalte], label='Tatsächliche Werte (Trainingsdaten 2017-2023)', color='blue')
    ax.axvline(pd.Timestamp('01-01-2023'), color='black', ls='--', linewidth=2)
    ax.axvline(pd.Timestamp('01-01-2022'), color='black', ls='--', linewidth=2)
    ax.axvline(pd.Timestamp('01-01-2021'), color='black', ls='--', linewidth=2)
    ax.axvline(pd.Timestamp('01-01-2020'), color='black', ls='--', linewidth=2)
    # Plot der Vorhersagen
    ax.plot(test.index, y_pred, label='Vorhersagen 2023-2024', color='red')

    # Achsen und Titel
    #ax.ylim(0.5e6, 2e6)
    ax.set_title('Stromverbrauchsdaten mit Vorhersagen für 2023')
    plt.ylabel('Stromverbrauch (in MWh)')
    plt.xlabel('Datum')
    #ax.legend(['Training Set', 'Test Set'])
    # Legende
    plt.legend()
    # Zeige das Diagramm an
    plt.show()


    # plot Testdaten 2023
    plt.figure(figsize=(16, 8))
    plt.plot(test.index, y_pred, label="Vorhersage", color="red", linestyle="--")
    plt.plot(test.index, y_test, label="Tatsächliche Werte (Testdaten 2023)", color="blue")
    plt.title('Stromverbrauchsdaten und Vorhersagen für 2023')
    plt.ylabel('Stromverbrauch (in MWh)')
    plt.xlabel('Datum')
    #ax.legend(['Training Set', 'Test Set'])
    # Legende
    plt.legend()
    # Zeige das Diagramm an
    plt.show()

    # Korrelation berechnen
    correlation_tmk = dataset[last_spalte].corr(dataset['TMK'])
    correlation_sdk = dataset[last_spalte].corr(dataset['SDK'])
    # Ergebnis anzeigen
    print(f"Korrelation zwischen Stromverbrauch und Tagesmitteltemperatur: {correlation_tmk:.2f}")
    print(f"Korrelation zwischen Stromverbrauch und Sonnenstunden: {correlation_sdk:.2f}")


    ### Save model for later
    # model.save_model(MODEL_PATH)
