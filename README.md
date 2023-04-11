# A Microgrid model with multiple EV(s)


This is a web application built using Streamlit that helps users visualize the impact of electric vehicles (EVs) on the energy demand of a microgrid. The app displays the imbalance profile of the microgrid and calculates the energy imported from the grid without EVs and with a specified number of EVs. Users can compare the energy demand with and without EVs and view a daily plot of the imbalance profiles for a selected date range. The app is useful for anyone interested in exploring the potential benefits of integrating EVs into a microgrid.

## Usage

1. Install the required packages by running `pip install -r requirements.txt`.
2. Run the app by running `streamlit run app.py`.
3. Select a day to view the energy demand and imbalance profile with and without EVs.
4. Select a number of PVs to view the energy demand and imbalance profile with and without EVs..

## Model Topology
![image.jpg](/data/image.jpg)

## Code Structure

- `DataLoader.py`: Loads data from a CSV file.
- `ImbalanceCalculator.py`: Calculates the energy imbalance of the microgrid.
- `DateTimeSplitter.py`: Splits the data into individual days.
- `Identification.py`: Identifies the maximum demand and production of the microgrid.
- `MetricsCalculator.py`: Calculates metrics such as area under the curve of the energy demand profile.
- `PlotOptions.py`: Contains functions to create various plots for energy demand visualization.
- `app.py`: Contains the main Streamlit app code.

## Functions

- `load_data()`: Loads the energy demand data from a CSV file.
- `calculate_imbalance(df)`: Calculates the energy imbalance of the microgrid using the energy demand data.
- `split_dataframe_by_day(df)`: Splits the energy demand data into individual days.
- `max_demand(df, n)`: Returns the top `n` demand values from the energy demand data.
- `max_production(df, n)`: Returns the top `n` production values from the energy demand data.
- `calculate_area(data)`: Calculates the area under the curve of the energy demand profile.
- `plot_energy_demand_by_category_over_time(data)`: Plots the energy demand over time by category.
- `plot_energy_demand_over_time(data)`: Plots the energy demand over time.
- `plot_demand_by_hour_and_weekday(data)`: Plots the energy demand by hour and weekday.
- `plot_energy_consumption_by_category(data)`: Plots the energy consumption by category.
- `plot_single(data)`: Plots the energy demand and imbalance profile for a single day.
- `calculate_energy_imported(data)`: Calculates the energy imported from the grid.
- `plot_multiple(days, start, end)`: Plots the energy demand and imbalance profile for multiple days.

"""

## Discussion Topics:

To determine the impact of EVs (charge/discharge) on the imbalance curve, we have to generate the corresponding datasets for charge and discharge for chosen day, and afterwards we have to merge the original dataset and the charge/discharge dataset.

1. **`charge_profile = ProfileGenerator.create_charge_profile(days, day)`** generates a charging profile for a specific day using the **`create_charge_profile`** method from the **`ProfileGenerator`** class, which takes a dictionary of daily data and a day as inputs.
2. **`day_charge = DatasetMerger.merge_datasets(days[day], charge_profile)`** merges the generated charging profile with the original data for the specified day using the **`merge_datasets`** method from the **`DatasetMerger`** class. This creates a new dataset called **`day_charge`** which includes the original data and the generated charging profile.
3. **`discharge_profile = ProfileGenerator.create_discharge_profile(days, day)`** generates a discharging profile for the same day using the **`create_discharge_profile`** method from the **`ProfileGenerator`** class.
4. **`day_discharge = DatasetMerger.merge_datasets(days[day], discharge_profile)`** merges the generated discharging profile with the original data for the specified day using the **`merge_datasets`** method from the **`DatasetMerger`** class. This creates a new dataset called **`day_discharge`** which includes the original data and the generated discharging profile.
5. **`charge_discharge = pd.concat([charge_profile, discharge_profile])`** concatenates the charging and discharging profiles into a single dataset called **`charge_discharge`** using the **`concat`** method from the Pandas library.
6. **`data = DatasetMerger.merge_datasets(days[day], charge_discharge)`** merges the **`charge_discharge`** dataset with the original data for the specified day using the **`merge_datasets`** method from the **`DatasetMerger`** class. This creates a new dataset called **`data`** which includes both the original data and the charging and discharging profiles.

# **Energy Data Visualization Functions**

This is a set of four functions for visualizing energy demand and production data using the pandas and matplotlib libraries in Python.

## **`plot_imported_energy_over_time`**

### Input: 
df: A pandas DataFrame containing columns named 'Time', 'TotalDemand', 'EV Demand (W)', 'PV (W)', and 'Imbalance'.

### Output:
A stacked area plot showing the energy demand by category (imported energy) over time. The plot includes a legend displaying the area under each category.

### Functionality:
- The function takes in a DataFrame and resets its index.
- It then converts the 'Time' column to a datetime format and creates a new figure with a specified size. 
- Next, it iterates over each row of the DataFrame, and if the 'Imbalance' value is greater than zero, it adds the sum of 'TotalDemand', 'EV Demand (W)', and 'PV (W)' to a new column named 'Energy Imported (W)'.

<b>If Imbaalance > 0:

 Energy Imported (W)=TotalDemand+EV Demand (W)+PV (W)</b>

The function then creates a stackplot using the 'Time' and 'Energy Imported (W)' columns of the DataFrame, with the label 'Energy Imported (W)'. It also creates a legend that displays the label and area for each category.

Finally, the function displays the plot using matplotlib. 

![image.jpg](/data/EnergyImportedOverTime.png)


## **`plot_energy_consumption_over_time`**
Input:
- df: pandas DataFrame containing the following columns:
    - Heating Demand (W): energy consumption for heating in Watts
    - EV Demand (W): energy consumption for electric vehicles in Watts
    - General Demand (W): energy consumption for other general purposes in Watts

Output:
- A bar chart showing the total energy consumption by category (heating, electric vehicle, and general)

![image1.jpg](/data/categorical.png)

## **`plot_demand_by_hour_and_weekday`**


### Input: 
df: A pandas DataFrame containing columns named 'Time' and 'TotalDemand'.

### Output:
A heatmap plot showing the average energy demand by hour of day and day of week.

### Functionality:
- The function takes in a DataFrame and converts the 'Time' column to a datetime format.
- It then creates two new columns, 'Hour' and 'DayOfWeek', using the datetime information in the 'Time' column.
- Next, it creates a pivot table that calculates the average 'TotalDemand' for each combination of 'Hour' and 'DayOfWeek'.
- The function then creates a heatmap plot using seaborn's sns.heatmap() function with the pivot table as input data and the 'YlGnBu' color map.
- Finally, the function sets the x-axis and y-axis labels and the plot title before displaying the plot using matplotlib.
![image1.jpg](/data/Heatamap.png)



# Check out the app here

[app](https://stediamant-microgridmodeling-app-c9e9e9.streamlit.app/)

# Check out the code here

[https://github.com/SteDiamant/MicroGridModeling](https://github.com/SteDiamant/MicroGridModeling)