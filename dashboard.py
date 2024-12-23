import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_season_df(df):
    # Create a new dataframe with season information
    season_df = df.groupby(by="season").agg({
        "instant": "nunique",
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    return season_df

def create_workingday_df(df):
    # Create a new dataframe with working day information
    workingday_df = df.groupby(by='workingday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    }).reset_index()
    return workingday_df

def create_cnt_df(df):
    # Create a DataFrame with total 'casual' and 'registered'
    total_casual = df['casual'].sum()
    total_registered = df['registered'].sum()

    cnt_df = pd.DataFrame({
        'User Type': ['Casual', 'Registered'],
        'Total Rentals': [total_casual, total_registered]
    })
    return cnt_df

def plot_pie_chart(data, labels, colors):
    plt.figure(figsize=(8, 8))
    plt.pie(data, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.title('Perbandingan Jumlah Casual dan Registered Users')
    plt.axis('equal')  # Membuat lingkaran sempurna
    st.pyplot()

all_df = pd.read_csv("main_data.csv")

datetime_columns = ["dteday"]
all_df.sort_values(by="dteday", inplace=True)
all_df.reset_index(drop=True, inplace=True)

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    st.image("logo.png")

    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= pd.Timestamp(start_date)) & 
                 (all_df["dteday"] <= pd.Timestamp(end_date))]

season_df = create_season_df(main_df)
workingday_df = create_workingday_df(main_df)
cnt_df = create_cnt_df(main_df)

st.header('Bike Sharing Data Analysis :sparkles:')
st.subheader('Number of Sharing Bike by Season')

col1, col2 = st.columns(2)

with col1:
    st.bar_chart(season_df["cnt"])

with col2:
    st.write(season_df["cnt"].sum())

fig, ax = plt.subplots(figsize=(16, 8))
colors = ['skyblue' if season !='Fall' else 'red' for season in season_df['season']]
ax.set_title('Number of Sharing Bike by Season')
ax.set_xlabel('Season')
ax.set_ylabel('Number of Sharing Bike')
st.pyplot(fig)

st.subheader('Percentage of Number of Bikes Rented Based on Working Day')
col1 = st.columns(1)[0]
with col1:
    fig, ax = plt.subplots(figsize=(16, 8))
    sns.barplot(
        x="workingday",
        y="cnt",
        data=workingday_df.sort_values(by="cnt", ascending=False),
        palette="viridis",
        ax=ax 
    )
    ax.set_title('Number of Sharing Bike by Working Day', loc="center", fontsize=20)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    st.pyplot(fig)

st.subheader('Comparison of Casual and Registered Users')
# Data untuk pie chart
labels = ['Casual', 'Registered']
sizes = cnt_df['Total Rentals']
colors = ['skyblue', 'lightcoral']
plot_pie_chart(sizes, labels, colors)
 
st.caption('Copyright (c) Dicoding 2023')
