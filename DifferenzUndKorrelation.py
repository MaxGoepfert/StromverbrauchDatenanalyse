import pandas as pd
import matplotlib.pyplot as plt

def cleanData(data, zeit_spalte, last_spalte):

    data = data.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    data[zeit_spalte] = pd.to_datetime(data[zeit_spalte], dayfirst=True, errors='raise')
    # print(data[zeit_spalte])
    data.set_index(zeit_spalte, inplace=True)

    # print(data.index)
    # Last Spalte in korrekte numerische Werte konvertieren
    data[last_spalte] = data[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    data[last_spalte] = data[last_spalte].str.replace(',', '.',
                                                      regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    data[last_spalte] = pd.to_numeric(data[last_spalte])

    # Neuer DataFrame mit nur Index und der Stromverbrauchs Spalte
    df_verbrauch = data[[last_spalte]]

    df_verbrauch = df_verbrauch.copy()

    return df_verbrauch

if __name__ == "__main__":
    #dataPath = "data/Realisierter_Stromverbrauch_201701010000_202301010000_Tag.csv"
    dataPath2 = "data/Realisierter_Stromverbrauch_2017_2023_Tag_50Hertz.csv"
    dataPath3 = "data/Realisierter_Stromverbrauch_2017_2023_Tag_BW.csv"

    #data = pd.read_csv(dataPath, delimiter=';')
    data_50Hertz = pd.read_csv(dataPath2, delimiter=';')
    data_TransNetBW= pd.read_csv(dataPath3, delimiter=';')
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

    # Clean data
    data_50Hertz= cleanData(data_50Hertz, zeit_spalte, last_spalte)
    data_TransNetBW = cleanData(data_TransNetBW, zeit_spalte, last_spalte)

    # Sicherstellen, dass die Zeitreihen übereinstimmen
    combined_data = data_50Hertz[[last_spalte]].join(
        data_TransNetBW[[last_spalte]],
        how='inner',
        lsuffix='_50Hertz',
        rsuffix='_TransNetBW'
    )

    # Differenz berechnen
    combined_data['Differenz'] = combined_data[f"{last_spalte}_50Hertz"] - combined_data[f"{last_spalte}_TransNetBW"]

    # Ergebnis anzeigen oder speichern
    combined_data.index = pd.to_datetime(combined_data.index)
    combined_data.to_csv("data/Differenz_Stromverbrauch.csv")
    #combined_data.index = pd.to_datetime(combined_data.index)
    print(combined_data.index.dtype)
    print(combined_data.head())

    # plot
    plt.figure(figsize=(10, 6))
    plt.plot(combined_data['Differenz'], label='Differenz (50Hertz - TransNetBW)', color='red')
    plt.axhline(0, color='black', linestyle='--')
    plt.title('Tägliche Verbrauchsdifferenz (50Hertz - TransNetBW)')
    plt.xlabel('Datum')
    plt.ylabel('Differenz (MWh)')
    plt.legend()
    plt.grid()
    plt.show()



# Korrelation berechnen
correlation = data_50Hertz[last_spalte].corr(data_TransNetBW[last_spalte])

# Ergebnis anzeigen
print(f"Korrelation zwischen 50Hertz und TransNetBW: {correlation:.2f}")

# Streudiagramm der Stromverbrauchswerte
plt.figure(figsize=(8, 6))
plt.scatter(data_50Hertz[last_spalte], data_TransNetBW[last_spalte], alpha=0.5, color='green')
plt.title("Zusammenhang zwischen 50Hertz und TransNetBW")
plt.xlabel("Stromverbrauch 50Hertz (MWh)")
plt.ylabel("Stromverbrauch TransNetBW (MWh)")
plt.grid(True)
plt.show()

### gleitende Korrelation
# Gleitende Korrelation mit einem Fenster von 30 Tagen
gleitende_korrelation = data_50Hertz[last_spalte].rolling(window=30).corr(data_TransNetBW[last_spalte])

# Plotten der gleitenden Korrelation
plt.figure(figsize=(12, 6))
plt.plot(gleitende_korrelation, label='Gleitende Korrelation (30 Tage)', color='blue')
plt.title('Gleitende Korrelation zwischen 50Hertz und TransNetBW')
plt.xlabel('Datum')
plt.ylabel('Korrelation')
plt.legend()
plt.show()







