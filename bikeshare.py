import time
import pandas as pd
import numpy as np

CITY_DATA = {'Chicago': 'chicago.csv',
             'New York city': 'new_york_city.csv',
             'Washington': 'washington.csv'}


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
        cities = ['Chicago', 'New York City', 'Washington']
        city = input(
            "\nWhich city would you like to analyse? (Chicago, New york city, Washington) \n").capitalize()
        if city in cities:
            print("\n{} is your choice".format(city))
            print('-'*30)
            break
        else:
            print("\nPlease enter a valid city name")

    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'None']
        month = input(
            "\nWhich month would you like to filter by? (Jan, Feb, Mar, Apr, May, Jun)? Type 'None' for no month filter\n").capitalize().title()
        if month in months:
            print("\nYou considered {}".format(month))
            print('-'*30)
            break
        else:
            print("\nPlease enter a valid month")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun', 'None']
        day = input(
            "\nWhich day of the week would you like to filter by? (Mon, Tues, Wed, Thur, Fri, Sat, Sun)? Type 'None' for no day filter \n").capitalize().title()
        if day in days:
            print("\nYou considered {}".format(day))
            break
        else:
            print("\nPlease enter a valid day")

    print('-'*50)
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

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.strftime("%a")
    if month != 'None':
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        month = months.index(month)+1
        df = df[df['month'] == month]

    if day != 'None':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\n\nCalculating the most frequent times of travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'None':
        pop_month = df['month'].mode()[0]
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        pop_month = months[pop_month-1]
        print("The most popular month is", pop_month)

    # display the most common day of week
    if day == 'None':
        pop_day = df['day_of_week'].mode()[0]
        print("The most popular day is", pop_day)

    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    pop_hour = df['Start Hour'].mode()[0]
    print("The popular start hour is {}:00 hrs".format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating the most popular stations and trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    print("The most commonly used start station is {}".format(pop_start_station))

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    print("The most commonly used end station is {}".format(pop_end_station))

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station']+" "+"to"+" " + df['End Station']
    pop_com = df['combination'].mode()[0]
    print("The most frequent combination of start and end station is {} ".format(pop_com))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating trip duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()
    minute, second = divmod(total_duration, 60)
    hour, minute = divmod(minute, 60)
    print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(
        hour, minute, second))

    # display mean travel time
    average_duration = round(df['Trip Duration'].mean())
    m, sec = divmod(average_duration, 60)
    if m > 60:
        h, m = divmod(m, 60)
        print("The total trip duration: {} hour(s) {} minute(s) {} second(s)".format(
            h, m, sec))
    else:
        print("The total trip duration: {} minute(s) {} second(s)".format(m, sec))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_counts = df['User Type'].value_counts()
    print("The user types are:\n", user_counts)

    # Display counts of gender
    if city.title() == 'Chicago' or city.title() == 'New York City':
        gender_counts = df['Gender'].value_counts()
        print("\nThe counts of each gender are:\n", gender_counts)

    # Display earliest, most recent, and most common year of birth
        earliest = int(df['Birth Year'].min())
        print("\nThe oldest user was born in the year", earliest)
        most_recent = int(df['Birth Year'].max())
        print("The youngest user was born in  the year", most_recent)
        common = int(df['Birth Year'].mode()[0])
        print("Most users were born in the year", common)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def display_data(df):

    while True:
        response = ['yes', 'no']
        view_individual_trip_data = input(
            "\nWould you like to view individual trip data (5 entries)? Type 'yes' or 'no'\n").lower()
        if view_individual_trip_data in response:
            if view_individual_trip_data == 'yes':
                start = 0
                end = 5
                data = df.iloc[start:end, :9]
                print(data)
            break
        else:
            print("Please enter a valid response")
    if view_individual_trip_data == 'yes':
         while True:
            choice_2 = input(
                "Would you like to view more trip data? Type 'yes' or 'no'\n").lower()
            if choice_2 in response:
                if choice_2 == 'yes':
                    start += 5
                    end += 5
                    data = df.iloc[start:end, :9]
                    print(data)
                else:
                    break
            else:
                print("Please enter a valid response")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\n\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
