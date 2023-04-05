import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime,timedelta
import numpy as np
import streamlit as st
import warnings
from scipy.integrate import trapz
warnings.filterwarnings("ignore", message="`st.beta_columns` is deprecated")
pd.options.mode.chained_assignment = None
st.set_option('deprecation.showPyplotGlobalUse', False)


class DataLoader():
    
    @staticmethod
    
    def load_data():
        df = pd.read_csv('data\data_original.csv')
        return df

class ImbalanceCalculator():
    def calculate_imbalance(df):
        # Calculate total demand
        df['TotalDemand'] = df['General Demand (W)'] + df['EV Demand (W)'] + df['Heating Demand (W)']
        
        # Calculate PV power
        pv_calc = PVCalculator(pv_number=327)
        df = pv_calc.calculate_pv_power(df)
        
        # Calculate imbalance
        df['Imbalnace'] = df['TotalDemand'] + df['PV (W)']
        
        # Add Imbalance check column
        df['Imbalance_check'] = df['Imbalnace'].apply(lambda x: True if x >= 0 else False)
        
        return df

class DateTimeSplitter:
    def __init__(self):
        self.date_format = '%m/%d/%Y'
        self.time_format = '%H:%M'
        
    def split_datetime(self, df):
        df['date'] = df['Time'].str.split(' ').str[0]
        df['time'] = df['Time'].str.split(' ').str[1]
        df['date'] = pd.to_datetime(df['date'], format=self.date_format)
        df['time'] = pd.to_datetime(df['time'], format=self.time_format).dt.time
        return df
    
    def split_dataframe(self, df):
        df['date'], df['time'] = zip(*df['Time'].apply(self.split_datetime))
        df.drop(columns=['Time'], inplace=True)
        
    def split_dataframe_by_day(self, df):
        days = [df[i:i+96] for i in range(0, len(df), 96)]
        return days

class PVCalculator():
    def __init__(self, pv_number):
        self.pv_number = pv_number
        
    def calculate_pv_power(self, df):
        df['PV (W)'] = df['PV (W)'] * self.pv_number
        return df

class Identification():
    
    @staticmethod
    def count_true_false(df):
        true_count = df['Imbalance_check'].value_counts()[True]
        false_count = df['Imbalance_check'].value_counts()[False]
        return true_count, false_count

    @staticmethod
    def max_production(df, amount):
        top_max_production = df.nsmallest(amount, 'PV (W)')
        top_max_production_values = abs(top_max_production['PV (W)'])
        top_max_production_time = top_max_production['Time']
        return (top_max_production_values.tolist(), top_max_production_time.tolist())
    @staticmethod
    def max_demand(df, amount):
        top_max_production = df.nlargest(amount, 'General Demand (W)')
        top_max_production_values = abs(top_max_production['General Demand (W)'])
        top_max_production_time = top_max_production['Time']
        return top_max_production_values.tolist(), top_max_production_time.tolist()
    @staticmethod
    def imbalance_check(days):
        df=days[DAY]
        st_time,end_time,st_date,end_date = ProfileGenerator.estimate_charging_hours(days,DAY)
        df_slice = df.loc[(df.index.date >= st_date) & (df.index.date <= end_date) & (df.index.time >= st_time) & (df.index.time <= end_time)]
  
        # Check if there is any imbalance in the sliced DataFrame
        if df_slice['Imbalance_check'].any():
            # If there is an imbalance, return False
            return False
        else:
            # If there is no imbalance, print the possible charging start time and date and return True
            #print(f"Possible Charging starts at:{st_time} - {end_time} Date:{st_date}")
            return True

class ProfileGenerator():

    @staticmethod
    def estimate_charging_hours(days, day):
        df = days[day]
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        max_pv_index = df['PV (W)'].idxmin()
        max_pv_time = datetime.combine(df['PV (W)'].idxmin().date(), max_pv_index.time())
        charge_range_start = max_pv_time
        charge_range_end = max_pv_time + timedelta(hours=3)
        return (max_pv_time.time(), charge_range_start.time(), charge_range_end.time(), charge_range_start.date(), charge_range_end.date()) 

    @staticmethod
    def create_charge_profile(days, day):
        time_start, charge_start, charge_end, date_start, date_end = ProfileGenerator.estimate_charging_hours(days, day)
        date_range = pd.date_range(start=datetime.combine(date_start, charge_start), end=datetime.combine(date_end, charge_end), freq='15min')
        charge_profile = pd.DataFrame(index=date_range)
        charge_profile['EV Demand (W)'] = pd.Series(data=MAX_NO_CARS*np.random.randint(low=6400, high=7000, size=len(date_range)), index=charge_profile.index)
        charge_profile.index.name = 'Time'
        return charge_profile
    
    @staticmethod
    def estimate_discharging_hours(days, day):
        df = days[day]
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        min_demand_index = df['General Demand (W)'].idxmax()
        min_demand_time = datetime.combine(df['General Demand (W)'].idxmax().date(), min_demand_index.time())
        discharge_range_start = min_demand_time
        discharge_range_end = min_demand_time + timedelta(hours=3)
        return (min_demand_time.time(), discharge_range_start.time(), discharge_range_end.time(), discharge_range_start.date(), discharge_range_end.date())

    @staticmethod
    def create_discharge_profile(days, day):
        time_start, discharge_start, discharge_end, date_start, date_end = ProfileGenerator.estimate_discharging_hours(days, day)
        date_range = pd.date_range(start=datetime.combine(date_start, discharge_start), end=datetime.combine(date_end, discharge_end), freq='15min')
        discharge_profile = pd.DataFrame(index=date_range)
        discharge_profile['EV Demand (W)'] = pd.Series(data=MAX_NO_CARS*np.random.randint(low=-7000, high=-6400, size=len(date_range)), index=discharge_profile.index)
        discharge_profile.index.name = 'Time'
        return discharge_profile

