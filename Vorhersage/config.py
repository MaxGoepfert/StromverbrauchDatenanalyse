import os

# Pfad zum Verzeichnis des Projekts
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

dataPath = "Realisierter_Stromverbrauch_2017_2024_Tag_de.csv"
dataPath2 = "Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
dataPath3 = "Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"
dataPath5 = "Prognostizierter_Stromverbrauch_2023_2024_Tag_de.csv"
dataPath6 = "Prognostizierter_Stromverbrauch_2023_2024_Tag_TransNetBW.csv"
dataPath7 = "Prognostizierter_Stromverbrauch_2023_2024_Tag_50Hertz.csv"

WEATHER_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'Wetterdaten')
DE_STROM_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath)
DE_STROM_PROG_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath5)
HERTZ_STROM_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath2)
BW_STROM_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath3)
BW_STROM_PROG_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath6)
HERTZ_STROM_PROG_DATA_PATH = os.path.join(BASE_PATH, 'Vorhersage', 'data', dataPath7)


