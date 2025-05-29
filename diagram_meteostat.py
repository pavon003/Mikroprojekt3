import matplotlib.pyplot as plt
import pandas as pd
from meteostat import Daily, Stations
from datetime import datetime

year_input = input("Die Wetterdaten welches Jahrs soll ich darstellen? ").strip()
try:
    year = int(year_input)
except ValueError:
    print("Ungültige Eingabe. Bitte ein Jahr als Zahl eingeben.")
    exit(1)

start = datetime(year, 1, 1)
end = datetime(year, 12, 31)

stations = Stations()
stations = stations.nearby(50.8659, 7.1427)
station = stations.fetch(1)

data = Daily(station.index[0], start, end)
data = data.fetch()

data = data.reset_index()
data['year'] = data['time'].dt.year
data['month'] = data['time'].dt.month
data['day'] = data['time'].dt.day
data['tavg'] = data['tavg']
data['tmin'] = data['tmin']
data['tmax'] = data['tmax']
data['prcp'] = data['prcp']
data['pres'] = data['pres']

for col in ['tavg', 'tmin', 'tmax', 'prcp', 'pres']:
    if col not in data.columns:
        data[col] = 0

#Niederschlag pro Monat
monthly_prcp = data.groupby('month')['prcp'].sum()

plt.figure(figsize=(10, 5))
monthly_prcp.plot(kind='bar', color='skyblue')
plt.title(f'Niederschlag pro Monat im Jahr {year}')
plt.xlabel('Monat')
plt.ylabel('Niederschlagsmenge (mm)')
plt.xticks(rotation=0)
plt.grid(axis='y')
plt.tight_layout()
plt.show()

#Temperaturstatistik pro Monat
monthly_temp = data.groupby('month').agg({
    'tmin': 'min',
    'tavg': 'mean',
    'tmax': 'max'
})

plt.figure(figsize=(10, 5))
plt.plot(monthly_temp.index, monthly_temp['tmin'], label='Min Temperatur', marker='o')
plt.plot(monthly_temp.index, monthly_temp['tavg'], label='Durchschnittstemperatur', marker='o')
plt.plot(monthly_temp.index, monthly_temp['tmax'], label='Max Temperatur', marker='o')
plt.title(f'Temperaturstatistik pro Monat im Jahr {year}')
plt.xlabel('Monat')
plt.ylabel('Temperatur (°C)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Streudiagramm: Luftdruck vs. Niederschlag
plt.figure(figsize=(10, 5))
plt.scatter(data['pres'], data['prcp'], alpha=0.5, c='green')
plt.title(f'Luftdruck vs. Niederschlag im Jahr {year}')
plt.xlabel('Luftdruck (hPa)')
plt.ylabel('Niederschlagsmenge (mm)')
plt.grid(True)
plt.tight_layout()
plt.show()
