import matplotlib
from LEACH_basics import Sensor, Model
from IPython.display import clear_output
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# todo: add condition to show sink only as red dot and not both red and blue
def start(Sensors: [Sensor], myModel: Model, round_number):
    print('########################################')
    print('############# plot Sensors #############')
    print('########################################')
    print()

    n = myModel.n
    fig, axis = plt.subplots()
    axis.set_xlim(left=0, right=myModel.x)
    axis.set_ylim(bottom=0, top=myModel.y)
    deadNum = 0
    n_flag = True
    c_flag = True
    d_flag = True
    for sensor in Sensors:
        if sensor.E > 0:
            if sensor.type == 'N':
                xl = [sensor.xd, Sensors[sensor.MCH].xd]
                yl = [sensor.yd, Sensors[sensor.MCH].yd]
                axis.plot(xl, yl)
                if n_flag:
                    axis.scatter([sensor.xd], [sensor.yd], c='k', edgecolors='k', label='Nodes')
                    axis.text(sensor.xd, sensor.yd, round(sensor.E,3))
                    n_flag = False
                else:
                    axis.scatter([sensor.xd], [sensor.yd], c='k', edgecolors='k')
            #       plot(Sensors(i).xd, Sensors(i).yd, 'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'k');
                    axis.text(sensor.xd, sensor.yd, round(sensor.E,3))
            #             pass  # todo: Plot here

            elif sensor.type == 'C':  # Sensors.type == 'C'
                if c_flag:
                    axis.scatter([sensor.xd], [sensor.yd], s=120, c='r', edgecolors='k', label='Cluster Head')
                    c_flag = False
                else:
                    axis.scatter([sensor.xd], [sensor.yd], s=120, c='r', edgecolors='k')
                # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize', 5, 'MarkerFaceColor', 'r');
                # pass  # todo: Plot here
        else:
            deadNum += 1
            if d_flag:
                axis.scatter([sensor.xd], [sensor.yd], c='w', edgecolors='k', label='Dead')
                d_flag = False
            else:
                axis.scatter([sensor.xd], [sensor.yd], c='w', edgecolors='k')
    #         # plot(Sensors(i).xd,Sensors(i).yd,'ko', 'MarkerSize',5, 'MarkerFaceColor', 'w');
    #         pass  # todo: plot here

    axis.scatter([Sensors[n].xd], [Sensors[n].yd], s=120, c='b', edgecolors='k', label="Sink")
    plt.title('Network Plot for Leach \n Round no: %d' % round_number + '  Dead No: %d ' % deadNum)
    plt.xlabel('X [m]')
    plt.ylabel('Y [m]')
    plt.legend(loc='upper right')
    plt.show()

