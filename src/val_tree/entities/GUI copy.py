#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk
import sys
import time

sys.path.insert(0, r'..\..\src')
import src.val_tree.adapters.http as http_adp
from src.val_tree.entities.tree_computer import TreeComputer
# Class which represents GUI interface for the application.
# App consists of one window with one input box for path to the file and the button which triggers tree evaluation.
# There is a logo of the app in the top left corner.

class GUI:
    def __init__(self, master=tk.Tk()):
        self.master = master
        self.master.geometry("720x300")  
        self.add_components()      

        master.mainloop()
        
    
    def clicke(self, event):
       self.entry.configure(state=tk.NORMAL)
       self.entry.delete(0, tk.END)
       self.entry.unbind('<Button-1>', self.c)
       
    def valuate(self):
            #print("Nazdárek!")
            self.vbutton.pack_forget()
            self.pb.pack()
            self.pb.start()
            time.sleep(5)
            tc = TreeComputer()
            # tc.valuate_sheet(self.entry.get()) 
            outpath = tc.valuate_sheet(r'd:\Ekopontis\Ekopontis\Automatizace\cz.ekopontis.val-tree\data\test_final.xlsm')
            self.open_popup(outpath) 
            self.pb.stop()
            self.pb.pack_forget()
            self.vbutton.pack()
            
    def quit(self):
        self.master.destroy()
        
    def open_popup(self, outpath):
       top= tk.Toplevel(self.master)
       top.geometry("750x250")
       top.title("Child Window")
       tk.Label(top, text= f"Výstup: {outpath}", font=('Arial 12 bold')).place(x=150,y=80)
    
    def add_components(self):
        self.master.title("Kalkulačka dřevin")
        self.label = tk.Label(self.master, text="Soubor XLSM:")
        self.label.pack()
        self.pb = ttk.Progressbar(
            self.master,
            orient='horizontal',
            mode='indeterminate',
            length=280
            )
        self.entry = tk.Entry (self.master,width=100) 
        self.entry.insert(0, r'D:\Ekopontis\Ekopontis\Automatizace\data\trees.xlsm')
        self.entry.pack()
        self.c = self.entry.bind('<Button-1>', self.clicke)
        self.vbutton = tk.Button(self.master, text="Vypočítej cenu stromů", command = self.valuate)
        self.vbutton.pack()
