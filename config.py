import os

# Beispiel für die Konfiguration des Dateipfads
BASE_PATH = os.getcwd() # Dies nutzt den aktuellen Arbeitsordner

dataPath = "Realisierter_Stromverbrauch_2017-2024_Tag.csv"
dataPath2 = "Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
dataPath3 = "Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"
dataPath4 = "klima_tag_1969_2023.txt"

WEATHER_DATA_PATH = os.path.join(BASE_PATH, '..' , 'data', dataPath4)
DE_STROM_DATA_PATH = os.path.join(BASE_PATH, "..", 'data',dataPath)
HERTZ_STROM_DATA_PATH = os.path.join(BASE_PATH, "..", 'data',dataPath2)
BW_STROM_DATA_PATH = os.path.join(BASE_PATH, "..", 'data', dataPath3)



