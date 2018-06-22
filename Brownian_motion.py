#!/usr/bin/env python
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation

FFMpegWriter = manimation.writers['ffmpeg']
metadata = dict(title='Movie Test', artist='Matplotlib', comment='Movie support!')
writer = FFMpegWriter(fps=15, metadata=metadata)

fig = plt.figure()
l, = plt.plot([], [], 'ro', markeredgecolor = 'none')

plt.xlim(-4, 6)
plt.ylim(-4, 4)

plt.xlabel('x')
plt.ylabel('y')

plt.title('2-D Brownian motion in a box with two chambers')

num_of_particles = 500

#x = np.zeros(num_of_particles)
x_set = np.ones(num_of_particles)
x = x_set*2.0
x_old = x_set*2.0

#y_set = np.zeros(num_of_particles)
y_set = np.ones(num_of_particles)
y = y_set*0.0
y_old = y_set*0.0

bound_x1 = -2.0
bound_x2 = 4.0
bound_y1 = -2.0
bound_y2 = 2.0

gate_x1 = 1.0

gate_y1 = -2.0

#gate_y2 = -0.
#gate_y3 = 0.
#gate_y2 = -0.25
#gate_y3 = 0.25
gate_y2 = -0.2
gate_y3 = 0.2

gate_y4 = 2.0

plt.axhline(y=-2.0, xmin=0.2, xmax=0.8, linewidth=2)
plt.axhline(y=2.0, xmin=0.2, xmax=0.8, linewidth=2)
plt.axvline(x=-2.0, ymin=0.25, ymax=0.75, linewidth=2)
plt.axvline(x=4.0, ymin=0.25, ymax=0.75, linewidth=2)

#plt.axvline(x=1.0, ymin=0.25, ymax=0.4375, linewidth=2)
#plt.axvline(x=1.0, ymin=0.5625, ymax=0.75, linewidth=2)
plt.axvline(x=1.0, ymin=0.25, ymax=0.475, linewidth=2)
plt.axvline(x=1.0, ymin=0.525, ymax=0.75, linewidth=2)

steps = 100
sigma_x = 0.1
sigma_y = 0.1

def slope(x_i, x_f, y_i, y_f):
    return (y_f - y_i) / (x_f - x_i)

def direction(x_i, x_f):
    return (x_f - gate_x1) * (x_i - gate_x1)

def offset(x_i, x_f, y_i, y_f):
    return y_i - x_i * (y_f - y_i) / (x_f - x_i)

def y_at_gate(x_i, x_f, y_i, y_f):
    return (y_i - x_i * (y_f - y_i) / (x_f - x_i)) + gate_x1 * (y_f - y_i) / (x_f - x_i)

with writer.saving(fig, "brownian-2d-1.mp4", steps):
    for i in range(steps):
        for j in range(len(x)):
            x_old[j] = x[j]
            y_old[j] = y[j]
            x[j] += sigma_x * np.random.randn()
            y[j] += sigma_y * np.random.randn()

#print 'i=', i, 'j=', j, 'x_old=', x_old[j], 'x=', x[j], 'y_old=', y_old[j],'y=', y[j]

cond = y_at_gate(x_old[j], x[j], y_old[j], y[j])

#if x[j] < bound_x1:
# x[j] = bound_x1 + abs(bound_x1-x[j])
#elif x[j] > bound_x2:
# x[j] = bound_x2 - abs(x[j]-bound_x2)

if (x[j] > gate_x1) and (x_old[j] < gate_x1) and (cond < gate_y2):
    x[j] = gate_x1 - abs(x[j] - gate_x1)
elif (x[j] > gate_x1) and (x_old[j] < gate_x1) and (cond > gate_y3):
    x[j] = gate_x1 - abs(x[j] - gate_x1)

if (x[j] < gate_x1) and (x_old[j] > gate_x1) and (cond < gate_y2):
    x[j] = gate_x1 + abs(x[j] - gate_x1)
elif (x[j] < gate_x1) and (x_old[j] > gate_x1) and (cond > gate_y3):
    x[j] = gate_x1 + abs(x[j] - gate_x1)

if x[j] < bound_x1:
    x[j] = bound_x1 + abs(bound_x1 - x[j])
elif x[j] > bound_x2:
    x[j] = bound_x2 - abs(x[j] - bound_x2)

if y[j] < bound_y1:
    y[j] = bound_y1 + abs(bound_y1 - y[j])
elif y[j] > bound_y2:
    y[j] = bound_y2 - abs(y[j] - bound_y2)

l.set_data(x, y)
writer.grab_frame()
