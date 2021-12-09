import matplotlib.pyplot as plt
import numpy as np

# Some customization
save_pdf = True
laminar_line_color = 'black'
relative_roughness_color = 'maroon'
interval_arrows_color = 'deepskyblue'

# Choose which relative roughness lines to plot and the major and minor ticks for the friction factor axis
relative_roughness = [0, 0.00001, 0.00005, 0.0001, 0.0002, 0.0004, 0.0006, 0.0008, 0.001, 0.002, 0.004, 0.006, 0.008, 0.01,
                      0.015, 0.02, 0.03, 0.04, 0.05]
major_ticks = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
minor_ticks = [0.008, 0.009, 0.0125, 0.015, 0.025]

fig, ax = plt.subplots()  # You can do more with figure and axis object

# Plotting the laminar line
Re_lam = np.linspace(64/0.1, 2300, 1000)
Re_transition = np.linspace(2300, 10_000, 1000)
ax.set_xscale('log')
ax.set_yscale('log')
ax.plot(Re_lam, 64/Re_lam, color=laminar_line_color)
ax.plot(Re_transition, 64/Re_transition, color=laminar_line_color, ls='--')

# Plotting the relative roughness lines
Re_turbulent = np.linspace(10_000, 1e8, 100_000)
for r in relative_roughness:
    f = (1/(-1.8*np.log10((r/3.7)**1.11 + 6.9/Re_turbulent)))**2  # Haaland Equation
    f_trans = (1/(-1.8*np.log10((r/3.7)**1.11 + 6.9/Re_transition)))**2
    ax.plot(Re_turbulent, f, color=relative_roughness_color)
    ax.plot(Re_transition, f_trans, color=relative_roughness_color, ls='--')
    if r != 0.001:  # This is just to fix the issue with the 0.001 being too close to 0.0008
        ax.annotate(f'{r:.5f}'.rstrip('0'), (1.2e8, np.min(f)), va='center',
                    bbox=dict(facecolor='white', pad=0, edgecolor='white'))
    else:
        ax.annotate(f'{r:.5f}'.rstrip('0'), (1.2e8, np.min(f)),
                    bbox=dict(facecolor='white', pad=0, edgecolor='white'))

# Make the laminar, transition, and turbulent intervals
# For more details on annotate: https://matplotlib.org/1.5.3/users/annotations_guide.html
arrow_style = dict(arrowstyle='<|-|>', connectionstyle='arc3', color=interval_arrows_color, lw=1.5,
                   shrinkB=0, shrinkA=0)  # ShrinkA and shrinkB are set to connect, meaning no space.
bbox_parameter = dict(facecolor='white', edgecolor='white', pad=0)
vertical = 0.088
ax.annotate('', xy=(64/0.1, vertical), xytext=(2300, vertical), arrowprops=arrow_style)
ax.annotate('', xy=(2300, vertical), xytext=(10_000, vertical), arrowprops=arrow_style)
ax.annotate('', xy=(10_000, vertical), xytext=(1e8, vertical), arrowprops=arrow_style)
ax.annotate('Laminar', xy=(np.sqrt(64/0.1*2300), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)
ax.annotate('Transition', xy=(np.sqrt(2300*10_000), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)
ax.annotate('Turbulent', xy=(np.sqrt(10_000*1e8), vertical + 0.002), va='bottom', ha='center', size='small',
            bbox=bbox_parameter)

# Grid and Axis Labels
# Do not need to call ax.minorticks_on() if the following gets called:
ax.set_yticks(ticks=major_ticks, labels=[str(i) for i in major_ticks])
ax.set_yticks(ticks=minor_ticks, labels=[str(i) for i in minor_ticks], minor=True)
ax.grid(which='minor', ls='--')
ax.grid(which='major')
ax.set_xlim(np.min(Re_lam), 4e8)
ax.set_ylim(0.007, 0.12)
ax.legend([ax.lines[0], ax.lines[2]],
          [r'Laminar Flow Line ($f=64/Re$)', r'Relative Roughness Lines ($\epsilon/D$)'], ncol=2)
ax.set_ylabel(r'Friction Factor ($f=-\frac{\partial P}{\partial x}\frac{D}{\rho {U_m}^2/2}$)')
ax.set_xlabel(r"Reynold's Number ($Re=\frac{U_mD}{\nu}$)")
ax.set_title('Moody Chart')


if save_pdf:
    fig.set_size_inches(11, 8.5)
    fig.savefig('horizontal_moody_chart.pdf')
    fig.set_size_inches(8.5, 11)
    fig.savefig('vertical_moody_chart.pdf')

plt.show()
