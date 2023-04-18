import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json



st. set_page_config(layout="wide")

class EnergyKPIs:
    def __init__(self, data):
        self.data = data

    def calculate_renewable_energy_generation_capacity(self):
        # Calculate the total installed capacity of renewable energy sources
        total_installed_pv_capacity = self.data['PV (W)'].sum() / 1000 # Convert to kilowatts
        total_intalled_EV_charging_capacity = self.data[self.data['EV Demand (W)'] < 0]['EV Demand (W)'].sum()/1000 # Convert to kilowatts
        total_installed_capacity = total_installed_pv_capacity + total_intalled_EV_charging_capacity
        return round(abs(total_installed_pv_capacity)) ,round(abs(total_intalled_EV_charging_capacity)) ,round(abs(total_installed_capacity))



    def calculate_ev_charging_station_utilization(self):
        # Calculate the utilization of EV charging stations
        total_charging_sessions = self.data['EV Demand (W)'].sum()
        total_available_charging_capacity = self.data[self.data['EV Demand (W)'] > 0]['EV Demand (W)'].sum()
        total_available_discharging_capacity = self.data[self.data['EV Demand (W)'] < 0]['EV Demand (W)'].sum()
        ev_charging_station_utilization = ( total_available_charging_capacity) 
        ev_discharging_station_utilization = ( total_available_discharging_capacity) 
        return ev_charging_station_utilization, ev_discharging_station_utilization

    
    def calculate_renewable_energy_and_ev_integration(self):
        # Calculate the extent of renewable energy and EV integration
        total_energy_imported = self.data['Energy Imported (W)'].sum()  # Convert to kilowatt hours
        total_energy_from_reneables=self.data['PV (W)'].sum()  # Convert to kilowatt hours
        total_intalled_EV_discharging_capacity = self.data[self.data['EV Demand (W)'] < 0]['EV Demand (W)'].sum() # Convert to kilowatts
        total_renewable_energy_generation = abs(total_energy_from_reneables) + abs(total_intalled_EV_discharging_capacity)/1000 # Convert to kilowatts
        total_renewable_energy_used_for_ev_charging = self.data[(self.data['EV Demand (W)'] > 0) & (self.data['Imbalnace'] > 0)]['PV (W)'].sum()*10  # Convert to kilowatt hours
    
        return total_renewable_energy_generation, total_renewable_energy_used_for_ev_charging,total_energy_imported
    

    def count_strategy_violations(self):
        # Count the number of strategy violations
        total_energy_violations = self.data[(self.data['EV Demand (W)'] > 0) & (self.data['Imbalnace'] > 0)]['EV Demand (W)'].count()/len(self.data['EV Demand (W)'])*100
        return total_energy_violations


    def plot_energy_demand(self):
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(self.data.index, self.data['General Demand (W)'], label='General Demand')
        ax.plot(self.data.index, self.data['Heating Demand (W)'], label='Heating Demand')
        ax.plot(self.data.index, self.data['EV Demand (W)'], label='EV Demand')
        ax.set_xlabel('Time')
        ax.set_ylabel('Power (W)')
        ax.set_title('Energy Demand')
        ax.legend()
        plt.show()

    def plot_pv_production(self):
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(self.data.index, self.data['PV (W)'])
        ax.set_xlabel('Time')
        ax.set_ylabel('Power (W)')
        ax.set_title('PV Production')
        plt.show()


class EnergyMetrics:
    
    def __init__(self, data):
        self.data = data
    
    def total_energy_consumption(self):
        result = self.data['TotalDemand'].sum()
        return f'Total energy consumption: {result:.2f} W'
    
    def average_energy_consumption_by_hour_and_day(self):
        result = self.data.groupby(['Hour', 'DayOfWeek'])['TotalDemand'].mean().unstack().round(2)
        markdown = result.to_json()
        
        
        return f'Average energy consumption by hour and day of the week:\n\n{markdown}'


    
    def energy_consumption_by_season(self,metric):
        
        seasons = pd.cut(self.data.index, 
                        bins=[-1, 90*96, 181*96, 273*96, 365*96], 
                        labels=['Winter', 'Spring', 'Summer', 'Fall'])
        result = self.data.groupby(seasons)[metric].mean().round(2)  # Convert to million units
        
        # Create a bar chart of the energy consumption by season
        fig, ax = plt.subplots()
        fig.set_size_inches(9, 10)
        ax.bar(result.index, result.values)
        ax.set_xlabel('Season')
        ax.set_ylabel(f'{metric} mean (million units)')
        ax.set_title(f'{metric} mean by Season')
    
        # Return the markdown table and the plot
        return f"""{metric} by season:\n\n\n{result.to_json()}""", fig
 

    def  energy_consumption_by_day(self, metric):
        # Calculate the day of the week for each timestamp
        weekdays = self.data['DayOfWeek']
        
        # Group the data by day of the week and calculate the mean for the specified metric
        result = self.data.groupby(weekdays)[metric].mean().round(2)
        
        # Create a bar chart of the energy consumption by day of the week
        fig, ax = plt.subplots()
        ax.bar(result.index, result.values)
        ax.set_xlabel('Day of the week')
        ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        ax.set_ylabel(f'{metric} mean (million units)')
        ax.set_title(f'{metric} mean by Day of the week')
        
        # Return the markdown table and the plot
        return f'Energy {metric} by day of the week:\n\n{result.to_json}', fig

