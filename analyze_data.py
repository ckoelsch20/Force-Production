# -*- coding: utf-8 -*-
"""
Created on Thu Oct 15 16:52:13 2020

@author: Connor
"""

from tkinter import *
import pandas as pd
import tkinter.font as tkFont

import graph_data


class SelectionInput:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("460x300")
        self.root.title("Force Production Analysis")
        self.root.configure(bg='black')
        
        _gray = '#595a61'
        
        title_font_style = tkFont.Font(size=30)
        
        ### Frames
        self.title_frame = Frame(self.root, bg='black')
        self.title_frame.grid(column=0, row=0)
        
        self.selection_labels_frame = Frame(self.root, bg='black')
        self.selection_labels_frame.grid(column=0, row=1)
        
        self.submit_frame = Frame(self.root, bg='black')
        self.submit_frame.grid(column=0, row=2)
        
        ### Labels
        self.title_label = Label(self.title_frame, font=title_font_style, text='Force Production Analysis')
        self.title_label.grid(column=0, row=0)
        self.title_label.configure(anchor='w', fg='orange', bg='black')
        
        self.graph_type_label = Label(self.selection_labels_frame, text='Graph Type:')
        self.graph_type_label.grid(column=0, row=0)
        self.graph_type_label.configure(bg='black', anchor='w', fg='orange')
        
        self.name_label = Label(self.selection_labels_frame, text='Name:')
        self.name_label.grid(column=0, row=1)
        self.name_label.configure(bg='black', anchor='w', fg='orange')
        
        self.mass_label = Label(self.selection_labels_frame, text='Mass:')
        self.mass_label.grid(column=0, row=2)
        self.mass_label.configure(bg='black', anchor='w', fg='orange')
        
        self.reps_label = Label(self.selection_labels_frame, text='Reps:')
        self.reps_label.grid(column=0, row=3)
        self.reps_label.configure(bg='black', anchor='w', fg='orange')
        
        self.style_label = Label(self.selection_labels_frame, text='Style:')
        self.style_label.grid(column=0, row=4)
        self.style_label.configure(bg='black', anchor='w', fg='orange')
        
        self.start_date_label = Label(self.selection_labels_frame, text='Start Date:')
        self.start_date_label.grid(column=0, row=5)
        self.start_date_label.configure(bg='black', anchor='w', fg='orange')
        
        self.end_date_label = Label(self.selection_labels_frame, text='End Date:')
        self.end_date_label.grid(column=0, row=6)
        self.end_date_label.configure(bg='black', anchor='w', fg='orange')
        
        ### Buttons
        
        self.submit_button = Button(self.submit_frame)
        self.submit_button.grid(column=0, row=0)
        self.submit_button.configure(text="Submit", fg='orange', bg=_gray, relief='raised', command=self.click_submit)
        
        self.close_button = Button(self.submit_frame)
        self.close_button.grid(column=1, row=0)
        self.close_button.configure(text="Close", fg='orange', bg=_gray, relief='raised', command=self.click_close)
        
        ### Entries
        self.graph_list = ["Max force over time", "Individual set"]
        self.names_list = ['All']
        self.dates_list = ['All']
        self.mass_list = ['All']
        self.reps_list = ['All']
        self.style_list = ['All']
        
        self.tk_strvar_graph = StringVar(self.selection_labels_frame)
        self.tk_strvar_graph.set(self.graph_list[0])
        self.tk_strvar_names = StringVar(self.selection_labels_frame)
        self.tk_strvar_names.set(self.names_list[0])
        self.tk_strvar_start_dates = StringVar(self.selection_labels_frame)
        self.tk_strvar_start_dates.set(self.dates_list[0])
        self.tk_strvar_end_dates = StringVar(self.selection_labels_frame)
        self.tk_strvar_end_dates.set(self.dates_list[0])
        self.tk_strvar_mass = StringVar(self.selection_labels_frame)
        self.tk_strvar_mass.set(self.mass_list[0])
        self.tk_strvar_reps = StringVar(self.selection_labels_frame)
        self.tk_strvar_reps.set(self.reps_list[0])
        self.tk_strvar_style = StringVar(self.selection_labels_frame)
        self.tk_strvar_style.set(self.style_list[0])
        
        self.get_data_setup()
        #print(self.graph_list)
        
        option_menu_width = 20
        
        self.graph_options = OptionMenu(self.selection_labels_frame, self.tk_strvar_graph, *self.graph_list)
        self.graph_options.grid(column=1, row=0)
        self.graph_options.configure(background=_gray, fg='orange', width=option_menu_width, activebackground='black', highlightthickness=0)
        
        self.name_options = OptionMenu(self.selection_labels_frame, self.tk_strvar_names, *self.names_list)
        self.name_options.grid(column=1, row=1)
        self.name_options.configure(bg=_gray, fg='orange', width=option_menu_width, activebackground='black', highlightthickness=0)
        
        self.mass_options = OptionMenu(self.selection_labels_frame, self.tk_strvar_mass, *self.mass_list)
        self.mass_options.grid(column=1, row=2)
        self.mass_options.configure(bg=_gray, fg='orange', width=option_menu_width, activebackground='black', highlightthickness=0)
        
        self.reps_options = OptionMenu(self.selection_labels_frame, self.tk_strvar_reps, *self.reps_list)
        self.reps_options.grid(column=1, row=3)
        self.reps_options.configure(bg=_gray, fg='orange', width=option_menu_width, activebackground='black', highlightthickness=0)
        
        self.style_options = OptionMenu(self.selection_labels_frame, self.tk_strvar_style, *self.style_list)
        self.style_options.grid(column=1, row=4)
        self.style_options.configure(bg=_gray, fg='orange', width=option_menu_width, activebackground='black', highlightthickness=0)
        
        self.start_date_options = OptionMenu(self.selection_labels_frame, self.tk_strvar_start_dates, *self.dates_list)
        self.start_date_options.grid(column=1, row=5)
        self.start_date_options.configure(bg=_gray, fg='orange', width=option_menu_width, activebackground='black', highlightthickness=0)
        
        self.end_date_options = OptionMenu(self.selection_labels_frame, self.tk_strvar_end_dates, *self.dates_list)
        self.end_date_options.grid(column=1, row=6)
        self.end_date_options.configure(bg=_gray, fg='orange', width=option_menu_width, activebackground='black', highlightthickness=0)
        
        ###
        
        
        self.root.mainloop()
        
        
    def get_data_setup(self):
        df = pd.read_excel('force_production_data.xlsx')
        #df.drop([0], axis=1)
        
        name_row = 0
        date_row = 1
        mass_row = 2
        reps_row = 3
        style_row = 4
        
        self.names_list.extend(df.iloc[name_row].drop_duplicates()[1:])
        self.dates_list.extend(df.iloc[date_row].drop_duplicates()[1:])
        self.mass_list.extend(df.iloc[mass_row].drop_duplicates()[1:])
        self.reps_list.extend(df.iloc[reps_row].drop_duplicates()[1:])
        self.style_list.extend(df.iloc[style_row].drop_duplicates()[1:])
        
    def click_submit(self):
        if self.tk_strvar_graph.get() == "Individual set":
            pass
        else:
            graph_data.GraphGUI(self.tk_strvar_graph.get(), self.tk_strvar_names.get(), self.tk_strvar_mass.get(), \
                                self.tk_strvar_reps.get(), self.tk_strvar_style.get(), self.tk_strvar_start_dates.get(), \
                                self.tk_strvar_end_dates.get())
    def click_close(self):
        self.root.quit()
        self.root.destroy()
        


if __name__ == '__main__':
    RUN = SelectionInput()