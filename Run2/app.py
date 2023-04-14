import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import pandas as pd
from sklearn import preprocessing
import numpy as np


class EnergyMetrics:
    
    def __init__(self, data):
        self.data = data
    
    def total_energy_consumption(self):
        result = self.data['TotalDemand'].sum()
        return f'Total energy consumption: {result:.2f} W'
    
    def average_energy_consumption_by_hour_and_day(self):
        result = self.data.groupby(['Hour', 'DayOfWeek'])['TotalDemand'].mean().unstack().round(2)
        return f'Average energy consumption by hour and day of the week:\n\n{result.to_markdown()}'
    
    def energy_consumption_by_season(self,metric):
        seasons = pd.cut(self.data.index, 
                         bins=[-1, 90*96, 181*96, 273*96, 365*96], 
                         labels=['Winter', 'Spring', 'Summer', 'Fall'])
        result = self.data.groupby(seasons)[metric].sum().round(2) / 1_000_000
        return f'Energy Imbalnace by season:\n\n{result.to_markdown()}'
    
    
    

@st.cache_resource
def load_data():
        df1 = pd.read_csv(r"C:\Users\stdia\Desktop\MicroGridModeling\models\MicroGridModeling\application\data_original.csv")
        df2 = pd.read_csv(r"C:\Users\stdia\Desktop\MicroGridModeling\models\MicroGridModeling\days.csv")
        df2.rename(columns={'Unnamed: 0':'Time'},inplace=True)
        print(df2)
        df1['Imbalnace']=df1['General Demand (W)']+df1['Heating Demand (W)']+df1['PV (W)']*327+df1['EV Demand (W)']
        df1['TotalDemand']=df1['General Demand (W)']+df1['Heating Demand (W)']+df1['EV Demand (W)']
        for index, row in df1.iterrows():
                    if row['Imbalnace'] > 0:
                        df1['Energy Imported (W)'] = df1['TotalDemand']  
                    else:
                        df1['Energy Imported (W)'] = 0
        for index, row in df2.iterrows():
                    if row['Imbalnace'] > 0:
                        df2['Energy Imported (W)'] = df2['TotalDemand']  
                    else:
                        df2['Energy Imported (W)'] = 0


        return df1 , df2
@st.cache_resource
def plot_imbalance_heatmap(df,metric):
                try:
                    df['Time'] = pd.to_datetime(df['Time'])
                except:
                      pass
                df['Hour'] = df['Time'].dt.hour
                df['Month'] = df['Time'].dt.month
                
                
                if metric == 'TotalDemand':
                       cmap1='YlOrBr'

                elif metric == 'Imbalnace':
                       cmap1='vlag'

                elif metric == 'General Demand (W)':
                    cmap1='Blues'
                else:
                       cmap1='Blues'
                
                demand_by_hour_weekday = df.pivot_table(index='Month', columns='Hour', values=metric, aggfunc='mean')
                fig, ax = plt.subplots(figsize=(15, 16))
                sns.heatmap(demand_by_hour_weekday, cmap=cmap1, ax=ax,vmin=df[metric].min()/2, vmax=df[metric].max()/2)
                ax.set_xlabel('Hours of Day')
                ax.set_ylabel('Month')
                ax.set_title(f'{metric} by Time of Day and Day of Week')
                plt.show()
                return fig
# Load the data for the first heatmap
@st.cache_resource
def boxplot(df,metric):
    fig, ax = plt.subplots(figsize=(5, 10))
    sns.boxplot(x='Time',y=metric,data=df)
    ax.set_xlabel('Time')
    ax.set_ylabel(metric)
    ax.set_title(f'{metric} Over Time')
    plt.show()
    return fig



def main():
    st.title('StrategyComparison')
    df1,df2 = load_data()
    
    with st.container() as c1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader('NoStrategy')
            choice=st.selectbox(label='Metric',options=(df1.columns[1:]))
            st.write(plot_imbalance_heatmap(df1,choice))
            positive_imbalance_avg = df1[df1['Imbalnace'] > 0]['Imbalnace'].mean()
            negative_imbalance_avg = df1[df1['Imbalnace'] < 0]['Imbalnace'].mean()
            em = EnergyMetrics(df1)
            st.write(em.energy_consumption_by_season(choice))
            st.write("Average positive Imbalnace:", str(round(positive_imbalance_avg)))
            st.write("Average negative Imbalnace:", str(round(negative_imbalance_avg)))
            fig, ax = plt.subplots()
            ax.plot(df1['Imbalnace'])
            ax.axhline(y=positive_imbalance_avg, color='g', linestyle='--', label='Average positive imbalance: {:.2f}'.format(positive_imbalance_avg))
            ax.axhline(y=negative_imbalance_avg, color='r', linestyle='--', label='Average negative imbalance: {:.2f}'.format(negative_imbalance_avg))
            ax.legend()
            st.pyplot(fig)
            
            
        with c2:
            st.subheader('Strategy')
            choice1=st.selectbox(label='Metric',options=(df2.columns))
            st.write(plot_imbalance_heatmap(df2,choice1))
            em2 = EnergyMetrics(df2)
            st.write(em2.energy_consumption_by_season(choice1))
            positive_imbalance_avg1 = df2[df2['Imbalnace'] > 0]['Imbalnace'].mean()
            negative_imbalance_avg1 = df2[df2['Imbalnace'] < 0]['Imbalnace'].mean()

            st.write("Average positive imbalance:", str(round(positive_imbalance_avg1)))
            st.write("Average negative imbalance:", str(round(negative_imbalance_avg1)))
            fig1, ax = plt.subplots()
            ax.plot(df2['Imbalnace'])
            ax.axhline(y=positive_imbalance_avg, color='g', linestyle='--', label='Average positive imbalance: {:.2f}'.format(positive_imbalance_avg1))
            ax.axhline(y=negative_imbalance_avg, color='r', linestyle='--', label='Average negative imbalance: {:.2f}'.format(negative_imbalance_avg1))
            ax.legend()
            st.pyplot(fig1)
            
            
            
        
        
        
        
        
    

if __name__ == '__main__':
       
       main()


    