class DatasetMerger():
    @staticmethod
    def merge_datasets(df1, df2):
        df1['Time']=pd.to_datetime(df1['Time'])
        df1=df1.set_index('Time')
        merged_df1 = pd.merge(df1, df2, left_index=True, right_index=True, how='outer')

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
        return merged_df1
        
class Plotter:
    @staticmethod
    def plot(df):
        try:
        # set Time column as index
            df = df.set_index('Time')
        except:
            pass
        # create a line chart of the demand and PV columns
        fig, ax = plt.subplots(figsize=(14, 8))
        ax.plot(df[['TotalDemand', 'EV Demand (W)',  'PV (W)','Imbalnace']])
        ax.set_xlabel('Time')
        ax.set_ylabel('Power (W)')
        ax.legend(['Total Demand', 'EV Demand', 'PV','Imbalnace'])
        
        # show the chart
        #plt.show()
        return fig

class ComparisonTable:
    
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2
    
    def plot(self):
        # create a figure with two subplots
        fig, axs = plt.subplots(1, 2, figsize=(16, 6))

        # plot data for first dataframe
        axs[0].set_title('Day Data')
        
        axs[0].plot(self.df1['General Demand (W)'], label='General Demand')
        axs[0].plot(self.df1['EV Demand (W)'], label='EV Demand')
        axs[0].plot(self.df1['Heating Demand (W)'], label='Heating Demand')
        axs[0].plot(self.df1['Imbalnace'], label='Imbalnace')
        axs[0].plot(self.df1['PV (W)'], label='PV')
        axs[0].set_xlabel('Time')
        axs[0].set_ylabel('Power (W)')
        axs[0].legend()

        # plot data for second dataframe
        axs[1].set_title('Charge Data')
        axs[1].plot(self.df2['General Demand (W)'], label='General Demand')
        axs[1].plot(self.df2['EV Demand (W)'], label='EV Demand')
        axs[1].plot(self.df2['Heating Demand (W)'], label='Heating Demand')
        axs[1].plot(self.df2['Imbalnace'], label='Imbalnace')
        axs[1].plot(self.df2['PV (W)'], label='PV')
        axs[1].set_xlabel('Time')
        axs[1].set_ylabel('Power (W)')
        axs[1].legend()

        # display the plot
        plt.show()


class metricsCalculator():
    def  calculate_area(df):
        # Assuming df['test'] contains the y-values of the function
        y = df['Imbalnace'].values

        # Assuming the x-values are evenly spaced
        x = np.linspace(0, 1, len(y))

        # Calculate the area using trapezoidal rule integration
        area = trapz(y, x)

        return area
    
    
def get_day_data(days, day):
    charge_profile = ProfileGenerator.create_charge_profile(days, day)
    day_charge = DatasetMerger.merge_datasets(days[day], charge_profile)
    
    discharge_profile = ProfileGenerator.create_discharge_profile(days, day)
    day_discharge = DatasetMerger.merge_datasets(days[day], discharge_profile)
    
    charge_discharge = pd.concat([charge_profile, discharge_profile])
    data = DatasetMerger.merge_datasets(days[day], charge_discharge)
    
    return data   

def plot_single(df):
    return(Plotter.plot(df))
    


def plot_miltiple(days,day_start,day_end):
        merged_data = pd.DataFrame()
        for i in range(day_start, day_end):
            day_data = get_day_data(days, i)
            merged_data = pd.concat([merged_data, day_data], ignore_index=True)
        # plot the merged data
        return(Plotter.plot(merged_data))



def main():
    
    st.title("My Streamlit App")
    
    
    df=DataLoader.load_data()
    df= ImbalanceCalculator.calculate_imbalance(df)
    days = DateTimeSplitter().split_dataframe_by_day(df)
    #days[176].to_csv('randomday.csv')
    #print(DateTimeSplitter().split_datetime(days[1]))
    #print(Identification.max_demand(df,10))
    data = get_day_data(days,DAY)
    
    #comp_table = ComparisonTable(days[DAY], day_discharge)
    #comp_table.plot()
    #st.pyplot(comp_table.plot())
    
    col1, col2 = st.beta_columns(2)
    with col1:
        data1=days[DAY]
        st.title("Without EV")
        msg1=int(metricsCalculator.calculate_area(data1))
        plot1=plot_single(data1)
        st.pyplot(plot1)
        st.write("Area under the curve",str(msg1))
        
    with col2:
        st.title("With EV")
        plot2=plot_single(data)
        msg2=int(metricsCalculator.calculate_area(data))
        st.pyplot(plot2)
        st.write("Area under the curve", str(msg2))
        
    st.write('Ev Integration Results:',(msg1 - msg2))

    st.title("Daily Plot")

    start=st.selectbox("StartDate", list(range(1, 362)))
    end=st.selectbox("EndDAte", list(range(1, 362)))

    st.pyplot(plot_miltiple(days, start, end))

  

if __name__ == '__main__':
    
    MAX_NO_CARS=st.sidebar.selectbox("MaxNoCars1", [1, 2, 3,4])
    DAY = st.sidebar.selectbox("DAY", list(range(1, 362)))

    main()