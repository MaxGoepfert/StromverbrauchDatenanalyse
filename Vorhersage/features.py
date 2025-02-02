from scipy.stats import spearmanr


def feature_engineering(dataset):
    zeit_spalte = "Datum von"
    verbrauch_spalte = "Gesamt (Netzlast) [MWh] Berechnete Auflösungen"
    rows = ['TMK', 'TXK', 'TNK', 'SDK', 'RSK', 'RSKF', 'PM', 'UPM', 'VPM']

    # Korrelationen mit Klimadaten berechnen
    for row in rows:
        correlation = dataset[verbrauch_spalte].corr(dataset[row])
        # Ergebnis anzeigen
        print(f"Korrelation zwischen Stromverbrauch und {row}: {correlation:.2f}")
        # Berechnung des Spearman-Korrelationskoeffizienten
        spearman_corr = spearmanr(dataset[row], dataset[verbrauch_spalte])
        # Ergebnis ausgeben
        print(f"Spearman-Korrelationskoeffizient {row}: {spearman_corr.correlation:.2f}")

    ### Feiertages Anomalien
    feiertage_avg = dataset.loc[dataset['is_holiday'], verbrauch_spalte].mean()
    feiertage_sum = dataset.loc[dataset['is_holiday'], verbrauch_spalte].sum()
    stromverbrauch_avg = dataset[verbrauch_spalte].mean()
    print(f"Durchschnitt Stromverbrauch an Feiertagen: {feiertage_avg: .2f}")
    print(f"Durchschnitt Stromverbrauch (Gesamt): {stromverbrauch_avg: .2f}")
    print(f"Summe Stromverbrauch an Feiertagen: {feiertage_sum: .2f}")

    anzahl_ausreißer = 0
    summe_feiertage = 0
    for i in range(0, 7):
        print(f"Weekday Index is: {i}")
        data_weekday = dataset.loc[(dataset['Weekday'] == i)]
        # IQR (Interquartilsabstand) berechnen
        Q1 = data_weekday[verbrauch_spalte].quantile(0.25)  # 1. Quartil
        Q3 = data_weekday[verbrauch_spalte].quantile(0.75)  # 3. Quartil
        IQR = Q3 - Q1

        # Grenzen für Ausreißer
        untere_grenze = Q1 - 1.5 * IQR
        obere_grenze = Q3 + 1.5 * IQR

        print(f"Wochentag {i}: Untere Grenze: {untere_grenze}, Obere Grenze: {obere_grenze}")

        # Ausreißer filtern
        ausreisser = data_weekday[
            (data_weekday[verbrauch_spalte] < untere_grenze) | (data_weekday[verbrauch_spalte] > obere_grenze)]
        if ausreisser.empty:
            print(f"Keine Ausreißer für den Wochentag {i}")
        else:
            # Überprüfen, ob diese Tage Feiertage sind
            print(f"Ausreißer-Daten für Wochentag {i}: ")
            print(f"Anzahl Ausreißer: {ausreisser.shape[0]}")
            print(ausreisser[[verbrauch_spalte, "is_holiday"]])
            anzahl_ausreißer += ausreisser.shape[0]
            summe_feiertage += ausreisser['is_holiday'].sum()
    print(f"Insgesamt Anzahl der Ausreißer: {anzahl_ausreißer}")
    print(f"Davon Feiertage: {summe_feiertage} ({summe_feiertage / anzahl_ausreißer * 100:.2f}%)")
