from scipy.stats import spearmanr

def inspect_holidays(data, column, verbrauch_spalte):
    # Berechne Feiertages-Durchschnitt im Vergleich zu allg. Durchschnitt
    feiertage_avg = data.loc[data[column], verbrauch_spalte].mean()
    stromverbrauch_avg = data[verbrauch_spalte].mean()
    print(f"\nAusreißer und Feiertage Untersuchung ({column}): \n")
    print(f"Durchschnitt Stromverbrauch an Feiertagen: {feiertage_avg: .2f} MWh")
    print(f"Durchschnitt Stromverbrauch (Gesamt): {stromverbrauch_avg: .2f} MWh\n")

    anzahl_ausreißer = 0
    summe_feiertage = 0
    for i in range(0, 7):
        data_weekday = data.loc[(data['Weekday'] == i)]
        # IQR (Interquartilsabstand) berechnen
        Q1 = data_weekday[verbrauch_spalte].quantile(0.25)  # 1. Quartil
        Q3 = data_weekday[verbrauch_spalte].quantile(0.75)  # 3. Quartil
        IQR = Q3 - Q1
        # Grenzen für Ausreißer
        untere_grenze = Q1 - 1.5 * IQR
        obere_grenze = Q3 + 1.5 * IQR
        # Ausreißer filtern
        ausreisser = data_weekday[
            (data_weekday[verbrauch_spalte] < untere_grenze) | (data_weekday[verbrauch_spalte] > obere_grenze)]
        if ausreisser.empty:
            print(f"Keine Ausreißer für den Wochentag-Index {i}")
        else:
            # Überprüfen, ob diese Tage Feiertage sind
            print(f"Anzahl Ausreißer an Wochentag-Index {i}: {ausreisser.shape[0]}")
            # print(ausreisser[[verbrauch_spalte, "is_holiday"]])
            anzahl_ausreißer += ausreisser.shape[0]
            summe_feiertage += ausreisser[column].sum()
    print(f"\nInsgesamt Anzahl der Ausreißer (Bei Gruppierung nach Wochentagen): {anzahl_ausreißer}")
    print(f"Davon Feiertage: {summe_feiertage} ({summe_feiertage / anzahl_ausreißer * 100: .2f}%)\n")


def feature_engineering(dataset, zone):
    verbrauch_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"
    rows = ['TMK', 'TXK', 'TNK', 'SDK', 'RSK', 'RSKF', 'PM', 'UPM', 'VPM']

    ### Korrelationen mit Klimadaten berechnen
    print("Wetterdaten Untersuchung:\n")
    for row in rows:
        correlation = dataset[verbrauch_spalte].corr(dataset[row])
        # Ergebnis ausgeben
        print(f"Korrelation (Pearson) zwischen Stromverbrauch und {row}: {correlation:.2f}")
        # Berechnung des Spearman-Korrelationskoeffizienten
        spearman_corr = spearmanr(dataset[row], dataset[verbrauch_spalte])
        # Ergebnis ausgeben
        print(f"Spearman-Korrelationskoeffizient {row}: {spearman_corr.correlation:.2f}")

    ### Feiertages Anomalien
    if zone == "50hertz":
        for states in ['BB', 'BE', 'MV', 'SN', 'ST', 'TH', 'HH']:
            column = 'is_holiday_' + states
            inspect_holidays(dataset, column, verbrauch_spalte)
    else:
        inspect_holidays(dataset, 'is_holiday', verbrauch_spalte)

