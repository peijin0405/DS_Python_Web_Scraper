#!/usr/bin/env python
# coding: utf-8

# In[26]:


get_ipython().system('pip install country-converter')
import pandas as pd
import numpy as np 
import requests # For downloading the website
from bs4 import BeautifulSoup # For parsing the website
import time # To put the system to sleep
import random # for random numbers
import country_converter as coco
import sqlite3
pd.options.display.max_rows = 10000


# In[2]:


###Q1(1)######


# In[3]:


# international-investment-agreements that we'll scrape. 
url = "https://investmentpolicy.unctad.org/international-investment-agreements/by-economy"
page = requests.get(url)
page.status_code # 200 == Connection


# In[4]:


# Parse the content 
soup = BeautifulSoup(page.text, 'lxml')
soup


# In[5]:


#be more specific in targeting specific content.
table = soup.find("table",{'class':"table countries ajax"})##find the table part on the page
table


# In[6]:


headers=[]##create a null list 
for i in table.find_all("th"):##loop for scraping the "columns"
    title=i.text.strip()
    headers.append(title)


# In[7]:


df0=pd.DataFrame(columns=headers)##create a df with columns 
df=df0.loc[:,'Name':'*\n\nTOTAL TIPs']##restrict the columns
df## check out the df 


# In[8]:


for row in table.find_all("tr")[1:]:##scrap the data in the table 
    data=row.find_all("td")##find the data in the table 
    row_data=[td.text.strip() for td in data]##put data into the df 
    length=len(df)
    df.loc[length]=row_data
df## check out the df 


# In[9]:


df[["bit","active_bit"]]=df["*\n\nTOTAL BITs"].str.split("(",expand=True)##splite the columns to get the total number of bilateral investment treaties 
df[["active_bit1","others"]]=df["active_bit"].str.split("in",expand=True)##splite the columns to get the total number of active bilateral investment treaties 
df##look into the data 


# In[10]:


df0=df.drop(columns=["*\n\nTOTAL BITs","*\n\nTOTAL TIPs","active_bit","others"])##drop extra columns 
df0##look into the data


# In[11]:


df1=df0.rename(columns={"Name":"raw_country","bit":"n_bits","active_bit1":"n_bits_active"})##rename the columns 
df2=df1.fillna(0)##fill the None with 0 
df2##look into the data


# In[12]:


df2["country"] = df2.raw_country.apply(lambda x: coco.convert(names=x, to='name_short', not_found=None))####standardize the countries name


# In[39]:


df_final0=df2.drop(columns=["raw_country"])##drop extra columns 
df_final=df_final0.filter(["country","n_bits","n_bits_active"])##reorder the columns in df 
df_final##look into the data


# In[40]:


###scrap all relevant UN Member States


# In[41]:


# list of all relevant UN Member States that we'll scrape. 
url0 = "https://www.un.org/about-us/member-states"
page0 = requests.get(url0)
page0.status_code # 200 == Connection


# In[42]:


# Parse the content 
soup0 = BeautifulSoup(page0.text, 'lxml')
soup0


# In[43]:


#be more specific in targeting specific content. 
un_country = [i.get_text() for i in soup0.find_all("h2")]## get the country name on the page
un_country.remove('Search the United Nations')##remove the first row of the list 


# In[44]:


##standardize the countries name 
standard_un_names = coco.convert(names=un_country, to='name_short')
standard_un_names##check out the standardized country names


# In[45]:


country_list=pd.DataFrame(standard_un_names,columns=["country"])##turn list into dataframe
country_list##look into the data


# In[57]:


country_level=country_list.merge(df_final,how="left",on="country")##merge the two columns based on "country"
country_level##look into the data


# In[58]:


country_level["n_bits"] = country_level["n_bits"].astype(int)##change the data type 
country_level["n_bits_active"] = country_level["n_bits_active"].astype(int)
country_level.info()##check the data type 


# In[61]:


country_level


# In[48]:


##store the dataframe in SQL


# In[63]:


# Establish a connection with the database
conn = sqlite3.connect("dataset4.sqlite")

# We can then write data to this database using .to_sql() method
country_level.to_sql(name="country_level",con=conn,index=False)


# In[ ]:




