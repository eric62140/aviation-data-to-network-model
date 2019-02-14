#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from numpy import array
from numpy import argmax


# In[2]:


#read data and show the first five lines of data
db = pd.read_csv('BWIFullOutageSelect_20181005.csv')
db = db[db['Log_Id,N,10,0'] != 0]
#rename each column 
db = db.rename(columns = {'Log_Id,N,10,0':'Log_id','Fac_Type,C,254':'Fac_type','Fac_Ident,C,254':'Fac_ident','Fac_Code,C,254':'Fac_code','Runway,C,254':'Runway','Latitude_D,N,19,11':'Latitude','Longitude_,N,19,11':'Longitude','Assoc_Airp,C,254':'Assoc_airp','Code_Categ,N,10,0':'Code_categ','Interrupt_,C,254':'Interrupt','Supplement,C,254':'Supplement','Sup_Codede,C,254':'Sup_code','Maint_Acti,C,254':'Maint_acti','Mac_Descri,C,254':'Mac_descri','Start_Date,D':'Start_date','End_Dateti,D':'End_date','Log_Summar,C,254':'Log_summary'})
#copy data and drop useless columns
db = db.drop(['Fac_code','Runway','Assoc_airp','Log_summary','Latitude','Longitude'], axis=1)
db['Fac'] = db.Fac_type + '-' + db.Fac_ident
db = db.drop(['Fac_type','Fac_ident'],axis = 1)
db['Start_date'] = pd.to_datetime(db['Start_date'],infer_datetime_format=True)
db['End_date'] = pd.to_datetime(db['End_date'],infer_datetime_format=True)
db['Outage_dur'] = db.End_date - db.Start_date
dbb = db.drop(db.index[0:21])


# In[3]:


# optional data processing 
De = pd.read_csv('delayed_per_day.csv')
eqt = pd.read_csv("eqt_delay.csv")
De['Date'] = pd.to_datetime(De['Date'], errors='coerce')#.dt.date
De['average_delay'] = De[['depart', 'arrive']].mean(axis=1)
De['isoutage'] = 0
dbb['eqt_delay'] = 0
dbb['eqt_min'] = 0
eqt['delay_eqt'] = 0
eqt['Date'] = pd.to_datetime(eqt['Date'], format='%Y/%m/%d')
dbb = dbb.reset_index()


# In[5]:


faclist = dbb['Fac'].unique().tolist()
faclist


# #-------------------------
# #-------------------------

# In[7]:


newdata = dbb[['Start_date', 'Fac', 'eqt_delay', 'eqt_min']].copy()
# remove the same startdate and facility type of the outage in the same day
def takeawaysame(newdata):
    kk = newdata[:]
    pp = kk # new dataframe to use 
    pp = pp.reset_index(drop=True)
    datee = []
    facc = []
    for i in range(len(pp)):
        s = pp[i:i+1]['Start_date']
        f = pp[i:i+1]['Fac']
        for k in s:
            k = k.strftime('%Y/%m/%d')
            datee.append(k)
        for ff in f:
            facc.append(ff)
    tt = pp.copy()
    
    dateee = datee
    faccc = facc
    for i in range(1,len(pp.index)):
        if (dateee[i-1] == dateee[i]) and (faccc[i-1] == faccc[i]):
            tt.iloc[i:i+1]['Fac'] = 'NaN'
    test = tt
    test = test[test.Fac != 'NaN']
    test = test.reset_index(drop=True)
    
       
    return test


# In[8]:


cleandata = takeawaysame(newdata)


# In[12]:


cleandata = cleandata.drop(['eqt_delay', 'eqt_min'], axis = 1)


# In[71]:


date = []
for i in temp['Start_date']:
    date.append(i)


# In[95]:


i = 0
source = []
sink = []
weight = []


# In[98]:


for i in range(len(date)):
    s = datetime.strptime(date[i+1].strftime('%Y/%m/%d'), FMT) - datetime.strptime(date[i].strftime('%Y/%m/%d'), FMT)
    if (s.days==1):
        t = temp.iloc[i]['Fac'] 
        k = temp.iloc[i+1]['Fac']
        t = t.split(',')
        k = k.split(',')
        for tt in range(len(t)):
            for kk in range(len(k)):
                if t[tt] != k[kk]:
                    source.append(t[tt])
                    sink.append(k[kk])
                    weight.append(1)      


# In[100]:


ad = {'Source':source,'Target':sink, 'Weight':weight}
adjacent = pd.DataFrame(ad)


# In[103]:


new_ad = adjacent.groupby(['Source','Target']).sum()


# In[122]:


fac_t = dbb['Fac'].unique()


# In[126]:


list1 = [a for a in range(len(fac_t))]


# In[128]:


no = {'id':list1,'fac':list(fac_t)}
nodes = pd.DataFrame(no)


# In[130]:


nodes.to_csv('nodes.csv')
new_ad.to_csv('new_ad.csv')


# In[ ]:




