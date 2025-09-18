import pandas as pd

df = pd.read_csv('Airplane_Cleaned.csv')
aircraft_cruise_speeds = df[['Model', 'Vcruise']].dropna()
aircraft_cruise_speeds['Vcruise_kmh'] = aircraft_cruise_speeds['Vcruise'] * 1.852
aircraft_cruise_speeds.to_csv('aircraft_cruise_speeds.csv', index=False)
print(aircraft_cruise_speeds.head())
