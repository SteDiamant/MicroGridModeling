import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime,timedelta
import numpy as np
import streamlit as st
import warnings
from scipy.integrate import trapz
import seaborn as sns
import os
pd.options.mode.chained_assignment = None
st.set_option('deprecation.showPyplotGlobalUse', False)


class DataLoader():
    
    @st.cache_data
    
    def load_data():
        os.chdir('data')
        df = pd.read_csv('data_original.csv')
        os.chdir('../data')
        return df

class PlotOptions():
        @st.cache_data            
        def plot_energy_demand_over_time(df):
                print(df)
                df['Time'] = pd.to_datetime(df['Time'])
                fig, ax = plt.subplots(figsize=(16, 11))
                ax.plot(df['Time'], df['TotalDemand'], label='Total Demand')
                ax.plot(df['Time'], df['EV Demand (W)'], label='EV Demand')
                ax.plot(df['Time'], df['PV (W)'], label='PV Production')
                ax.legend()
                ax.set_xlabel('Time')
                ax.set_ylabel('Demand (W)')
                ax.set_title('Energy Demand and PV Production over Time')
                plt.show()
                return fig
        @st.cache_data
        def plot_energy_consumption_by_category(df):
                demand_by_category = df[['TotalDemand', 'EV Demand (W)', 'PV (W)']].sum()
                ax = demand_by_category.plot(kind='bar', figsize=(6, 10))
                
                # Add text labels to the bars to show the sum of each category
                for i, v in enumerate(demand_by_category):
                        ax.annotate(str(int(v)), xy=(i, v), ha='center', va='bottom', fontsize=12)
                
                plt.title('Energy Consumption by Category')
                plt.xticks(rotation=45) # Rotate x-tick labels to horizontal
                plt.xlabel('Category')
                plt.ylabel('Energy (W)')
                plt.show()
        
        @st.cache_data
        def plot_demand_by_hour_and_weekday(df):
                print(df)
                df.reset_index(inplace=True)
                df['Time'] = pd.to_datetime(df['Time'])
                df['Hour'] = df['Time'].dt.hour
                df['DayOfWeek'] = df['Time'].dt.dayofweek
                df['TotalDemand'] = df['General Demand (W)'] + df['EV Demand (W)'] + df['Heating Demand (W)']
                demand_by_hour_weekday = df.pivot_table(index='Hour', columns='DayOfWeek', values='TotalDemand', aggfunc='mean')
                fig, ax = plt.subplots(figsize=(6, 10))
                sns.heatmap(demand_by_hour_weekday, cmap='YlGnBu', ax=ax)
                ax.set_xlabel('Day of Week')
                ax.set_ylabel('Hour of Day')
                ax.set_title('Demand Heatmap by Time of Day and Day of Week')
                plt.show()
                

        @st.cache_data
        def plot_energy_demand_by_category_over_time(df):
                df.reset_index(inplace=True)
                df['Time'] = pd.to_datetime(df['Time'])
                fig, ax = plt.subplots(figsize=(16, 11))
                stack_data = ax.stackplot(df['Time'],
                                            df['Imbalnace'],
                                            df['TotalDemand'],
                                            df['EV Demand (W)'],
                                            df['PV (W)'],
                                            labels=['Imbalance','TotaDemand', 'EV','PV'])
                handles, labels = [], []
                ax.legend(loc='upper left')
                ax.set_xlabel('Time')
                ax.set_ylabel('Demand (W)')
                ax.set_title('Energy Demand by Category over Time')

                for i, stack in enumerate(stack_data):
                        vertices = stack.get_paths()[0].vertices
                        x = vertices[:, 0]
                        y = vertices[:, 1]
                        area = np.trapz(y, x)
                        label = f'{ax.get_legend().get_texts()[i].get_text()} (area: {area:.0f} W)'
                        handles.append(plt.Rectangle((0,0), 1, 1, fc=stack.get_facecolor()[0]))
                        labels.append(label)
                    
                ax.legend(handles, labels, loc='lower left', labelspacing=1)
                plt.show()
                    
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
    
    @st.cache_data
    def count_true_false(df):
        true_count = df['Imbalance_check'].value_counts()[True]
        false_count = df['Imbalance_check'].value_counts()[False]
        return true_count, false_count

    @st.cache_data
    def max_production(df, amount):
        top_max_production = df.nsmallest(amount, 'PV (W)')
        top_max_production_values = abs(top_max_production['PV (W)'])
        top_max_production_time = top_max_production['Time']
        return top_max_production_values, top_max_production_time
    @st.cache_data
    def max_demand(df, amount):
        top_max_production = df.nlargest(amount, 'General Demand (W)')
        top_max_production_values = abs(top_max_production['General Demand (W)'])
        top_max_production_time = top_max_production['Time']
        return top_max_production_values, top_max_production_time
    @st.cache_data
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

    @st.cache_data
    def estimate_charging_hours(days, day):
        df = days[day]
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        max_pv_index = df['PV (W)'].idxmin()
        max_pv_time = datetime.combine(df['PV (W)'].idxmin().date(), max_pv_index.time())
        charge_range_start = max_pv_time
        charge_range_end = max_pv_time + timedelta(hours=3)
        return (max_pv_time.time(), charge_range_start.time(), charge_range_end.time(), charge_range_start.date(), charge_range_end.date()) 

    @st.cache_data
    def create_charge_profile(days, day):
        time_start, charge_start, charge_end, date_start, date_end = ProfileGenerator.estimate_charging_hours(days, day)
        date_range = pd.date_range(start=datetime.combine(date_start, charge_start), end=datetime.combine(date_end, charge_end), freq='15min')
        charge_profile = pd.DataFrame(index=date_range)
        charge_profile['EV Demand (W)'] = pd.Series(data=MAX_NO_CARS*np.random.randint(low=6400, high=7000, size=len(date_range)), index=charge_profile.index)
        charge_profile.index.name = 'Time'
        return charge_profile
    
    @st.cache_data
    def estimate_discharging_hours(days, day):
        df = days[day]
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        min_demand_index = df['General Demand (W)'].idxmax()
        min_demand_time = datetime.combine(df['General Demand (W)'].idxmax().date(), min_demand_index.time())
        discharge_range_start = min_demand_time
        discharge_range_end = min_demand_time + timedelta(hours=3)
        return (min_demand_time.time(), discharge_range_start.time(), discharge_range_end.time(), discharge_range_start.date(), discharge_range_end.date())

    @st.cache_data
    def create_discharge_profile(days, day):
        time_start, discharge_start, discharge_end, date_start, date_end = ProfileGenerator.estimate_discharging_hours(days, day)
        date_range = pd.date_range(start=datetime.combine(date_start, discharge_start), end=datetime.combine(date_end, discharge_end), freq='15min')
        discharge_profile = pd.DataFrame(index=date_range)
        limit_low=days[DAY]['TotalDemand'].min()
        print(limit_low)
        discharge_profile['EV Demand (W)'] = pd.Series(data=MAX_NO_CARS*np.random.randint(low=-limit_low/2, high=(-limit_low/2+1), size=len(date_range)), index=discharge_profile.index)
        discharge_profile.index.name = 'Time'
        return discharge_profile

