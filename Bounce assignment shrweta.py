	#!/usr/bin/env python
	# coding: utf-8

	# In[35]:

def Load(path="train.csv"):
    import pandas as pd
    x=pd.read_csv(path)
    return(x)
    


	# In[37]:


	#data.head()


	# In[38]:


	#data.info()


	# In[39]:


    #import matplotlib.pyplot as plt  # For plotting graphs 
	#from datetime import datetime    # To access datetime 
	        # To work on series 
	#get_ipython().run_line_magic('matplotlib', 'inline')


	# In[40]:


	#data.dtypes


	# In[41]:


	#data.shape


	# In[42]:
def Transform(data):
    import pandas as pd
    from datetime import datetime

    data['datetime'] = pd.to_datetime(data['datetime'], errors='coerce')


	# In[43]:


    data['year'] = data['datetime'].dt.year 
    data['month'] = data['datetime'].dt.month 
    data['day'] = data['datetime'].dt.day 
    data['hour'] = data['datetime'].dt.hour 
    return (data)


	# In[44]:
def normalize(df,columns):
    result=df.copy()
    for feature_name in columns :
        mean_value = df[feature_name].mean()
        std_value = df[feature_name].std()
        result[feature_name] = (df[feature_name] - mean_value) / std_value
        
    return result


	# In[45]:

def dummy_data(data, columns):
    for column in columns:
        data = pd.concat([data, pd.get_dummies(data[column], prefix=column)], axis=1)
        data = data.drop(column, axis=1)
    return data


def split_valid_test_data(data, fraction=(1 - 0.8)):
    data_y = data["count"]
    
    

    data_x = data.drop(["count","casual","registered"], axis=1)

    

    return data_x.values, data_y

data_x, data_y = split_valid_test_data(data)



	# In[46]:

def model_building():
    from keras.models import Sequential
    from keras.layers import Dense, Activation, Flatten
    from keras.callbacks import ModelCheckpoint


# In[66]:


   NN_model = Sequential()

# The Input Layer :
   NN_model.add(Dense(128, kernel_initializer='normal',input_dim = data_x.shape[1], activation='relu'))

# The Hidden Layers :
   NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))
    NN_model.add(Dense(256, kernel_initializer='normal',activation='relu'))

# The Output Layer :
    NN_model.add(Dense(1, kernel_initializer='normal',activation='linear'))

# Compile the network :
    NN_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
    model_summary=NN_model.summary()
    return model_summary
    



	# In[47]:

    def callbacks():
        checkpoint_name = 'Weights-{epoch:03d}--{val_loss:.5f}.hdf5' 
        checkpoint = ModelCheckpoint(checkpoint_name, monitor='val_loss', verbose =1, save_best_only = True, mode ='auto')
        callbacks_list = [checkpoint]
    return callbacks_list

	# In[48]:





	# In[49]:


	#X = data.drop('datetime',1)


	# In[50]:


	#X.head()


	# In[51]:


    


    # In[52]:


    #X.columns


    # In[53]:


    #X.head()


    # In[54]:

def Visualize1(data):
    import seaborn as sns
    import matplotlib.pyplot as plt


    data['holiday'].value_counts().plot.bar()


    # In[55]:


    data['workingday'].value_counts().plot.bar()


    # In[56]:


    #X.columns


    # In[57]:


    #X.shape


    # In[58]:


    #import seaborn as sns


    # In[59]:


    plt.figure(1)
    plt.subplot(121)
    sns.distplot(data['temp']); 
    plt.subplot(122)
    data['temp'].plot.box(figsize=(16,5)) 
    plt.show()


    # In[60]:


    plt.figure(1)
    plt.subplot(121)
    sns.distplot(data['atemp']); 
    plt.subplot(122)
    data['atemp'].plot.box(figsize=(16,5)) 
    plt.show()


    # In[61]:


    plt.figure(1)
    plt.subplot(121)
    sns.distplot(data['humidity']); 
    plt.subplot(122)
    data['humidity'].plot.box(figsize=(16,5)) 
    plt.show()


    # In[62]:


    plt.figure(1)
    plt.subplot(121)
    sns.distplot(data['windspeed']); 
    plt.subplot(122)
    data['windspeed'].plot.box(figsize=(16,5)) 
    plt.show()


    # In[63]:


    #X.isnull().sum()


    # In[64]:


    matrix = data.corr()
    f, ax = plt.subplots(figsize=(16, 6))
    sns.heatmap(matrix, vmax=.8, square=True, cmap="BuPu");


    # In[65]:

    import numpy as np
    corrMat = data.corr()
    mask = np.array(corrMat)
    mask[np.tril_indices_from(mask)] = False
    fig, ax= plt.subplots(figsize=(30, 10))
    sns.heatmap(corrMat, mask=mask,vmax=1., square=True,annot=True)

    return 


def head(data):
    head=data.head()
    return(head)


def columns(data):
    columns=data.columns
    return(columns)

def null(data):
    null_values=data.isnull().sum()
    return(null_values)

def shape(data):
    shape=data.shape
    return(shape)

def datatype(data):
    data_types=data.dtypes
    return(data_types)

def corr(data):
    corr=data.corr()
    return(corr)







