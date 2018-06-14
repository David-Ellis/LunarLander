# -*- coding: utf-8 -*-
"""
Lunar Lander

Created on Tue Oct  4 15:30:25 2016

@author: David

Version 1:
-Basic falling physics with thrust capability using slider

Version 2:
-resticted thrust based on fuel availability
-added fuel gauge
-added win/lose popup message box

Version 3
- Added speed gauge
- Game window opens as active window
- Added axis labels for trajectory plot
"""

from __future__ import print_function
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib import use
import matplotlib.gridspec as gridspec
import numpy as np
import ctypes 
import sys

use('TkAgg')

def press(event):
    global theta
    if event.key == 'a':
        del_theta = -del_t*np.pi
    elif event.key == 'd':
        del_theta = +del_t*np.pi
    else:
        del_theta = 0
    theta = theta + del_theta
    return 0

def updateLander(height, xPosn, angle, xSpeed, ySpeed, xAcc, yAcc, thr,
                 del_t, fuel, mass):
                            
    nxSpeed = xSpeed + xAcc*del_t
    nySpeed = ySpeed + yAcc*del_t
    
    del_X = xSpeed*del_t + 0.5*xAcc*del_t**2
    del_Y = ySpeed*del_t + 0.5*yAcc*del_t**2
    
    weight = mass*g
    nmass = startMass - 0.5*(startFuel-fuel)

    if fuel>0:
        nyAcc = (thr*np.cos(angle) - weight) / mass
        nxAcc = thr*np.sin(angle)/mass
        nfuel = fuel - 0.007*thr*del_t
    else:
        nyAcc = -weight/mass
        nxAcc = 0
        nfuel = 0
        
    nheight = height + del_Y
    nXposn = xPosn + del_X
    
    return nheight, nXposn, nxSpeed, nySpeed, nxAcc, nyAcc, nfuel, nmass
    
def updatePlots(height, fuel, speed):
    #update height meter
    ax2.set_yticks([height,])
    ax2.set_yticklabels([("%.1f m " % height)])
    hmeter.set_height(height)
    
    #update fuel meter
    ax3.set_yticks([fuel,])
    ax3.set_yticklabels(["%2.0f %%" % (100*fuel/startFuel)])
    fmeter.set_height(fuel)
    
    #initiate speed meter
    ax4.set_yticks([abs(speed)])
    ax4.set_yticklabels(["%2.1f m/s" % abs(speed)])    
    smeter.set_height(abs(speed))
    
    plt.pause(0.01)
    plt.show()
    
    fig.canvas.draw_idle()
    try:
        fig.canvas.flush_events()
    except NotImplementedError:
        pass

def plotLander(x, y, theta, thr):
    ax1.cla() 
    # plot ground
    ax1.plot(groundX, groundY, ' ')
    ax1.fill(groundX, groundY, color = 'gray')
    # plot sky
    ax1.plot(skyX, skyY, '.', color='white')
    
    stdLen = 3
    
    X1 = 1.3*stdLen
    X2 = 1*stdLen
    X3 = 0.6*stdLen
    
    Y1 = 0.3*stdLen
    Y2 = 2*stdLen
    Y3 = 3*stdLen
    YF1 = 0.5*stdLen
    YF2 = 0.7*stdLen
    YF3 = 1*stdLen
    
    landerXvals = np.array([x - (X2/2)*np.cos(theta) + Y1*np.sin(theta),
                            x - X2*np.cos(theta) + Y1*np.sin(theta),
                            x - X1*np.cos(theta), 
                            x - X2*np.cos(theta) + (Y2-Y1)*np.sin(theta),
                            x - X3*np.cos(theta) + (Y3-Y1)*np.sin(theta),
                            x + X3*np.cos(theta) + (Y3-Y1)*np.sin(theta),
                            x + X2*np.cos(theta) + (Y2-Y1)*np.sin(theta),
                            x + X1*np.cos(theta),
                            x + X2*np.cos(theta) + Y1*np.sin(theta),
                            x + (X2/2)*np.cos(theta) + Y1*np.sin(theta),
                            x - YF1*np.sin(theta),
                            x - YF2*np.sin(theta),
                            x - YF3*np.sin(theta)])
                            
    landerYvals = np.array([y + Y1*np.cos(theta) + (X1/2)*np.sin(theta),
                            y + Y1*np.cos(theta) + X2*np.sin(theta),
                            y + X1*np.sin(theta),
                            y + Y2*np.cos(theta) + X2*np.sin(theta),
                            y + Y3*np.cos(theta) + X3*np.sin(theta),
                            y + Y3*np.cos(theta) - X3*np.sin(theta),
                            y + Y2*np.cos(theta) - X2*np.sin(theta),
                            y - X1*np.sin(theta),
                            y + Y1*np.cos(theta) - X2*np.sin(theta),
                            y + Y1*np.cos(theta) - (X2/2)*np.sin(theta),
                            y - YF1*np.cos(theta),
                            y - YF2*np.cos(theta),
                            y - YF3*np.cos(theta)])
                            
          
    ax1.axis([0, 200, 0, 110])
    ax1.set_xticks([])
    ax1.set_yticks([])
    #plot base
    baseXvals = landerXvals[[0, 1, 2, 3, 6, 7, 8, 0]]
    baseYvals = landerYvals[[0, 1, 2, 3, 6, 7, 8, 0]]
    ax1.plot(baseXvals, baseYvals, 'k')
    ax1.fill(baseXvals,baseYvals, color = '#e5a80d')
    #plot top
    topXvals = landerXvals[[3, 4, 5, 6, 3]]
    topYvals = landerYvals[[3, 4, 5, 6, 3]]
    ax1.plot(topXvals, topYvals, 'k')
    ax1.fill(topXvals, topYvals, color = 'gray')
    if thr>10 and thr <5000:
        #plot flame 1
        flameXvals = landerXvals[[0, 9, 10, 0]]
        flameYvals = landerYvals[[0, 9, 10, 0]]
        ax1.plot(flameXvals, flameYvals, 'k')
        ax1.fill(flameXvals, flameYvals, color = 'red')
    elif thr>5000 and thr < 15000:
        #plot flame 2
        flameXvals = landerXvals[[0, 9, 11, 0]]
        flameYvals = landerYvals[[0, 9, 11, 0]]
        ax1.plot(flameXvals, flameYvals, 'k')
        ax1.fill(flameXvals, flameYvals, color = 'red')
    elif thr > 15000:
        #plot flame 3
        flameXvals = landerXvals[[0, 9, 12, 0]]
        flameYvals = landerYvals[[0, 9, 12, 0]]
        ax1.plot(flameXvals, flameYvals, 'k')
        ax1.fill(flameXvals, flameYvals, color = 'red')
    
                            
g = 1 # acceleration due to gravity on the moon in m/s
startMass = 15000
mass = startMass # mass with fuel in kg
maxThrust = 27000 # maximum amount of throttleable thrust in Newtons
height = 100 # start height in meters 
xposn = 50 # starting horizontal position
yspeed = 0 # initial virtical speed
xspeed = 0 # initial horizontal speed
yacc = 0 # initial virtical acceleration
xacc = 0 # initital horizontal acceleration
startFuel = 1500
fuel = startFuel
theta = 0

groundX = np.linspace(0, 201, 35)
groundY = np.array([0])
groundY = np.append(groundY,7*np.random.rand(33))
groundY = np.append(groundY, 0)

skyX = 201*np.random.rand(30)
skyY = 10+90*np.random.rand(30)

#bottom = np.zeros(35)

openMessage = """Welcome to The Lunar Lander! 
Press 'a' and 'd' to tild the lander and slide the thrust bar to increase 
the thrust
"""

winMessage = 'The Eagle has landed!'
loseMessage1 = ' You crashed and died. \n\n You\'ve let NASA down, you\'ve let \
your family down... \n But most of all,  you\'ve let yourself down.'

loseMessage2 = 'You didn\'t land straight, \n and therefore crashed and died/ \
\n\n Well done!'

loseMessage3 = ' You ran out of fuel then crashed and died \n\n You\'ve let\
 NASA down, you\'ve let your family down... \n But most of all,  you\'ve let\
 yourself down.'

weight = mass*g

t = 0
thrust = 0


plt.close('all')
fig = plt.figure('Lunar Lander Game', figsize=(10,6), dpi=80, facecolor='#003489')
fig.suptitle('Lunar Lander', fontsize = 20, color = 'white')
gs = gridspec.GridSpec(9, 3)

#initiate view screen
ax1 = plt.subplot(gs[0:5,:])
ax1.axis([0, 200, 0, 110])
screen = plt.plot()
ax1.set_xticks([])
ax1.set_yticks([])
ax1.set_axis_bgcolor('#002868')

#initiate height meter
ax2 = plt.subplot(gs[5:9, 0])
hmeter, = plt.bar(0, height, facecolor='#9999ff', edgecolor = 'black')
plt.axis([0, hmeter.get_width()/3, 0, height ])
ax2.set_xticks([0.5*hmeter.get_width()])
ax2.set_xticklabels(['Height'],color = 'white')
ax2.set_ylim([0, 100])
ax2.set_yticks([height,])
ax2.set_yticklabels([("%.1f m " % height)],color = 'white', fontsize = 10)

#initiate fuel meter
ax3 = plt.subplot(gs[5:9, 1])
fmeter, = plt.bar(0, fuel, facecolor='#ed5769', edgecolor = 'black')
plt.axis([0, fmeter.get_width()/3, 0, fuel ])
ax3.set_xticks([0.5*fmeter.get_width()])
ax3.set_xticklabels(['Fuel'],color = 'white')
ax3.set_ylim([0, fuel])
ax3.set_yticks([100])
ax3.set_yticklabels(["%2.0f %%" % (100*fuel/startFuel)],color = 'white', fontsize = 10)

#initiate speed meter
ax4 = plt.subplot(gs[5:9, 2])
smeter, = plt.bar(0, fuel, facecolor='#54dd5b', edgecolor = 'black')
plt.axis([0, fmeter.get_width()/3, 0, yspeed ])
ax4.set_xticks([0.5*fmeter.get_width()])
ax4.set_xticklabels(['Speed'],color = 'white')
ax4.set_ylim([0, 15])
ax4.set_yticks([0])
ax4.set_yticklabels(["%2.1f m/s" % yspeed],color = 'white', fontsize = 10)
ax4.yaxis.tick_right()

axThrust = plt.axes([0.18, 0.025, 0.65, 0.04])
thrust = Slider(axThrust, 'Thrust', 0.0, maxThrust, color='#8602e5')
thrust.valfmt = '%.f N'

ctypes.windll.user32.MessageBoxW(0, openMessage, 'Welcome!', 1)

fig.canvas.mpl_connect('key_press_event', press)    

timeStamps = np.array([0])
heightStamps = np.array([height])

t = 0
del_t = 0

while height > 0:
    
    if len(plt.get_fignums()) == 0:
        sys.exit("Program closed")
    
    tic = time.clock() 

    height, xposn, xspeed, yspeed, xacc, yacc, fuel, mass = updateLander(height, xposn, theta, xspeed, yspeed, xacc, yacc, 
                        thrust.val, del_t, fuel, mass)
                                   
    plotLander(xposn, height, theta, thrust.val)                                        
    updatePlots(height, fuel, yspeed)   
    
    del_t = time.clock() - tic
    t = t + del_t
    
    timeStamps = np.append(timeStamps, t)
    heightStamps = np.append(heightStamps, height)   


if abs(yspeed) < 6 and abs(theta) < np.pi/5:
    ctypes.windll.user32.MessageBoxW(0, winMessage, 'Mission Success!', 1)
elif fuel > 0:
    ctypes.windll.user32.MessageBoxW(0, loseMessage1, 'Mission Failed!', 1)
elif abs(theta) > np.pi/5:
    ctypes.windll.user32.MessageBoxW(0, loseMessage2, 'Mission Failed!', 1)
else:
    ctypes.windll.user32.MessageBoxW(0, loseMessage3, 'Mission Failed!', 1)
 
plt.figure("Mission trajectory")
plt.plot(timeStamps, heightStamps)  
plt.xlabel("Time of flight (s)")
plt.ylabel("Height (m)")
plt.title("Flight Trajectory", fontsize = 16)
plt.show()