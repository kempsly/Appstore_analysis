#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import statements
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px


# In[2]:


# LET'S READ THE FILE FOR OUR ANALYSIS
df_apps = pd.read_csv('apps.csv')


# In[3]:


# PRELIMINARY DATA EXPLORATION


# In[4]:


df_apps.shape


# In[5]:


df_apps.head()


# In[6]:


df_apps.sample(10)


# In[7]:


df_apps.tail()


# In[8]:


# DATA CLEANING


# In[9]:


columns_to_delete = ['Last_Updated', 'Android_Ver']
df_apps.drop(columns_to_delete,  inplace=True, axis=1)


# In[10]:


nan_rows = df_apps[df_apps.Rating.isna()]
print(nan_rows.shape)
nan_rows.head()


# In[11]:


df_apps_clean = df_apps.dropna()
df_apps_clean.shape


# In[12]:


duplicated_rows = df_apps_clean[df_apps_clean.duplicated()]
print(duplicated_rows.shape)
duplicated_rows.head()


# In[13]:


# Now we can actually check for an individual app in our dataframe


# In[14]:


df_apps_clean[df_apps_clean.App == 'Facebook']


# In[15]:


df_apps_clean = df_apps_clean.drop_duplicates()


# In[16]:


df_apps_clean[df_apps_clean.App == 'Instagram']


# In[17]:


df_apps_clean = df_apps_clean.drop_duplicates(subset=['App', 'Type', 'Price'])
df_apps_clean[df_apps_clean.App == 'Instagram']


# In[18]:


# PRELIMINARY DATA EXPLORATION


# In[19]:


df_apps_clean.sort_values('Rating', ascending=False).head()


# In[20]:


# We see that only apps with very few reviews (and a low number on installs)
# have perfect 5 star ratings (most likely by friends and family).


# In[21]:


df_apps_clean.sort_values('Size_MBs', ascending=False).head()


# In[22]:


df_apps_clean.sort_values('Reviews', ascending=False).head(50)


# In[23]:


# Data Visualisation with Plotly: Create Pie and Donut Charts


# In[24]:


ratings = df_apps_clean.Content_Rating.value_counts()
ratings


# In[25]:


# Let's create a pie chart
fig = px.pie(labels=ratings.index, values=ratings.values,
            title="Content Rating",
names=ratings.index)

fig.update_traces(textposition='outside', textinfo='percent+label')

fig.show()


# In[26]:


fig = px.pie(labels=ratings.index,
values=ratings.values,
title="Content Rating",
names=ratings.index,
hole=0.6,
)
fig.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
 
fig.show()


# In[27]:


# We see the greatest part of the rating come from everyone(80.8%)


# In[28]:


# Let's find how many apps had over 1 billion installations? 
# How many apps just had a single install?


# In[29]:


df_apps_clean.Installs.describe()


# In[30]:


df_apps_clean.info()


# In[31]:


df_apps_clean[['App', 'Installs']].groupby('Installs').count()


# In[32]:


# Let's remove any commas in our dataframe
df_apps_clean.Installs = df_apps_clean.Installs.astype(str).str.replace(',', "")
df_apps_clean.Installs = pd.to_numeric(df_apps_clean.Installs)
df_apps_clean[['App', 'Installs']].groupby('Installs').count()


# In[33]:


# Finding the most Expensive Apps and Filtering out the Junk


# In[34]:


df_apps_clean.Price = df_apps_clean.Price.astype(str).str.replace('$', "")
df_apps_clean.Price = pd.to_numeric(df_apps_clean.Price)
 
df_apps_clean.sort_values('Price', ascending=False).head(20)


# In[35]:


# There are 15 I am Rich Apps in the Google Play Store apparently.
# They all cost $300 or more, which is the main point of the app.

# Leaving this bad data in our dataset will misrepresent our analysis of the most expensive 'real' apps
# Let's remove it


# In[36]:


df_apps_clean = df_apps_clean[df_apps_clean['Price'] < 250]
df_apps_clean.sort_values('Price', ascending=False).head(10)


# In[37]:


# When we look at the top 10 apps now, we see that 7 out of 10 are medical apps.


# In[38]:


# Let's get the highest grossing paid apps

df_apps_clean['Revenue_Estimate'] = df_apps_clean.Installs.mul(df_apps_clean.Price)
df_apps_clean.sort_values('Revenue_Estimate', ascending=False)[:10]


# In[39]:


# The top spot of the highest-grossing paid app goes 
# to … Minecraft at close to $70 million. 
 
# If we include these titles, we see that 7 out the top 10 highest-grossing apps are games.
# The Google Play Store seems to be quite flexible with its category labels.



# In[40]:


# Plotly Bar Charts & Scatter Plots: The Most Competitive & Popular App Categories


# In[41]:


# Finding the number of different categories

df_apps_clean.Category.nunique()


# In[42]:


# The number of apps per category
top10_category = df_apps_clean.Category.value_counts()[:10]
top10_category


# In[43]:


# Let's use plotly express to visualize this in a bar chart


# In[44]:


bar = px.bar(x = top10_category.index, # index = category name
             y = top10_category.values)
 
bar.show()


# In[45]:


# According to the number of apps, the Family, Game and Tools categories are the most competitive.
# Releasing yet another app into these categories will make it hard to get noticed.


# In[46]:


# Let's group all our apps by category and sum the number of installations

category_installs = df_apps_clean.groupby('Category').agg({'Installs': pd.Series.sum})
category_installs.sort_values('Installs', ascending=True, inplace=True)


