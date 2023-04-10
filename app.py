import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
import numpy as np
import streamlit as st
from scipy.integrate import trapz
import seaborn as sns
import os
import base64

pd.options.mode.chained_assignment = None
st.set_option('deprecation.showPyplotGlobalUse', False)
st. set_page_config(layout="wide")



class DataLoader():
    def load_data():
        #path=os.path.join(os.getcwd(),'data')
        #print(path)
        ##THERE IS A BUG HERE WHEN I RUN THE CODE ON STREAMLIT CLOUD I HAVE TO DELETE THE {data}/data_original.csv FILE AND RUN THE CODE AGAIN
        df = pd.read_csv(r'data/data_original.csv')
        return df

class PlotOptions():
        def plot_energy_imported_bar(data1, data):
            labels = [f'0 EVs', f'{MAX_NO_CARS} EVs']
            values = [calculate_energy_imported(data1), calculate_energy_imported(data)]
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar(labels, values)
            ax.set_ylabel('Energy Imported (W)')
            ax.set_title('Energy Imported (W)')
            plt.xticks(rotation=45)
            plt.show()
        
        def plot_energy_demand_over_time_bar(df):
            df['Time'] = pd.to_datetime(df['Time'])
            fig, ax = plt.subplots(figsize=(16, 11))
            ax.fill_between(df['Time'], df['EV Demand (W)'], label='EV Demand')
            ax.fill_between(df['Time'], df['Imbalnace'], label='Imbalnace')
            ax.legend()
            ax.set_xlabel('Time')
            ax.set_ylabel('Demand (W)')
            ax.set_title('Imbalnace and EV_Usage(W) over Time')
            plt.show()
        
       
        def plot_energy_consumption_by_category(df):
                demand_by_category = df[['Heating Demand (W)', 'EV Demand (W)', 'General Demand (W)']].sum()
                ax = demand_by_category.plot(kind='bar', figsize=(6, 10))
                
                # Add text labels to the bars to show the sum of each category
                for i, v in enumerate(demand_by_category):
                        ax.annotate(str(int(v)), xy=(i, v), ha='center', va='bottom', fontsize=12)
                
                plt.title('Energy Consumption by Category')
                plt.xticks(rotation=45) # Rotate x-tick labels to horizontal
                plt.xlabel('Category')
                plt.ylabel('Energy (W)')
                plt.show()
        
       
        def plot_demand_by_hour_and_weekday(df):
                #print(df)
                df.reset_index(inplace=True)
                df['Time'] = pd.to_datetime(df['Time'])
                df['Hour'] = df['Time'].dt.hour
                df['DayOfWeek'] = df['Time'].dt.dayofweek
                demand_by_hour_weekday = df.pivot_table(index='Hour', columns='DayOfWeek', values='TotalDemand', aggfunc='mean')
                fig, ax = plt.subplots(figsize=(6, 10))
                sns.heatmap(demand_by_hour_weekday, cmap='YlGnBu', ax=ax)
                ax.set_xlabel('Day of Week')
                ax.set_ylabel('Hour of Day')
                ax.set_title('Demand Heatmap by Time of Day and Day of Week')
                plt.show()
                

       
        def plot_energy_demand_by_category_over_time(df):
                df.reset_index(inplace=True)
                df['Time'] = pd.to_datetime(df['Time'])
                fig, ax = plt.subplots(figsize=(16, 11))
                for index, row in df.iterrows():
                    if row['Imbalnace'] > 0:
                        df.at[index, 'Energy Imported (W)'] = row['TotalDemand'] + row['EV Demand (W)'] + row['PV (W)']
                stack_data = ax.stackplot(df['Time'],
                                            df['Energy Imported (W)'],
                                            labels=['Energy Imported (W)'])
                handles, labels = [], []
                ax.legend(loc='upper left')
                ax.set_xlabel('Time')
                ax.set_ylabel('Demand (W)')
                ax.set_title('Imported Energy Profile over Time')

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
        df['TotalDemand'] = df['General Demand (W)']  + df['Heating Demand (W)']
        
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
    
   
    def count_true_false(df):
        true_count = df['Imbalance_check'].value_counts()[True]
        false_count = df['Imbalance_check'].value_counts()[False]
        return true_count, false_count

   
    def max_production(df, amount):
        top_max_production = df.nsmallest(amount, 'PV (W)')
        top_max_production_values = abs(top_max_production['PV (W)'])
        top_max_production_time = top_max_production['Time']
        return top_max_production_values, top_max_production_time
   
    def max_demand(df, amount):
        top_max_production = df.nlargest(amount, 'TotalDemand')
        top_max_production_values = abs(top_max_production['TotalDemand'])
        top_max_production_time = top_max_production['Time']
        return top_max_production_values, top_max_production_time
   
    def imbalance_check(days):
        df=days[DAY]
        st_time,end_time,st_date,end_date = ProfileGenerator.estimate_charging_hours(days,DAY)
        df_slice = df.loc[(df.index.date >= st_date) & (df.index.date <= end_date) & (df.index.time >= st_time) & (df.index.time <= end_time)]
  
        # Check if there is any imbalance in the sliced DataFrame
        if df_slice['Imbalance_check'].any():
            # If there is an imbalance, return False
            return False
        else:
            # If there is no imbalance, #print the possible charging start time and date and return True
            ##print(f"Possible Charging starts at:{st_time} - {end_time} Date:{st_date}")
            return True

