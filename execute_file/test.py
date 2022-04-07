import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.font_manager import FontProperties
Simsun = FontProperties(fname="../font/SimSun.ttf")
Times = FontProperties(fname="../font/Times.ttf")
config = {
    "font.family":'serif',
    "mathtext.fontset": 'stix',
    "font.serif": ['SimSun'],
}
mpl.rcParams.update(config)

plt.title(r'分为$\mathrm{Title}$',fontsize=20)
plt.axis('off')
plt.show()