import pandas as pd
import matplotlib.pyplot as plt

ZEIT_SPALTE = "Datum von"
VERBRAUCH_SPALTE = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"

def cleanData(data):
    data = data.copy()
    # Umwandlung der Zeit-Spalte in datetime und als index setzen
    data[ZEIT_SPALTE] = pd.to_datetime(data[ZEIT_SPALTE], dayfirst=True, errors='raise')
    # print(data[ZEIT_SPALTE])
    data.set_index(ZEIT_SPALTE, inplace=True)

    # print(data.index)
    # Last Spalte in korrekte numerische Werte konvertieren
    data[VERBRAUCH_SPALTE] = data[VERBRAUCH_SPALTE].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    data[VERBRAUCH_SPALTE] = data[VERBRAUCH_SPALTE].str.replace(',', '.',
                                                                regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    data[VERBRAUCH_SPALTE] = pd.to_numeric(data[VERBRAUCH_SPALTE])

    # Neuer DataFrame mit nur Index und der Stromverbrauchs Spalte
    df_verbrauch = data[[VERBRAUCH_SPALTE]]

    df_verbrauch = df_verbrauch.copy()

    return df_verbrauch


if __name__ == "__main__":
    dataPath2 = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_50Hertz.csv"
    dataPath3 = "Vorhersage/data/Realisierter_Stromverbrauch_2017_2024_Tag_BW.csv"

    data_50Hertz = pd.read_csv(dataPath2, delimiter=';')
    data_TransNetBW = pd.read_csv(dataPath3, delimiter=';')

    # Clean data
    data_50Hertz = cleanData(data_50Hertz)
    data_TransNetBW = cleanData(data_TransNetBW)

    # Sicherstellen, dass die Zeitreihen übereinstimmen
    combined_data = data_50Hertz[[VERBRAUCH_SPALTE]].join(
        data_TransNetBW[[VERBRAUCH_SPALTE]],
        how='inner',
        lsuffix='_50Hertz',
        rsuffix='_TransNetBW'
    )

    # Differenz berechnen
    combined_data['Differenz'] = combined_data[f"{VERBRAUCH_SPALTE}_50Hertz"] - combined_data[
        f"{VERBRAUCH_SPALTE}_TransNetBW"]

    # Ergebnis anzeigen oder speichern
    combined_data.index = pd.to_datetime(combined_data.index)
    combined_data.to_csv("../data/Differenz_Stromverbrauch.csv")
    # combined_data.index = pd.to_datetime(combined_data.index)

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

    ### Korrelation berechnen
    correlation = data_50Hertz[VERBRAUCH_SPALTE].corr(data_TransNetBW[VERBRAUCH_SPALTE])

    # Ergebnis anzeigen
    print(f"Korrelation zwischen 50Hertz und TransNetBW: {correlation:.2f}")

    # Streudiagramm der Stromverbrauchswerte
    plt.figure(figsize=(10, 8))
    plt.scatter(data_50Hertz[VERBRAUCH_SPALTE], data_TransNetBW[VERBRAUCH_SPALTE], alpha=0.5, color='green')
    plt.title("Zusammenhang zwischen 50Hertz und TransNetBW")
    plt.xlabel("Stromverbrauch 50Hertz (MWh)")
    plt.ylabel("Stromverbrauch TransNetBW (MWh)")
    plt.grid(True)
    plt.show()
