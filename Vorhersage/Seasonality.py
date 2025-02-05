
def add_seasons(df):
    df['Day_of_year'] = df.index.day_of_year
    df['Weekday'] = df.index.weekday
    df['Month'] = df.index.month
    df['Season'] = df.index.day_of_year.map(add_yearly_seasons)
    df['is_weekend'] = df.index.weekday.isin([5, 6])  # Samstag (5) und Sonntag (6)
    df['is_weekend'] = df['is_weekend'].astype(int)

    return df

# Jahreszeiten hinzufügen (ungefähr per Monate)
def add_yearly_seasons(day):
    """
    In normalen Jahren (Keine Schaltjahre)
    Frühling: 20. März – 20. Juni (Day_of_year 80 bis 171)
    Sommer: 21. Juni – 22. September (Day_of_year 172 bis 265)
    Herbst: 23. September – 20. Dezember (Day_of_year 266 bis 354)
    Winter: 21. Dezember – 19. März (Day_of_year 355 bis 79)
    """
    if 80 <= day <= 171:
        return 1  # Fruehling
    elif 172 <= day <= 265:
        return 2  # Sommer
    elif 266 <= day <= 354:
        return 3  # Herbst
    else:
        return 4  # Winter
