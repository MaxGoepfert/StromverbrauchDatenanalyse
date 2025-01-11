import pandas as pd
import holidays



# Feiertage für Deutschland/TransNetBW/50Hertz hinzufügen
def add_holidays_50Hertz(df):
    for states in ["BB", "BE", "MV", "SN", "ST", "TH", "HH"]:
        holiday_states = holidays.Germany(state=states)
        df['is_holiday_' + states] = df.index.to_series().apply(lambda x: x in holiday_states)
    return df

# Optional: Namen der Feiertage als zusätzliches Feature
#df['holiday_name'] = df['date'].map(de_holidays)  # Gibt den Namen des Feiertags zurück, wenn es einer ist

if __name__ == '__main__':
    # Beispiel: Zeitreihe mit täglichen Daten
    date_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
    df = pd.DataFrame({'date': date_range})
    df['date'] = df['date'].dt.date

    de_holidays = holidays.Germany(state="BW")
    # Feature: Ist der Tag ein Feiertag?
    df['is_holiday'] = df.index.to_series().apply(lambda x: x in de_holidays)
    # Ausgabe
    print(df.head(50))


