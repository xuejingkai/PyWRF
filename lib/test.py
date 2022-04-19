import numpy as np
import matplotlib.pyplot as plt
x, y = np.meshgrid(np.arange(10),np.arange(10))
z = np.sqrt(x**2 + y**2)
cs = plt.contourf(x,y,z,levels=[2,3,4,8])

proxy = [plt.Rectangle((0,0),1,1,fc = pc.get_facecolor()[0])
    for pc in cs.collections]

plt.legend(proxy, ["range(2-3)", "range(3-4)", "range(4-6)"])
plt.show()