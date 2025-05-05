#This is for my dashboard

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Setting up the page
st.set_page_config(page_title='COVID-19 Dashboard', layout='wide')

st.title('🌍 COVID-19 Dashboard')
st.markdown("""
This dashboard provides insights into COVID-19 cases, deaths, and vaccination trends across key countries.
""")

# Uploading the data
@st.cache_data
def load_data():
    cols_to_use = [
        'iso_code', 'continent', 'location','date',
        'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
        'total_vaccinations', 'people_fully_vaccinated_per_hundred'
    ]
    df = pd.read_csv('owid-covid-data.csv', usecols=cols_to_use)
    return df

df = load_data()



# Selecting countries
countries = ['South Africa', 'Kenya', 'Nigeria', 'Egypt', 'Morocco', 'Russia', 'China', 'India']
df_countries = df[df['location'].isin(countries)].copy()

# Cleaning and processing data
df_countries['date'] = pd.to_datetime(df_countries['date'])
numeric_cols = ['total_cases', 'new_cases', 'total_deaths', 'new_deaths', 'total_vaccinations']
df_countries[numeric_cols] = df_countries[numeric_cols].fillna(0)

# Sidebar filters
st.sidebar.header('Filters')
selected_country = st.sidebar.selectbox('Select a country:', countries)
selected_metric = st.sidebar.radio(
    'Select metric to view:',
    ('Total Cases', 'Total Deaths', 'New Cases', 'Death Rate', 'Vaccinations')
)

# Subset data for selected country
subset = df_countries[df_countries['location'] == selected_country]

# Show last update
st.sidebar.write(f"Latest data date: {subset['date'].max().date()}")

# Display plots based on selection
st.subheader(f'{selected_metric} in {selected_country}')

if selected_metric == 'Total Cases':
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=subset, x='date', y='total_cases', ax=ax)
    ax.set_ylabel('Total Cases')
    st.pyplot(fig)

elif selected_metric == 'Total Deaths':
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=subset, x='date', y='total_deaths', ax=ax, color='red')
    ax.set_ylabel('Total Deaths')
    st.pyplot(fig)

elif selected_metric == 'New Cases':
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=subset, x='date', y='new_cases', ax=ax, color='orange')
    ax.set_ylabel('New Cases')
    st.pyplot(fig)

elif selected_metric == 'Death Rate':
    df_countries['death_rate'] = df_countries['total_deaths'] / df_countries['total_cases']
    subset['death_rate'] = subset['total_deaths'] / subset['total_cases']
    subset['death_rate'] = subset['death_rate'].fillna(0)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=subset, x='date', y='death_rate', ax=ax, color='purple')
    ax.set_ylabel('Death Rate')
    st.pyplot(fig)

elif selected_metric == 'Vaccinations':
    fig = px.line(
        subset,
        x='date',
        y='total_vaccinations',
        title=f'Cumulative Vaccinations in {selected_country}',
        labels={'total_vaccinations': 'Total Vaccinations'}
    )
    st.plotly_chart(fig, use_container_width=True)

# For the interactive map (for Africa)
st.subheader('Vaccination Coverage in Africa')

african_countries = ['South Africa', 'Kenya', 'Nigeria', 'Egypt', 'Morocco']
df_africa = df[df['continent'] == 'Africa']

latest_vax = (
    df_africa
    .sort_values('date')
    .dropna(subset=['people_fully_vaccinated_per_hundred'])
    .groupby('location')
    .tail(1)
)

fig = px.choropleth(
    latest_vax,
    locations='iso_code',
    color='people_fully_vaccinated_per_hundred',
    hover_name='location',
    color_continuous_scale='YlGnBu',
    title='Fully Vaccinated People per 100 Population (Africa)',
    scope='africa',
    color_continuous_midpoint=50
)
fig.update_layout(margin={'r': 0, 't': 40, 'l': 0, 'b': 0})
st.plotly_chart(fig, use_container_width=True)

st.sidebar.title("Filter Options")

country_options = df_countries['location'].unique()
selected_countries = st.sidebar.multiselect(
    'Select Countries:',
    options=country_options,
    default=['South Africa', 'Kenya']
)

date_range = st.sidebar.date_input(
    'Select Date Range:',
    [df_countries['date'].min(), df_countries['date'].max()]
)

total_cases = df_countries[df_countries['location'].isin(selected_countries)]['total_cases'].sum()
total_deaths = df_countries[df_countries['location'].isin(selected_countries)]['total_deaths'].sum()
total_vax = df_countries[df_countries['location'].isin(selected_countries)]['total_vaccinations'].sum()

col1, col2, col3 = st.columns(3)

col1.metric("Total Cases", f"{total_cases:,.0f}")
col2.metric("Total Deaths", f"{total_deaths:,.0f}")
col3.metric("Total Vaccinations", f"{total_vax:,.0f}")

import plotly.express as px

# Filter the data based on user selections
filtered_data = df_countries[
    (df_countries['location'].isin(selected_countries)) &
    (df_countries['date'] >= pd.to_datetime(date_range[0])) &
    (df_countries['date'] <= pd.to_datetime(date_range[1]))
]

fig_cases = px.line(
    filtered_data,
    x='date',
    y='total_cases',
    color='location',
    title='Total COVID-19 Cases Over Time'
)
st.plotly_chart(fig_cases, use_container_width=True)
# Add a download button to export the filtered data
st.subheader('Download Data')
csv = df_countries.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='covid_data_filtered.csv',
    mime='text/csv',
)
