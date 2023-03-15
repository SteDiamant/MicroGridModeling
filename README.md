# Microgrid Modeling

This is a Streamlit app for analyzing and visualizing data from a microgrid modeling project. 

## Requirements

- streamlit
- pandas
- matplotlib
- numpy
- seaborn
- scikit-learn

## Installation
 >pip install -r requirements.txt</title>
## Navigate to the directory that you have saved the project and run the command:
>streamlit run app.py
## Data
The data for this app can be found in the `data` directory. The app reads in the `data_f.csv` file and performs some data preprocessing to prepare it for analysis.
## Code
The code for this app is contained in the `app.py` file. The app is organized into several functions:
* `load_data()`: Loads the data from the CSV file and preprocesses it.
* `calculate_average_per_day(df, column_choice)`: Calculates the daily average for a specified column.
* `Imbalance_Analysis(df)`: Performs analysis on the imbalance column.
* `clustering(df)`: Performs clustering on the data.
* `count_clusters(df)`: Counts the number of clusters.
## Functionality
The app currently has two main functionalities:
- **Data Exploration:** Allows users to explore the data by selecting a date range and a column to visualize. The app will display a histogram of the selected column, as well as the daily average for that column.
- **Imbalance Analysis:** Displays the range of the imbalance, the highest and lowest imbalances, and performs clustering on the data to group similar values together.
## Author
Stelios Diamantopoulos