class DatasetMerger():
    @st.cache_data
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
    @st.cache_data
    def plot(df):
        try:
        # set Time column as index
            df = df.set_index('Time')
        except:
            pass
        # create a line chart of the demand and PV columns
        fig, ax = plt.subplots(figsize=(16, 8))
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
    def total_positive_energy(df):
        return df['Imbalnace'].sum()
    
    
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
    
def calculate_energy_imported(df):
    # calculate energy imported from grid when imbalance is positive
    df['Energy Imported (W)'] = 0  # initialize column to all zeros
    positive_imbalance = df['Imbalnace'] > 0
    df.loc[positive_imbalance, 'Energy Imported (W)'] = df.loc[positive_imbalance, 'TotalDemand'] + df.loc[positive_imbalance, 'EV Demand (W)'] + df.loc[positive_imbalance, 'PV (W)']

    return int(df["Energy Imported (W)"].sum())

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
    # col1, col2 = st.columns(2)
    # with col1:
    #     st.subheader("Max Demand")
    #     test1=(Identification.max_demand(df,10))
    #     st.table(test1)
    # with col2:
    #     st.subheader("Max Production")
    #     test2=(Identification.max_production(df,10))
    #     st.table(test2)

    

    data = get_day_data(days,DAY)
    st.subheader(f"Imbalance Profile Without EV ")
    con1=st.container()
    
    
    with con1:
        data1=days[DAY]
        col1 , col2 = st.columns(2)
        with col1:
            msg1=int(metricsCalculator.calculate_area(data1))
            plot1=plot_single(data1)
            st.pyplot(plot1)
            
            importEnergy = calculate_energy_imported(data1)
            
            with col2:
                col11, col12,col13 = st.columns(3)
                with col11:
                    st.pyplot(PlotOptions.plot_energy_demand_by_category_over_time(days[DAY]))
                    st.pyplot(PlotOptions.plot_energy_demand_over_time(days[DAY]))
                with col12:
                    st.pyplot(PlotOptions.plot_demand_by_hour_and_weekday(days[DAY]))
                with col13:
                    st.pyplot(PlotOptions.plot_energy_consumption_by_category(days[DAY]))
            st.write("Imbalance area",str(msg1),"Wh")
            st.write("Power Inporetd From the GridWithout EVs",str(calculate_energy_imported(data1)),'W')

    st.subheader(f"Imbalance Profile With {MAX_NO_CARS}  EV(s)")
    con2=st.container()
    with con2:  
        col1,col2 = st.columns(2)
        with col1:
            plot2=plot_single(data)
            msg2=int(metricsCalculator.calculate_area(data))
            st.pyplot(plot2)
            importEnergy1 = calculate_energy_imported(data)
        with col2:
            col1, col2,col3 = st.columns(3)
            with col1:
                st.pyplot(PlotOptions.plot_energy_demand_by_category_over_time(data))
                st.pyplot(PlotOptions.plot_energy_demand_over_time(data))
            with col2:
                st.pyplot(PlotOptions.plot_demand_by_hour_and_weekday(data))
                print(1)
            with col3:
                st.pyplot(PlotOptions.plot_energy_consumption_by_category(data))
    st.write("Imbalance area", str(msg2),'Wh')
    st.write(f"Power Inporetd From the Grid With {MAX_NO_CARS} EVs",str(calculate_energy_imported(data)),"W")



    st.write(f'When {MAX_NO_CARS} EV(s) are integrated, microgird receives ',str(abs(msg1 - msg2)),'Wh less energy is required from the grid')
    st.write(f'When {MAX_NO_CARS} EV(s) are integrated, microgrid receives',str(round((importEnergy - importEnergy1)/data['TotalDemand'].sum()*100)),'%','less power from the grid')
    
               

    
        

    st.title("Daily Plot")

    
    cl1,cl2=st.columns(2)
    with cl1:
        start=st.selectbox("StartDate", list(range(1, 362)))
        end=st.selectbox("EndDAte", list(range(1, 362)),1)
    with cl2:
        data2=(plot_miltiple(days, start, end))
        st.pyplot(data2)

    
if __name__ == '__main__':
    
    MAX_NO_CARS=st.sidebar.selectbox("MaxNoCars1", [1, 2, 3,4])
    DAY = st.sidebar.selectbox("DAY", list(range(1, 362)))

    main()