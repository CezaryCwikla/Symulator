import matplotlib
from LEACH_basics import Sensor, Model
from IPython.display import clear_output
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# todo: add condition to show sink only as red dot and not both red and blue
def start(Sensors: [Sensor], myModel: Model, round_number, wersja, curr_fun):
    print('########################################')
    print('############# Wyświetl węzły ###########')
    print('########################################')
    print()

    n = myModel.n
    fig, axis = plt.subplots()
    axis.set_xlim(left=0, right=myModel.x)
    axis.set_ylim(bottom=0, top=myModel.y)
    deadNum = 0
    f1_flag = True
    f2_flag = True
    f3_flag = True
    f4_flag = True
    c_flag = True
    d_flag = True
    w_flag = True
    rozmiar_wezla = 10
    oddalenie_od_srodka_hor = 0.5
    oddalenie_od_srodka = 1
    for sensor in Sensors:
        if sensor.E > 0:
            if sensor.type == 'N':
                if curr_fun in sensor.Fun:
                    xl = [sensor.xd, Sensors[sensor.MCH].xd]
                    yl = [sensor.yd, Sensors[sensor.MCH].yd]
                    axis.plot(xl, yl)
                if w_flag:
                    axis.scatter([sensor.xd], [sensor.yd], c='k', edgecolors='k', s=rozmiar_wezla, label='Węzeł')
                    w_flag = False
                else:
                    axis.scatter([sensor.xd], [sensor.yd], c='k', edgecolors='k', s=rozmiar_wezla)
                if 'f4' in sensor.Fun and f4_flag:
                    axis.scatter(sensor.xd-oddalenie_od_srodka_hor, [sensor.yd], c='b', s=80, edgecolors='k', label='Funkcja f4 węzła', marker='>')
                    f4_flag = False
                elif 'f4' in sensor.Fun:
                    axis.scatter(sensor.xd-oddalenie_od_srodka_hor, [sensor.yd], c='b', s=80, edgecolors='k', marker='>')

                if 'f3' in sensor.Fun and f3_flag:
                    axis.scatter(sensor.xd+oddalenie_od_srodka_hor, [sensor.yd], c='g', s=80, edgecolors='k', label='Funkcja f3 węzła', marker='<')

                    f3_flag = False
                elif 'f3' in sensor.Fun:
                    axis.scatter(sensor.xd+oddalenie_od_srodka_hor, [sensor.yd], c='g', s=80, edgecolors='k', marker='<')

                if 'f2' in sensor.Fun and f2_flag:
                    axis.scatter([sensor.xd], sensor.yd+oddalenie_od_srodka, c='orange', s=80, edgecolors='k', label='Funkcja f2 węzła', marker='v')

                    f2_flag = False
                elif 'f2' in sensor.Fun:
                    axis.scatter([sensor.xd], sensor.yd+oddalenie_od_srodka, c='orange', s=80, edgecolors='k', marker='v')

                if 'f1' in sensor.Fun and f1_flag:
                    axis.scatter([sensor.xd], sensor.yd-oddalenie_od_srodka, c='m', s=80, edgecolors='k', label='Funkcja f1 węzła', marker='^')

                    f1_flag = False
                elif 'f1' in sensor.Fun:
                    axis.scatter([sensor.xd], sensor.yd-oddalenie_od_srodka, c='m', s=80, edgecolors='k', marker='^')

                axis.text(sensor.xd, sensor.yd, round(sensor.E, 3))
                #       plot(Sensors(i).xd, Sensors(i).yd, 'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'k');
        #             pass  # todo: Plot here

            elif sensor.type == 'C':  # Sensors.type == 'C'
                if c_flag:
                    axis.scatter([sensor.xd], [sensor.yd], s=140, c='r', edgecolors='k', marker=(5, 0),
                                 label='Głowa klastra')
                    axis.text(sensor.xd, sensor.yd, round(sensor.E, 3))
                    c_flag = False
                else:
                    axis.scatter([sensor.xd], [sensor.yd], s=140, c='r', edgecolors='k', marker=(5, 0))
                    axis.text(sensor.xd, sensor.yd, round(sensor.E, 3))
                # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'r');
                # pass  # todo: Plot here
        else:
            deadNum += 1
            if d_flag:
                axis.scatter([sensor.xd], [sensor.yd], c='w', edgecolors='k', marker='X', label='Wyczerpany węzeł')
                d_flag = False
            else:
                axis.scatter([sensor.xd], [sensor.yd], c='w', edgecolors='k', marker='X')
    #         # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize',5, 'MarkerFaceColor', 'w');
    #         pass  # todo: plot here

    axis.scatter([Sensors[n].xd], [Sensors[n].yd], s=140, c='b', edgecolors='k', label="Stacja bazowa", marker='*')
    if wersja == 1:
        plt.title(
            'Wykres sieci dla pierwszego zaproponowanego algorytmu \n Runda numer: %d' % round_number + '  Liczba wyczerpanych węzłów: %d ' % deadNum)
    elif wersja == 2:
        plt.title(
            'Wykres sieci dla drugiego zaproponowanego algorytmu \n Runda numer: %d' % round_number + '  Liczba wyczerpanych węzłów: %d ' % deadNum)
    elif wersja == 3:
        plt.title(
            'Wykres sieci dla trzeciego zaproponowanego algorytmu \n Runda numer: %d' % round_number + '  Liczba wyczerpanych węzłów: %d ' % deadNum)
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.legend(loc='upper right')
    plt.show()

