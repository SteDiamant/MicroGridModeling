import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import functools
import matplotlib.gridspec as gridspec
PV_NUMBER=327

class PlotOptions():
        @staticmethod
        def load_data():
                
                original_df=pd.read_csv( r'C:\Users\stdia\Desktop\MicroGridModeling\models\MicroGridModeling\data\data_original.csv')
                #original_df.drop(columns='Heating Demand (W)',inplace=True)
                original_df['PV (W)'] = original_df['PV (W)']*(PV_NUMBER)##327 + 222 is the amount of PVs at the region 
                original_df['Imbalnace']=original_df['General Demand (W)']+original_df['EV Demand (W)']+original_df['PV (W)']+original_df['Heating Demand (W)']
                original_df['Time']=pd.to_datetime(original_df['Time'])
                original_df['TotalDemand']=original_df['General Demand (W)']+original_df['Heating Demand (W)']+original_df['EV Demand (W)']
                columns_to_plot = ['General Demand (W)', 'EV Demand (W)', 'PV (W)','Imbalnace']
                days = [original_df[i:i+96] for i in range(0, len(original_df), 96)]
                return days
                
        def plot_energy_demand_over_time(df):
                df['Time'] = pd.to_datetime(df['Time'])
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(df['Time'], df['TotalDemand'], label='Total Demand')
                ax.plot(df['Time'], df['EV Demand (W)'], label='EV Demand')
                ax.plot(df['Time'], df['PV (W)'], label='PV Production')
                ax.legend()
                ax.set_xlabel('Time')
                ax.set_ylabel('Demand (W)')
                ax.set_title('Energy Demand and PV Production over Time')
                plt.show()
                return ax
        
        def plot_energy_consumption_by_category(df):
                demand_by_category = df[['TotalDemand', 'EV Demand (W)', 'PV (W)']].sum()
                ax = demand_by_category.plot(kind='bar', figsize=(6, 8))
                
                # Add text labels to the bars to show the sum of each category
                for i, v in enumerate(demand_by_category):
                        ax.annotate(str(int(v)), xy=(i, v), ha='center', va='bottom', fontsize=12)
                
                plt.title('Energy Consumption by Category')
                plt.xticks(rotation=45) # Rotate x-tick labels to horizontal
                plt.xlabel('Category')
                plt.ylabel('Energy (W)')
                plt.show()
                
        
        def plot_demand_by_hour_and_weekday(df):
                df['Time'] = pd.to_datetime(df['Time'])
                df['Hour'] = df['Time'].dt.hour
                df['DayOfWeek'] = df['Time'].dt.dayofweek
                demand_by_hour_weekday = df.pivot_table(index='Hour', columns='DayOfWeek', values='TotalDemand', aggfunc='mean')
                fig, ax = plt.subplots(figsize=(5, 6))
                sns.heatmap(demand_by_hour_weekday, cmap='YlGnBu', ax=ax)
                ax.set_xlabel('Day of Week')
                ax.set_ylabel('Hour of Day')
                ax.set_title('General Demand Heatmap by Time of Day and Day of Week')
                plt.show()
                

        
        def plot_energy_demand_by_category_over_time(df):
                df['Time'] = pd.to_datetime(df['Time'])
                fig, ax = plt.subplots(figsize=(10, 6))
                stack_data = ax.stackplot(df['Time'],
                                        df['Imbalnace'],
                                        df['TotalDemand'],
                                        df['EV Demand (W)'],df['PV (W)'],
                                        labels=['Imbalance','Total', 'EV','PV'])
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
                        return(plt.show())
        



