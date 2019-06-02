import matplotlib.pyplot as plt

# Plots configuration
# list of styles:

# plt.style.use('dark_background')

#  https://matplotlib.org/gallery/style_sheets/style_sheets_reference.html
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 10
plt.rcParams['figure.figsize'] = 10, 15
# To look as crispy as osciloscope images:
plt.rcParams['lines.linewidth'] = 0.1
plt.rcParams['lines.antialiased'] = False
# # plt.rcParams['axes.facecolor'] = 'black'

# matplotlib alpha
ALPHA = .8
