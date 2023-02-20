import random
import math
# random.seed(9)


class Model:
    def __init__(self, n):
        self.n = n

        # Rozmiary obszaru
        self.x = 100
        self.y = 100

        # Pozycja stacji bazowej
        self.stacja_x = self.x * 0.5
        self.stacja_y = self.y * 0.5
        self.stacja_E = 1000

        self.F = ["f1", "f2", "f3", "f4"]

        # Prawdopodobieństwo, że węzeł zostanie głową klastra
        self.p = 0.05

        ############### ENERGIA (jednostki to J, każda wartośc opowiada 1B danych) #####################
        # Wstępna energia
        self.Eo = 1

        # Energia utracona podczas transmisji (ETX) i odbiorze (ERX)
        self.Eelec = 50 * 0.000000001  # Energia utracona przy wyborze
        self.ETX = 50 * 0.000000001
        self.ERX = 50 * 0.000000001

        # Rodzaje wzmacniaczy transmisji
        self.Efs = 10e-12

        self.Emp = 0.0013 * 0.000000000001

        # Energia utracona w wyniku agregacji danych
        self.EDA: float = 5 * 0.000000001

        # Obliczenie "do", wynosi około 80 jednostek
        self.do = math.sqrt(self.Efs / self.Emp)

        ######################## PARAMETRY SYMULACJI #############################
        # maksymalna liczba rund
        self.rmax = 400

        # Rozmiar pakietu danych
        self.data_packet_len = 4000

        # Rozmiar pakietu Hello
        self.hello_packet_len = 100

        # Liczba pakietów wysłanych w fazie stanu ustalonego
        self.NumPacket = 10

        # Zasieg radiowy
        self.RR = 0.5 * self.x * math.sqrt(2)


class Sensor:
    def __init__(self):
        self.xd = 0
        self.yd = 0  # Koordynaty
        self.G = 0  # czy  był głowa klastra? 0 - nie
        self.df = 0  # dead? 0 - nie
        self.type = 'N'  # Typ
        self.E = 0  # Energia
        self.id = 0  # ID
        self.dis2sb = 0  # Oedległość do stacji
        self.dis2ch = 0  # Odległość do głowy
        self.MCH = 0  # Member którego klastra
        self.RR = 0
        self.Fun = []
        self.MIN_DIST = 3


def check_dist_and_relocate(sens: Sensor, list_of_sens):

    for node in list_of_sens:
        if node == sens:
            continue
        distance = math.sqrt(pow(sens.xd - node.xd, 2) + pow(sens.yd - node.yd, 2))
        if distance < sens.MIN_DIST:
            return False
    return True


def create_sensors(model: Model):
    n = model.n
    # Jeden dodatkowy jako stacja bazowa
    sensors = [Sensor() for _ in range(n + 1)]

    with open(r"C:\Users\Czarko\PycharmProjects\SymulatorRFLEACH\sensor_x.txt", "r") as f:
        for i, line in enumerate(f):
            sensors[i - 1].xd = int(line.strip())
    with open(r"C:\Users\Czarko\PycharmProjects\SymulatorRFLEACH\sensor_y.txt", "r") as f:
        for i, line in enumerate(f):
            sensors[i - 1].yd = int(line.strip())

    sensors[n].xd = model.stacja_x
    sensors[n].yd = model.stacja_y
    sensors[n].E = model.stacja_E
    sensors[n].id = model.n
    sensors[n].type = 'S'
    sensors[n].Fun = random.sample(set(model.F), 4)


    for i, sensor in enumerate(sensors[:-1]):
        # Koordynaty
        # sensor.xd = random.randint(1, model.x-1)
        # sensor.yd = random.randint(1, model.y-1)
        # while not check_dist_and_relocate(sensor, sensors):
        #     sensor.xd = random.randint(1, model.x-1)
        #     sensor.yd = random.randint(1, model.y-1)

        # with open("sensor_x.txt", "w") as f:
        #     for sensor in sensors[:-1]:
        #         f.write(str(sensor.xd) + "\n")
        # with open("sensor_y.txt", "w") as f:
        #     for sensor in sensors[:-1]:
        #         f.write(str(sensor.yd) + "\n")

        # Czy był głową klastra? 0 - nie, 1 - tak
        sensor.G = 0
        # Flaga czy padł węzeł? 0 - nie
        sensor.df = 0
        # Węzeł na początku nie jest głową klastra. N - normalny, S - stacja bazowa
        sensor.type = 'N'
        # Na początku wszystkie węzły zaczynają od energii = 1
        sensor.E = model.Eo
        # id
        sensor.id = i
        # Zasięg radiowy
        sensor.RR = model.RR
        sensor.MCH = n
        # odegłość do stacji bazowej
        sensor.dis2sb = math.sqrt(pow((sensor.xd - sensors[-1].xd), 2) + pow((sensor.yd - sensors[-1].yd), 2))
        sensor.Fun = random.sample(set(model.F), random.randint(4,4))

    return sensors
