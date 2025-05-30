from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import pandas as pd
from meteostat import Daily, Stations
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    year = None
    error = None

    if request.method == "POST":
        year_input = request.form.get("year", "").strip()

        try:
            year = int(year_input)
            start = datetime(year, 1, 1)
            end = datetime(year, 12, 31)

            stations = Stations().nearby(50.8659, 7.1427)
            station = stations.fetch(1)

            data = Daily(station.index[0], start, end).fetch().reset_index()
            data['month'] = data['time'].dt.month
            data['tavg'] = data['tavg']
            data['tmin'] = data['tmin']
            data['tmax'] = data['tmax']
            data['prcp'] = data['prcp']
            data['pres'] = data['pres']

            for col in ['tavg', 'tmin', 'tmax', 'prcp', 'pres']:
                if col not in data.columns:
                    data[col] = 0

            os.makedirs("static/plots", exist_ok=True)

            plt.figure(figsize=(10, 5))
            data.groupby('month')['prcp'].sum().plot(kind='bar', color='skyblue')
            plt.title(f'Niederschlag pro Monat im Jahr {year}')
            plt.xlabel('Monat')
            plt.ylabel('Niederschlagsmenge (mm)')
            plt.xticks(rotation=0)
            plt.grid(axis='y')
            plt.tight_layout()
            plt.savefig("static/plots/prcp.png")
            plt.close()

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
            plt.savefig("static/plots/temp.png")
            plt.close()

            plt.figure(figsize=(10, 5))
            plt.scatter(data['pres'], data['prcp'], alpha=0.5, c='green')
            plt.title(f'Luftdruck vs. Niederschlag im Jahr {year}')
            plt.xlabel('Luftdruck (hPa)')
            plt.ylabel('Niederschlagsmenge (mm)')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("static/plots/scatter.png")
            plt.close()

        except ValueError:
            error = "Ungültige Eingabe. Bitte ein Jahr als Zahl eingeben."

    return render_template("index.html", year=year, error=error)

if __name__ == "__main__":
    app.run(debug=True)