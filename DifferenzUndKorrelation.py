### TO DO
### Skizze Differenz
"""
# Pivot-Tabelle erstellen
pivot_data = data.pivot_table(values='Verbrauch', index='Datum', columns='Regelzone')

# Differenz berechnen
pivot_data['Differenz'] = pivot_data['TransNetBW'] - pivot_data['50Hertz']

# Plot der Differenz
plt.figure(figsize=(10, 6))
plt.plot(pivot_data['Differenz'], label='Differenz (TransNetBW - 50Hertz)', color='red')
plt.axhline(0, color='black', linestyle='--')
plt.title('Tägliche Verbrauchsdifferenz (TransNetBW - 50Hertz)')
plt.xlabel('Datum')
plt.ylabel('Differenz (MWh)')
plt.legend()
plt.grid()
plt.show()
"""
### TO DO
### Skizze Korrelation
"""
correlation = pivot_data.corr()
print(correlation)

sns.heatmap(correlation, annot=True, cmap='coolwarm')
plt.title('Korrelationsmatrix (Verbrauch TransNetBW & 50Hertz)')
plt.show()
"""

### Langfristige Trends -> Gleitender Durchschnitt
### data['30-Tage-Mittel'] = data.groupby('Regelzone')['Verbrauch'].transform(lambda x: x.rolling(30).mean())
""""
# Plot
sns.lineplot(data=data, x='Datum', y='30-Tage-Mittel', hue='Regelzone')
plt.title('30-Tage gleitender Mittelwert des Stromverbrauchs')
plt.xlabel('Datum')
plt.ylabel('Verbrauch (MWh)')
plt.legend(title='Regelzone')
plt.grid()
plt.show()
"""

