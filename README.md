# Microgrid Modeling **EV Charging Scheduler**

This is a simple app that generates a charge schedule for electric vehicles (EVs) based on the predicted production from a photovoltaic (PV) system and the total demand of a household. 
The app uses a dataset containing measurements of PV production, household demand, and EV charging demand over the course of a year.
## Requirements

- streamlit
- pandas
- matplotlib
- numpy
- seaborn
- scikit-learn

## Installation
 >pip install -r requirements.txt
## Navigate to the directory that you have saved the project and run the command:
>streamlit run app.py
## Data
The data for this app can be found in the `data` directory. The app reads in the `data_f.csv` file and performs some data preprocessing to prepare it for analysis.

