#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def myOpenFileCollab(myUrlfromGit):
# import from git

    url =myUrlfromGit
    if url.endswith('.csv'):
        df = pd.read_csv(io.StringIO(response.content.decode('utf-8')))
    elif url.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(io.BytesIO(response.content), engine='openpyxl')

    return df

