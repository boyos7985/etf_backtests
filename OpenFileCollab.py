#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import requests
import io

def myOpenFileCollab(myUrlfromGit):
    
    
# import from git

    url =myUrlfromGit
    
    # Make a GET request to fetch the raw content of the file
    response = requests.get(url)
    
    # Check if the URL is indeed pointing to a file and we received a response
    if response.status_code == 200:
        if url.endswith('.csv'):
            # If the file is a CSV, read it into a DataFrame
            df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
        elif url.endswith(('.xls', '.xlsx')):
            # If the file is an Excel file, read it into a DataFrame
            df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')
        return df
    else:
        # Handle cases where the URL might be wrong or the file is inaccessible
        print("Failed to fetch the file. Status code:", response.status_code)
        return None

