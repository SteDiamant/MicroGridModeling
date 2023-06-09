# A tool to investigate the impact of 4 EVs to Aardenhuizen region
![image1.png](/data/image.png)
# Main Questions
  - What are the impacts on the load curve when multiple EVs are introduced (max 4)? 
  - What are the strategies to minimize the load imbalance?
  - How will the charge/discharge cycle and speed reduce the car battery's state of health?
# Introduction
The Aardenhuizen community is a small region consisting of 24 households. The community has installed 327 solar panels to generate electricity and four electric vehicles (EVs) to promote sustainable transportation.
The community members are committed to reducing their carbon footprint by adopting environmentally friendly practices. They prioritize the use of renewable energy sources, such as solar power, to minimize their reliance on non-renewable energy sources.
# Methodology
Agile methodology is a project management approach that emphasizes flexibility, collaboration, and continuous improvement. While Agile is most commonly associated with software development, it can also be applied to research projects.


![image1.png](/data/Agile-Methodology.png)

One of the key principles of Agile methodology is the ability to adapt to changing circumstances. In research, this could mean adjusting the project plan based on new data or insights, or pivoting the focus of the project based on emerging trends or opportunities.
# High Level Model Architecture
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

# Tool Overview
The designed tool consists of two software programs. The first software reads the original dataset and user input variables such as </br>
<li>MAX_NO_CARS, which determines the height of the charge and discharge curve, <li>CHARGING_DURATION, which determines the duration of the charge, <li>MOVE_CHARGING_DURATION_BEFORE_PEAK_TIME, which determines how early the charging process will start before the estimated maximum production timestamp, <li>DISCHARGING_DURATION, which determines the duration of the discharge, and <li>MOVE_DISCHARGING_TIME_BEFORE_PEAK_TIME, which determines how early the discharging process will start before the estimated maximum demand timestamp.</li>


![image2.png](/data/tools.png)
The Second software load 2 strategies and compares them next to each other several plots and Visualizatiosn are used to estimate the impact of the strategy to the imbalance curve .

## Profile Generator


## Model Topology


The model topology of the energy demand tool can be described as a sequence of operations that takes energy demand data as input, calculates various metrics, and produces visualizations of the data in different forms. The following is a high-level overview of the tool's main functions:


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
# **Input Control**
**MAX_NO_CARS** : A Variable that represents the maximum number of cars.
![image.jpg](/data/max_CARS_INPUT.png)
**Profile Impact**: Control The Height of the Charging profile

----------------------------------------------------------------
**DURATION_OF_DISCHARGING**: A variable that represent the duration of discharging with respect to the prediction of the maximum demand Timestamp.<br>
**MOVE DISCHARGING PROFILE BEFORE PEAK DEMAND**: A variable that represent the duration of discharging with respect to the prediction of the maximum demand Timestamp.
![image.jpg](/data/InputControl1.png)
**Profile Impact**: Control the Width of the discahrging with respect to the maximum demand Timestamp

----------------------------------------------------------------
**DURATION_OF_CHARGING**: A variable that represent the duration of charging with respect to the prediction of the maximum production Timestamp.<br>
**MOVE DISCHARGING PROFILE BEFORE PEAK DEMAND**: A variable that represent the duration of charging with respect to the prediction of the maximum demand Timestamp.
![image.jpg](/data/InputControl2.png)
**Profile Impact**: Control the Width of the charging with respect to the maximum demand Timestamp

----------------------------------------------------------------
**Daily_Plots**:Variables that represent the start and End date that i want to generate profiles for .
![image.jpg](/data/DailyPlots.png)
**Profile Impact**: This tool allows the user to customize the range of charging and discharging patterns for a given dataset. The tool scales the profile to fit a custom daily dataset by means of controling the start and end date.

----------------------------------------------------------------
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

## **`plot_daily_scale_day`**
### Positive Impact
![image1.jpg](/data/positiveImpact.jpg)
### Negative Impact
![image1.jpg](/data/negativeImpact.jpg)


# Check out the [Profile Generator!!](https://stediamant-microgridmodeling-app-c9e9e9.streamlit.app/)
![image1.jpg](/data/qrcode001.png)<br>

# Check out the [Strategy Comparison!!](https://stediamant-microgridmodeling-run2app-7pu80d.streamlit.app/)
![image1.jpg](/data/qrcode002.png)<br>

# StrategyComparisonTool:

![image1.png](/data/ImbalanceComparison.png)

Imbalance is a measure of the difference between the electricity generation and consumption in a power system, and it can have significant impacts on the stability and reliability of the grid.


If the goal of the strategy is to minimize the imbalance in the power system, then the aim is to make the heatmap for Imbalance metric as white as possible.

A white cell in the heatmap means that the generation and consumption of electricity in the power system are balanced, and there is no significant difference between them. This indicates that the power system is stable and reliable.

![image1.png](/data/ImbalanceByDay&Season.png)
![image1.png](/data/ImblanaceRangeEffect.png)
![image1.png](/data/ReneablleEnergyStatistics.png)
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

# Strategy Comparison Tool
Assessing the effectiveness of various strategies and their influence on the Imbalance Curve can be challenging. To gain a deeper comprehension of the correlation between strategies and their impact on the Imbalance Curve, a tool that utilizes basic metrics and suitable visualizations will be employed. This will aid in accurately estimating the relationship between different strategies and their effect on the Imbalance Curve.
![image1.jpg](/data/NewFeature1.png)
![image1.jpg](/data/NewFeature2.png)