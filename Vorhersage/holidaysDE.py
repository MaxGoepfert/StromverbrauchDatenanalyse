import pandas as pd
import holidays

# Beispiel: Zeitreihe mit täglichen Daten
date_range = pd.date_range(start="2023-01-01", end="2023-12-31", freq="D")
df = pd.DataFrame({'date': date_range})
df['date'] = df['date'].dt.date

# Feiertage für Deutschland hinzufügen
de_holidays = holidays.Germany()  # geht auch für Bundesländer: z.B. holidays.Germany(state='BY') für Bayern

# Feature: Ist der Tag ein Feiertag?
df['is_holiday'] = df['date'].apply(lambda x: x in de_holidays) # funktioniert irgendwie nicht mit .isin(de_holidays), deswegen extra lambda-Funktion


# Optional: Namen der Feiertage als zusätzliches Feature
df['holiday_name'] = df['date'].map(de_holidays)  # Gibt den Namen des Feiertags zurück, wenn es einer ist

# Ausgabe
print(df.tail(50))

def add_holidays(df):
    de_holidays = holidays.Germany()  # geht auch für Bundesländer: z.B. holidays.Germany(state='BY') für Bayern
    # Feature: Ist der Tag ein Feiertag?
    df['is_holiday'] = df['date'].apply(lambda x: x in de_holidays)  # funktioniert irgendwie nicht mit .isin(de_holidays), deswegen extra lambda-Funktion


