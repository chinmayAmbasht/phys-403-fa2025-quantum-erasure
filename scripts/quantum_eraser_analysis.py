import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 

class QuantumVisibilityCalculation:
    def __init__(self, file):
        self.file = file
        self.data = pd.read_csv(file)
        self.data['Max Counts'] = self.data['Max'] * 1000
        self.data['Min Counts'] = self.data['Min'] * 1000
        
    def calculate_visibility(self):
        mean_max = np.mean(self.data['Max Counts'])
        mean_min = np.mean(self.data['Min Counts'])
        mean_visibility = (mean_max - mean_min) / (mean_max + mean_min)
        self.visibility = mean_visibility
        self.mean_max = mean_max
        self.mean_min = mean_min
        
        sem_max = np.std(self.data['Max Counts'], ddof = 1)
        sem_min = np.std(self.data['Min Counts'], ddof = 1)
        
        self.mean_sem_max = sem_max
        self.mean_sem_min = sem_min
        
        partial_V_max = (2 * mean_min) / ((mean_max + mean_min)**2)
        partial_V_min = (-2 * mean_max) / ((mean_max + mean_min)**2)
        self.visibility_error = np.sqrt((partial_V_max * sem_max)**2 + (partial_V_min * sem_min)**2) 
        
        return self.visibility, self.visibility_error
        