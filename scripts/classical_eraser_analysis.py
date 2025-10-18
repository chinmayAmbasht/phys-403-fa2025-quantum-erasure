import numpy as np
import pandas as pd
import scipy.signal as sig 
import matplotlib.pyplot as plt

class VisibilityCalculation:
    def __init__(self, file, distance=40, prominence=0.15e-6):
        self.file = file
        self.distance = distance
        self.prominence = prominence
        self.data = pd.read_csv(file, skiprows = 5, delimiter=';', skipfooter=8 ,engine = 'python')
        self.data[' Power(W)'] = pd.to_numeric(self.data[' Power(W)'], errors='coerce')
        # Combine Date and Time columns into a single datetime column
        self.data['Datetime'] = pd.to_datetime(self.data['Date (MM/dd/yyyy) '] + ' ' + self.data[' Time of day (hh:mm:ss.fff)'])

        # Calculate elapsed time in seconds since the start of the day
        self.data['Elapsed Time (s)'] = (self.data['Datetime'] - self.data['Datetime'].dt.normalize()).dt.total_seconds()
        self.data['Elapsed Time (s)'] -= self.data['Elapsed Time (s)'].iloc[0]  # Normalize to start from zero
        # # Drop the original "Time of day" and "Date" columns if no longer needed
        self.data = self.data.drop(columns=['Datetime', 'Date (MM/dd/yyyy) ', ' Time of day (hh:mm:ss.fff)'])
    def get_data(self):
        return self.data
    
    def get_maxs_mins(self):
        self.i = sig.find_peaks(self.data[' Power(W)'], distance = self.distance,  prominence=self.prominence)
        self.j = sig.find_peaks(-1 * self.data[' Power(W)'], distance = self.distance, prominence=self.prominence)
        self.maxs = self.data[' Power(W)'][self.i[0]]
        self.mins = self.data[' Power(W)'][self.j[0]]
        return 
    
    def run_diagnostic_plot(self): 
        self.get_maxs_mins()
        plt.figure(figsize=(10,6))
        plt.plot(self.data['Elapsed Time (s)'], self.data[' Power(W)'], label='Data')
        plt.plot(self.data['Elapsed Time (s)'][self.i[0]], self.maxs, "x", label='Maxima')
        plt.plot(self.data['Elapsed Time (s)'][self.j[0]], self.mins, "o", label='Minima')
        plt.xlabel('Time (s)')
        plt.ylabel('Power (W)')
        plt.title('Visibility Calculation Diagnostic Plot', fontsize = 20)
        plt.legend()
        plt.grid()
        plt.show()
    
    
    def get_visibility(self):
        self.get_maxs_mins()
        self.visibility = (np.mean(self.maxs) - np.mean(self.mins)) / (np.mean(self.maxs) + np.mean(self.mins))

        # standard error of the mean
        mean_max = np.mean(self.maxs)
        mean_min = np.mean(self.mins)
        sem_max = np.std(self.maxs) 
        sem_min = np.std(self.mins)
        
        partial_V_max = (2 * mean_min) / ((mean_max + mean_min)**2)
        partial_V_min = (-2 * mean_max) / ((mean_max + mean_min)**2)
        self.visibility_error = np.sqrt((partial_V_max * sem_max)**2 + (partial_V_min * sem_min)**2) 
        

        return self.visibility, self.visibility_error
        