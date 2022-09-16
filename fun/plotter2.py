import matplotlib
from LEACH_basics import Sensor, Model
from IPython.display import clear_output
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# todo: add condition to show sink only as red dot and not both red and blue
def start(Sensors: [Sensor], myModel: Model, round_number):
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
    for sensor in Sensors:
        if sensor.E > 0:
            if sensor.type == 'N':
                xl = [sensor.xd, Sensors[sensor.MCH].xd]
                yl = [sensor.yd, Sensors[sensor.MCH].yd]
                axis.plot(xl, yl)
                if 'f4' in sensor.Fun and f4_flag:
                    axis.scatter(sensor.xd-0.2, [sensor.yd], c='b', s=80, edgecolors='k', label='Węzeł o funkcji f4', marker='>')
                    f4_flag = False
                elif 'f4' in sensor.Fun:
                    axis.scatter(sensor.xd-0.2, [sensor.yd], c='b', s=80, edgecolors='k', marker='>')
                if 'f3' in sensor.Fun and f3_flag:
                    axis.scatter(sensor.xd+0.2, [sensor.yd], c='g', s=80, edgecolors='k', label='Węzeł o funkcji f3', marker='<')
                    f3_flag = False
                elif 'f3' in sensor.Fun:
                    axis.scatter(sensor.xd+0.2, [sensor.yd], c='g', s=80, edgecolors='k', marker='<')
                if 'f2' in sensor.Fun and f2_flag:
                    axis.scatter([sensor.xd], sensor.yd+0.2, c='orange', s=80, edgecolors='k', label='Węzeł o funkcji f2', marker='v')
                    f2_flag = False
                elif 'f2' in sensor.Fun:
                    axis.scatter([sensor.xd], sensor.yd+0.2, c='orange', s=80, edgecolors='k', marker='v')
                if 'f1' in sensor.Fun and f1_flag:
                    axis.scatter([sensor.xd], sensor.yd-0.2, c='k', s=80, edgecolors='k', label='Węzeł o funkcji f1', marker='^')
                    f1_flag = False
                elif 'f1' in sensor.Fun:
                    axis.scatter([sensor.xd], sensor.yd-0.2, c='k', s=80, edgecolors='k', marker='^')
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
                axis.scatter([sensor.xd], [sensor.yd], c='w', edgecolors='k', marker='X', label='Wyczerpany')
                d_flag = False
            else:
                axis.scatter([sensor.xd], [sensor.yd], c='w', edgecolors='k', marker='X')
    #         # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize',5, 'MarkerFaceColor', 'w');
    #         pass  # todo: plot here

    axis.scatter([Sensors[n].xd], [Sensors[n].yd], s=140, c='b', edgecolors='k', label="Stacja bazowa", marker='*')
    plt.title(
        'Wykres sieci dla nowego algorytmu \n Runda numer: %d' % round_number + '  Liczba wyczerpanych węzłów: %d ' % deadNum)
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.legend(loc='upper right')
    plt.show()

