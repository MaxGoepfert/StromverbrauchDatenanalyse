import os

# Beispiel für die Konfiguration des Dateipfads
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Eventuelle Lösung für Dateipfad der config.py: BASE_PATH = os.path.dirname(os.path.abspath(__file__))

dataPath = "Realisierter_Stromverbrauch_2017_2024_Tag_de.csv"
dataPath2 = "Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
dataPath3 = "Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"
dataPath5 = "Prognostizierter_Stromverbrauch_2023_2024_Tag_de.csv"

WEATHER_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'Wetterdaten')
DE_STROM_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath)
DE_STROM_PROG_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath5)
HERTZ_STROM_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath2)
BW_STROM_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath3)




