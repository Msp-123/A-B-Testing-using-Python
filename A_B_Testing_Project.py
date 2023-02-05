#!/usr/bin/env python
# coding: utf-8

# In[217]:


import numpy as np
import pandas as pd
import datetime
from datetime import date, timedelta
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt


# In[218]:


control_data = pd.read_csv('control_group.csv', sep=';')
test_data = pd.read_csv('test_group.csv', sep=';')


# In[219]:


control_data.head(8)


# In[220]:


test_data.head(8)


# ## Data Preperation

# ### The datasets have some errors in column names. Let's change them

# In[221]:


control_data.columns


# In[222]:


control_data.columns = ["Campaign Name", "Date", "Amount Spent",
                       "Number of Impressions", "Reach", "Website Clicks",
                       "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases"
                       ]


# In[223]:


test_data.columns = ["Campaign Name", "Date", "Amount Spent", 
                        "Number of Impressions", "Reach", "Website Clicks", 
                        "Searches Received", "Content Viewed", "Added to Cart",
                     "Purchases"
                    ]


# In[224]:


control_data.head()


# In[225]:


test_data.head()


# ### Check the datasets if there are null values:

# In[226]:


control_data.isnull().sum().any()


# In[227]:


control_data.isnull().sum()


# In[228]:


test_data.isnull().sum().any()


# In[229]:


test_data.isnull().sum()


# ### The control dataset has null values in a row. We can impute them with the mean value of each column

# ### There are 7 columns which have null values. We will use Scikit-Learn library to fill them.

# In[230]:


from sklearn.impute import SimpleImputer
si = SimpleImputer(strategy='mean')
control_data[["Number of Impressions", "Reach", "Website Clicks",
                       "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases" ]] = np.round(si.fit_transform(control_data[["Number of Impressions", "Reach",
                         "Website Clicks", "Searches Received", "Content Viewed", "Added to Cart",
                        "Purchases" ]]),2)


# In[231]:


control_data.isnull().sum().any()


# ### Creating a new dataset by merging both datasets.

# In[232]:


ab_data = control_data.merge(test_data, how='outer').sort_values(['Date'])


# In[233]:


ab_data = ab_data.reset_index(drop=True)


# In[234]:


ab_data


# ### Checking if the dataset has an equal number of samples about both campaigns

# In[235]:


ab_data['Campaign Name'].value_counts()


# ## A/B Testing to Find the Best Marketing Strategy

# ### Analyzing the relationship between the number of impressions we got from both campaigns and the amount spent on both campaigns

# In[236]:


figure = px.scatter(data_frame = ab_data,
                   x='Number of Impressions',
                    y='Amount Spent',
                    size='Amount Spent',
                    color= 'Campaign Name',
                    trendline='ols'  #  Ordinary Least Squares regression 
                   )
figure.show()


# ### The control campaign resulted in more impressions according to the amount spent on both campaigns. 
# ### Now let’s have a look at the number of searches performed on the website from both campaigns:

# In[237]:


labels = ["Total Searches from Control Campaign", 
         "Total Searches from Test Campaign"]
values = [sum(control_data['Searches Received']),
         sum(test_data['Searches Received'])]

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:.1f} )".format(pct, absolute)

plt.pie(values, labels=labels, autopct=lambda pct: func(pct, values),textprops=dict(color="w"),radius=1.5)
plt.legend(bbox_to_anchor=(1.2,1),loc="center left",fontsize=12)
plt.show()


# ### The test campaign resulted in more searches on the website.

# ### Now let’s have a look at the number of website clicks from both campaigns

# In[238]:


plt.bar("Content Viewed \nfrom Control Campaign",sum(control_data["Content Viewed"]))
plt.bar("Content Viewed \nfrom Test Campaign",sum(test_data["Content Viewed"]))
3#lt.ylabel("Website Clicks",fontsize=14)
plt.text(-0.2,30000,"Total : "+'\n' + str(sum(control_data["Content Viewed"])),fontsize=12)
plt.text(0.88,30000,"Total : " +'\n' + str(sum(test_data["Content Viewed"])),fontsize=12)
plt.show()


