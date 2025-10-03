import numpy as np
import pandas as pd
import scipy.signal as sig 


class VisibilityCalculation:
    def __init__(self, file, distance=40, prominence=0.15e-6):
        self.file = file
        self.distance = distance
        self.prominence = prominence
        self.data = pd.read_csv(file, skiprows = 5, delimiter=';', skipfooter=8)
        self.data[' Power(W)'] = pd.to_numeric(self.data[' Power(W)'], errors='coerce')
    
    def get_data(self):
        return self.data
    
    def get_maxs_mins(self):
        self.i = sig.find_peaks(self.data[' Power(W)'], distance = self.distance,  prominence=self.prominence)
        self.j = sig.find_peaks(-1 * self.data[' Power(W)'], distance = self.distance, prominence=self.prominence)
        self.maxs = self.data[' Power(W)'][self.i[0]]
        self.mins = self.data[' Power(W)'][self.j[0]]
        return 
    
    def get_visibility(self):
        self.get_maxs_mins()
        self.visibility = (np.mean(self.maxs) - np.mean(self.mins)) / (np.mean(self.maxs) + np.mean(self.mins))
        self.visibility_error = self.visibility * np.sqrt((np.std(self.maxs)/np.mean(self.maxs))**2 + (np.std(self.mins)/np.mean(self.mins))**2)
        return self.visibility, self.visibility_error
        