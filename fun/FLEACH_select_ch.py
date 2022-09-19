import random
import numpy as np
import math
random.seed(9)
from FLEACH_basics import Sensor



def start(sensors: list[Sensor], model, round_number: int, version = 1):
    CH = []
    n = model.n
    p = model.p

    list_of_nodes = sorted(sensors[:-1], key=lambda item: item.E, reverse=True)

    if version != 3:
        for node in list_of_nodes[:int(p * n)]:
            CH.append(node.id)
            node.type = 'C'
            # node.G = round (1 / model.p) - 1 # <- to moze do innego algorytmu
    else:
        for node in list_of_nodes[:int(p * n)]:
            flag = False
            if CH:
                for ch in CH:
                    distance = math.sqrt(
                        pow(sensors[ch].xd - node.xd, 2) + pow(sensors[ch].yd - node.yd, 2))
                    if distance < 5:
                        flag = True
                        break
            if not flag:
                CH.append(node.id)
                node.type = 'C'


    return CH