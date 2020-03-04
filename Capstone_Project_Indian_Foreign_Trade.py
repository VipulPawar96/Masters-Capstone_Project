# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:50:01 2019

@author: Vipul
"""


#...........................DATA PREPROCESSING...............................

#Libraries providing structures and data analysis tools
import numpy as np 
import pandas as pd 

#Libraries for data visualisation and charts
import seaborn as sns 
import matplotlib.pyplot as plt
import squarify 
import plotly.graph_objects as go
from plotly.offline import plot

#ignore warning 
import warnings
warnings.filterwarnings("ignore")

# Input data files 
import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))
        
data_import = pd.read_csv("2018-2010_import.csv")
data_export = pd.read_csv("2018-2010_export.csv")


#...............................DESCRIPTIVE STATISTICAL...................... 

# Getting a view at the Data
data_export.head(5)
data_import.head(5)


# Retrieving different statistical information on the import and export
data_export.describe()

data_import.describe()     

data_export.info()   

data_import.info()

#..................................DATA CLEANUP.........................................

# Finding and dealing with the missing values
data_import.isnull().sum()

data_import[data_import.value==0].head(5)

data_import[data_import.country == "UNSPECIFIED"].head(5)

print("Duplicate imports : "+str(data_import.duplicated().sum()))
print("Duplicate exports : "+str(data_export.duplicated().sum()))


def cleanup(data_df):
    #setting country UNSPECIFIED to nan
    data_df['country']= data_df['country'].apply(lambda x : np.NaN if x == "UNSPECIFIED" else x)
    #ignoring where import value is 0 . 
    data_df = data_df[data_df.value!=0]
    data_df.dropna(inplace=True)
    data_df.year = pd.Categorical(data_df.year)
    data_df.drop_duplicates(keep="first",inplace=True)
    return data_df

data_import = cleanup(data_import)
data_export = cleanup(data_export)

data_import.isnull().sum()

#......................................DATA ANALYSIS.......................................

# Examining the variable Commodity
print("Import Commodity Count : "+str(len(data_import['Commodity'].unique())))
print("Export Commodity Count : "+str(len(data_export['Commodity'].unique())))

# Retrieving the count of Top 20 commodities being most frequently imported 
df = pd.DataFrame(data_import['Commodity'].value_counts())
df.head(20)

# Retrieving the count of Top 20 commodities being most frequently exported 
df1 = pd.DataFrame(data_export['Commodity'].value_counts())
df1.head(20)

# Listing the number of countries that does import and export trade with India 
print("No of Country were we are importing Comodities are "+str(len(data_import['country'].unique())))
print("No of Country were we are Exporting Comodities are "+str(len(data_export['country'].unique())))


# Trade Deficit-
# The amount by which the cost of a country's imports exceeds the value of its exports.

# We calculate the trade Deficit that India has incurred during the years 2010 to 2018
df3 = data_import.groupby('year').agg({'value':'sum'})

df4 = data_export.groupby('year').agg({'value':'sum'})

df3['deficit'] = df4.value - df3.value
df3


# Visualizing the Deficit through Bar-Graph to get a more lucid understanding 
trace1 = go.Bar(
                x = df3.index,
                y = df3.value,
                name = "Import",
                marker = dict(color = 'rgba(0,191,255, 1)',
                             line=dict(color='rgb(0,0,0)',width=1.5)),
                text = df3.value)

trace2 = go.Bar(
                x = df4.index,
                y = df4.value,
                name = "Export",
                marker = dict(color = 'rgba(1, 255, 130, 1)',
                              line=dict(color='rgb(0,0,0)',width=1.5)),
                text = df4.value)

trace3 = go.Bar(
                x = df3.index,
                y = df3.deficit,
                name = "Trade Deficit",
                marker = dict(color = 'rgba(220, 20, 60, 1)',
                              line=dict(color='rgb(0,0,0)',width=1.5)),
                text = df3.deficit)


data = [trace1, trace2, trace3]
layout = go.Layout(barmode = "group")
fig = go.Figure(data = data, layout = layout)
fig.update_layout(
    title=go.layout.Title(
        text="Yearwise Import/Export/Trade deficit",
        xref="paper",
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Year",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Value",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
    )
)

plot(fig)

# As observed from the above figure 
# 1) India has incurred a trade deficit every year of the considered data
# 2) 2 Basic Observations that we can make that their was a huge surge in India's Import for the years 2011 and 2012 with respect to Indian exported goods.
# 3) The imports started declining every since then till the year 2017.
# 4) It is accounted to a sluggish export growth and a remarkable deficit in non-oil, non-gold trade.


# Visualizing Import and Export based on different countries

df5 = data_import.groupby('country').agg({'value':'sum'})
df5 = df5.sort_values(by='value', ascending = False)
df5 = df5[:10]

df6 = data_export.groupby('country').agg({'value':'sum'})
df6 = df6.sort_values(by='value', ascending = False)
df6 = df6[:10]

sns.set(rc={'figure.figsize':(15,6)})
ax1 = plt.subplot(121)

sns.barplot(df5.value,df5.index).set_title('Country Wise Import')

ax2 = plt.subplot(122)
sns.barplot(df6.value,df6.index).set_title('Country Wise Export')
plt.tight_layout()
plt.show()


# Analysis of the Figures 

# Figure 1
# As seen in the first figure the 5 biggest importers in India are UAE, China Republic, USA, Saudi Arab and Switzerland.
# With China Republic having the largest market

# Figure 2
# As observed in the second pattern the countries that India exports the most goods are UAE, China Republic, USA, Hong Kong and Singapore.
# USA being the biggest importer of Indian commodities.



# A side by side comparison of the overall trend into Indian Trade
fig = go.Figure()
fig.add_trace(go.Scatter(x=df3.index, y=df3.value, name='Export',mode='lines+markers',
                         line=dict(color='firebrick', width=4)))
fig.add_trace(go.Scatter(x=df4.index, y=df4.value, name = 'Import',mode='lines+markers',
                         line=dict(color='royalblue', width=4)))
fig.update_layout(
    title=go.layout.Title(
        text="Yearwise Import/Export",
        xref="paper",
        x=0
    ),
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text="Year",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text="Value",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            )
        )
    )
)

plot(fig)

# Observations

#Right out of the bat the 2 most noticeable trends were a notable increase in the Foreign  trading back in 2010 through 2011
#and a drop in trade between the years 2014 - 2015.
#In 2016 and 2013, it shows Indian commodities that were shipped out were steady or decreasing, but the import was growing.
#Export shows a descending trend after 2011-2012 till 2016, after which the export increased again.
#Import showing an upward trend of 2010 - 2011 then till 2014 shows a sideways trend then a sharp decline in 2015 and an upward trend after that.



# Commodity Wise Imports
df3 = data_import.groupby('Commodity').agg({'value':'sum'})
df3 = df3.sort_values(by='value', ascending = False)
df3 = df3[:10]

sns.set(rc={'figure.figsize':(15,10)})
sns.barplot(df3.value,df3.index).set_title('Commodity Wise Import')
plt.show()


# Commodity Wise Exports
df4 = data_export.groupby('Commodity').agg({'value':'sum'})
df4 = df4.sort_values(by='value', ascending = False)
df4 = df4[:10]

sns.barplot(df4.value,df4.index).set_title('Commodity Wise Export')
plt.show()

# We will now examine the expensive imports
expensive_import = data_import[data_import.value>1000]
expensive_import.head(10)


# Ploting a box plot of HSCode and value w.r.t. expensive import
plt.figure(figsize=(20,9))
ax = sns.boxplot(x="HSCode", y="value", data=expensive_import).set_title('Expensive Imports HsCode distribution')
plt.show()


# Visual representation of the TreeMap between HsCode VS Expensive Imports

df =expensive_import.groupby(['HSCode']).agg({'value': 'sum'})
df = df.sort_values(by='value')
 
value=np.array(df)
commodityCode=df.index
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10.0, 6.0)
squarify.plot(sizes=value, label=commodityCode, alpha=.7 )
plt.axis('off')
plt.title("Expensive Imports HsCode Share")
plt.show()

data_import.loc[data_import['HSCode'] == 27, 'Commodity'].unique() 
data_import.loc[data_import['HSCode'] == 71, 'Commodity'].unique()
data_import.loc[data_import['HSCode'] == 85, 'Commodity'].unique()
data_import.loc[data_import['HSCode'] == 84, 'Commodity'].unique()


# This helps show some of the most expensive imports based on their HSCode that plays a major role in the trade deficit of India 
# Them being 27, 71, 85, 84 etc. that rise to the top 



# Visual representation of the TreeMap between HsCode VS Countries

df1 = expensive_import.groupby(['country']).agg({'value': 'sum'})
df1 = df1.sort_values(by='value')
value=np.array(df1)
country=df1.index
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (10.0, 10.0)
squarify.plot(sizes=value, label=country, alpha=.7 )
plt.title("Expensive Imports Countrywise Share")
plt.axis('off')
plt.show()

# This exhibits the major players from which India imports from
