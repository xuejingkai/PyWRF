import numpy as np
import matplotlib.pyplot as plt

x=np.linspace(-3,3,100)
y=3*x+4

fig, (ax1, ax2) = plt.subplots(1, 2)

ax1.plot(x, y)
ax1.set_title("Normal Plot")

ax2.plot(x, y)
ax2.set_title("Reverted axes")
#ax2.invert_xaxis()
ax2.invert_yaxis()

fig.tight_layout()
plt.show()