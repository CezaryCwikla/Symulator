import random
random.seed(9)
from LEACH_basics import Sensor


def start(sensors: list[Sensor], model, round_number: int):
    CH = []
    n = model.n

    for sensor in sensors[:-1]:
        if sensor.E > 0 and sensor.G <= 0:
            temp = random.uniform(0,1)
            value = model.p / (1 - model.p * (round_number % round(1 / model.p)))
            if temp <= value:
                CH.append(sensor.id)
                sensor.type = 'C'
                sensor.G = round(1 / model.p) - 1
    return CH