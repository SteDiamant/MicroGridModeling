import pandas as pd
import matplotlib.pyplot as plt

# create a pandas DataFrame with the data for Demand (W), EV Demand (W), heating Demand (W), and PV
data=pd.read_csv('randomday.csv')


# create a new column for total Demand (W)
data['total_Demand (W)'] = data['General Demand (W)'] + data['EV Demand (W)'] + data['Heating Demand (W)']

# plot the data as a line graph

plt.plot(data['Time'], data['EV Demand (W)'], label='EV Demand (W)')

plt.plot(data['Time'], data['PV (W)'], label='PV')
plt.plot(data['Time'], data['total_Demand (W)'], label='Total Demand (W)')
plt.plot(data['Time'], data['Imbalnace'],label='Imbalnace')
# set the labels and title for the plot
plt.xlabel('Time (hours)')
plt.ylabel('Power (kW)')
plt.title('Duck Curve')

# add a legend to the plot
plt.legend()

# show the plot
plt.show()
