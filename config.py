import os

# Beispiel für die Konfiguration des Dateipfads
BASE_PATH = os.getcwd() # Dies nutzt den aktuellen Arbeitsordner
# Eventuelle Lösung für Dateipfad der config.py: BASE_PATH = os.path.dirname(os.path.abspath(__file__))

dataPath = "Realisierter_Stromverbrauch_2017-2024_Tag.csv"
dataPath2 = "Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
dataPath3 = "Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"
#dataPath4 = "klima_tag_1969_2023.txt"
dataPath5 = "Prognostizierter_Stromverbrauch_2023-2024_Tag.csv"
dataPath6 = "xgb_model.json"

WEATHER_DATA_PATH = os.path.join(BASE_PATH, "..", 'Wetterdaten')
DE_STROM_DATA_PATH = os.path.join(BASE_PATH, "..", 'data',dataPath)
DE_STROM_PROG_DATA_PATH = os.path.join(BASE_PATH, "..", 'data', dataPath5)
HERTZ_STROM_DATA_PATH = os.path.join(BASE_PATH, "..", 'data', dataPath2)
BW_STROM_DATA_PATH = os.path.join(BASE_PATH, "..", 'data', dataPath3)
MODEL_PATH = os.path.join(BASE_PATH, "..", 'Vorhersage', dataPath6)




