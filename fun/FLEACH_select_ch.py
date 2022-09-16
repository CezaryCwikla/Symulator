import random
random.seed(9)
from FLEACH_basics import Sensor


def start(sensors: list[Sensor], model, round_number: int):
    CH = []
    n = model.n
    p = model.p

    list_of_nodes = sorted(sensors[:-1], key=lambda item: item.E, reverse=True)

    for node in list_of_nodes[:int(p * n)]:
        CH.append(node.id)
        node.type = 'C'
        # node.G = round (1 / model.p) - 1 # <- to moze do innego algorytmu

    return CH