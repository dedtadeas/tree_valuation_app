import tkinter as tk
from threading import Thread
import time
import os, sys
from tkinter import ttk
from src.val_tree.entities.tree_computer import TreeComputer # assuming you have a class TreeComputer in a separate file

class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tree Computer")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
        self.window.configure(bg="#F5F5F5")
    
        # path to the folder where the script is located
        if getattr(sys, 'frozen', False):
            application_path = sys._MEIPASS
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))

        # company logo
        logoFile =  application_path.split('entities')[0] + '\imgs\logo.png' # relative path for exe generation
        self.logo = tk.PhotoImage(file=logoFile) # replace with your logo path
        self.logo_label = tk.Label(self.window, image=self.logo, bg="#F5F5F5")
        self.logo_label.pack(pady=10)
        
        # entry box
        self.path_var = tk.StringVar()
        self.path_var.set(r"d:\Ekopontis\Ekopontis\Automatizace\cz.ekopontis.val-tree\data\test_final.xlsm") # default path
        self.path_entry = tk.Entry(self.window, textvariable=self.path_var, width=85, bd=3, relief=tk.GROOVE)
        self.path_entry.pack(pady=10)

        # button
        self.run_button = tk.Button(self.window, text="Run", bg="#4CAF50", fg="white", font=("Arial", 12), bd=0, command=self.run_tree_computer)
        self.run_button.pack(pady=10)
        
        self.progress_label = tk.Label(self.window, text="Computing...", font=("Arial", 12), bg="#F5F5F5")
        
        self.progress_bar = ttk.Progressbar(self.window, orient="horizontal", length=200, mode="determinate")
        
        # log window
        self.log_window = tk.Text(self.window, height=5, bg="white", fg="black", state=tk.DISABLED)
        self.log_window.pack(pady=10, padx=10)
        self.log_window.tag_config("error", foreground="red")

        self.window.mainloop()

    def run_tree_computer(self):
        path = self.path_var.get()
        if path.lower().endswith(".xlsm") and os.path.exists(path):
            self.path_entry.configure(bg="white")
            self.path_entry.update_idletasks()
            self.run_button.configure(state=tk.DISABLED)
            self.run_button.update_idletasks()
            self.progress_label.configure(text="Computing...")
            self.progress_label.pack()
            self.progress_label.update_idletasks()
            self.progress_bar.pack()
            self.progress_bar.start()
            self.progress_bar.update_idletasks()

            self.window.update_idletasks()
            
            def compute_tree():
                # tree computation
                tree_computer = TreeComputer()
                tree_computer.valuate_tree(path)
                while not tree_computer.output_path and not tree_computer.error:
                    time.sleep(0.1)

                if tree_computer.output_path:
                    output_path = tree_computer.output_path
                    message = f"Your file was generated here: {output_path}\n"
                    self.log_window.configure(state=tk.NORMAL)
                    self.log_window.insert(tk.END, message)
                    self.log_window.see(tk.END)
                    self.log_window.configure(state=tk.DISABLED)
                else:
                    error_message = f"Error: {tree_computer.error}\n"
                    self.log_window.configure(state=tk.NORMAL)
                    self.log_window.insert(tk.END, error_message, "error")
                    self.log_window.see(tk.END)
                    self.log_window.configure(state=tk.DISABLED)

                # enable button
                self.run_button.configure(state=tk.NORMAL)
                self.run_button.update_idletasks()
                self.progress_label.configure(text="")
                self.progress_bar.stop()
                self.progress_bar.pack_forget()
                self.progress_bar.update_idletasks()
                self.progress_label.update_idletasks()

            t = Thread(target=compute_tree)
            t.start()
        else:
            self.path_entry.configure(bg="#FFCDD2")
            message = "Error: Invalid file path or file type.\n"
            self.log_window.configure(state=tk.NORMAL)
            self.log_window.insert(tk.END, message)
            self.log_window.see(tk.END)
            self.log_window.configure(state=tk.DISABLED)
            