import random

from LEACH_basics import Sensor


def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


def start(sensors: list[Sensor], model, round_number: int):
    CH = []
    n = model.n

    for sensor in sensors[:-1]:
        if sensor.E > 0 and sensor.G <= 0:
            # Wybór głowy klastra
            temp = random.uniform(0,1)
            value = model.p / (1 - model.p * (round_number % round(1 / model.p)))
            print(f' dla węzła {sensor.id} losowa wartość wynosi = {temp}, wartość progowa: {value}')
            if temp <= value:
                print(f' Węzeł {sensor.id} zostaje głowa klastra!')
                CH.append(sensor.id)
                sensor.type = 'C'
                sensor.G = round(1 / model.p) - 1
    return CH