@st.cache_resource
def load_data():
        ##FOR GITHUB
        ##df1 = pd.read_csv(r"Run2/strategies/data_original.csv")
        ##df2 = pd.read_csv(r"Run2/strategies/days.csv")
        ###FOR LOCAL
        df1 = pd.read_csv(r"Run2/strategies/strategy_0.csv")
        df2 = pd.read_csv(r"Run2/strategies/strategy_1.csv")
        df2.rename(columns={'Unnamed: 0':'Time'},inplace=True)
        df1['PV (W)']=df1['PV (W)']*327
        df1['Imbalnace']=df1['General Demand (W)']+df1['Heating Demand (W)']+df1['PV (W)']+df1['EV Demand (W)']
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
                
                
                df['Time'] = pd.to_datetime(df['Time'])
                df['DayOfWeek'] = df['Time'].dt.dayofweek
                df['Hour'] = df['Time'].dt.hour
                df['Month'] = df['Time'].dt.month
                
                
                if metric == 'TotalDemand':
                       cmap1='YlOrBr'
                elif metric == 'EV Demand (W)':
                      cmap1='YlOrBr_r'
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

def plot_installed_capacity(pv_capacity, ev_capacity, total_capacity):
        fig, ax = plt.subplots()
        ax.bar(["PV Capacity", "EV Discharging Capacity", "Total Installed Capacity"], 
            [pv_capacity, ev_capacity, total_capacity])
        ax.set_ylabel("Powe (W)")
        ax.set_title("Installed Capacity")
        ax.tick_params(axis='x', rotation=15)
        

        return fig
def station_utilization(charging,discharging):
        fig, ax = plt.subplots()
        ax.bar(["Total Charging", "Total Discharging"], 
            [charging, abs(discharging)])
        ax.set_ylabel("Capacity (W)")
        ax.set_title("Installed Capacity (W)")
        ax.tick_params(axis='x', rotation=15)

        return fig
def EV_Green(charging,discharging,total):
        fig, ax = plt.subplots()
        ax.bar(["Total PV Production", "Reneables Used For EV Charging",'Total energy imported'], 
            [charging, abs(discharging),total])
        
        ax.set_ylabel("Power (W)")
        ax.set_title("Renewable energy and EV integration")
        ax.tick_params(axis='x', rotation=15)
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
            st.write("----------------------------------------------")  
            positive_imbalance_avg = df1[df1['Imbalnace'] > 0]['Imbalnace'].mean()
            negative_imbalance_avg = df1[df1['Imbalnace'] < 0]['Imbalnace'].mean()
            st.subheader(f'{choice}, by day of the week & Season')
            em = EnergyMetrics(df1)
            message,plot=em.energy_consumption_by_season(choice)
            message_w,plot_w=em.energy_consumption_by_day(choice)
            c121, c221 = st.columns(2)
            with c121:
                
                st.write(message_w)
                
                st.pyplot(plot_w)
             
            with c221:
                st.write(message)
                
                
                st.pyplot(plot)
            
            st.write("----------------------------------------------") 
            
            st.subheader('**Imbalance Range Without Strategy**')
            st.write("Average positive Imbalnace:", str(round(positive_imbalance_avg)))
            st.write("Average negative Imbalnace:", str(round(negative_imbalance_avg)))
            fig, ax = plt.subplots()
            mean_val=(df1['Imbalnace'].mean())
            ax.plot(df1['Imbalnace'])
            ax.axhline(mean_val, color='r', linestyle='--', label=f'Mean Imbalance: {mean_val:.2f}')
            ax.axhline(y=positive_imbalance_avg, color='g', linestyle='--', label='Average positive imbalance: {:.2f}'.format(positive_imbalance_avg))
            ax.axhline(y=negative_imbalance_avg, color='r', linestyle='--', label='Average negative imbalance: {:.2f}'.format(negative_imbalance_avg))
            ax.legend()
            st.pyplot(fig)


           
             
            
        with c2:
            st.subheader('Strategy')
            choice1=st.selectbox(label='Metric',options=(df2.columns[3:]))
            st.write(plot_imbalance_heatmap(df2,choice1))
            st.write("----------------------------------------------")  
            em2 = EnergyMetrics(df2)
            
            positive_imbalance_avg1 = df2[df2['Imbalnace'] > 0]['Imbalnace'].mean()
            negative_imbalance_avg1 = df2[df2['Imbalnace'] <= 0]['Imbalnace'].mean()


            st.subheader(f'{choice1},by day of the week & Season')
            message,plot=em2.energy_consumption_by_season(choice1)
            message_w,plot_w=em2.energy_consumption_by_day(choice1)
            c122, c222 = st.columns(2)
            with c122:
                st.write(json.dumps(message_w),'\n')
                st.write(plot_w)
            st.write("----------------------------------------------")  
            with c222:
                
                st.write(json.dumps(message))
                st.pyplot(plot)

            st.subheader('**Imbalance Range With Strategy**')
            st.write("Average positive imbalance:", str(round(positive_imbalance_avg1)))
            st.write("Average negative imbalance:", str(round(negative_imbalance_avg1)))
            fig1, ax2 = plt.subplots()
            mean_val1=(df2['Imbalnace'].mean())
            
            ax2.plot(df2['Imbalnace'])
            ax2.axhline(mean_val, color='r', linestyle='--', label=f'Mean Imbalance: {mean_val1:.2f}')
            ax2.axhline(y=positive_imbalance_avg1, color='g', linestyle='--', label='Average positive imbalance: {:.2f}'.format(positive_imbalance_avg1))
            ax2.axhline(y=negative_imbalance_avg1, color='r', linestyle='--', label='Average negative imbalance: {:.2f}'.format(negative_imbalance_avg1))
            ax2.legend()
            st.pyplot(fig1)

            
            
    st.write("----------------------------------------------")
    with st.container() as c2:
        data = df2
        # Create an instance of the EnergyKPIs class with the data
        energy_kpis = EnergyKPIs(data)
        # Calculate the renewable energy generation capacityW
        
        with st.container() as c1:
            c11,c12,c13=st.columns(3)
            with c11:
                with st.container():
                    st.subheader("Renewable energy ")
                    pv_energy_generation_capacity,ev_energy_generation_capacity,total_capacity = energy_kpis.calculate_renewable_energy_generation_capacity()
                    st.write("**Renewable energy generation capacity:**", str(total_capacity))
                    st.write("**PV energy generation capacity:**", str(pv_energy_generation_capacity))
                    st.write("**Ev energy generation capacity :**", str(ev_energy_generation_capacity))
                
                    st.pyplot(plot_installed_capacity(pv_energy_generation_capacity,ev_energy_generation_capacity,total_capacity))
                    
                    st.write("""
                    Renewable energy generation capacity: This KPI measures the total amount of renewable energy generation .
                    Renewable energy can be produced from PV of EV discharging
                    """)
            with c12:
                with st.container():
                    st.subheader("EV charging station utilization")
                    ev_charging_station_utilization,ev_discharging_station_utilization = energy_kpis.calculate_ev_charging_station_utilization()
                    st.write("**EV charging station utilization:**", str(ev_charging_station_utilization))
                    st.write("**Discharging station utilization:**", str(abs(ev_discharging_station_utilization)))
                    st.write("**Discharging station utilization:**")
                    st.pyplot(station_utilization(ev_charging_station_utilization,ev_discharging_station_utilization))
                    st.write("""""")
                    st.write("""
                        EV charging station utilization: This KPI measures the usage of EV charging stations.
                        It is the sum of power while charging and discahrging for a full year.
                    """)
            with c13:
                    with st.container():
                        st.subheader("Renewable energy and EV integration")
                        imported_energy_for_charging_evs,renewable_energy_and_ev_integration,total_energy_imported = energy_kpis.calculate_renewable_energy_and_ev_integration()
                        st.write("**TotalReneableEnergy:**", str(round(imported_energy_for_charging_evs)))
                        st.write("**RenewableEnergy Used For EV charging:**", str(round(renewable_energy_and_ev_integration)))
                        st.write("**Total energy imported:**", str(round(total_energy_imported)))
                        st.pyplot(EV_Green(imported_energy_for_charging_evs,renewable_energy_and_ev_integration,total_energy_imported))
                        
                        st.write("""
                        Renewable energy and EV integration: This KPI measures the extent to which renewable energy and EV charging are integrated into the electric grid. 
                        Basicly i try to label the proportion of the green energy used for charging EVs .
                        """)                 
            
                 
            st.write("----------------------------------------------")
        # Meaure Strategy Efficiency
        st.subheader("Strategy Efficiency")
        with st.container() as c4:
             c41,c42=st.columns(2)
             with c41:
                st.write("**Strategy Efficiency:**", str(round(energy_kpis.count_strategy_violations(),2)))
                import_energy_data1=df1['Energy Imported (W)'].sum()
                import_energy_data2=df2['Energy Imported (W)'].sum()
                st.write("**Energy Imported Without Strategy:**", str(round(import_energy_data1)))
                st.write("**Energy Imported With Strategy:**", str(round(import_energy_data2)))
                st.write("**Imported Energy Strategy Comparison Ratio:**", str(round(import_energy_data2/import_energy_data1,3)*100),'%')
                st.write('**Imported Energyy Difference:**',str(round(import_energy_data1-import_energy_data2)),'W')
                st.write("**Cost Savings:**", str(round(((import_energy_data1-import_energy_data2)/1000)*0.45,2)),'$')
if __name__ == '__main__':
       
       main()


    
