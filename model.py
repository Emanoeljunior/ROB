from math import sin, cos, pi
import numpy as np
import math


class model(object):
    def __init__(self, th=[0, 0], dt=0.002):
        self.th = np.array([th]).transpose()
        self.l1 = 5
        self.l2 = 3
        self.dt = dt

    def setPos(self, th=[0, 0]):
        self.th = np.array([th]).transpose()

    def integrate(self, thd = [0.1, 0.1]):
        self.thd = np.array([thd]).transpose()
        self.th = self.th + self.thd*self.dt

    def kinematics(self, th=None):

        if th is None:
            th = self.th
        else:
            np.array([th]).transpose()

        x1 = self.l1 * cos(th[0][0])
        y1 = self.l1 * sin(th[0][0])

        x2 = x1 + self.l2 * cos(th[0][0] + th[1][0])
        y2 = y1 + self.l2 * sin(th[0][0] + th[1][0])

        return [[0, x1, x2], [0, y1, y2]]

    def inverseKin(self, p=[0, 0]):

        # escolha qual técnica de cálculo da cinemática inversa
        
        th = self.inverseKinAnalitic(p)
        #th = self.inverseKinNumeric(p)
        
        return th

    def inverseKinAnalitic(self, p=[0, 0]):

        # implementar inversa analítica robô dois elos

        th2 = - math.acos((p[0]**2 + p[1]**2 -self.l1**2 - self.l2**2)/( 2*self.l1*self.l2))
        th1 = math.atan2(p[1], p[0]) - math.asin((self.l2 * math.sin(th2)/math.sqrt(p[0]**2 + p[1]**2)))
        th =  np.array([[th1,th2]]).transpose()
        # th = self.th
        return th

    def inverseKinNumeric(self, p=[0, 0]):
        # implementar inversa numérica robô dois elos

        th = self.th
        return th


