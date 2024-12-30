import pandas as pd
import matplotlib.pyplot as plt
import xgboost as xgb
import numpy as np
from sklearn.metrics import mean_squared_error
import holidays

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 500)

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
    dataPath = "/home/maximiliangoepfert/PycharmProjects/StromverbrauchDatenanalyse/data/Realisierter_Stromverbrauch_2017-2024_Tag.csv"
    #dataPath2 = "data/Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
    #dataPath3 = "data/Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"

    data = pd.read_csv(dataPath, delimiter=';')
    #data_50Hertz = pd.read_csv(dataPath2, delimiter=';')
    #data_TransNetBW= pd.read_csv(dataPath3, delimiter=';')
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

    ### Clean data
    #cleanData(data_50Hertz, zeit_spalte, last_spalte)
    #cleanData(data_TransNetBW, zeit_spalte, last_spalte)
    dataset = cleanData(data, zeit_spalte, last_spalte)


    # Lags (optional)
    def add_lag(df):
        dictOfLastSpalte = df[last_spalte].to_dict()
        # zieht von Datum ein Jahr ab und gibt Wert von diesem Datum zurück
        df['lag_year'] = (df.index - pd.Timedelta('364 days')).map(dictOfLastSpalte)
        df['lag_week'] = (df.index - pd.Timedelta('7 days')).map(dictOfLastSpalte)
        df['lag_day_before'] = (df.index - pd.Timedelta('1 days')).map(dictOfLastSpalte)
        # oder zB
        #df['shift'] = df.index.shift(7)
        df['rolling_mean_week'] = df[last_spalte].rolling(window=7).mean()
        df['rolling_mean'] = df[last_spalte].rolling(window=30).mean()
        return df

    # Feiertage hinzufügen (TO-DO)
    def add_holidays(df):
        de_holidays = holidays.Germany()
        # Feature: Ist der Tag ein Feiertag?
        df['is_holiday'] = df.index.to_series().apply(lambda x: x in de_holidays)
        return df

        # Wetterdaten hinzufügen (TO-DO)

    ### Features
    def createFeatures(df_verbrauch):
        df_verbrauch = df_verbrauch.copy()
        df_verbrauch['Wochentag'] = df_verbrauch.index.weekday
        df_verbrauch['Monat'] = df_verbrauch.index.month
        df_verbrauch['Quartal'] = df_verbrauch.index.quarter
        df_verbrauch['is_weekend'] = df_verbrauch.index.weekday.isin([5, 6])  # Samstag (5) und Sonntag (6)
        # Lags hinzufügen
        df_verbrauch = add_lag(df_verbrauch)
        # Feiertage hinzufügen
        df_verbrauch = add_holidays(df_verbrauch)

        return df_verbrauch


    dataset = createFeatures(dataset)
    print(dataset.tail(20))
    print(dataset.columns)
    features = ['Wochentag', 'Monat', 'Quartal',
                'lag_year','lag_week', 'lag_day_before',
                'is_holiday', 'is_weekend',
                'rolling_mean', 'rolling_mean_week']
    target = last_spalte

    ### Train and Test Split

    # so oder einfach die zwei Datensätze nehmen
    train = dataset.loc[dataset.index < '01-01-2023']
    test = dataset.loc[dataset.index >= '01-01-2023']
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
    X_train = train[features]
    y_train = train[target]

    X_test = test[features]
    y_test = test[target]

    reg = xgb.XGBRegressor(
        max_depth=8,
        min_child_weight=10,
        gamma=0.3,
        subsample=0.7,
        colsample_bytree=0.7,
        learning_rate=0.005,  # gesenkt
        n_estimators=3000,
        reg_alpha=1,
        reg_lambda=5,
        early_stopping_rounds=20,
        objective='reg:squarederror'
        )

    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=50)

    ### Evaluate
    y_pred = reg.predict(X_test)
    score = np.sqrt(mean_squared_error(y_test, y_pred))

    ### Save model for later
    #reg.save_model('Vorhersage/modelXGB.json')

    ### and use again
    #reg_new = xgb.XGBRegressor()
    #reg_new.load_model('Vorhersage/modelXGB.json')



