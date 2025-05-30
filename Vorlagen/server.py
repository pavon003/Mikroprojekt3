

def load_data(filename):
    samples = []

    with open(filename) as file:
        header = file.readline()
        for line in file:
            year, month, day, tavg, tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun = line.split(',')
            samples.append(
                (int(year), int(month), int(day),
                 float(tavg), float(tmin), float(tmax),
                 float(prcp), float(snow),
                 int(wdir), float(wspd), float(wpgt),
                 float(pres), int(tsun)))

    print(" Temp (min/o/max)    | Niederschlag  | Luftdruck  | Sonne    | Datum")
    print("---------------------+---------------+------------+----------+-----------")

    for s in samples:
        year, month, day, tavg, tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun = s
        print(f"{tavg:4.1f} C {tmin:4.1f} C {tmax:4.1f} C | {prcp:4.1f} mm {snow:2.0f} mm | {pres:6.1f} hPa | {tsun:4d} min | {day:02d}.{month:02d}.{year:04d}")

    print(len(samples), "Tageswerte eingelesen.")
    return samples


if __name__ == '__main__':
    input_file = "airport-cgn.csv"
    samples = load_data(input_file)
    # ...


