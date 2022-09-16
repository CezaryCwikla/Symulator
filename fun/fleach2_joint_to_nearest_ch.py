from FLEACH_basics import Model, Sensor
from math import inf, sqrt

def zeros(row, column):
    re_list = []
    for x in range(row):
        # JoinToNearestCH specific modification
        temp_list = [0 for _ in range(column)]
        re_list.append(temp_list)

    return re_list


def get_min_and_id_of_ch(model: Model, TotalCH, distance: list):
    min_dist_from_all_ch = []
    id_of_min_dist_ch = []
    total_nodes = model.n
    number_of_ch = len(TotalCH)

    for node in range(total_nodes):
        min_dist = inf
        ch_id = -1
        for ch in range(number_of_ch):
            if distance[ch][node] <= min_dist:
                min_dist = distance[ch][node]
                ch_id = ch

        min_dist_from_all_ch.append(min_dist)
        id_of_min_dist_ch.append(ch_id)
    return min_dist_from_all_ch, id_of_min_dist_ch



def start(Sensors: list [Sensor], model: Model, TotalCH):
    # print('# ##############################################################')
    # print('# ############# Węzły dołączają do najbliższego CH #############')
    # print('# ##############################################################')

    total_nodes = model.n
    number_of_ch = len(TotalCH)

    if number_of_ch > 0:
        # tworzenie macierzy 2x2 gdzie kazdy wiersz posiada infroamcje odleglosci wszystkich wezlow od CH
        distance = zeros(number_of_ch, total_nodes)
        for i in range(total_nodes):
            for j in range(number_of_ch):
                distance[j][i] = sqrt(
                    pow(Sensors[i].xd - Sensors[TotalCH[j]].xd, 2) + pow(Sensors[i].yd - Sensors[TotalCH[j]].yd, 2)
                )

        # co poniżej robi to:
        # Zapisaliśmy wszystkie CH jako wiersz i wzięliśmy odległość między każdym CH a wszystkimi węzłami w jego kolumnach
        # to przyjmuje minimalną wartość każdej kolumny, tj. min dist dla każdego węzła i ta dist to dist to CH
        min_dist_from_all_ch, id_of_min_dist_ch = get_min_and_id_of_ch(model, TotalCH, distance)

        for i, sensor in enumerate(Sensors[:-1]):
            if sensor.E > 0:
                # jeśli węzeł znajduje się w RR CH i jest bliżej CH niż Stacja
                if min_dist_from_all_ch[i] <= model.RR:
                    # print(f'{sensor.id} dołącza do {TotalCH[id_of_min_dist_ch[i]]}')
                    sensor.MCH = TotalCH[id_of_min_dist_ch[i]]
                    sensor.dis2ch = min_dist_from_all_ch[i]
