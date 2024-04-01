
import pandas as pd
import tkinter as tk
import math
from tkinter import filedialog

def myOpenFile():
    root=tk.Tk()
    root.withdraw()

    file_path=filedialog.askopenfilename(title="Select an Anna Excel or CSV dump",filetypes=[("Excel files","*.xlsx *.xls"),("CSV files","*.csv")])
    if file_path:
        if file_path.endswith(('.xlsx','.xls')):
            df=pd.read_excel(file_path,engine='openpyxl')
        elif file_path.endswith('.csv'):
            df=pd.read_csv(file_path,sep=";")

    else:
        print("No file selected.")
    return df
