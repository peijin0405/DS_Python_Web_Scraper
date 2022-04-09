#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import sqlite3
from matplotlib import pyplot as plt
import numpy as np
from plotnine import *
import warnings
warnings.filterwarnings('ignore')


# In[3]:


##V_1
# Establish a connection with the database
conn = sqlite3.connect("dataset4.sqlite")


# In[4]:


# We can write pretty much any query we would in SQLite,
# evalutate it, and then return back the results from
# the query.
query = '''
select 
	country, 
	n_bits, 
	n_bits_active, 
	n_bits - n_bits_active as n_bits_inactive 
from country_level
order by n_bits desc
'''


# In[5]:


V1=pd.read_sql(query,conn)##read in the data
V1


# In[6]:


# Disconnect from connection
conn.close()


# In[7]:


plt.rcParams["figure.figsize"] = [20, 30]
countries = V1["country"]
actives = V1['n_bits_active']
inactives = V1['n_bits_inactive']
ind = [x for x, _ in enumerate(countries)]## loop through each country 
plt.rcParams["figure.autolayout"] = True


# In[8]:


plt.barh(ind, actives, label='Actives BITs', color='red')
plt.barh(ind, inactives, left=actives, label='Inactives BITs', color='green')
plt.gca().invert_yaxis()

plt.yticks(ind, countries)
plt.xlabel("Number of BITs")
plt.ylabel("Countries")
plt.title("Number of BITs of Each Country")
plt.legend(loc="lower right")

plt.annotate('[Data from: https://investmentpolicy.unctad.org/international-investment-agreements/by-economy]', (0,0), (10,-40), fontsize=10, 
             xycoords='axes fraction', textcoords='offset points', va='top')
plt.show()


# In[11]:


##V2
# Establish a connection with the database
conn = sqlite3.connect("dataset4.sqlite")


# In[12]:


# We can write pretty much any query we would in SQLite,
# evalutate it, and then return back the results from
# the query.
query1 = '''
with k as(
	WITH algeria_a as (
		select 
			year_enforced,
			count(*) as n1
		from dyad_level 
		group by year_enforced
	),
	algeria_b as (
		select 
			year_terminated,
			count(*) as n2
		from dyad_level 
		group by year_terminated
	)
	select * 
	from algeria_a
	inner join algeria_b on (algeria_a.year_enforced = algeria_b.year_terminated )
)
select
	year_enforced,
	n1,
	n2,
	n1-n2 as n
from k
'''


# In[13]:


V2=pd.read_sql(query1,conn)##read in the data
V2


# In[14]:


# Establish a connection with the database
conn = sqlite3.connect("dataset4.sqlite")


# In[15]:


#Creating the visualization.
year = V2['year_enforced']
net_new = V2['n']

plt.plot(year, net_new)
plt.xlabel("Years")
plt.ylabel("Numbers of Net New BITs")
plt.title("Number of Net New BITs on Each Year")

plt.annotate('[Data from: https://investmentpolicy.unctad.org/international-investment-agreements/by-economy]', (0,0), (70,-40), fontsize=10, 
             xycoords='axes fraction', textcoords='offset points', va='top')

plt.savefig('vis2.png', dpi = 300)
plt.rcParams["figure.figsize"] = [10, 7]
plt.show()


# In[19]:


##V3
# Establish a connection with the database
conn = sqlite3.connect("dataset4.sqlite")


# In[20]:


# We can write pretty much any query we would in SQLite,
# evalutate it, and then return back the results from
# the query.
query2 = '''
WITH algeria_a as (
	SELECT 
	country_A,
	country_B,
	case 
		when status ='active'then 1  
		when status ='signed'then 0
		when status ='terminated'then 0
	end as status_a
	FROM dyad_level
	WHERE
	country_A =  'United States'
),
algeria_b as (
	SELECT 
	country_A,
	country_B,
	case 
		when status ='active'then 1  
		when status ='signed'then 0
		when status ='terminated'then 0
	end as status_a
	FROM dyad_level
	WHERE
	country_A =  'Russia'
),
algeria_c as (
	SELECT 
	country_A,
	country_B,
	case 
		when status ='active'then 1  
		when status ='signed'then 0
		when status ='terminated'then 0
	end as status_a
	FROM dyad_level
	WHERE
	country_A =  'Germany'
),
algeria_d as (
	SELECT 
	country_A,
	country_B,
	case 
		when status ='active'then 1  
		when status ='signed'then 0
		when status ='terminated'then 0
	end as status_a
	FROM dyad_level
	WHERE
	country_A =  'China'
)
select * from algeria_a
UNION ALL
select * from algeria_b
UNION ALL
select * from algeria_c
UNION ALL
select * from algeria_d
'''


# In[21]:


V3=pd.read_sql(query2,conn)##read in the data
V3


# In[24]:



#Creating the visualization.
(
    ggplot(V3,aes(x="country_B",y="country_A",fill="status_a", width=.95, height=.95)) +
    geom_tile(aes(width=.5, height=.1)) +
    labs(x = '', y = '', title = 'Countries‘ Active BIT status with United States, Russia, Germany, and China', fill="red for not signed, blue for signed") +
    theme(figure_size=(45,10), axis_text_x=element_text(rotation=55)) +
    theme(legend_position = "bottom") +
    scale_fill_gradientn(["red", "blue"])
)


# Task 3: Insights

# 1. Referring to plot 1, are there certain characteristics about countries that sign many BIT agreements
# #vis-a-vis those that sign few? You may reference other data (such as regime type or GDP data used
# #in class) to investigate your claim. 

# Countries that sign many BIT agreements are those with relatively high GDP and GDP per capital. These countries are always with high democratic level, attaches great importance to diplomacy, and more open. According to the data from World bank, these countries are always higher cross-border trade volume.

# 2. Referring to plot 2, are there moments in time when countries entered into more or less BIT agreements? If so, can you speculate why?

# there are surges in signed BIT agreements in 1990s and 2000s, ther are less before 1980 and after 2000. The reason may be the surge did something with the development of WTO and the decline may be correlated with COVID-19.

# 3. Referring to plot 3, does one country (among the four on the x-axis) enter into noticeably more or fewer BITs than the other three? If so, what is it about this country compared to the other three that might explain this difference?

# The US has noticeably less BITs than other three countries, compared to other countries, US has higher GDP and GDP per capital, which means it rely on less on the relationship with other countries. China has more BITs than other countries, for it attaches great importance to the relationship with other countries. 
