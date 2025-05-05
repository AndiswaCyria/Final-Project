#Importing the libraries

import pandas as pd

#Loading the dataset 

df = pd.read_csv('owid-covid-data.csv')

# Checking the first 5 rows to see if the data is loaded correctly 

print(df.head())

# Checking column names 
print(df.columns)

# Checking for missing values 
print(df.isnull().sum())

# Checking data types 
print(df.dtypes)

## Cleaning the data!

countries = ['South Africa', 'Kenya', 'Nigeria', 'Egypt', 'Morocco','Russia', 'China', 'India']

#Filtering the dataset
df_countries = df[df['location'].isin(countries)].copy()

#Conversion of date column to datetime
df_countries['date'] = pd.to_datetime(df_countries['date'])

# Fill missing values in key columns
numeric_cols = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations']
df_countries[numeric_cols] = df_countries[numeric_cols].fillna(0)

#Quick check of the cleaned data 
print(df_countries['location'].unique())
print(df_countries.head())


## Exploratory Data Analysis (EDA)

import matplotlib.pyplot as plt
import seaborn as sns

# Setting the style 
sns.set(style='whitegrid')

# Plotting total cases over time for each country
plt.figure(figsize=(14,7))

for country in df_countries['location'].unique():
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['total_cases'], label=country)
    
plt.title('Total COVID-19 Cases Over Time', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Total Cases')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()


## Plotting total deaths over time 

plt.figure(figsize=(14,7))

for country in df_countries ['location'].unique():
    subset = df_countries[df_countries['location'] == country] 
    plt.plot(subset['date'], subset ['total_deaths'], label=country) 
    
    
plt.title('Total COVID-19 Deaths Over Time', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Total Deaths') 
plt.legend(loc='center left', bbox_to_anchor=(1,0.5))
plt.tight_layout()
plt.show()

## Plotting new cases over time

plt.figure(figsize=(14,7))

for country in df_countries['location'].unique():
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['new_cases'], label=country)
    
plt.title('Daily New Covid-19 Cases')
plt.xlabel('Date')
plt.ylabel('New Cases')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()

## Plotting Deaths over time 

#Calculating the death rate
df_countries['death_rate'] = df_countries['total_deaths'] / df_countries['total_cases']
df_countries['death_rate'] = df_countries ['death_rate'].fillna(0)

plt.figure(figsize=(14,7))

for country in df_countries['location'].unique():
    subset = df_countries [df_countries['location'] == country]
    plt.plot(subset['date'], subset['death_rate'], label=country)
    
    
plt.title('COVID-19 Death Rate Over Time', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Death Rate (Total Deaths / Total Cases)')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()


##Visualizing Vaccination Progress

#This shows how total vaccindations have grown over time:
plt.figure(figsize=(14,7))

for country in df_countries['location'].unique():
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['total_vaccinations'], label=country, linewidth=2)
    
plt.title('Cumulative COVID-19 Vaccinations Over Time', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Total Vaccinations')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()

# Plotting people fully vaccinated (%  of Population)
plt.figure(figsize=(14,7))

for country in df_countries['location'].unique():
    subset = df_countries[df_countries['location'] == country]
    plt.plot(subset['date'], subset['people_fully_vaccinated_per_hundred'], label=country, marker='o', linewidth=1)
    
plt.title('People Fully Vaccinated (% of Population)', fontsize=16)
plt.xlabel('Date')
plt.ylabel('% Fully Vaccinated')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.tight_layout()
plt.show()

# Fix: Define `df_africa` by filtering African countries
african_countries = ['South Africa', 'Kenya', 'Nigeria', 'Egypt', 'Morocco']
df_africa = df[df['continent'] == 'Africa']
# Fix: Retrieve the latest data for each African country
latest_vax = df_africa.sort_values('date').groupby('location').tail(1)

if latest_vax.empty:
    print("No data found for African countries' latest vaccinations.")
else:
    print(latest_vax[['location', 'iso_code', 'people_fully_vaccinated_per_hundred']])

print(latest_vax[['location', 'iso_code']])



# Show the key data for African countries
import plotly.express as px

latest_vax = (
    df_africa[df_africa['people_fully_vaccinated_per_hundred'].notnull()]
    .sort_values('date')
    .groupby('location')
    .tail(1)
)

print(latest_vax[['location', 'iso_code', 'people_fully_vaccinated_per_hundred']])

fig = px.choropleth(
    latest_vax,
    locations='iso_code',
    color='people_fully_vaccinated_per_hundred',
    hover_name='location',
    color_continuous_scale='YlGnBu',
    title='COVID-19: Fully Vaccinated People per 100 Population (World)',  # Fixed typo
    scope='world',
    color_continuous_midpoint=50 
)

fig.update_layout(margin={'r': 0, 't': 40, 'l': 0, 'b': 0})
fig.show()







print(latest_vax[['location', 'people_fully_vaccinated_per_hundred', 'date']])


