import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans

st.set_option('deprecation.showPyplotGlobalUse', False)

# Load data
def load_data():
    df=pd.read_csv(r'C:\Users\stdia\Desktop\MicroGridModeling\models\data\data_f.csv')
    df.set_index('TimeStamp', inplace=True)
    print(df.columns)
    df.drop(columns=['Unnamed: 0','Imbalance pre control assets (kWh)', 'Capacity Check Storage',
       'Storage SoC (kWh)', 'Imbalance Remaining (kWh)'],inplace=True)
    df.index = pd.to_datetime(df.index)
    df1 = df.resample("1H").mean()
    df1['Dates'] = pd.to_datetime(df1.index).date
    df1['Time'] = pd.to_datetime(df1.index).time
    return df1
def calculate_average_per_day(df, column_choice):
    # Group by date and calculate the mean for the specified column
    daily_mean = df.groupby(pd.Grouper(freq='D'))[column_choice].mean()
    # Convert the Pandas Series to a NumPy array
    return daily_mean.to_frame()
def Imbalance_Analysis(df):
    df.dropna(inplace=True)
    imbalance = df['Imbalance pre control assets (kW)']
    max_positive_imbalance = imbalance.max()
    min_negative_imbalance = imbalance.min()
    st.write(f"""
    The Imbalance Range: {max_positive_imbalance - min_negative_imbalance}\n
    Highest Imbalance appearing at {imbalance.idxmax()} with Value {max_positive_imbalance}\n
    The Lowest Imbalance appearing at {imbalance.idxmin()} with Value {min_negative_imbalance}\n
            """)
def clustering(df):
    imbalance = df['Imbalance pre control assets (kW)']
    X = imbalance.values.reshape(-1,1)
    # Define the number of clusters
    k = 3
    # Initialize the k-means algorithm
    kmeans = KMeans(n_clusters=k)
    # Fit the algorithm to the data
    kmeans.fit(X)
    # Get the cluster assignments for each data point
    df['clustering'] = kmeans.predict(X)
    return df
def count_clusters(df):
    return df['clustering'].value_counts()
def main():
    # Set page title
    st.set_page_config(page_title='My Streamlit App')

    # Add a title
    st.title('My Streamlit App')

    # Create a sidebar menu
    menu = ['Data Exploration', 'Imbalance Analysis']
    choice = st.sidebar.selectbox('Select an option', menu)

    # Load the data
    df = load_data()

    # Data exploration
    if choice == 'Data Exploration':
        # Add a subtitle
        st.sidebar.subheader('Data Exploration')

        # Add a slider to filter the data by date
        start_date = st.sidebar.date_input('Start date', value=df['Dates'].min())
        end_date = st.sidebar.date_input('End date', value=df['Dates'].max())
        filtered_df = df[(df['Dates'] >= pd.to_datetime(start_date)) & (df['Dates'] <= pd.to_datetime(end_date))]

        # Display a histogram of one column
        column = st.sidebar.selectbox('Select a column', df.columns)
        plt.xticks(rotation=90)
        sns.lineplot(data=filtered_df, x=filtered_df.index,y=column)
        st.pyplot()

        # Display the average
        ave = calculate_average_per_day(filtered_df, column)
        plt.xticks(rotation=90)
        sns.lineplot(data=ave, x=ave.index,y=column)
        st.pyplot()
        st.sidebar.write(ave)

    # Imbalance analysis
    elif choice == 'Imbalance Analysis':
        Imbalance_Analysis(df)
        st.sidebar.subheader('Clustering')
        st.write("Cluster assignments:")
        cl = (clustering(df))
        st.write(cl)
        plt.xticks(rotation=90)
        sns.scatterplot(data=cl, x=cl['clustering'],y=cl.index,hue='clustering')
        st.pyplot()
        sns.countplot(data=cl, x='clustering')
        st.pyplot()
        st.sidebar.write(count_clusters(cl))

    # Add a footer with some text
    st.text('Stelios Diamantopoulos')

if __name__ == '__main__':
    main()