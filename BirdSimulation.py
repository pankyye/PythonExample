import sys, argparse
import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform,pdist,cdist
from numpy.linalg import norm 

width, height = 640, 480 

class Boids:
    def __init__(self,N):
        # init position
        # 调用reshape()生成N*2的二维数组
        # np.random.rand(2*N) 创建一个包含2N个在[0，1]之间的一维数组
        # 对窗口中心加上10个单位的随机偏移
        self.pos=[width/2.0,height/2.0]+10*np.random.rand(2*N).reshape(N,2) 
        angles=2*math.pi*np.random.rand(N)
        # init velocity
        # zip将两个列表合并成一个元组的列表
        self.vel=np.array(list(zip(np.sin(angles),np.cos(angles)))) 
        self.N=N 
        self.minDist=25.0  # minimal distance 
        self.maxRuleVel=0.03 # max magnitude of velocities calculated by "rules"
        self.maxVel=2.0 # max magnitude of final velocity 

    def applyBC(self):
        '''apply boundary conditions'''
        deltaR=2.0
        for coord in self.pos:
            if coord[0]>width+deltaR:
                coord[0]=-deltaR 
            if coord[0]< - deltaR:
                coord[0]=width + deltaR
            if coord[1]>height + deltaR:
                coord[1] = - deltaR
            if coord[1] < - deltaR:
                coord[1] = height + deltaR

    def tick(self,frameNum,pts,beak):
        '''update the simulation by one time step'''
        # get pairwise distances
        self.distMatrix=squareform(pdist(self.pos))
        # apply rules
        self.vel += self.applyRules()
        self.limit(self.vel, self.maxVel)
        self.pos+=self.vel 
        self.applyBC()
        # update data
        pts.set_data(self.pos.reshape(2*self.N)[::2],
                    self.pos.reshape(2*self.N)[1::2])
        vec=self.pos + 10*self.vel/self.maxVel 
        beak.set_data(vec.reshape(2*self.N)[::2], 
                      vec.reshape(2*self.N)[1::2])

    def limitVec(self,vec,maxVal):
        '''limit magnitude of 2D vevtor'''
        mag=norm(vec)
        if mag>maxVal:
            vec[0], vec[1] = vec[0]*maxVal/mag, vec[1]*maxVal/mag

    def limit(self,X,maxVal):
        '''limit magnitude of 2D vectors in array X to maxValue'''
        for vec in X:
            self.limitVec(vec,maxVal)

    def applyRules(self):
        # apply rule 1: separation 
        D=self.distMatrix<25.0
        vel=self.pos*D.sum(axis=1).reshape(self.N,1)-D.dot(self.pos)
        self.limit(vel,self.maxRuleVel)

        D=self.distMatrix<50.0

        # apply rule 2: alignment
        vel2=D.dot(self.vel)
        self.limit(vel2,self.maxRuleVel)
        vel+=vel2

        # apply rule 2: cohesion
        vel3=D.dot(self.pos)-self.pos 
        self.limit(vel3,self.maxRuleVel)
        vel+=vel3

        return vel 

    def buttonPress(self,event):
        # left click - add a boid
        if event.button == 1:
            self.pos=np.concatenate((self.pos, 
                                       np.array([[event.xdata, event.ydata]])), 
                                      axis=0)
            angles = 2*math.pi*np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel = np.concatenate((self.vel, v), axis=0)
            self.N += 1
        # right click - scatter
        elif event.button == 3:
            # add scattering velocity 
            self.vel += 0.1*(self.pos - np.array([[event.xdata, event.ydata]]))

def tick(frameNum,pts,beak,boids):
    boids.tick(frameNum,pts,beak)
    return pts,beak

def main():
    print('starting boids...')

    parser = argparse.ArgumentParser(description="Implementing Craig Reynold's Boids...")
    parser.add_argument('--num-boids', dest='N', required=False)
    args = parser.parse_args()

    N=100
    if args.N:
        N=int(args.N)

    boids = Boids(N)

    # setup plot
    fig=plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))
    pts, = ax.plot([], [], markersize=10, 
                  c='k', marker='o', ls='None')
    beak, = ax.plot([], [], markersize=4, 
                  c='r', marker='o', ls='None')
    anim = animation.FuncAnimation(fig, tick, fargs=(pts, beak, boids), 
                                 interval=50)

    cid=fig.canvas.mpl_connect('button_press_event',boids.buttonPress)

    plt.show()

if __name__=='__main__':
    main() 





























