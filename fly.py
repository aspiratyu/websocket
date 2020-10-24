import asyncio
import threading

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import math
import time

from websocket_server import Server

N = 1


# def animate(i):
#    for dot in a:
#        dot.move()
#    d.set_data([dot.x for dot in a],
#               [dot.y for dot in a])
#    return d,


class point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # def move(self):
    #     def distance(x1, y1, x2, y2):
    #         return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    #
    # def inside(x1, y1):
    #     if distance(x1, y1, x2, y2) <= Radius:
    #         return True
    #     else:
    #         return False
    #
    # def calc_dist(d):
    #     ret = 0
    #     for x in a:
    #         if inside(x.x, x.y) and x != d:
    #             ret = ret + distance(x.x, x.y, d.x, d.y)
    #         return ret


class fly:

    def __init__(self, max_x, max_y, radius):
        self.max_x = max_x
        self.max_y = max_y
        self.RADIUS = radius
        self.n = 1e7
        self.k = 0.9
        self.destination = point(max_x * np.random.random_sample(), max_y * np.random.random_sample())
        # target = point(10, 10)
        self.point2 = point(0, 0)
        self.point3 = point(0, 0)
        self.target = point(0, 0)
        self.a = [self.destination, self.point2, self.point3, self.target]
#        self.animate()

    def getflycoord(self) -> point:
        return self.a[4]

    def get_x(self):
        return self.a[len(self.a)-1].x

    def get_y(self):
        return self.a[len(self.a) - 1].y

    def start_fly(self):
        thread = threading.Thread(target=self.animate())
        thread.start()
        thread.join()

    async def animate(self):
        while True:
            #print("target ", self.a[0].x, " ", self.a[0].y)

            for i in range(1, len(self.a)):
                self.a[i].x = self.k * self.a[i].x + (1 - self.k) * self.a[i - 1].x
                self.a[i].y = self.k * self.a[i].y + (1 - self.k) * self.a[i - 1].y

            dx = self.a[0].x - self.a[len(self.a) - 1].x
            dy = self.a[0].y - self.a[len(self.a) - 1].y
            if math.sqrt(dx ** 2 + dy ** 2) <= self.RADIUS:
                while math.sqrt(dx ** 2 + dy ** 2) <= self.RADIUS:
                    self.a[0].x = self.max_x * np.random.random_sample()
                    self.a[0].y = self.max_y * np.random.random_sample()
                    dx = self.a[0].x - self.a[len(self.a) - 1].x
                    dy = self.a[0].y - self.a[len(self.a) - 1].y
                    #print("target ", self.a[0].x, " ", self.a[0].y)

            print("fly ", self.a[len(self.a) - 1].x, " ", self.a[len(self.a) - 1].y)
            #Server.send_to_all(str(self.a[len(self.a) - 1].x) + " " + str(self.a[len(self.a) - 1].y))
            await asyncio.sleep(0.1)

        # ax.plot(a[len(a) - 1].x, a[len(a) - 1].y, 'ro')
        # ax.plot(a[0].x, a[0].y, 'bx')



# anim = animation.FuncAnimation(fig, animate, interval=20)
# plt.show()
#
# for p in a:
#    plt.scatter(p.x, p.y)
#    plt.pause(0.01)
# plt.scatter(a[len(a)-1].x, a[len(a)-1].y)
# plt.pause(0.01)
