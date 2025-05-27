import socket
import threading

def load_data(filename):
    samples = []

    with open(filename) as file:
        header = file.readline()
        for line in file:
            year, month, day, tavg, tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun = line.strip().split(',')
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
        print(
            f"{tavg:4.1f} C {tmin:4.1f} C {tmax:4.1f} C | {prcp:4.1f} mm {snow:2.0f} mm | {pres:6.1f} hPa | {tsun:4d} min | {day:02d}.{month:02d}.{year:04d}")

    print(len(samples), "Tageswerte eingelesen.")
    return samples

def find_weather(samples, requested_day):

    day, month, year = map(int, requested_day.strip().split('.'))

    for s in samples:
        if s[0] == year and s[1] == month and s[2] == day:
            tavg, tmin, tmax, prcp, snow, wdir, wspd, wpgt, pres, tsun = s[3:]
            return (f"{tavg:4.1f} C {tmin:4.1f} C {tmax:4.1f} C | "
                    f"{prcp:4.1f} mm {snow:2.0f} mm | "
                    f"{pres:6.1f} hPa | {tsun:4d} min | "
                    f"{day:02d}.{month:02d}.{year:04d}")
    return "Keine Daten für diesen Tag gefunden."

def handle_client(conn, addr, samples):
    print(f"Verbindung von {addr}")
    data = conn.recv(1024).decode()
    print("Anfrage erhalten:", data)
    response = find_weather(samples, data)
    conn.send(response.encode())
    conn.close()

def run_server(host='localhost', port=5000):
    input_file = r"C:\Users\hallo\Downloads\airport-cgn.csv"
    samples = load_data(input_file)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()

    print(f"Server läuft auf {host}:{port}...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr, samples)).start()

if __name__ == '__main__':
    run_server()