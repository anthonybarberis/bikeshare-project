import time
import pandas as pd

CITY_DATA = { 'chicago': 'data/chicago.csv',
              'new york': 'data/new_york_city.csv',
              'washington': 'data/washington.csv' }

MONTH_NAMES = ['january', 'february', 'march', 'april', 'may', 'june']
DAY_NAMES = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

def get_filters():
   
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # get the city filter from the user and check it against CITY_DATA dictionary
    city = input('Let\'s start by choosing a city (Chicago, New York, or Washington):').lower()
    while city not in CITY_DATA:
        city = input('Please input a valid city (Chicago, New York, or Washington):').lower()
    
    print('\nNext, let\'s choose our calendar filter.')
    
    #get the month filter from the users and check it against the MONTH_NAMES list
    month = input('Which month do you want to report on? (January to June, or ENTER for any):').lower() or 'any'
    while month not in MONTH_NAMES and month != 'any':
        month = input('Please input a valid month? (or ENTER for any):').lower() or 'any'
    
    #get the weekday filter from the users and check if against the DAY_NAMES list
    day = input('Which day of the week do you want to report on? (or ENTER for any):').lower() or 'any'
    while day not in DAY_NAMES and day != 'any':
        day = input('Please input a valid weekday? (or ENTER for any):').lower() or 'any'
        
    return city, month, day

def load_data(city, month, day):

    start_time = time.time()
    print('\nGreat! Loading data with these filters:\nCity: {}\nMonth: {}\nWeekday: {}'.format(city.title(), month.title(), day.title()))
    
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'any':
        month = MONTH_NAMES.index(month)+1
        df = df.loc[df['month'] == month]
    
    # filter by day of week if applicable
    if day != 'any':
        day = DAY_NAMES.index(day)
        df = df.loc[df['day_of_week'] == day]
    
    print("\nThis took %s seconds to load." % (time.time() - start_time))
    print('-'*40)
    
    return df

def section_intro(intro_line):
    # build the intro line based on the user's filter selections
    intro = '\nIn {}'.format(city.title())
    if month != 'any':
        intro += ', in {}'.format(month.title())
    if day != 'any':
        intro += ', on {}s'.format(day.title())
    intro += ', {}...'.format(intro_line)
    input('{} (press ENTER to continue)'.format(intro))

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    # call the section_intro function
    section_intro('people most frequently travel')
    
    start_time = time.time()
      
    # display the most common month if a month filter was not chosen
    if month == 'any':
        month_num = df['month'].mode()[0]
        monthly_trips = df['month'].value_counts()[month_num]
        print('In {} (Month {}) ({} trips)'.format(MONTH_NAMES[month_num-1].title(),month_num,monthly_trips))

    # display the most common day of week if a weekday filter was not chosen
    if day == 'any':
        day_num = df['day_of_week'].mode()[0]
        daily_trips = df['day_of_week'].value_counts()[day_num]
        print('On {} (Day {}) ({} trips)'.format(DAY_NAMES[day_num-1].title(),day_num,daily_trips))
        
    # display the most common start hour
    hour = df['hour'].mode()[0]
    hourly_trips = df['hour'].value_counts()[hour]
    print('Between {}:00:00 and {}:59:59 ({} trips)'.format(hour,hour,hourly_trips))

    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    
    # call the section_intro function
    section_intro('the most popular stations are')
    
    start_time = time.time()
    
    # create trip column from start and end stations
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    
    # display most commonly used start station
    top_start = df['Start Station'].mode()[0]
    start_trips = df['Start Station'].value_counts()[top_start]
    print('Starting: {} ({} trips)'.format(top_start,start_trips))

    # display most commonly used end station
    top_end = df['End Station'].mode()[0]
    end_trips = df['End Station'].value_counts()[top_end]
    print('Ending: {} ({} trips)'.format(top_end,end_trips))

    # display most frequent combination of start station and end station trip
    top_trip = df['trip'].mode()[0]
    full_trips = df['trip'].value_counts()[top_trip]
    print('Full trip: {} ({} trips)'.format(top_trip,full_trips))


    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    # call the section_intro function
    section_intro('time travelled is')
    
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    days = int(total_time // 86400)
    hours = int(total_time % 86400 // 3600)
    minutes = int(total_time % 3600 // 60)
    seconds = int(total_time % 60)
    print('Total: {} days, {} hours, {} mintues, {} seconds ({} seconds)'.format(days,hours,minutes,seconds,total_time))

    # display mean travel time
    avg_time = df['Trip Duration'].mean()
    minutes = int(avg_time // 60)
    seconds = round(avg_time % 60,3)
    print('Average per trip: {} mintues, {} seconds ({} seconds)'.format(minutes,seconds,round(avg_time,3)))


    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""


    # call the section_intro function
    section_intro('user demographics are')
    
    start_time = time.time()
    
    # Display counts of user types    
    print('\nUser types:')
    for i in range(len(df['User Type'].value_counts())):
        user_type = df['User Type'].value_counts().index.values[i]
        type_count = df['User Type'].value_counts()[i]
        type_percent = round((df['User Type'].value_counts()[i] / df['User Type'].value_counts().sum()) * 100, 3)
        print('{} {}s ({}%)'.format(type_count,user_type,type_percent))

    # Display counts of gender
    if 'Gender' in df.columns:
        print('\nGenders:')
        for i in range(len(df['Gender'].value_counts())):
            gender_type = df['Gender'].value_counts().index.values[i]
            gender_count = df['Gender'].value_counts()[i]
            gender_percent = round((df['Gender'].value_counts()[i] / df['Gender'].value_counts().sum()) * 100, 3)
            print('{} {}s ({}%)'.format(gender_count,gender_type,gender_percent))
    else:
        print('\nNo gender data available for {}'.format(city.title()))

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nBirth Years:')
        print('Earliest: {}'.format(int(df['Birth Year'].describe()['min'])))
        print('Most recent: {}'.format(int(df['Birth Year'].describe()['max'])))
        print('Most common: {}'.format(int(df['Birth Year'].mode())))
    else:
        print('\nNo birth year data available for {}'.format(city.title()))


    print("\nThis took %s seconds to calculate." % (time.time() - start_time))
    print('-'*40)

def show_raw_data(response):
    # show raw data five lines at a time, if the users wants it
    df.drop(['month','day_of_week','hour','trip'], axis=1, inplace=True)
    startline = 0
    while response in {'yes', 'y'}:
        print(df.iloc[startline:startline+5].to_json(orient='records', lines=True))
        response = input('\nWould you like to view five more records? (y/n)')
        startline += 5

while True:
    city, month, day = get_filters()
    df = load_data(city, month, day)

    time_stats(df)
    station_stats(df)
    trip_duration_stats(df)
    user_stats(df)
    show_raw_data(input('\nWould you like to view the raw data? (y/n)'))

    restart = input('\nWould you like to start again? (y/n)\n')
    if restart.lower() not in {'yes', 'y'}:
        print('See ya!')
        break