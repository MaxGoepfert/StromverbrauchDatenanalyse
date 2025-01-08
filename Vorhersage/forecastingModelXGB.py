import pandas as pd
import xgboost as xgb
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
import holidays
from Klima import get_weather_data
from config import BW_STROM_DATA_PATH, HERTZ_STROM_DATA_PATH, DE_STROM_DATA_PATH

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 2000)

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

# Lags hinzufügen
def add_lag(df):
    dictOfLastSpalte = df[last_spalte].to_dict()
    # zieht von Datum ein Jahr ab und gibt Wert von diesem Datum zurück
    df['lag_year'] = (df.index - pd.Timedelta('364 days')).map(dictOfLastSpalte)
    df['lag_week'] = (df.index - pd.Timedelta('7 days')).map(dictOfLastSpalte)
    df['lag_day_before'] = (df.index - pd.Timedelta('1 days')).map(dictOfLastSpalte)
    # gleitenden Durchschnitt hinzufügen
    df['rolling_mean_week'] = df[last_spalte].rolling(window=7).mean()
    df['rolling_mean'] = df[last_spalte].rolling(window=30).mean()
    return df

# Feiertage hinzufügen
def add_holidays(df):
    de_holidays = holidays.Germany()
    # Feature: Ist der Tag ein Feiertag?
    df['is_holiday'] = df.index.to_series().apply(lambda x: x in de_holidays)
    return df

### Wetterdaten hinzufügen (TO-DO)

# Jahreszeiten hinzufügen (ungefähr per Monate)
def add_seasons(month):
    if month in [12, 1, 2]:
        return 1 # winter
    elif month in [3, 4, 5]:
        return 2 # Frühling
    elif month in [6, 7, 8]:
        return 3 # Sommer
    else:
        return 4 # Herbst

### Features
def createFeatures(df_verbrauch):
    df_verbrauch = df_verbrauch.copy()
    df_verbrauch['Day_of_year'] = df_verbrauch.index.day_of_year
    df_verbrauch['Weekday'] = df_verbrauch.index.weekday
    df_verbrauch['Month'] = df_verbrauch.index.month
    df_verbrauch['Season'] = df_verbrauch.index.month.map(add_seasons)
    df_verbrauch['is_weekend'] = df_verbrauch.index.weekday.isin([5, 6])  # Samstag (5) und Sonntag (6)
    # Lags hinzufügen
    df_verbrauch = add_lag(df_verbrauch)
    # Feiertage hinzufügen
    df_verbrauch = add_holidays(df_verbrauch)

    return df_verbrauch

if __name__ == "__main__":

    data = pd.read_csv(DE_STROM_DATA_PATH, delimiter=';')
    data_50Hertz = pd.read_csv(HERTZ_STROM_DATA_PATH, delimiter=';')
    data_TransNetBW = pd.read_csv(BW_STROM_DATA_PATH, delimiter=';')
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

    ### Clean data
    #dataset = cleanData(data_50Hertz, zeit_spalte, last_spalte)
    #dataset = cleanData(data_TransNetBW, zeit_spalte, last_spalte)
    dataset = cleanData(data, zeit_spalte, last_spalte)

    ### merge
    data_klima = get_weather_data()
    # DataFrames: dataset1, dataset2
    dataset = pd.merge(dataset, data_klima, left_index=True, right_index=True,
                      how='inner')  # nur gemeinsame Datumswerte zur Sicherheit

    ### Features und Target
    dataset = createFeatures(dataset)
    #print(dataset.tail(20))
    print(dataset.columns)
    features = ['Day_of_year', 'Weekday', 'Month', 'Season',
                'lag_year', 'lag_week', 'lag_day_before',
                'is_holiday', 'is_weekend',
                'rolling_mean', 'rolling_mean_week', 'TMK',]
    # TO DO: Wetterdaten
    target = last_spalte

    ### Train and Test Split

    # so oder einfach die zwei Datensätze nehmen
    train = dataset.loc[dataset.index < '2023-01-01']
    test = dataset.loc[dataset.index >= '2023-01-01']
    print(train.head())
    print(test.head())
    # plot
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(train.index, train[last_spalte], label='Training Set', color='red')
    ax.plot(test.index, test[last_spalte], label='Test Set', color='blue')
    ax.axvline(pd.Timestamp('01-01-2023'), color='black', ls='--', linewidth=2)
    ax.set_title('Test and Train Split')
    plt.ylabel('Stromverbrauch (in MWh)')
    plt.xlabel('Zeit')
    ax.legend(['Training Set', 'Test Set'])
    plt.show()
    """
    ### Train model
    x_train = train[features]
    y_train = train[target]

    x_test = test[features]
    y_test = test[target]

    model = xgb.XGBRegressor(
        max_depth=8,
        min_child_weight=10,
        gamma=0.3,
        subsample=0.7,
        colsample_bytree=0.7,
        learning_rate=0.005,  # gesenkt
        n_estimators=3000,
        reg_alpha=1,
        reg_lambda=5,
        early_stopping_rounds=50,
        objective='reg:squarederror'
        )

    model.fit(x_train, y_train, eval_set=[(x_train, y_train), (x_test, y_test)], verbose=50)

    ### Evaluate
    y_pred = model.predict(x_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    mape = mean_absolute_percentage_error(y_test, y_pred)
    print(f"Evaluation: Root mean squared error is: {rmse: .3f}")
    print(f"Evaluation: Mean absolute error is: {mae: .3f}")
    print(f"Evaluation: Mean absolute percentage error is: {mape * 100: .3f} %")


    ### Save model for later
    #model.save_model('Vorhersage/modelXGB.json')

    ### and use again
    #model_new = xgb.XGBRegressor()
    #model_new.load_model('Vorhersage/modelXGB.json')



