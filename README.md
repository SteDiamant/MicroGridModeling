# A Microgrid model with multiple EV(s)


This is a web application built using Streamlit that helps users visualize the impact of electric vehicles (EVs) on the energy demand of a microgrid. The app displays the imbalance profile of the microgrid and calculates the energy imported from the grid without EVs and with a specified number of EVs. Users can compare the energy demand with and without EVs and view a daily plot of the imbalance profiles for a selected date range. The app is useful for anyone interested in exploring the potential benefits of integrating EVs into a microgrid.

## Usage

1. Install the required packages by running `pip install -r requirements.txt`.
2. Run the app by running `streamlit run app.py`.
3. Select a day to view the energy demand and imbalance profile with and without EVs.
4. Select a number of PVs to view the energy demand and imbalance profile with and without EVs..
## Model Topology
![Alt text](C:\Users\stdia\Desktop\MicroGridModeling\models\MicroGridModeling\data\image.png)
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

## **`plot_energy_demand_over_time`**

This function takes a pandas DataFrame containing energy demand and production data over time, and plots the TotalDemand, EV Demand, and PV Production on a single plot over time.

The input DataFrame is expected to have the following columns:

- Time: a datetime column representing the time of the energy measurement
- TotalDemand: a column representing the total energy demand at the given time
- EV Demand (W): a column representing the energy demand specifically from electric vehicles at the given time
- PV (W): a column representing the energy production from solar panels at the given time

The output of the function is a matplotlib figure object.

## **`plot_energy_consumption_over_time`**

This function takes a pandas DataFrame containing energy demand and production data, and plots the total energy consumption by category as a bar plot.

The input DataFrame is expected to have the following columns:

- TotalDemand: a column representing the total energy demand at the given time
- EV Demand (W): a column representing the energy demand specifically from electric vehicles at the given time
- PV (W): a column representing the energy production from solar panels at the given time

The output of the function is a matplotlib figure object.

## **`plot_demand_by_hour_and_weekday`**

This function takes a pandas DataFrame containing energy demand and production data, and plots the average energy demand by hour of the day and day of the week as a heatmap.

The input DataFrame is expected to have the following columns:

- Time: a datetime column representing the time of the energy measurement
- TotalDemand: a column representing the total energy demand at the given time

The output of the function is a matplotlib figure object.

## **`plot_energy_demand_by_category_over_time`**

This function takes a pandas DataFrame containing energy demand and production data over time, and plots the energy demand over time broken down by category (EV Demand, Imbalance, TotalDemand, PV Production) as a stacked area plot.

The input DataFrame is expected to have the following columns:

- Time: a datetime column representing the time of the energy measurement
- TotalDemand: a column representing the total energy demand at the given time
- EV Demand (W): a column representing the energy demand specifically from electric vehicles at the given time
- Imbalance: a column representing the energy imbalance at the given time
- PV (W): a column representing the energy production from solar panels at the given time

# Check out the app here

[app](https://stediamant-microgridmodeling-app-c9e9e9.streamlit.app/)

# Check out the code here

[https://github.com/SteDiamant/MicroGridModeling](https://github.com/SteDiamant/MicroGridModeling)