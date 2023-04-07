# Microgrid Modeling **EV Charging Scheduler**

This is a simple app that generates a charge schedule for electric vehicles (EVs) based on the predicted production from a photovoltaic (PV) system and the total demand of a household. 
The app uses a dataset containing measurements of PV production, household demand, and EV charging demand over the course of a year.

## Installation
 >pip install -r requirements.txt
## Navigate to the directory that you have saved the project and run the command:
>streamlit run app.py
## Data
The data for this app can be found in the `data` directory. The app reads in the `data_f.csv` file and performs some data preprocessing to prepare it for analysis.
# **Flowchart for Charging and Discharging EVs**

This flowchart describes the process of estimating the charging and discharging hours for electric vehicles (EVs) using energy consumption data and solar panel output.

**Estimate Charging Hours Function**

1. Retrieve energy consumption data for the specified day from the days dictionary
2. Convert the Time column to a datetime format and set it as the index of the dataframe
3. Find the time when the solar panel output is at its minimum (the best time to start charging the EVs)
4. Set the start and end times for the charging period to be three hours after the time of minimum solar panel output
5. Return a tuple containing the start time, charge range start time, charge range end time, charge range start date, and charge range end date

## **Create Charge Profile Function**

1. Call the estimate_charging_hours function to retrieve the start and end times for the charging period
2. Create a date range using the start and end times with a 15-minute frequency
3. Create a dataframe with the date range as the index
4. Generate random values for the EV demand using the maximum number of cars and random values between 6400 and 7000 watts
5. Set the index name to Time and return the charge profile dataframe

## **Estimate Discharging Hours Function**

1. Retrieve energy consumption data for the specified day from the days dictionary
2. Convert the Time column to a datetime format and set it as the index of the dataframe
3. Find the time when the energy demand is at its maximum (the best time to start discharging the EVs)
4. Set the start and end times for the discharging period to be three hours after the time of maximum energy demand
5. Return a tuple containing the start time, discharge range start time, discharge range end time, discharge range start date, and discharge range end date

## **Create Discharge Profile Function**

1. Call the estimate_discharging_hours function to retrieve the start and end times for the discharging period
2. Create a date range using the start and end times with a 15-minute frequency
3. Create a dataframe with the date range as the index
4. Generate random values for the EV demand using the maximum number of cars and random values between -7000 and -6400 watts (since discharging means negative demand)
5. Set the index name to Time and return the discharge profile dataframe

Note: The maximum number of cars is a variable that is not specified in the code and should be defined elsewhere in the program.