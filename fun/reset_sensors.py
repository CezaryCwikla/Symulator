import math

from LEACH_basics import Sensor, Model

def start(Sensors: list[Sensor], model: Model, round_number):
    for sensor in Sensors[:-1]:
        # print(f"\nresetting {sensor.id}")

        # Ustawienia by węzły znowu mogły zostać głową klastra
        # Po każdej rundzie AroundClear, każdy węzeł może być głową klastra
        AroundClear = 1 / model.p
        if round_number % AroundClear == 0:
            sensor.G = 0

        # na początku wszystkie węzły mają stację bazową jako głowę klastra:
        sensor.MCH = model.n

        if sensor.type != 'S':
            sensor.type = 'N'

        sensor.dis2ch = math.inf

    srp = 0  # liczba wysłanych pakietów dot routingu
    rrp = 0  # liczba odebranych pakietów dot routingu
    sdp = 0  # liczba wysłanych  pakietów danych do stacji
    rdp = 0  # liczba odebranych pakietów danych przez stację

    return srp, rrp, sdp, rdp