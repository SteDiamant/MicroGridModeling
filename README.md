# A tool to investigate the impact of 4 EVs to Aardenhuizen region
![image1.png](/data/image.png)
## Main Questions
  - What are the impacts on the load curve when multiple EVs are introduced (max 4)? 
  - What are the strategies to minimize the load imbalance?
  - How will the charge/discharge cycle and speed reduce the car battery's state of health?
## Introduction
The Aardenhuizen community is a small region consisting of 24 households. The community has installed 327 solar panels to generate electricity and four electric vehicles (EVs) to promote sustainable transportation.
The community members are committed to reducing their carbon footprint by adopting environmentally friendly practices. They prioritize the use of renewable energy sources, such as solar power, to minimize their reliance on non-renewable energy sources.
## Methodology
Agile methodology is a project management approach that emphasizes flexibility, collaboration, and continuous improvement. While Agile is most commonly associated with software development, it can also be applied to research projects.


![image1.png](/data/Agile-Methodology.png)

One of the key principles of Agile methodology is the ability to adapt to changing circumstances. In research, this could mean adjusting the project plan based on new data or insights, or pivoting the focus of the project based on emerging trends or opportunities.
## High Level Model Architecture
At a high level, the model represents the energy demand of a household with two main components 
<li>
heating demand 
</li>
<li>
general demand 
</li>
<br>
which are collectively met by the energy generated from photovoltaic (PV) panels.
Additionally, the model accounts for the energy demand of four electric vehicles (EVs) that require periodic 
<li>charging</li>
<li>discharing</li>
Therefore, the total energy demand of the household is the sum of heating demand, general demand, and the charging requirements of the EVs.

![image.jpg](/data/MODEL_PLAN.png)(https://www.cleanenergyreviews.info/blog/bidirectional-ev-charging-v2g-v2h-v2l)


## Model Topology


The model topology of the energy demand tool can be described as a sequence of operations that takes energy demand data as input, calculates various metrics, and produces visualizations of the data in different forms. The following is a high-level overview of the tool's main functions:

1. `load_data()`: loads energy demand data.
2. `calculate_imbalance(df)`: calculates energy imbalance of the microgrid.
3. `split_dataframe_by_day(df)`: splits energy demand data into individual days.
4. `max_demand(df, n)`: returns top n demand values from energy demand data.
5. `max_production(df, n)`: returns top n production values from energy demand data.
6. `calculate_area(data)`: calculates area under the curve of energy demand profile.
7. `plot_energy_demand_by_category_over_time(data)`: visualizes energy demand data by category over time.
8. `plot_energy_demand_over_time(data)`: visualizes energy demand data over time.
9. `plot_demand_by_hour_and_weekday(data)`: visualizes energy demand data by hour and weekday.
10. `plot_energy_consumption_by_category(data)`: visualizes energy consumption data by category.
11. `plot_single(data)`: plots energy demand and imbalance profile for a single day.
12. `calculate_energy_imported(data)`: calculates energy imported from the grid.
13. `plot_multiple(days, start, end)`: plots energy demand and imbalance profile for multiple days.
![image2.png](/data/flowChart1.png)
<br>
Additionally, there are several functions related to generating charging and discharging profiles for electric vehicles (EVs) and merging them with the energy demand data. These include:

1. `ProfileGenerator.create_charge_profile(days, day)`: generates charging profile for EVs.
2. `DatasetMerger.merge_datasets(days[day], charge_profile)`: merges charging profile with energy demand data.
3. `ProfileGenerator.create_discharge_profile(days, day)`: generates discharging profile for EVs.
4. `DatasetMerger.merge_datasets(days[day], discharge_profile)`: merges discharging profile with energy demand data.
5. `pd.concat([charge_profile, discharge_profile])`: concatenates charging and discharging profiles.
6. `DatasetMerger.merge_datasets(days[day], charge_discharge)`: merges concatenated profiles with energy demand data.

The tool's workflow can be customized by selecting specific functions based on the user's needs. The resulting visualizations can help users understand and optimize energy usage in the microgrid.

![image.jpg](/data/image.jpg)

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


## Discussion Topics:

To determine the impact of EVs (charge/discharge) on the imbalance curve, we have to generate the corresponding datasets for charge and discharge for chosen day, and afterwards we have to merge the original dataset and the charge/discharge dataset.

1. **`charge_profile = ProfileGenerator.create_charge_profile(days, day)`** generates a charging profile for a specific day using the **`create_charge_profile`** method from the **`ProfileGenerator`** class, which takes a dictionary of daily data and a day as inputs.
2. **`day_charge = DatasetMerger.merge_datasets(days[day], charge_profile)`** merges the generated charging profile with the original data for the specified day using the **`merge_datasets`** method from the **`DatasetMerger`** class. This creates a new dataset called **`day_charge`** which includes the original data and the generated charging profile.
3. **`discharge_profile = ProfileGenerator.create_discharge_profile(days, day)`** generates a discharging profile for the same day using the **`create_discharge_profile`** method from the **`ProfileGenerator`** class.
4. **`day_discharge = DatasetMerger.merge_datasets(days[day], discharge_profile)`** merges the generated discharging profile with the original data for the specified day using the **`merge_datasets`** method from the **`DatasetMerger`** class. This creates a new dataset called **`day_discharge`** which includes the original data and the generated discharging profile.
5. **`charge_discharge = pd.concat([charge_profile, discharge_profile])`** concatenates the charging and discharging profiles into a single dataset called **`charge_discharge`** using the **`concat`** method from the Pandas library.
6. **`data = DatasetMerger.merge_datasets(days[day], charge_discharge)`** merges the **`charge_discharge`** dataset with the original data for the specified day using the **`merge_datasets`** method from the **`DatasetMerger`** class. This creates a new dataset called **`data`** which includes both the original data and the charging and discharging profiles.
# Check out the app here

Check out the [app](https://stediamant-microgridmodeling-app-c9e9e9.streamlit.app/)!
# Check out the code here

[https://github.com/SteDiamant/MicroGridModeling](https://github.com/SteDiamant/MicroGridModeling)

# Technical details

## Classes

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
