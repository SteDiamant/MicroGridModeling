import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime, time, timedelta
import datetime

PV_NUMBER=327
MAX_NO_CARS=4
DAY=12
def load_data():
    original_df=pd.read_csv( r'C:\Users\stdia\Desktop\MicroGridModeling\models\MicroGridModeling\data\data_original.csv')
    #original_df.drop(columns='Heating Demand (W)',inplace=True)
    original_df['PV (W)'] = original_df['PV (W)']*(PV_NUMBER)##327 + 222 is the amount of PVs at the region 
    original_df['Imbalnace']=original_df['General Demand (W)']+original_df['EV Demand (W)']+original_df['PV (W)']+original_df['Heating Demand (W)']
    original_df['Time']=pd.to_datetime(original_df['Time'])
    original_df.set_index('Time',inplace=True)
    columns_to_plot = ['General Demand (W)', 'EV Demand (W)', 'PV (W)','Imbalnace']
    days = [original_df[i:i+96] for i in range(0, len(original_df), 96)]
    return days
def create_charge_profile(time_start,time_end,date_start,date_end,car_no):
  """
  Creates a charge profile DataFrame for a given time range and number of cars
  
  Parameters:
  time_start (str): start time in 'HH:MM' format
  time_end (str): end time in 'HH:MM' format
  date_start (str): start date in 'YYYY-MM-DD' format
  date_end (str): end date in 'YYYY-MM-DD' format
  car_no (int): number of cars to create charge profile for
  
  Returns:
  charge_profile (pd.DataFrame): DataFrame with date_range as the index and EV Demand (W) as a column
  """
  
  # create a list of dates and times for the 15-minute intervals
  date_range = pd.date_range(start=f'{date_start} {time_start}', end=f'{date_end} {time_end}', freq='15min')

  # create a dataframe with the date_range as the index
  charge_profile = pd.DataFrame(index=date_range)

  # create a column for the EV charging data (in this case, randomly generated numbers)
  charge_profile['EV Demand (W)'] = pd.Series(data=car_no*np.random.randint(low=6400, high=7000, size=len(date_range)), index=charge_profile.index)

  # return the resulting dataframe
  return charge_profile
def estimate_charging_hours(days,day):
  """
  Estimates the optimal time range for charging a given day
    
  Parameters:
  days (list): list of dataframes for each day
  day (int): index of the day to estimate charging hours for
    
  Returns:
  st_time (datetime.time): start time for charging
  charge_range (datetime.time): end time for charging
  st_date (datetime.date): start date for charging
  charge_range.date() (datetime.date): end date for charging
  """
  df=days[day]
  # find the time with the lowest PV (W) value
  max_pv_index = df['PV (W)'].idxmin()
  max_pv_time = datetime.datetime.combine(df['PV (W)'].idxmin().date(), max_pv_index.time())

  # add 3 hours to the time with the lowest PV (W) value to determine charging range
  charge_range = max_pv_time + datetime.timedelta(hours=3)

  # return the start time, end time, start date, and end date for charging
  return (max_pv_index.time(),charge_range.time(),charge_range.date(),charge_range.date())
def merge_profiles(days,charge_profile,day):
  """
  Merges the charge profile DataFrame with the corresponding day's data DataFrame
  
  Parameters:
  days (list): list of dataframes for each day
  charge_profile (pd.DataFrame): DataFrame containing the EV Demand (W) for the given charging range
  day (int): index of the day to merge data for
  
  Returns:
  merged_df1 (pd.DataFrame): DataFrame containing the merged data with additional columns for Imbalnace and Imbalance_check
  """
  # Define columns to plot
  columns_to_plot = ['General Demand (W)', 'EV Demand (W)', 'PV (W)', 'Imbalnace']

  # Get data for the corresponding day
  testDat=days[day]

  # Merge the charge profile with the corresponding day's data
  merged_df1 = pd.merge(testDat, charge_profile, left_index=True, right_index=True, how='outer')

  # Fill NaN values with 0
  merged_df1.fillna(0,inplace=True)

  # Add EV Demand values
  merged_df1['EV Demand (W)'] = merged_df1['EV Demand (W)_x'] + merged_df1['EV Demand (W)_y']

  # Drop old EV Demand columns
  merged_df1.drop(columns=['EV Demand (W)_x','EV Demand (W)_y'], inplace=True)
  
  # Calculate Imbalance
  merged_df1['Imbalnace'] = merged_df1['General Demand (W)'] + merged_df1['EV Demand (W)'] + merged_df1['PV (W)'] + merged_df1['Heating Demand (W)']
  
  # Add Imbalance check column
  merged_df1['Imbalance_check'] = merged_df1['Imbalnace'].apply(lambda x: True if x >= 0 else False)
  merged_df1.plot()
  plt.show()
  ## Return the merged DataFrame
  return merged_df1
