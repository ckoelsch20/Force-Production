# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 00:10:25 2020

@author: Connor
"""

import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema


class GraphGUI:
    def __init__(self, GRAPH, NAME, MASS, REPS, STYLE, START, END):
        self.graph = GRAPH
        self.name = NAME
        self.mass = MASS
        self.reps = REPS
        self.style = STYLE
        self.start_date = START
        self.end_date = END
        
        
        name_index = 0
        date_index = 1
        mass_index = 2
        reps_index = 3
        style_index = 4
        x_y_index = 5
        
        list_of_cols = []
        list_of_cols_mass = []
        list_of_cols_reps = []
        list_of_cols_styles = []
        full_list = []
        max_forces = []
        max_dates = []
        graph_maxes = pd.DataFrame(columns=['Date', 'Max Acceleration'])
        
        self.df = pd.read_excel('force_production_data.xlsx')
        for i in self.df.columns:
            if type(i) == int and i % 2 == 0:
                full_list.append(i)
        
        if self.name != 'All':
            for i in range(1,len(self.df.columns)):
                if self.df.iloc[name_index][i] == self.name:
                    list_of_cols.append(i)
        else:
            list_of_cols = full_list

        
        if self.mass != 'All':
            self.mass = int(self.mass)
            for i in range(1,len(self.df.columns)):
                if self.df.iloc[mass_index][i] == self.mass:
                    list_of_cols_mass.append(i)
        else:
            list_of_cols_mass = full_list
        
        #5, 6, 9, 10
        if self.reps != 'All':
            self.reps = int(self.reps)
            for i in range(1,len(self.df.columns)):
                if self.df.iloc[reps_index][i] == self.reps:
                    list_of_cols_reps.append(i)
        else:
            list_of_cols_reps = full_list
        
        #empty
        if self.style != 'All':
            for i in range(1,len(self.df.columns)):
                if self.df.iloc[style_index][i] == self.style:
                    list_of_cols_styles.append(i)
        else:
            list_of_cols_styles = full_list
            
        use_cols_list = list(set(list_of_cols) & set(list_of_cols_mass) & set(list_of_cols_reps) & set(list_of_cols_styles))
        use_cols_list.sort()
        
        new_df = self.df.iloc[:, use_cols_list]
        graph_df = new_df.drop([name_index, date_index, mass_index, reps_index, style_index, x_y_index], axis=0)
        graph_df = graph_df.dropna()
        
        #print(graph_df[2])
        
        for i in graph_df:
            max_dates.append(new_df[i][date_index])
            max_forces.append(graph_df[i].max())
        
        print(new_df.head(7))
        graph_maxes['Date'] = max_dates
        graph_maxes['Max Acceleration'] = max_forces
        print(graph_maxes.head())
        print(max_forces)
        
        plt.plot_date(graph_maxes['Date'], graph_maxes['Max Acceleration'], xdate=True)
        
        
        


if __name__ == '__main__':
    RUN = GraphGUI('Max force over time', 'Connor', 'All', 'All', 'All', 'All', 'All')