# ### The audience of the control campaign viewed more content than the test campaign. Although there is not much difference, as the website clicks of the control campaign were low, its engagement on the website is higher than the test campaign.

# ### Let’s have a look at the number of products added to the cart from both campaigns

# In[239]:


labels = ["Products Added to Cart from Control Campaign", 
         "Products Added to Cart from Test Campaign"]
values = [sum(control_data['Added to Cart']),
         sum(test_data['Added to Cart'])]

def func(pct, allvals):
    absolute = int(np.round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n({:.1f} )".format(pct, absolute)

plt.pie(values, labels=labels, autopct=lambda pct: func(pct, values),textprops=dict(color="w"),radius=1.5)
plt.legend(bbox_to_anchor=(1.2,1),loc="center left",fontsize=12)
plt.show()


# ### Despite low website clicks, more products were added to the cart from the control campaign.

# ###  Let’s have a look at the amount spent on both campaigns

# In[240]:


labels = ["Amount of Spent in Control Campaign", 
         "Amount of Spent in Test Campaign"]
values = [sum(control_data['Amount Spent']),
         sum(test_data['Amount Spent'])]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_layout(title_text='Control vs Test: Amount Spent')
fig.update_traces(hoverinfo='label+percent',textinfo='percent+value',textfont_size=16,
                 marker=dict(line=dict(color='black', width=2)))


# ### The amount spent on the test campaign is higher than the control campaign.
# ### However as we can see that the control campaign resulted in more content views and more products in the cart, the control campaign is more efficient than the test campaign.

# ### Let’s have a look at the purchases made by both campaigns

# In[241]:


labels = ["Purchases Made by Control Campaign", 
         "Purchases Made by Test Campaign"]
values = [sum(control_data['Purchases']),
         sum(test_data['Purchases'])]

fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
fig.update_layout(title_text='Control vs Test: Purchases')
fig.update_traces(hoverinfo='label+percent',textinfo='percent+value',textfont_size=16,
                 marker=dict(line=dict(color='black', width=2)))


# ### There’s only a difference of around 0.2% in the purchases made from both ad campaigns. As the Control campaign resulted in more sales in less amount spent on marketing, the control campaign wins here!

# ### Let’s analyze some metrics to find which ad campaign converts more

# ### First look at the relationship between the number of website clicks and content viewed from both campaigns

# In[245]:


fig = px.scatter(data_frame = ab_data,
                x='Content Viewed',
                y='Website Clicks',
                size='Website Clicks',
                color='Campaign Name',
                trendline='ols')
fig.show()


# ### The website clicks are higher in the test campaign, but the engagement from website clicks is higher in the control campaign. So the control campaign wins!

# ### The relationship between the amount of content viewed and the number of products added to the cart from both campaigns:

# In[248]:


fig = px.scatter(data_frame=ab_data,
                x='Added to Cart',
                y='Content Viewed',
                size='Added to Cart',
                color='Campaign Name',
                trendline='ols')
fig.show()


# ### The engagement from Content Viewed is higher in the control campaign.Again, the control campaign wins!

# ### The relationship between the number of products added to the cart and the number of sales from both campaigns:

# In[251]:


fig = px.scatter(data_frame=ab_data,
                x='Purchases',
                y='Added to Cart',
                size='Purchases',
                color='Campaign Name',
                trendline='ols')
fig.show()


# ### Although the control campaign resulted in more sales and more products in the cart, the conversation rate of the test campaign is higher.

# ## Conclusion

# ### The A/B tests showed that the control campaign was more successful in terms of sales and engagement from visitors. Visitors viewed more products in the control campaign, leading to more products in carts and sales. However, the test campaign had a higher conversion rate for products in carts. While the test campaign generated more sales based on products viewed and added to carts, the control campaign resulted in higher overall sales. Hence, the test campaign is suitable for targeting specific products to specific audiences, while the control campaign is better for promoting multiple products to a broader audience.

# In[ ]:




