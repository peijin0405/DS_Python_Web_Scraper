#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install country-converter')
import pandas as pd
import requests # For downloading the website
from bs4 import BeautifulSoup # For parsing the website
import time # To put the system to sleep
import random # for random numbers
import country_converter as coco
import numpy as np 
import sqlite3


# In[2]:


main_bit_page_url = "https://investmentpolicy.unctad.org/international-investment-agreements/by-economy"
main_page = requests.get(main_bit_page_url)##download the page
main_page.status_code### 200 == Connection


# In[3]:


main_soup = BeautifulSoup(main_page.content,'html.parser')### Parse the content 


# In[4]:


# Extract relevant links
links = set()## no duplicated 
for tag in main_soup.find_all("a"):
    href = tag.attrs.get("href")##just give me back the link
    if "international-investment-agreements/countries" in href:##"stories include world-us-canada"
        links.update(["https://investmentpolicy.unctad.org" + href])
links


# In[5]:


print(links)


# In[6]:


link_country0=list(links)##turn set into list 
link_country0##check out the links 


# In[7]:


##create a function to process each link 
def un_country_scraper(url=None):
    # Download the webpage
    page = requests.get(url)
    # If a connection was reached
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, 'lxml')# Parse the content 
        table = soup.find("table",{"class":"table ajax"})#be more specific in targeting specific content.
        
        headers=[]##create a null list 
        for i in table.find_all("th"):##loop for scraping the "columns"
            title=i.text.strip()
            headers.append(title)
        df0=pd.DataFrame(columns=headers)##create a df with columns 
        df=df0.loc[:,'Full title': 'Text']##create the columns of the df 
        for row in table.find_all("tr")[1:]:##scrap the data in the table 
            data=row.find_all("td")##find the data in the table 
            row_data=[td.text.strip() for td in data]##put data into the df 
            length=len(df)
            df.loc[length]=row_data
        df["country"]=url.split("/")[-1]##create a new column to mark the country
        data_array=np.array(df)##turn df into array 
        data_list=data_array.tolist()
        ##turn array into list 
    
        return data_list##return the list


# In[8]:


# Extract one webpage to check：
##un_country_scraper("https://investmentpolicy.unctad.org/international-investment-agreements/countries/188/seychelles")


# In[9]:


# Let's write the above as a single function
def link_scrape(urls=None,sleep=3):
    """Scrape multiple BIT URLS.

    Args:
        urls (list): list of valid BIT urls.
        sleep (int): Integer value specifying how long the machine should be
                    put to sleep (random uniform). Defaults to 3.

    Returns:
        DataFrame: frame containing the BIT information of different countries 
    """
    scraped_data = []
    for url in urls:
        print(url) # Keep track of where we are at.
        try:
            # Scrape the content This will break on URLs that we haven't
            # accounted for the structure on. So we'll use a try and except 
            # clause so our code continues even though it breaks on some urls. 
            scraped_data.append(un_country_scraper(url))
        except:
            print("URL doesn't work with scraper")
        # Put the system to sleep for a random draw of time (be kind)
        time.sleep(random.uniform(0,sleep))
    
    all_case=[]##create a new list 
    for single_case in scraped_data:
        for subject in single_case:
            all_case.append(subject)###flatten the 3D list 
    dat=pd.DataFrame(all_case)##turn the list into a df 
    return dat##return the value 

dat = link_scrape(urls=link_country0)
dat


# In[10]:


dat1=dat.rename(columns={2:"TYPES",3:"status",4:"country_B_raw",5:"year_signed",6:"year_enforced",7:"year_terminated",9:"country_A_raw"})##rename the columns
dat1


# In[11]:


dat2=dat1.drop(columns=[0,1,8])##drop extra columns 
dat3=dat2.filter(["country_A_raw","country_B_raw","TYPES","status","year_signed","year_enforced","year_terminated"])##reorder the columns in df
dat3


# In[12]:


dat3["status"].unique()##check out the value in the column 


# In[13]:


dat3["status"]=dat3["status"].replace("Signed", "signed")##replace with "signed", "active", and "terminated"
dat3["status"]=dat3["status"].replace('Signed (not in force)', "signed")##replace with "signed", "active", and "terminated"
dat3["status"]=dat3["status"].replace("In force", "active")##replace with "signed", "active", and "terminated"
dat3["status"]=dat3["status"].replace("Terminated", "terminated")##replace with "signed", "active", and "terminated"
dat3##


# In[14]:


####standardize the countries name
cc = coco.CountryConverter()
dat3["country_A"] = cc.convert(dat3["country_A_raw"], to = 'name_short')


# In[15]:


####standardize the countries name
dat3["country_B"] = cc.convert(dat3["country_B_raw"], to = 'name_short')


# In[16]:


dat4=dat3.drop(columns=["country_A_raw","country_B_raw"])##drop extra columns 
dat5=dat4.filter(["country_A","country_B","TYPES","status","year_signed","year_enforced","year_terminated"])##reorder the columns in df
dat5##look into the data


# In[17]:


dat5 = dat5.query('TYPES == "BITs"')


# In[18]:


###scrap all relevant UN Member States


# In[19]:


# list of all relevant UN Member States that we'll scrape. 
url0 = "https://www.un.org/about-us/member-states"
page0 = requests.get(url0)
page0.status_code # 200 == Connection


# In[20]:


# Parse the content 
soup0 = BeautifulSoup(page0.text, 'lxml')
#be more specific in targeting specific content. 
un_country = [i.get_text() for i in soup0.find_all("h2")]## get the country name on the page
un_country.remove('Search the United Nations')##remove the first row of the list 


# In[21]:


##standardize the countries name 
standard_un_names = coco.convert(names=un_country, to='name_short')
standard_un_names##check out the standardized country names


# In[22]:


country_list=pd.DataFrame(standard_un_names,columns=["country"])##turn list into dataframe
country_list##look into the data


# In[23]:


##Restrict this dataset to included countries


# In[24]:


UN_country0=country_list.merge(dat5, how="left", left_on='country', right_on='country_A')##merge the two columns based on "country"
UN_country1=UN_country0.drop(columns=["country_A"])##drop extra columns 
UN_country2=UN_country1.rename(columns={"country":"country_A"})##rename the column
UN_country2


# In[25]:


UN_country3= country_list.merge(UN_country2, how = 'inner', left_on = 'country', right_on = 'country_B')##merge the two columns based on "country"
UN_country3


# In[26]:


UN_country4=UN_country3.drop(columns=["country"])##drop extra columns 
UN_country5=UN_country4.drop(columns=["TYPES"])##drop extra columns 
UN_country5##final version of the df


# In[27]:


UN_country5[["year_signed1","year_signed2","year_signed3"]]=UN_country5["year_signed"].str.split("/",n=2,expand=True)##splite the columns to get the total number of bilateral investment treaties
UN_country5[["year_enforced1","year_enforced2","year_enforced3"]]=UN_country5["year_enforced"].str.split("/",n=2,expand=True)##splite the columns to get the total number of bilateral investment treaties
UN_country5[["year_terminated1","year_terminated2","year_terminated3"]]=UN_country5["year_terminated"].str.split("/",n=2,expand=True)##splite the columns to get the total number of bilateral investment treaties
UN_country5


# In[60]:


UN_country6=UN_country5.drop(columns=["year_signed1","year_signed2","year_enforced1","year_signed1","year_enforced2","year_terminated1","year_terminated2","year_signed","year_enforced","year_terminated"])##drop extra columns
UN_country6


# In[61]:


UN_country7=UN_country6.rename(columns={"year_signed3":"year_signed","year_enforced3":"year_enforced","year_terminated3":"year_terminated"})##rename the columns
UN_country7##final dataframe 


# In[66]:


UN_country7["year_signed"] = UN_country7["year_signed"].astype('float')##change the data type
UN_country7["year_enforced"] = UN_country7["year_enforced"].astype('float')
UN_country7["year_terminated"] = UN_country7["year_terminated"].astype('float')
UN_country7.info()


# In[68]:


UN_country7


# In[46]:


##store the dataframe in SQL


# In[70]:


# Establish a connection with the database
conn = sqlite3.connect("dataset4.sqlite")

# We can then write data to this database using .to_sql() method
UN_country7.to_sql(name="dyad_level",con=conn,index=False)


# In[ ]:




