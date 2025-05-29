import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    input_file = r"C:\Users\hallo\Downloads\airport-cgn.csv"
    weather_df = pd.read_csv(input_file)

    weather_df['date'] = pd.to_datetime(weather_df[['year', 'month', 'day']])

    year_input = input("Die Wetterdaten welches Jahrs soll ich darstellen?").strip()
    try:
        year = int(year_input)
    except ValueError:
        print("Ungültige Eingabe. Bitte ein Jahr als Zahl eingeben.")
        exit(1)

    year_df = weather_df[weather_df['year'] == year]

    if year_df.empty:
        print(f"Keine Wetterdaten für das Jahr {year} gefunden.")
        exit(1)

    monthly_prcp = year_df.groupby('month')['prcp'].sum()

    #Niederschlag pro Monat
    plt.figure(figsize=(10, 5))
    monthly_prcp.plot(kind='bar', color='skyblue')
    plt.title(f'Niederschlag pro Monat im Jahr {year}')
    plt.xlabel('Monat')
    plt.ylabel('Niederschlagsmenge (mm)')
    plt.xticks(rotation=0)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

    #Temperatur pro Monat
    monthly_temp = year_df.groupby('month').agg({
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

    #Luftdruck und Niedershclag
    plt.figure(figsize=(10, 5))
    plt.scatter(year_df['pres'], year_df['prcp'], alpha=0.5, c='green')
    plt.title(f'Luftdruck vs. Niederschlag im Jahr {year}')
    plt.xlabel('Luftdruck (hPa)')
    plt.ylabel('Niederschlagsmenge (mm)')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
