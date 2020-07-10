import time
import pandas as pd
import numpy as np

#This is the givin data
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#We only have the data of the first six months of the year
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        global city
        city = input('Would you like to see data for Chicago, New York City, Washington?\n').lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("It's not an appropriate choice")
        else:
            break
    # get user input for month (all, january, february, ... , june)
    while True:
        global month
        month = input('Which month would you like to filter the data? All, January, February, ... , June?\n').lower()
        if month not in months and month != 'all':
            print("It's not an appropriate choice")
        else:
            break
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        global day
        day = input('Which day would you like to filter the data? All, Monday, Tuesday, ... , Sunday?\n').lower()
        if day not in days and day != 'all':
            print("It's not an appropriate choice")
        else:
            break

    print('-'*40)
    return city, month, day


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
    global df
    df = pd.read_csv(CITY_DATA[city])

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # display the most common month
    global month
    if month == 'all':
        popular_month = df['month'].mode()[0]
        print('Most Poplar Month:', popular_month)
    else:
        month = months.index(month) + 1
        df = df[df['month'] == month]
        print('Filtered Month:', month)
    # display the most common day of week
    global day
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('Most Popular Day:', popular_day)
    else:
        df = df[df['day_of_week'] == day.title()]
        print('Filtered Day:', day.title())
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    # display most commonly used start station
    most_used_start_station = df['Start Station'].mode()[0]
    print('Most Used Start Station:', most_used_start_station)
    # display most commonly used end station
    most_used_end_station = df['End Station'].mode()[0]
    print('Most Used End Station', most_used_end_station)
    # display most frequent combination of start station and end station trip
    most_combinations_stations = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).index[0]
    most_combination_start_end_stations = '/ '.join(most_combinations_stations)
    print('Most Frequent Combination of Start Station and End Station:', most_combination_start_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum() / (60*60)
    print('Total Travel Time in hours:', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean() / 60
    print('Mean Travel Time in minutes:', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    # Display counts of gender
    if city.lower() == 'chicago' or city.lower() == 'new york city':
        gender = df['Gender'].value_counts()
        print(gender)
    # Display earliest, most recent, and most common year of birth
    if city.lower() == 'chicago' or city.lower() == 'new york city':
        earliest_year_birth = df['Birth Year'].min()
        print('Earliest Year of Birth:', earliest_year_birth)
        most_recent_birth = df['Birth Year'].max()
        print('Most Recent Year of Birth:', most_recent_birth)
        most_common_birth = df['Birth Year'].mode()[0]
        print('Most Common Year of Bith:', most_common_birth)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        count = 0
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        while True:
            if raw_data.lower() == 'yes':
                count += 1
                print(df.head(5*count))
                raw_data = input('\nWould you like to see another 5 lines of raw data? Enter yes or no.\n')
            else:
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
