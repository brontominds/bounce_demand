#!/usr/bin/env python
# coding: utf-8

# In[35]:


import pandas as pd


# In[36]:


data=pd.read_csv("train.csv")#Making it Relative Path -Mayank


# In[37]:


data.head()


# In[38]:


data.info()


# In[39]:


import matplotlib.pyplot as plt  # For plotting graphs 
from datetime import datetime    # To access datetime 
from pandas import Series        # To work on series 
get_ipython().run_line_magic('matplotlib', 'inline')


# In[40]:


data.dtypes


# In[41]:


data.shape


# In[42]:


data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')


# In[43]:


data['year'] = data['datetime'].dt.year 
data['month'] = data['datetime'].dt.month 
data['day'] = data['datetime'].dt.day 
data['hour'] = data['datetime'].dt.hour 


# In[44]:


data.head()


# In[45]:


data['weather'].replace(1, 'Clear',inplace=True) 
data['weather'].replace(2, 'Mist',inplace=True)
data['weather'].replace(3, 'Light snow',inplace=True) 
data['weather'].replace(4, 'Heavy rain',inplace=True)


# In[46]:


data.head()


# In[47]:


data['season'].replace(1, 'Spring',inplace=True) 
data['season'].replace(2, 'Summer',inplace=True)
data['season'].replace(3, 'Fall',inplace=True) 
data['season'].replace(4, 'Winter',inplace=True)


# In[48]:


data.head()


# In[49]:


X = data.drop('datetime',1)


# In[50]:


X.head()


# In[51]:


X=pd.get_dummies(X)


# In[52]:


X.columns


# In[53]:


X.head()


# In[54]:


X['holiday'].value_counts().plot.bar()


# In[55]:


X['workingday'].value_counts().plot.bar()


# In[56]:


X.columns


# In[57]:


X.shape


# In[58]:


import seaborn as sns


# In[59]:


plt.figure(1)
plt.subplot(121)
sns.distplot(X['temp']); 
plt.subplot(122)
X['temp'].plot.box(figsize=(16,5)) 
plt.show()


# In[60]:


plt.figure(1)
plt.subplot(121)
sns.distplot(X['atemp']); 
plt.subplot(122)
X['atemp'].plot.box(figsize=(16,5)) 
plt.show()


# In[61]:


plt.figure(1)
plt.subplot(121)
sns.distplot(X['humidity']); 
plt.subplot(122)
X['humidity'].plot.box(figsize=(16,5)) 
plt.show()


# In[62]:


plt.figure(1)
plt.subplot(121)
sns.distplot(X['windspeed']); 
plt.subplot(122)
X['windspeed'].plot.box(figsize=(16,5)) 
plt.show()


# In[63]:


X.isnull().sum()


# In[64]:


matrix = X.corr()
f, ax = plt.subplots(figsize=(16, 6))
sns.heatmap(matrix, vmax=.8, square=True, cmap="BuPu");


# In[65]:


corrMat = X.corr()
mask = np.array(corrMat)
mask[np.tril_indices_from(mask)] = False
fig, ax= plt.subplots(figsize=(30, 10))
sns.heatmap(corrMat, mask=mask,vmax=1., square=True,annot=True)


# In[66]:


X.corr()


# In[67]:


X['windspeed_log'] = np.log(X['windspeed'])


# In[68]:


X['windspeed_log']


# In[ ]:




