from LEACH_basics import Sensor

def start(Sensors: list[Sensor], receiver):
    sender = []
    for sensor in Sensors[:-1]:
        if sensor.MCH == receiver and sensor .id != receiver:
            sender.append(sensor.id)

    return sender