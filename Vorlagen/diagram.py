

import matplotlib.pyplot as plt
import pandas as pd

if __name__ == '__main__':
    input_file = "airport-cgn.csv"
    weather_df = pd.read_csv(input_file)
    weather_df.info()

    year = input("Die Wetterdaten welches Jahrs soll ich darstellen? ")
