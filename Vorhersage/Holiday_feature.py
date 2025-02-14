import holidays
def add_holidays_de(df):
    de_holidays = holidays.Germany()
    # Feature: Ist der Tag ein Feiertag?
    df['is_holiday'] = df.index.to_series().apply(lambda x: x in de_holidays)
    # df['is_holiday'] = df['is_holiday'].astype(int)
    return df


def add_holidays_50Hertz(df):
    for states in ["BB", "BE", "MV", "SN", "ST", "TH", "HH"]:
        holiday_states = holidays.Germany(state=states)
        df['is_holiday_' + states] = df.index.to_series().apply(lambda x: x in holiday_states)
        #df['is_holiday_' + states] = df['is_holiday_' + states].astype(int)
    return df


def add_holidays_TransNetBW(df):
    de_holidays = holidays.Germany(state="BW")
    # Feature: Ist der Tag ein Feiertag?
    df['is_holiday'] = df.index.to_series().apply(lambda x: x in de_holidays)
    #df['is_holiday'] = df['is_holiday'].astype(int)
    return df

# Optional: Namen der Feiertage als zusätzliches Feature
#df['holiday_name'] = df['date'].map(de_holidays)  # Gibt den Namen des Feiertags zurück, wenn es einer ist



