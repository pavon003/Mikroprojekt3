import socket
from datetime import datetime

def request_weather(requested_day, host='localhost', port=5000):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.send(requested_day.encode())
        data = s.recv(1024).decode()
        return data

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    while True:
        requested_day = input("Die Wetterdaten welchen Tags soll ich suchen? (TT.MM.JJJJ) ")
        if is_valid_date(requested_day):
            break
        else:
            print("Ungültiges Format. Bitte TT.MM.JJJJ eingeben!")

    result = request_weather(requested_day)
    print("\nHier sind die Wetterdaten des", requested_day)
    print(" Temp (min/o/max)    | Niederschlag  | Luftdruck  | Sonne    | Datum")
    print("---------------------+---------------+------------+----------+-----------")
    print(result)
