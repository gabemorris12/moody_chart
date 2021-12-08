import matplotlib.pyplot as plt
import numpy as np

friction_factors = [0.008, 0.009, 0.01, 0.015, 0.02, 0.025, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
major_friction = np.arange(0.01, friction_factors[-1] + 0.01, 0.01)
minor_friction = sorted(list(set(friction_factors).difference(major_friction)))

fig, ax1 = plt.subplots()  # You can do more with figure and axis object

# Plotting the laminar line
Re_lam = np.linspace(64/max(friction_factors), 2300, 1000)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.plot(Re_lam, 64/Re_lam)

# Grid and Axis Labels
ax1.set_yticks(ticks=major_friction, labels=[f'{i:.2f}' for i in major_friction])
ax1.set_yticks(ticks=minor_friction, labels=[str(i) for i in minor_friction], minor=True)
ax1.grid(which='minor', ls='--')
ax1.grid(which='major')
plt.show()