def imbalance_check(df, st_time, end_time, st_date, end_date):
  """
  Checks whether there is any imbalance in the given time range and date range
  
  Parameters:
  df (pd.DataFrame): DataFrame containing the merged data with additional columns for Imbalance and Imbalance_check
  st_time (str): start time of the time range to check for imbalance
  end_time (str): end time of the time range to check for imbalance
  st_date (str): start date of the date range to check for imbalance
  end_date (str): end date of the date range to check for imbalance
  
  Returns:
  bool: True if there is no imbalance in the given time range and date range, False otherwise
  """
  # Slice the DataFrame to include only the data within the given time range and date range
  df_slice = df.loc[(df.index.date >= st_date) & (df.index.date <= end_date) & (df.index.time >= st_time) & (df.index.time <= end_time)]
  
  # Check if there is any imbalance in the sliced DataFrame
  if df_slice['Imbalance_check'].any():
    # If there is an imbalance, return False
    return False
  else:
    # If there is no imbalance, print the possible charging start time and date and return True
    #print(f"Possible Charging starts at:{st_time} - {end_time} Date:{st_date}")
    return True
def model_evaluation(days,no_cars):
  """
  Evaluates the charging model for the given number of cars and calculates the accuracy of the model
  
  Parameters:
  days (list): list of dataframes for each day
  no_cars (int): number of cars to charge
  
  Returns:
  None
  """
  for no_cars in range(1,no_cars+1):
    Bad_prediction=0
    Good_prediction=0
    for day in range(len(days)):
      # estimate the charging hours for the day
      st_time,end_time,st_date,end_date=estimate_charging_hours(days,day)
      # create the charging profile for the given number of cars and estimated charging hours
      charge_profile=create_charge_profile(st_time,end_time,st_date,end_date,no_cars)
      # merge the charging profile with the power data for the day
      possible_plan=merge_profiles(days,charge_profile,day)
      # check if the power plan is balanced or not
      check_var=imbalance_check(possible_plan,st_time,end_time,st_date,end_date)
      # increment the good or bad predictions based on the check_var
      if check_var == True:
        Good_prediction=Good_prediction+1
      else:
        Bad_prediction=Bad_prediction+1
    # calculate the accuracy of the model
    accuracy = round(Good_prediction/len(days)*100)
    # print the accuracy and other details
    print("_______________________________________________")
    print('Accuracy :',accuracy,'%', 'Number of  Cars',no_cars)
    print("Good_Prediction : ",Good_prediction ,'/',len(days))
    print("_______________________________________________")
def count_true_false(df):
    true_count = df['Imbalance_check'].value_counts()[True]
    false_count = df['Imbalance_check'].value_counts()[False]
    return true_count, false_count

def main():
    days=load_data()
    #model_evaluation(days,MAX_NO_CARS)
    original_data=days[DAY]
    print(estimate_charging_hours(days,DAY))
    time_start,time_end,date_start,date_end = estimate_charging_hours(days,DAY) 
    charge_profile=create_charge_profile(time_start,time_end,date_start,date_end,MAX_NO_CARS)
    meged_data=merge_profiles(days,charge_profile,DAY)
    print(time_start,time_end,date_start,date_end)
    
    #merged_df=(merge_profiles(days,profile,DAY))
    recalculation=imbalance_check(meged_data,time_start,time_end,date_start,date_end)
    i=1
    while not recalculation and i <= 24:
        try:
            datetime_start1 = datetime.datetime.combine(date_start, time_start) + timedelta(minutes=15)  # subtract two hours from the combined datetime
            time_start1 = datetime_start1.time()  # extract the time component from the resulting datetime object

            datetime_end1 = datetime.datetime.combine(date_end, time_end) + timedelta(hours=i)  # add two hours to the combined datetime
            time_end1 = datetime_end1.time()  # extract the time component from the resulting datetime object

            date_range = pd.date_range(start=f'{date_start} {time_start}', end=f'{date_end} {time_end}', freq='15min')

            charge_profile1 = create_charge_profile(time_start1, time_end1, date_start, date_end, MAX_NO_CARS)
            charge_profile1['EV Demand (W)'] = pd.Series(data=MAX_NO_CARS*np.random.randint(low=6400/i, high=7000/i, size=len(charge_profile1.index)), index=charge_profile1.index)

            merged1_data = merge_profiles(days, charge_profile1, DAY)
            print(merged1_data)
            true_count, false_count = count_true_false(merged1_data)
            print('TreuCopunter',true_count, 'FalseCounter',false_count)

            recalculation=imbalance_check(merged1_data,time_start1,time_end1,date_start,date_end)
            print(time_start1, time_end1, date_start, date_end)
            i=i+1
        except Exception as e:
            print('Error:', e)
            continue
      

if __name__ == '__main__':
    main()
