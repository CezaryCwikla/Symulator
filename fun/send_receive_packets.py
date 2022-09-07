import math

from LEACH_basics import Sensor
from LEACH_basics import Model


def send_rec(sensors: list[Sensor], sender, sap):
    # dla wysyłających
    # pakiet zostanie wysłany jeśli węzeł ma na to energię
    if sensors[sender].E > 0:
        # Wyślij pakiet i zwieksz licznik o 1
        sap += 1
        #print(f'{sender} wysłał pakiet. Nowa energia węzła {sender} = {sensors[sender].E}')
    else:
        #print(f' węzeł {sensors[sender].id} padł!')
        sensors[sender].df = 1
    return sap


def start(sensors: list[Sensor], model: Model, senders: list, receivers: list, srp, rrp, sdp, rdp, packet_type: str):
    sent_packets = 0  # liczba wysłanych pakietów
    rec_packets = 0  # liczba odebranych pakietów

    PacketSize = model.hello_packet_len if packet_type == 'Hello' else model.data_packet_len

    # todo sprawdz czy sie nie zwieksza rdp i/lub rdp gdy padł odbiorca i nadawca

    # Badanie utraty energii przez czujniki za przesłanie pakietu
    # Każdy wysylający prześle pakiet do odpowiedniego odbiorcy:

    for sender in senders:
        for receiver in receivers:
            #print("########wysyłający to: ", sender, "odbierający to: ", receiver)
            #print()
            distance = math.sqrt(
                pow(sensors[sender].xd - sensors[receiver].xd, 2) +
                pow(sensors[sender].yd - sensors[receiver].yd, 2)
            )
            #print(f'odległość pomiędzy {sender}  i  {receiver} wynosi: {distance}')

            if distance > model.do:
                sensors[sender].E -= (model.ETX * PacketSize) + model.Emp * PacketSize * pow(distance, 4)
                sent_packets = send_rec(sensors, sender, sent_packets)
            else:
                sensors[sender].E -= (model.ETX * PacketSize) + model.Efs * PacketSize * pow(distance,
                                                                                           2)  # różnica jest potęgi do 2 i do 4
                sent_packets = send_rec(sensors, sender, sent_packets)

    for receiver in receivers:
        sensors[receiver].E -= (model.ERX + model.EDA) * PacketSize

    # Energia rozpraszana z odbiorników w celu odebrania pakietu, jeśli nadawca zginął podczas transmisji,
    # energia odbiornika zostanie zmarnowana, ale nie otrzyma żadnego pakietu

    for sender in senders:
        for receiver in receivers:
            if sensors[receiver].E > 0 and sensors[sender].E > 0:
                rec_packets += 1
                #print(f'{receiver} odebrał pakiet, nowa energia odbiorcy: {receiver} = {sensors[receiver].E}')
            elif sensors[receiver].E < 0:
                sensors[receiver].df = 1

    if packet_type == 'Hello':
        srp += sent_packets
        rrp += rec_packets
        #print(f"zwiększono srp o: {sent_packets} pakietów i rrp o: {rec_packets} pakietów")
    elif packet_type == 'Data':
        sdp += sent_packets
        rdp += rec_packets
        #print(f"zwiększono sdp o: {sent_packets} pakietów i rdp o: {rec_packets} pakietów")

    print()
    return srp, rrp, sdp, rdp