class ProfileGenerator():

   
    def estimate_charging_hours(days, day):
        df = days[day]
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        max_pv_index = df['PV (W)'].idxmin()
        max_pv_time = datetime.combine(df['PV (W)'].idxmin().date(), max_pv_index.time())
        charge_range_start = max_pv_time -timedelta(hours=MOVE_CHARGING_BEFORE_PEAK_PRODUCTION)
        charge_range_end = max_pv_time + timedelta(hours=CHARGE_TIME)
        return (max_pv_time.time(), charge_range_start.time(), charge_range_end.time(), charge_range_start.date(), charge_range_end.date()) 

   
    def create_charge_profile(days, day):
        time_start, charge_start, charge_end, date_start, date_end = ProfileGenerator.estimate_charging_hours(days, day)
        date_range = pd.date_range(start=datetime.combine(date_start, charge_start), end=datetime.combine(date_end, charge_end), freq='15min')
        charge_profile = pd.DataFrame(index=date_range)
        charge_profile['EV Demand (W)'] = pd.Series(data=MAX_NO_CARS*np.random.randint(low=6400, high=7000, size=len(date_range)), index=charge_profile.index)
        charge_profile.index.name = 'Time'
        return charge_profile
    
   
    def estimate_discharging_hours(days, day):
        df = days[day]
        df['Time'] = pd.to_datetime(df['Time'])
        df = df.set_index('Time')
        min_demand_index = df['General Demand (W)'].idxmax()
        min_demand_time = datetime.combine(df['General Demand (W)'].idxmax().date(), min_demand_index.time())
        discharge_range_start = min_demand_time -timedelta(hours=MOVE_DISCHARGING_BEFORE_PEAK_DEMAND)
        discharge_range_end = min_demand_time + timedelta(hours=DISCHARGE_TIME) 
        return (min_demand_time.time(), discharge_range_start.time(), discharge_range_end.time(), discharge_range_start.date(), discharge_range_end.date())

   
    def create_discharge_profile(days, day):
        time_start, discharge_start, discharge_end, date_start, date_end = ProfileGenerator.estimate_discharging_hours(days, day)
        date_range = pd.date_range(start=datetime.combine(date_start, discharge_start), end=datetime.combine(date_end, discharge_end), freq='15min')
        discharge_profile = pd.DataFrame(index=date_range)
        limit_low=days[DAY]['TotalDemand'].min()
        #print(limit_low)
        discharge_profile['EV Demand (W)'] = pd.Series(data=MAX_NO_CARS*np.random.randint(low=-limit_low/2, high=(-limit_low/2+1), size=len(date_range)), index=discharge_profile.index)
        discharge_profile.index.name = 'Time'
        return discharge_profile

class DatasetMerger():
   
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
        return(merged_data)

def main():
    
    st.title("EV Impact on Microgrid Energy Demand Visualizer")
    
    
    df=DataLoader.load_data()
    df= ImbalanceCalculator.calculate_imbalance(df)
    days = DateTimeSplitter().split_dataframe_by_day(df)
    """

    """
    col1, col2 = st.columns(2)
    with col1:
            st.subheader("Max Demand")
            test1=(Identification.max_demand(df,10))
            st.table(list(test1))
    with col2:
        st.subheader("Max Production")
        test2=(Identification.max_production(df,10))
        st.table(test2)

    

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
                    st.pyplot(PlotOptions.plot_energy_demand_over_time_bar(days[DAY]))
                with col12:
                    st.pyplot(PlotOptions.plot_demand_by_hour_and_weekday(days[DAY]))
                with col13:
                    st.pyplot(PlotOptions.plot_energy_consumption_by_category(days[DAY]))
            

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
                st.pyplot(PlotOptions.plot_energy_demand_over_time_bar(data))
            with col2:
                st.pyplot(PlotOptions.plot_demand_by_hour_and_weekday(data))
                #print(1)
            with col3:
                st.pyplot(PlotOptions.plot_energy_consumption_by_category(data))
    col1,col2 = st.columns(2)
    with col1:
        st.pyplot(PlotOptions.plot_energy_imported_bar(data1, data))
        
    with col2:
        if int(round((importEnergy - importEnergy1)/data['TotalDemand'].sum()*100)) >= 0:
            arrow = "🟢↑"  # Green arrow up for positive values of x
            word='less'
        else:
            arrow = "🔴↓"  # Red arrow down for negative values of x
            word='more'
        st.markdown(f"## Impact of {MAX_NO_CARS} EV(s)")
        st.markdown(f"When {MAX_NO_CARS} EV(s) are integrated, microgrid receives  {round((importEnergy - importEnergy1)/data['TotalDemand'].sum()*100)}% {word} power from the grid{arrow}")
        st.markdown(f'When {MAX_NO_CARS} EV(s) are integrated, the microgrid receives {abs(msg1 - msg2)} Wh {word} energy is required from the grid.')
        st.markdown(f"### Impact on Imbalance area")
        st.markdown(f"- Imbalance area with **NO Evs**: {msg1} Wh")
        st.markdown(f'- Imbalance area with **{MAX_NO_CARS} EVs**: {msg2} Wh')
        st.markdown(f"### Impact on Power IMported from the Grid")
        st.markdown(f"- Power imported from the grid without EVs: {calculate_energy_imported(data1)/1000:.2f} kW")
        st.markdown(f"- Power imported from the grid with **{MAX_NO_CARS} EVs**: {calculate_energy_imported(data)/1000:.2f} kW ")

    st.title("Daily Plot")

    cl1,cl2=st.columns(2)
    with cl1:
        start=st.selectbox("StartDate", list(range(1, 362)))
        end=st.selectbox("EndDAte", list(range(1, 362)),1)
        data2=(plot_miltiple(days, start, end))
        st.write(Plotter.plot(data2))
    with cl2:
        
        mean_total_demand = data2['TotalDemand'].mean()
        max_total_demand = data2['TotalDemand'].max()
        min_total_demand = data2['TotalDemand'].min()
        mean_total_production = data2['PV (W)'].mean()
        max_total_production = data2['PV (W)'].max()
        min_total_production = abs(data2['PV (W)'].min())




        for index, row in data2.iterrows():
                    if row['Imbalnace'] > 0:
                        data2['Energy Imported (W)'] = data2['TotalDemand'] + data2['EV Demand (W)'] + data2['PV (W)']
                    else:
                        data2['Energy Imported (W)'] = 0
        total_imported_energy = data2['Energy Imported (W)'].sum()
        total_demand_distribution = data2['TotalDemand'].describe()
        col3,col4=st.columns(2)
        with col3:
            st.markdown(f"## TotalDemand Statistics\n"
                    f"* Mean TotalDemand: {mean_total_demand/1000:.2f} kW\n"
                    f"* Maximum TotalDemand: {max_total_demand/1000:.2f} kW\n"
                    f"* Minimum TotalDemand: {min_total_demand/1000:.2f} kW\n\n")
        with col4:
             st.markdown(f"## PV Production Statistics\n"
                    f"* Mean PV Production: {mean_total_production/1000:.2f} W\n"
                    f"* Maximum PV Production: {min_total_production/1000:.2f} kW\n\n")
             

        st.markdown(f"## Energy Imported Statistics\n"
            f"* Total energy Imported: {total_imported_energy/1000:.2f} kWh\n\n"
            f"* Total Costs for Energy Imported For the neighborhood: {((total_imported_energy/1000)*0.45):.2f} $ for a duration of {end-start} days\n\n")

        

    
if __name__ == '__main__':
    st.sidebar.header('Select the parameters')

    st.sidebar.subheader('Choose the number of EVs')
    MAX_NO_CARS=st.sidebar.selectbox("MaxNoCars1", [1, 2, 3,4])

    st.sidebar.subheader('Choose the day')
    DAY = st.sidebar.selectbox("Days Index", list(range(1, 362)))

    st.sidebar.subheader('Choose the EV charging parameters')
    CHARGE_TIME=st.sidebar.selectbox("Duration of Charging", [1, 2, 3,4])
    MOVE_CHARGING_BEFORE_PEAK_PRODUCTION=st.sidebar.selectbox("Move Charging Profile Before Peak Production Hours",  list(range(0, 5)),0)

    st.sidebar.subheader('Choose the EV discharging parameters')
    DISCHARGE_TIME=st.sidebar.selectbox("Duration of Discharging", [1, 2, 3,4])
    MOVE_DISCHARGING_BEFORE_PEAK_DEMAND=st.sidebar.selectbox("Move Discharging Profile Before Peak Demand Hours", list(range(0, 5)),0)

    main()
