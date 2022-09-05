import math

from LEACH_basics import Sensor, Model


def zeros(row, column):
    re_list = []
    for x in range(row):
        # Todo: UNCOMMENT
        # FindReceiver specific modification
        temp_list = [float(0) for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


def start(sensors: list[Sensor],model: Model, sender, sender_rr):
    receiver = []

    # Oblicz dystans wszystki węzłów z wysyłającym
    n = model.n
    distance = zeros(1, n)

    for i, sensor in enumerate(sensors[:-1]):
        distance[i] = math.sqrt(
            pow(sensor.xd - sensors[sender].xd, 2) + pow(sensor.yd - sensors[sender].yd, 2)
        )

        # węzeł musi być w zasięgu

        if distance[i] <= sender_rr and sender != sensor.id:
            receiver.append(sensor.id)
            print(f"{sender} ma odbiorcę: {sensor.id}")
    return receiver