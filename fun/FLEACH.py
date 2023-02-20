from math import *
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import FLEACH_basics
import FLEACH_select_ch
import reset_sensors
import send_receive_packets
import findReceiver
import findSender
import join_to_nearest_ch
import plotter2, plotter
matplotlib.use('TkAgg')


def zeros(row, column):
    re_list = []
    for x in range(row):
        temp_list = [0 for _ in range(column)]
        if row == 1:
            re_list.extend(temp_list)
        else:
            re_list.append(temp_list)

    return re_list


class FLEACHSimulation:

    def __init__(self, n=100, version=1):
        self.n = n  # Przypisz liczbę węzłów
        self.version = version
        # ###################################################################
        # ############# Dla przypisz_początkowe_wartości_węzłom #############
        # ###################################################################
        self.dead_num = 0  # Liczba padnięty węzłów
        self.num_of_ch = 0  # Liczba głów klastrów
        self.flag_first_dead = 0  # Flaga do wskazywania kiedy umarł pierwszy węzeł
        self.initEnergy = 0

        # Stwórz węzły i model energii, a następnie przypisz parametry
        self.model = FLEACH_basics.Model(self.n)

        # Poniżej będzie długość (Max_rounds), więc każdy element będzie przechowywać całkowitą liczbę pakietów w każdej rundzie
        # długość to rmax + 1, ponieważ wykonujemy również jedną rundę inicjalizacji.
        self.SRP = zeros(1, self.model.rmax + 1)  # liczba wysłanych pakietów dot routingu
        self.RRP = zeros(1, self.model.rmax + 1)  # liczba odebranych pakietów dot routingu
        self.SDP = zeros(1, self.model.rmax + 1)  # liczba wysłanych  pakietów danych
        self.RDP = zeros(1, self.model.rmax + 1)  # liczba odebranych pakietów danych

        # #########################################################
        # ############# Zmienne pod początek symulacji ############
        # #########################################################

        # licznik bitów przesyłanych do stacji bazowej i głów klastrów
        self.srp = 0  # liczba wysłanych pakietów dot routingu
        self.rrp = 0  # liczba odebranych pakietów dot routingu
        self.sdp = 0  # liczba wysłanych  pakietów danych do stacji
        self.rdp = 0  # liczba odebranych pakietów danych przez stację


        # Do inicjalizacji main_loop

        self.dead_num = []
        self.packets_to_base_station = 0
        self.first_dead_in = -1
        # ##########################################
        # ############# Dla statystyk ##############
        # ##########################################
        self.alive = self.n

        # wyzerowanie liczby padniętych węzłow
        self.sum_dead_nodes = zeros(1, self.model.rmax + 1)
        self.ch_per_round = zeros(1, self.model.rmax + 1)
        self.alive_sensors = zeros(1, self.model.rmax + 1)
        self.alive_sensors[0] = self.n

        self.sum_energy_left_all_nodes = zeros(1, self.model.rmax + 1)
        self.avg_energy_All_sensor = zeros(1, self.model.rmax + 1)
        self.consumed_energy = zeros(1, self.model.rmax + 1)
        self.Enheraf = zeros(1, self.model.rmax + 1) #srednia energia wezłów żywych!

        ##testtyyyyyyy

        print(self.model)
        print(vars(self.model))
        print("LEN SRP =", len(self.SRP))
        print("self.SRP", self.SRP)
        print("self.RRP", self.RRP)
        print("self.SDP", self.SDP)
        print("self.RDP", self.RDP)
        print('----------------------------------------------')

    def start(self):
        print("#################################")
        print("############# Start #############")
        print("#################################")
        print()

        # ##########################################
        # ############# Stwórz Sensory #############
        # ##########################################
        self.create_sen()

        # ############################################
        # ############# Start Simulation #############
        # ############################################
        self.start_simulation()

        # #############################################
        # ############# Main loop program #############
        # #############################################
        self.main_loop()

        # Todo: all plotting should be done in Leach_plotter file

        print('-------------------- XXX --------------------')
        print('############# Koniec symulacji #############')
        print('-------------------- XXX --------------------')

    def create_sen(self):
        print("##########################################")
        print("############# Tworzenie czujników #############")
        print("##########################################")
        print()

        # tworzenie losowego scenariusza i ladowanie losowej lokalizacji węzłow
        self.Sensors = FLEACH_basics.create_sensors(self.model)

        for sensor in self.Sensors[:-1]:
            self.initEnergy += sensor.E

        # Na początku jest pełna energia
        self.sum_energy_left_all_nodes[0] = self.initEnergy
        self.avg_energy_All_sensor[0] = self.initEnergy / self.n

        print("self.initEnergy", self.initEnergy)
        print('----------------------------------------------')

    def start_simulation(self):
        print("############################################")
        print("############# Start Simulation #############")
        print("############################################")
        print()

        # print("###############################################################################")
        # print("############# Stacja rozsyła wiadomość Hello do wszystkich węzłów #############")
        # print("###############################################################################")
        # print()

        self.sender = [self.n]
        self.receivers = [_ for _ in range(self.n)]

        self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
            self.Sensors, self.model, self.sender, self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
            packet_type='Hello'
        )

        print("self.srp", self.srp)
        print("self.rrp", self.rrp)
        print("self.sdp", self.sdp)
        print("self.rdp", self.rdp)

        self.SRP[0] = self.srp
        self.RRP[0] = self.rrp
        self.SDP[0] = self.sdp
        self.RDP[0] = self.rdp

        print('self.SRP', self.SRP)
        print('self.RRP', self.RRP)
        print('self.SDP', self.SDP)
        print('self.RDP', self.RDP)

    def main_loop(self):
        print("################################################")
        print("############# Główna część programu#############")
        print("################################################")
        print()

        for round_number in range(1, self.model.rmax +1):
            self.r = round_number

            # print('############# Inicjalizacja głównej pętli ##########')
            self.srp, self.rrp, self.sdp, self.rdp = reset_sensors.start(self.Sensors, self.model, round_number)

            # ############# wybór głowy klastra #############
            self.cluster_head_selection_phase(round_number)
            self.no_of_ch = len(self.list_CH)  # Liczba głów klastrów
            if self.no_of_ch < 5:
                print(self.no_of_ch)
            # if round_number == 1 or round_number == self.model.rmax or round_number == self.model.rmax - 10:
            #     plotter2.start(self.Sensors, self.model, round_number, self.version)

            # #################################################
            # ############# faza stanu ustalonego #############
            # #################################################
            self.steady_state_phase()
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

    def plots(self):
        figure, axis = plt.subplots(3, 2, figsize=(10, 6), constrained_layout=True)

        a = list(range(len(self.SRP)))
        axis[0, 0].plot(a, self.SRP, label="Wysłane pakiety")
        axis[0, 0].plot(a, self.RRP, label="Odebrane pakiety")
        axis[0, 0].set_title("Liczba wysłanych i odebranych pakietów dotyczących routingu")
        axis[0, 0].legend(loc='lower right', shadow=True)
        axis[0, 0].set_ylabel('Liczba pakietów')
        axis[0, 0].set_xlabel('Numer rundy')
        axis[0, 0].grid(True)


        axis[0, 1].plot(a, self.SDP, label="Sent packets")
        axis[0, 1].plot(a, self.RDP, label="Received packets")
        axis[0, 1].set_title("Number of data packets sent and received")
        axis[0, 1].legend(loc='lower right', shadow=True)
        axis[0, 1].set_ylabel('Number of data packets')
        axis[0, 1].set_xlabel('Round number')
        axis[0, 1].grid(True)

        axis[1, 0].plot(a, self.sum_dead_nodes)
        axis[1, 0].set_title("Total number of nodes discharged")
        axis[1, 0].set_ylabel('Number of nodes discharged')
        axis[1, 0].set_xlabel('Round number')
        axis[1, 0].grid(True)

        axis[1, 1].plot(a, self.ch_per_round)
        axis[1, 1].set_title("Liczba głów klastrów na rundę")
        axis[1, 1].set_ylabel('Liczba głów klastrów')
        axis[1, 1].set_xlabel('Numer rundy')
        axis[1, 1].grid(True)

        axis[2, 0].plot(a, self.avg_energy_All_sensor)
        axis[2, 0].set_title("Average node energy per round")
        axis[2, 0].set_ylabel('Energy')
        axis[2, 0].set_xlabel('Round number')
        axis[2, 0].grid(True)
        # plt.show()

        axis[2, 1].plot(a, self.consumed_energy)
        axis[2, 1].set_title("Total energy consumption per round")
        axis[2, 1].set_ylabel('Energy')
        axis[2, 1].set_xlabel('Round number')
        axis[2, 1].grid(True)
        plt.show()
        print(f"Pierwszy węzeł padł w rundzie {self.first_dead_in}")

    def cluster_head_selection_phase(self, round_number):

        # Wybór Głowy Klastra  na podstawie fazy konfiguracji LEACH
        # self.list_CH przechowuje identyfikatory wszystkich CH w bieżącej rundzie
        self.list_CH = FLEACH_select_ch.start(self.Sensors, self.model, round_number, self.version)
        self.no_of_ch = len(self.list_CH)

        #rozgłaszanie głów
        self.broadcast_cluster_head()

        #dołącz do najblizszej głowy klastra, bez stacji bazowych!
        join_to_nearest_ch.start(self.Sensors, self.model, self.list_CH, self.version)

        # ########################################
        # ############# wykres dla wezłow #############
        # ########################################
        # plotter.start(self.Sensors, self.model, round_number)


    def broadcast_cluster_head(self):
        # print('#########################################################################################')
        # print('############# Rozgłaszanie do wszystkich węzłów, które są w zasięgu #####################')
        # print('#########################################################################################')
        # print()

        # Nadawanie CH x do wszystkich czujników, które znajdują się w wściekłości radiowej x. (nie transmituj do zlewu)
        # Robi to dla wszystkich CH
        for ch_id in self.list_CH:
            # print(f'for cluster head: {ch_id}')
            self.receivers: list = findReceiver.start(self.Sensors, self.model, sender=ch_id,
                                                      sender_rr=self.Sensors[ch_id].RR)
            # todo: test
            # print("\n sender (lub CH): ", ch_id)
            # print('self.Receivers: ', end='')
            # print(self.receivers)

            self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                self.Sensors, self.model, [ch_id], self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                packet_type='Hello'
            )
        # print("self.srp", self.srp)
        # print("self.rrp", self.rrp)
        # print("self.sdp", self.sdp)
        # print("self.rdp", self.rdp)
        # print("Sensors: ", )

    def steady_state_phase(self):
        # print('#################################################')
        # print('############# faza stanu ustalonego #############')
        # print('#################################################')
        # print()
        for i in range(self.model.NumPacket):  # liczba pakietow w danej rundzie


            # print('##################################################################')
            # print('############# wszystkie czujniki wysylaja dane do CH #############')
            # print('##################################################################')

            for receiver in self.list_CH:
                sender = findSender.start(self.Sensors, receiver)

                # print("sender: ", sender)
                # print("receiver: ", receiver)

                self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                    self.Sensors, self.model, sender, [receiver], self.srp, self.rrp, self.sdp, self.rdp,
                    packet_type='Data'
                )

                # print("self.srp", self.srp)
                # print("self.rrp", self.rrp)
                # print("self.sdp", self.sdp)
                # print("self.rdp", self.rdp)
                # print("Sensors: ", )

                # plotter.start(self.Sensors, self.model, round_number)

            # print("################################################################")
            # print("wyślij pakiet danych bezpośrednio z węzłów (nie znajdują się w żadnym klastrze) do Stacji #############")
            # print(################################################################")

            for sender in self.Sensors:
                # if the node has sink as its CH but it's not sink itself and the node is not dead
                if sender.MCH == self.n and sender.id != self.n and sender.E > 0:
                    self.receivers = [self.n]
                    sender = [sender.id]

                    # print(f'wezel {sender} przesle prosto do stacji bazowej')

                    self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                        self.Sensors, self.model, sender, self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                        packet_type='Data'
                    )

        # print('###################################################################################')
        # print('############# Po agregacji danych wyslij dane z CH do Stacji Bazowej ##############')
        # print('###################################################################################')
        # print()
        # print('wysyłający (lub CH) = ', self.list_CH)

            for sender in self.list_CH:
                self.receivers = [self.n]

                # print("wysylajacy: ", sender)
                # print("odbierajacy: ", self.receivers)

                self.srp, self.rrp, self.sdp, self.rdp = send_receive_packets.start(
                    self.Sensors, self.model, [sender], self.receivers, self.srp, self.rrp, self.sdp, self.rdp,
                    packet_type='Data'
                )
        # print("self.srp", self.srp)
        # print("self.rrp", self.rrp)
        # print("self.sdp", self.sdp)
        # print("self.rdp", self.rdp)
        # print("Sensors: ", )
    def check_dead_num(self, round_number):
        # jesli padl
        for sensor in self.Sensors:
            if sensor.E <= 0 and sensor not in self.dead_num:
                sensor.df = 1
                self.dead_num.append(sensor)
                print(f'{sensor.id} padł, \ndeadnum=')
                for _ in self.dead_num:
                    print(_.id, end=' ')
                print()

        # flaga ze padl
        if len(self.dead_num) > 0 and self.flag_first_dead == 0:
            self.first_dead_in = round_number
            self.flag_first_dead = 1
            print(f'pierwszy wezel padł w rundzie: {round_number}')

    def statistics(self, round_number):
        # print('######################################')
        # print('############# STATYSTKI ##############')
        # print('######################################')

        self.sum_dead_nodes[round_number] = len(self.dead_num)
        self.ch_per_round[round_number] = self.no_of_ch

        self.SRP[round_number] += self.srp
        self.RRP[round_number] += self.rrp
        self.SDP[round_number] += self.sdp
        self.RDP[round_number] += self.rdp

        self.alive = 0
        sum_energy_left_all_nodes_in_curr_round = 0
        for sensor in self.Sensors[:-1]:
            if sensor.E > 0:
                self.alive += 1
                sum_energy_left_all_nodes_in_curr_round += sensor.E

        self.alive_sensors[round_number] = self.alive
        self.sum_energy_left_all_nodes[round_number] = sum_energy_left_all_nodes_in_curr_round
        if self.alive:
            self.avg_energy_All_sensor[round_number] = sum_energy_left_all_nodes_in_curr_round / self.alive
        else:
            self.avg_energy_All_sensor[round_number] = 0
        self.consumed_energy[round_number] = (self.initEnergy - self.sum_energy_left_all_nodes[round_number])

        En = 0

        for sensor in self.Sensors:
            if sensor.E > 0:
                En += pow(sensor.E - self.avg_energy_All_sensor[round_number], 2)

        if self.alive:
            self.Enheraf[round_number] = En / self.alive
        else:
            self.Enheraf[round_number] = 0

    def print_statistics(self):
        #print("round number:", round_number)
        print("len(self.SRP)", len(self.SRP))
        print("self.SRP", self.SRP)
        print("self.RRP", self.RRP)
        print("self.SDP", self.SDP)
        print("self.RDP", self.RDP)

        print('----------------------------------------------')
        a = 200
        b = 300
        c = 400

        # print('self.total_energy_dissipated', self.total_energy_dissipated)
        # print('self.AllSensorEnergy', self.AllSensorEnergy)
        print('self.sum_dead_nodes', self.sum_dead_nodes)
        print('self.ch_per_round', self.ch_per_round)
        print('self.alive_sensors', self.alive_sensors)
        print('self.sum_energy_all_nodes', self.sum_energy_left_all_nodes)
        print('self.avg_energy_All_sensor', self.avg_energy_All_sensor)
        print('self.consumed_energy', self.consumed_energy)
        print('self.Enheraf', self.Enheraf)
        print('----------------------------------------------')
        print(self.SRP[a], ",", self.SRP[b], ",", self.SRP[c])
        print(self.RRP[a], ",", self.RRP[b], ",", self.RRP[c])
        print(self.SDP[a], ",", self.SDP[b], ",", self.SDP[c])
        print(self.RDP[a], ",", self.RDP[b], ",", self.RDP[c])
        print(self.sum_dead_nodes[a], ",", self.sum_dead_nodes[b], ",", self.sum_dead_nodes[c])
        print(self.ch_per_round[a], ",", self.ch_per_round[b], ",", self.ch_per_round[c])
    #    print(self.alive_sensors[150], ",", self.alive_sensors[175], ",", self.alive_sensors[200])
        print(self.sum_energy_left_all_nodes[a], ",", self.sum_energy_left_all_nodes[b], ",",
              self.sum_energy_left_all_nodes[c])
        # #print(self.avg_energy_All_sensor[150], ",", self.avg_energy_All_sensor[175], ",",
        #       self.avg_energy_All_sensor[200])
        print("SDP - sumarycznie", sum(self.SDP))
        print("RDP - sumarycznie", sum(self.RDP))
        print(self.consumed_energy[a], ",", self.consumed_energy[b], ",", self.consumed_energy[c])