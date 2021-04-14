import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()

def animate(i):
    plt.plot(0,i,'ro')
    print(i)

anim = FuncAnimation(fig, animate, interval=1000)

plt.show()