# use data from ventos result files
# e.g. veh delay for without attacks and with attacks (0.001 and 0.01 atk rate)


data = [vehDelay_without, vehDelay_with_001, vehDelay_3_01]

# Multiple box plots on one Axes
fig, ax = plt.subplots()
ax.boxplot(data)

plt.show()
