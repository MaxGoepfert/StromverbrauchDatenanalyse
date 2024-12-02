import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
color_pal = sns.color_palette()

dataPath = 'Realisierter_Stromverbrauch_2017_2023_Tag_50Hertz.csv'
data = pd.read_csv(dataPath, delimiter=';')
zeit_spalte = 'Datum von'
last_spalte = 'Gesamt (Netzlast) [MWh] Berechnete Auflösungen'

# Umwandlung der Zeit-Spalte in datetime und als index setzen
data[zeit_spalte]= pd.to_datetime(data[zeit_spalte], dayfirst=True, errors='raise')
#print(data[zeit_spalte])
data.set_index(zeit_spalte, inplace=True)

#print(data.index)
# Last Spalte in korrekte numerische Werte konvertieren
data[last_spalte] = data[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
data[last_spalte] = data[last_spalte].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
data[last_spalte] = pd.to_numeric(data[last_spalte])

# Neuer DataFrame mit nur Index und der Stromverbrauchs Spalte
df_verbrauch = data[[last_spalte]]

#df_verbrauch.plot(style='.', figsize=(15,5), title = '50Hertz Stromverbrauch')
#plt.show()

df_verbrauch = df_verbrauch.copy()
"""
df_verbrauch['dayOfWeek'] = df_verbrauch.index.dayofweek
fig, ax = plt.subplots(figsize=(10,8))
sns.boxplot(data=df_verbrauch, x='dayOfWeek', y=last_spalte)
ax.set_title('Stromverbrauch Wochentage')
plt.show()
"""

df_verbrauch['month'] = df_verbrauch.index.month
fig, ax = plt.subplots(figsize=(10,8))
sns.boxplot(data=df_verbrauch, x='month', y=last_spalte, palette='Blues')
ax.set_title('Stromverbrauch Monate')
plt.show()
