#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time


# In[ ]:


import pandas as pd
import numpy as np


# In[ ]:


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York City': 'new_york_city.csv',
              'Washington': 'washington.csv' }


# In[ ]:


def get_filters():

    """
       Asks user to specify a city, month, and day to analyze.

       Returns:
           (str) city - name of the city to analyze
           (str) month - name of the month to filter by, or "all" to apply no month filter
           (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    print("Let's get started....")

    city_name = input('Please enter the name of the city you want to explore\n').title()
    
    while city_name not in CITY_DATA:
        try:
            print('The list of available options are: {}'.format(list(CITY_DATA.keys())))
            city_name = input('Oops!...Please enter a city name from the list above\n').title()
        except:
            print('\nTry Again Please')
            
    city = CITY_DATA[city_name]
    
    months = ['All', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    print("\nIf you wish to not filter by month, enter 'All'")
    month = input('Please enter the month of interest\n').title()
    
    while month not in months:
        try:
            print('The list of available options are: {}'.format(months))
            month = input('Oops!...Please enter a valid month from the list above\n').title()
        except:
            print('\nTry Again Please')

    print("\nIf you wish to not filter by day, enter 'All'")
    day = input('Please enter the day of interest\n').title()
    week_day = ['All', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    while day not in week_day:
        try:
            print('The list of available options are: {}'.format(week_day))
            day = input('Oops!...Please enter a valid day from the list above\n').title()
        except:
            print('\nInvalid...Please try again')
            
    print('-' * 40)
    return city, month, day


# In[ ]:


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    city_data = pd.read_csv(city)
    df = pd.DataFrame(city_data).dropna()

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Start Month'] = df['Start Time'].dt.month_name()
    df['Start Day'] = df['Start Time'].dt.day_name()
    df['End Month'] = df['End Time'].dt.month_name()
    df['End Day'] = df['End Time'].dt.day_name()

    if month != 'All' and day != 'All':
        df = df[df['Start Month'] == month]
        df = df[df['End Month'] == month]
        df = df[df['Start Day'] == day]
        df = df[df['End Day'] == day]
    elif month != 'All':
        df = df[df['Start Month'] == month]
        df = df[df['End Month'] == month]
    elif day != 'All':
        df = df[df['Start Day'] == day]
        df = df[df['End Day'] == day]
    
    return df


# In[ ]:


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print('\nThe most common month is: {}'.format(df['Start Month'].mode()[0]))
    print('\nThe most common day of week is: {}'.format(df['Start Day'].mode()[0]))

    start_hour = pd.to_datetime(df['Start Time']).dt.hour
    most_start_hour = start_hour.mode()[0]
    print('\nThe most common start hour is: {}'.format(most_start_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print('\nThe most commonly used start station is: {}'.format(df['Start Station'].mode()[0]))
    print('\nThe most commonly used end station is: {}'.format(df['End Station'].mode()[0]))

    start_and_end_station = df['Start Station'] + ' - ' + df['End Station']
    print('\nThe most frequent combination of start station and end station is: {}'.format(start_and_end_station.mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    time_sum = df['Trip Duration'].sum()
    mean_time = df['Trip Duration'].mean()
    
    print('\nThe total time travel in years: {} Years \nThe total travel time in days is: {} Days \nThe total travel time in hours is: {} Hours'.format(time_sum//31536000, time_sum//86400, time_sum//3600))
    print('\nThe mean travel time is: {} Minutes:{} Seconds'.format(int(mean_time//60), int(mean_time%60)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


# In[ ]:


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    print('\nThe number of different User_Types are: ')
    print(df.groupby(['User Type']).size())
    
    #To check if Gender and Year of Birth data is provided
    try:
        print('\nCount of gender: ')
        print(df.groupby(['Gender']).size())
        print('\nThe earliest year of birth is: {} \nThe most recent year of birth is: {} \nThe most common year of birth is: {} '.format(int(df['Birth Year'].min()), int(df['Birth Year'].max()), int(df['Birth Year'].mode()[0])))
    except:
        print('\nNo available Gender and Year of Birth Data')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


# In[ ]:


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        #To check if empty dataframe is returned
        if df.empty is False: 
            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
        else:
            print('\nNo available data')

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
    
    #To display raw data upon user request
    city_data = pd.read_csv(city)
    df = pd.DataFrame(city_data).dropna()       
    i = 0
    user_input = input('\nWould you like to see the raw data? Enter yes or no.\n')
    
    while user_input == 'yes':
        print(df[i:i + 5])
        if i < len(df):
            i +=5
        user_input = input('\nWould you like to see more? Enter yes or no.\n')
    print('-'*40)


# In[ ]:


if __name__ == "__main__":
	main()


# In[ ]:




