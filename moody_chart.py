import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve

import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

plt.rcParams['text.usetex'] = True

# Some customization
save_pdf = True
laminar_line_color = 'black'
relative_roughness_color = 'maroon'
interval_arrows_color = 'deepskyblue'

# Choose which relative roughness lines to plot and the major and minor ticks for the friction factor axis
relative_roughness = [0, 0.00001, 0.00005, 0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 0.001, 0.002, 0.004, 0.006, 0.008,
                      0.01, 0.015, 0.02, 0.03, 0.04, 0.05]
major_ticks = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
minor_ticks = [0.008, 0.009, 0.0125, 0.015, 0.025]

fig, ax = plt.subplots()  # You can do more with figure and axis object

# Plotting the laminar line
Re_lam = np.linspace(64/0.1, 2000, 1000)
Re_critical = np.linspace(2000, 4500, 1000)
ax.set_xscale('log')
ax.set_yscale('log')
ax.plot(Re_lam, 64/Re_lam, color=laminar_line_color)
ax.plot(Re_critical, 64/Re_critical, color=laminar_line_color, ls='--')

# Plotting the relative roughness lines
Re_turbulent = np.linspace(4500, 1e8, 100_000)
f_lamb = lambda Re_, r_: 0.3086/((np.log10(6.9/Re_ + (r_/3.7)**1.11))**2)  # Haaland Equation (p. 10)
for r in relative_roughness:
    f = f_lamb(Re_turbulent, r)
    f_trans = (1/(-1.8*np.log10((r/3.7)**1.11 + 6.9/Re_critical)))**2
    ax.plot(Re_turbulent, f, color=relative_roughness_color)
    ax.plot(Re_critical, f_trans, color=relative_roughness_color, ls='--')
    if r != 0.001:  # This is just to fix the issue with the 0.001 being too close to 0.0008
        ax.annotate(f'{r:.5f}'.rstrip('0'), (1.2e8, np.min(f)), va='center',
                    bbox=dict(facecolor='white', pad=0, edgecolor='white'))
    else:
        ax.annotate(f'{r:.5f}'.rstrip('0'), (1.2e8, np.min(f)),
                    bbox=dict(facecolor='white', pad=0, edgecolor='white'))

# Plotting the transitional line
f_T = lambda r_: 0.3086/(1.11*np.log10(r_/3.7))**2
Re_lamb = lambda Re, r_: 1.011*f_T(r_) - f_lamb(Re, r_)
Re_trans, f_values = [], []
guess = 1e7
for r in np.linspace(relative_roughness[1] - relative_roughness[1]/3, relative_roughness[-1] + relative_roughness[-1]/3,
                     100_000):
    Re_tran = fsolve(Re_lamb, np.array([guess, ]), args=(r,))[0]
    guess = Re_tran
    if Re_tran > 10**8:
        continue
    Re_trans.append(Re_tran)
    f_values.append(1.011*f_T(r))
ax.plot(Re_trans, f_values, color='darkgrey', ls='-.')

# Make the laminar, critical, and turbulent intervals
# For more details on annotate: https://matplotlib.org/1.5.3/users/annotations_guide.html
arrow_style = dict(arrowstyle='<|-|>', connectionstyle='arc3', color=interval_arrows_color, lw=1.5,
                   shrinkB=0, shrinkA=0)  # ShrinkA and shrinkB are set to connect, meaning no space.
bbox_parameter = dict(facecolor='white', edgecolor='white', pad=0)
vertical = 0.088
ax.annotate('', xy=(64/0.1, vertical), xytext=(2000, vertical), arrowprops=arrow_style)
ax.annotate('', xy=(2000, vertical), xytext=(4500, vertical), arrowprops=arrow_style)
ax.annotate('', xy=(4500, vertical), xytext=(1e8, vertical), arrowprops=arrow_style)
ax.annotate('Laminar', xy=(np.sqrt(64/0.1*2000), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)
ax.annotate('Critical', xy=(np.sqrt(2000*4500), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)
ax.annotate('Turbulent', xy=(np.sqrt(4500*1e8), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)

# Grid and Axis Labels
# Do not need to call ax.minorticks_on() if the following gets called:
ax.set_yticks(ticks=major_ticks, labels=[str(i) for i in major_ticks])
ax.set_yticks(ticks=minor_ticks, labels=[str(i) for i in minor_ticks], minor=True)
ax.grid(which='minor', ls='--')
ax.grid(which='major')
ax.set_xlim(np.min(Re_lam), 2.5e8)
ax.set_ylim(0.007, 0.1)
fig.legend([ax.lines[0], ax.lines[2], ax.lines[-1]],
           [r'Laminar Flow Line ($f=64/Re$)', r'Relative Roughness Lines ($\epsilon/D$)', r'Transition Line'], ncol=3,
           loc='upper center')
ax.set_ylabel(r'Friction Factor ($f=-\frac{\partial P}{\partial x}\frac{D}{\rho {V}^2/2}$)')
ax.set_xlabel(r"Reynold's Number ($Re=\frac{\rho VD}{\mu}$)")
ax.set_title('Moody Chart')
fig.tight_layout()

if save_pdf:
    fig.set_size_inches(8.5, 11)
    fig.savefig('vertical_moody_chart.pdf')
    fig.set_size_inches(11, 8.5)
    fig.savefig('horizontal_moody_chart.pdf')

plt.show()
