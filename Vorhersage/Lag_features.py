import pandas as pd
def add_lag(df, verbrauch_spalte):
    dictOfLastSpalte = df[verbrauch_spalte].to_dict()
    # zieht von Datum ein Jahr ab und gibt Wert von diesem Datum zurück
    """
    if leak == "J":
        print("Laden der Daten des Vortages...")
    """
    df['lag_day'] = (df.index - pd.Timedelta('1 days')).map(dictOfLastSpalte)
    df['lag_week'] = (df.index - pd.Timedelta('7 days')).map(dictOfLastSpalte)
    # Annahme: ein Jahr hat 52 Wochen (also 364 Tage) -> Gleiche Wochentage werden somit "gemapped"
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
