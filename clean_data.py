#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


products_file = r'C:\Users\sharm\OneDrive\Desktop\Test\Data\PRODUCTS_TAKEHOME.csv'
transactions_file = r"C:\Users\sharm\OneDrive\Desktop\Test\Data\TRANSACTION_TAKEHOME.csv"
users_file = r"C:\Users\sharm\OneDrive\Desktop\Test\Data\USER_TAKEHOME.csv"
products_df = pd.read_csv(products_file)
transactions_df = pd.read_csv(transactions_file)
users_df = pd.read_csv(users_file)


# In[3]:


# Convert to date
transactions_df['PURCHASE_DATE'] = pd.to_datetime(transactions_df['PURCHASE_DATE'])
transactions_df['SCAN_DATE'] = pd.to_datetime(transactions_df['SCAN_DATE'])


# In[4]:


# Convert the column FINAL_SALE to float, coercing non-convertible values to NaN
transactions_df['FINAL_SALE'] = pd.to_numeric(transactions_df['FINAL_SALE'], errors='coerce')


# In[9]:


transactions_df = transactions_df.astype({
    'RECEIPT_ID': 'string',
    'STORE_NAME': 'string',
    'USER_ID': 'string'
})


# In[40]:


transactions_df['BARCODE'] = transactions_df['BARCODE'].astype('float64')


# In[5]:


users_df['CREATED_DATE'] = pd.to_datetime(users_df['CREATED_DATE'])
users_df['BIRTH_DATE'] = pd.to_datetime(users_df['BIRTH_DATE'])


# In[10]:


users_df = users_df.astype({
    'ID': 'string',
    'STATE': 'string',
    'LANGUAGE': 'string',
    'GENDER': 'string'
})


# In[50]:


products_df['BARCODE'] = products_df['BARCODE'].astype('float64')


# In[11]:


products_df = products_df.astype({
    'CATEGORY_1': 'string',
    'CATEGORY_2': 'string',
    'CATEGORY_3': 'string',
    'MANUFACTURER': 'string',
    'BRAND': 'string'
})


# In[46]:


product=products_df.dropna(axis=0, how='any')


# In[34]:


transaction=transactions_df.dropna(axis=0, how='any')


# In[35]:


user=users_df.dropna(axis=0, how='any')


# In[51]:


user.head()


# In[52]:


transaction.head()


# In[53]:


product.head()


# In[58]:


p=[]
for i in range(len(product)):
    pi = tuple(product.iloc[i])
    p.append(pi)


# In[65]:


u=[]
for j in range(len(user)):
    uj = tuple(user.iloc[j])
    u.append(uj)


# In[60]:


t=[]
for k in range(len(transaction)):
    tk = tuple(transaction.iloc[k])
    t.append(tk)


# In[62]:


with open('pfile.txt', 'w', encoding='utf-8') as file:
    for tuple in p:
        file.write(str(tuple) + ',' + '\n')


# In[63]:


with open('ufile.txt', 'w', encoding='utf-8') as file:
    for tuple in u:
        file.write(str(tuple) + ',' + '\n')


# In[64]:


with open('tfile.txt', 'w', encoding='utf-8') as file:
    for tuple in t:
        file.write(str(tuple) + ',' + '\n')


# In[ ]:




