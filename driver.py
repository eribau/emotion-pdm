import csv

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
blacklist = [11, 12, 13, 14, 15, 16, 17, 18]

def animate(i):
    with open('a.dat') as data_file:
        data = np.genfromtxt(data_file, delimiter=", ")
    n = len(data)
    y = [-100] * 16
    global blacklist
    #sums = [sum(col) for col in zip(*data)]
    #averages = [sum / n for sum in sums]
    x = [11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    if data[n-1][0] == 0:
        y = [e / -16 for e in data[n-1][1:]] # divide by the TSCH_STATS_RSSI_SCALING_FACTOR
    elif data[n-1][0] == 1:
        blacklist = data[n-1][1:10]
        print("bl: ", blacklist)

    ax1.clear()
    plt.axis([11, 26, -60, -110])
    ax1.set_ylabel('dBm')
    ax1.set_xlabel('channels')

    for channel in blacklist:
        plt.vlines(x=channel, ymin=-60, ymax=-110, colors='r', linewidth=6)
    ax1.plot(x, y)

ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()
