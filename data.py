import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
#plt.use('TkAgg')  # Stabileres Backend für macOS

def plotData(dataset, zeit_spalte, last_spalte):
    # Alle Spalten anzeigen
    pd.set_option('display.max_columns', None)

    # Alle Zeilen anzeigen
    pd.set_option('display.max_rows', None)

    # Maximale Breite einer Spalte erhöhen
    pd.set_option('display.width', 1000)

    # Clean data
    cleanData(dataset, zeit_spalte, last_spalte)

    # Plot erstellen
    plt.figure(figsize=(12, 6))  # Größe des Plots festlegen
    plt.plot(dataset[zeit_spalte], dataset[last_spalte], label="Gesamtlast Strom", color='blue')

    # Achsentitel und Plot-Titel
    plt.xlabel("Zeit (Datum von)")
    plt.ylabel("Gesamtlast Strom (in MWh)")  # Einheit anpassen, falls bekannt
    plt.title("Gesamtlast Strom über die Zeit")

    # Legende und Gitter
    plt.legend()
    plt.grid()
    # Plot anzeigen
    plt.show()

def cleanData(dataset, zeit_spalte, last_spalte):
    # Umwandlung der Zeit-Spalte in datetime, zur Sicherheit
    dataset[zeit_spalte] = pd.to_datetime(dataset[zeit_spalte], dayfirst=True, errors='raise')
    dataset[last_spalte] = dataset[last_spalte].str.replace('.', '', regex=False)  # Tausendertrennzeichen entfernen
    dataset[last_spalte] = dataset[last_spalte].str.replace(',', '.', regex=False)  # Dezimal-Komma durch Dezimal-Punkt ersetzen
    dataset[last_spalte] = pd.to_numeric(dataset[last_spalte])

    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values1 = dataset[zeit_spalte].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{zeit_spalte}': {missing_values1}")
    # Prüfen, ob ungültige Werte (NaN) existieren
    missing_values2 = dataset[last_spalte].isnull().sum()
    print(f"Fehlende Werte in der Spalte '{last_spalte}': {missing_values2}")


if __name__ == "__main__":
    dataPath = "Realisierter_Stromverbrauch_201701010000_202301010000_Tag.csv"
    data = pd.read_csv(dataPath, delimiter=';')
    zeit_spalte = "Datum von"
    last_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"
    plotData(data,zeit_spalte, last_spalte)

    varianz = data[last_spalte].var()
    print(f"Die Varianz der Netzlast beträgt: {varianz}")

    std = data[last_spalte].std()
    print(f"Die Standartabweichung der Netzlast beträgt: {std}")

    # Größten Wert in der Zielspalte anzeigen
    max_value = data[last_spalte].max()
    print(f"Der größte Wert in der Spalte {last_spalte} ist: {max_value}")


# TO DO Variationskoeffizent Zusammenhänge: Kovarianz/Korrelation, Korrelationskoeffizient
