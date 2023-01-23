import FLEACH_basics
from FLEACH import FLEACHSimulation
import findReceiver_RF_LEACH
import join_to_nearest_ch_RF_LEACH
from math import *
import matplotlib
import matplotlib.pyplot as plt
import LEACH_basics
import reset_sensors
import LEACH_select_ch
import send_receive_packets
import findReceiver
import findSender
import join_to_nearest_ch
import plotter, plotter2, plotter3
matplotlib.use('TkAgg')


class RFLEACH(FLEACHSimulation):

    def __init__(self):
        super().__init__()

    def start(self):
        print("#################################")
        print("############# Start #############")
        print("#################################")
        print()
        self.create_sen()

        # todo: Plot sensors Here
        self.start_simulation()

        self.main_loop()

    def main_loop(self):
        print("################################################")
        print("############# Główna część programu#############")
        print("################################################")
        print()

        for round_number in range(1, self.model.rmax +1):
            self.r = round_number

            # print('#####################################')
            # print(f'############# Rounda {round_number} #############')
            # print('#####################################')

            for sens_fun in self.model.F:
                self.srp, self.rrp, self.sdp, self.rdp = reset_sensors.start(self.Sensors, self.model, round_number)
                curr_sens = [sens for sens in self.Sensors if sens_fun in sens.Fun]

                self.cluster_head_selection_phase(round_number, curr_sens)
                self.no_of_ch = len(self.list_CH)  # Liczba głów klastrów
                print(self.no_of_ch)
                plotter3.start(self.Sensors, self.model, round_number, 1, sens_fun)
                self.steady_state_phase(curr_sens)
                self.check_dead_num(round_number)

                # if all nodes are dead or only sink is left, exit
                if len(self.dead_num) >= self.n:
                    self.lastPeriod = round_number
                    print(f"all dead (dead={len(self.dead_num)}) in round {round_number}")
                    break
                # ######################################
                # ############# STATISTICS #############
                # ######################################
                self.statistics(round_number)
        self.print_statistics()
        self.plots()

    def cluster_head_selection_phase(self, round_number, curr_sens):
        # self.list_CH przechowuje identyfikatory wszystkich CH w bieżącej rundzie
        self.list_CH = LEACH_select_ch.start(curr_sens, self.model, round_number)
        self.no_of_ch = len(self.list_CH)

        self.broadcast_cluster_head(curr_sens)

        # dołącz do najblizszej głowy klastra, bez stacji bazowych!
        join_to_nearest_ch_RF_LEACH.start(self.Sensors, self.model, self.list_CH, curr_sens)

        #plotter.start(self.Sensors, self.model, round_number)

    def broadcast_cluster_head(self, curr_sens):
        for ch_id in self.list_CH:
            # print(f'for cluster head: {ch_id}')
            # Poniżej mozna zmienic sender na object zamiast id
            self.receivers: list = findReceiver_RF_LEACH.start(self.Sensors, self.model, curr_sens, sender=ch_id,
                                                      sender_rr=self.Sensors[ch_id].RR)

            # todo: test
            # print("\n sender (lub CH): ", ch_id)
            # print('self.Receivers: ', end='')
            # print(self.receivers)
            self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                self.Sensors, self.model, [ch_id], self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                packet_type='Hello'
            )

    def steady_state_phase(self, curr_sens):
        for i in range(self.model.NumPacket):  # liczba pakietow w danej rundzie

            for receiver in self.list_CH:
                sender = findSender.start(curr_sens, receiver)

                # print("sender: ", sender)
                # print("receiver: ", receiver)
                self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                    self.Sensors, self.model, sender, [receiver], self.srp, self.rrp, self.sdp, self.rdp,
                    packet_type='Data'
                )
            for sender in curr_sens:
                # if the node has sink as its CH but it's not sink itself and the node is not dead
                if sender.MCH == self.n and sender.id != self.n and sender.E > 0:
                    self.receivers = [self.n]
                    sender = [sender.id]

                    # print(f'wezel {sender} przesle prosto do stacji bazowej')

                    self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                        self.Sensors, self.model, sender, self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                        packet_type='Data'
                    )

            for sender in self.list_CH:
                self.receivers = [self.n]

                # print("wysylajacy: ", sender)
                # print("odbierajacy: ", self.receivers)
                self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                    self.Sensors, self.model, [sender], self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                    packet_type='Data'
                )

sim = RFLEACH()
sim.start()