# In[47]:


# Let's create a horizontal bar chart with h orientation

h_bar = px.bar(x = category_installs.Installs,
               y = category_installs.index,
               orientation='h',
               title='Category Popularity')
 
h_bar.update_layout(xaxis_title='Number of Downloads', yaxis_title='Category')
h_bar.show()


# In[48]:


# From the above chart, we see that Games and Tools are actually the most popular categories.


# In[49]:


# Let's determine how concentrate a category is by plotting 
# the popularity of a category next to the number of apps in that category


# In[50]:


# Number of apps in each category
cat_number = df_apps_clean.groupby('Category').agg({'App': pd.Series.count})


# In[51]:


cat_merged_df = pd.merge(cat_number, category_installs, on='Category', how="inner")
print(f'The dimensions of the DataFrame are: {cat_merged_df.shape}')
cat_merged_df.sort_values('Installs', ascending=False)


# In[52]:


scatter = px.scatter(cat_merged_df, # data
                    x='App', # column name
                    y='Installs',
                    title='Category Concentration',
                    size='App',
                    hover_name=cat_merged_df.index,
                    color='Installs')
 
scatter.update_layout(xaxis_title="Number of Apps (Lower=More Concentrated)",
                      yaxis_title="Installs",
                      yaxis=dict(type='log'))
 
scatter.show()


# In[53]:


# What we see is that the categories like Family, Tools, 
# and Game have many different apps sharing a high number of downloads.
# But for the categories like video players and entertainment, 
# all the downloads are concentrated in very few apps.


# In[54]:


# number of differents genres
len(df_apps_clean.Genres.unique())


# In[55]:


df_apps_clean.Genres.value_counts().sort_values(ascending=True)[:10]


# In[56]:


# Split the strings on the semi-colon and then .stack them.
stack = df_apps_clean.Genres.str.split(';', expand=True).stack()
print(f'We now have a single column with shape: {stack.shape}')
num_genres = stack.value_counts()
print(f'Number of genres: {len(num_genres)}')


# In[57]:


bar = px.bar(x = num_genres.index[:15], # index = category name
             y = num_genres.values[:15], # count
             title='Top Genres',
             hover_name=num_genres.index[:15],
             color=num_genres.values[:15],
             color_continuous_scale='Agsunset')
 
bar.update_layout(xaxis_title='Genre',
yaxis_title='Number of Apps',
coloraxis_showscale=False)
 
bar.show()


# In[58]:


# investivation into paid and free apps

df_apps_clean.Type.value_counts()


# In[59]:


# We see that the majority of apps are free on the Google Play Store.
# But perhaps some categories have more paid apps than others. 


# In[60]:


df_free_vs_paid = df_apps_clean.groupby(["Category", "Type"], as_index=False).agg({'App': pd.Series.count})
df_free_vs_paid.head()


# In[61]:


g_bar = px.bar(df_free_vs_paid,
               x='Category',
               y='App',
               title='Free vs Paid Apps by Category',
               color='Type',
               barmode='group')
 
g_bar.update_layout(xaxis_title='Category',
                    yaxis_title='Number of Apps',
                    xaxis={'categoryorder':'total descending'},
                    yaxis=dict(type='log'))
 
g_bar.show()


# In[62]:


# we see is that while there are very few paid apps 
# on the Google Play Store, some categories have relatively more paid apps than others,
# including Personalization, Medical and Weather. 


# In[63]:


# Let's see how much money we can make if we want to release one app based on it category


# In[66]:


# Box plots show us some handy descriptive statistics in a graph -
# things like the median value, 
# the maximum value, the minimum value, and some quartiles. 

# This box plot that shows the number of Installs for free versus paid apps.

box = px.box(df_apps_clean,
             y='Installs',
             x='Type',
             color='Type',
             notched=True,
             points='all',
             title='How Many Downloads are Paid Apps Giving Up?')
 
box.update_layout(yaxis=dict(type='log'))
 
box.show()


# In[ ]:


# From the box plot we see that the median number of downloads for free apps is 500,000, 
# while the median number of downloads for paid apps is around 5,000


# In[64]:


# Let’s see how much revenue we would estimate per category.


df_paid_apps = df_apps_clean[df_apps_clean['Type'] == 'Paid']
box = px.box(df_paid_apps, 
             x='Category', 
             y='Revenue_Estimate',
             title='How Much Can Paid Apps Earn?')
 
box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Ballpark Revenue',
                  xaxis={'categoryorder':'min ascending'},
                  yaxis=dict(type='log'))
 
 
box.show()


# In[ ]:


# If an Android app costs $30,000 to develop, 
# then the average app in very few categories would cover that development cost.
# The median paid photography app earned about $20,000.


# In[65]:


# App Pricing by Category

box = px.box(df_paid_apps,
             x='Category',
             y="Price",
             title='Price per Category')
 
box.update_layout(xaxis_title='Category',
                  yaxis_title='Paid App Price',
                  xaxis={'categoryorder':'max descending'},
                  yaxis=dict(type='log'))
 
box.show()


# In[ ]:


# The median price for an Android app is $2.99.

# However, some categories have higher median prices than others. 
# This time we see that Medical apps have the most expensive apps as well as 
# a median price of $5.49. In contrast, Personalisation apps are quite cheap on average at $1.49. 
# Other categories which higher median prices are Business ($4.99) and Dating ($6.99).

