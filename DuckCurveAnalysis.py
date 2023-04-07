import numpy as np
import pandas as pd
from scipy.optimize import minimize

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import minimize

class DuckCurveOptimizer:
    def __init__(self, data_path):
        self.data = pd.read_csv(data_path)
        
    def calculate_imbalance(self):
        self.data['TotalDemand'] = self.data['General Demand (W)'] + self.data['EV Demand (W)'] + self.data['Heating Demand (W)']
        self.data['Imbalance'] = self.data['TotalDemand'] - self.data['PV (W)']
        self.data['Imbalance_check'] = np.where(self.data['Imbalance']>=0, self.data['Imbalance'], 0)
        return self.data
    
    def optimize(self):
        self.calculate_imbalance()
        p_max = self.data['EV Demand (W)'].max()
        t = self.data['Time']
        p_imb = self.data['Imbalance_check']
        p_pv = self.data['PV (W)']
        
        # Calculate discharge
        q_dis = np.zeros(len(t))
        for i in range(len(t)):
            if p_imb[i] > p_max:
                q_dis[i] = p_imb[i] - p_max
        
        # Calculate charge
        q_ch = np.zeros(len(t))
        for i in range(len(t)):
            if p_imb[i] < 0:
                q_ch[i] = -p_imb[i]
        
        # Calculate net power
        p_net = p_pv - q_dis + q_ch
        
        # Plot results
        plt.figure(figsize=(12,6))
        plt.plot(t, p_pv, label='PV Production')
        plt.plot(t, q_ch, label='EV Charge')
        plt.plot(t, -q_dis, label='EV Discharge')
        plt.plot(t, p_net, label='Net Power')
        plt.title('Duck Curve Optimization')
        plt.xlabel('Time (hour)')
        plt.ylabel('Power (W)')
        plt.legend()
        plt.show()


opt = DuckCurveOptimizer("randomday.csv")
opt.optimize()
