# DSC510
# Week 12
# Programming Assignment Week 12
# Author: Adam McMahan
# 11/17/2024
# Program is designed to pull user inputs on location to populate weather information in area.

import requests

# read file to protect API key)
api_key = open('apikey.txt', 'r').read()

# gets lat and long coordinates.
# international post codes require country (KT3,GB)
# unable to figure out how to use the geo/1.0/direct for pulling lat/lon for city entry. Error could not be str.
# created second if in zip to use geo/1.0/zip
def get_coords(location, zip=False):
    try:
        if zip:
            url = f"http://api.openweathermap.org/geo/1.0/zip?zip={location}&appid={api_key}"

            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if response.status_code == 200:
                lat = data['lat']
                lon = data['lon']
                return lat, lon
        else:
            city, state = location.split(',')
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{state}&appid={api_key}"

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200:
            lat = data['coord']['lat']
            lon = data['coord']['lon']
            return lat, lon

        else:
            print("Invalid location data. Please try again.")

    except requests.exceptions.RequestException as e:
        print(f"There was an error fetching your request: {e}")
        return None


#Gets data by lat and long as assignment request
def get_data(lat, lon):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if response.status_code == 200:
            return data
        else:
            print("Invalid location data. Please try again..")
            return None

    except requests.exceptions.RequestException as e:
        print(f"There was an error fetching your request: {e}")
        return None


# converts temps
def convert_temperature(kelvin, scale='C'):
    if scale == 'C':
        return kelvin - 273.15
    elif scale == 'F':
        return (kelvin - 273.15) * 9 / 5 + 32
    else:
        return kelvin


# formats
def format_weather(data, scale='F'):
    city = data['name']
    country = data['sys']['country']
    weather = data['weather'][0]['description']
    main = data['main']

    temp = convert_temperature(main['temp'], scale)
    feels_like = convert_temperature(main['feels_like'], scale)
    temp_min = convert_temperature(main['temp_min'], scale)
    temp_max = convert_temperature(main['temp_max'], scale)

    print('-' * 40)
    print(f"Hear is your weather information for {city}, {country}:")
    print('-' * 40)
    print(f"Weather: {weather.capitalize()}")
    print(f"Current Temperature: {temp:.2f}°{scale}")
    print(f"Feels Like: {feels_like:.2f}°{scale}")
    print(f"Today's Low: {temp_min:.2f}°{scale}")
    print(f"Today's High: {temp_max:.2f}°{scale}")
    print(f"Pressure: {main['pressure']} hPa")
    print(f"Humidity: {main['humidity']}%")
    print('-' * 40)

# collects user request
# is there a way post codes could be used
def user_input():
    while True:
        print("Please indicate if you are searching by \n"
              "Zip Code or by City:")
        print("1. Zip Code")
        print("2. City")
        choice = input("Enter 1 or 2: \n")

        if choice == '1':
            location = input("Enter the zip code: \n"
                             "For international ex: KTE,GB (no space after comma)\n")
            return location, True

        elif choice == '2':
            location = input("Enter the the name of city. If searching within the USA \n"
                             "please enter a State as well (ex: New York City, New York or London, England) \n")
            return location, False

        else:
            print("Invalid input. Please enter 1 or 2.")

# runs program
def main():
    print("Welcome to your personal weather application!")

    while True:
        location, is_zip = user_input()

        lat_lon = get_coords(location, is_zip)

        if lat_lon:
            lat, lon = lat_lon

            weather_data = get_data(lat, lon)

            if weather_data:
                scale = input("Choose temperature unit (C for Celsius, F for Fahrenheit, K for Kelvin): \n")
                if scale not in ['C', 'F', 'K']:
                    print("Invalid unit. Please try again: \n")

                format_weather(weather_data, scale)

            else:
                print("We're sorry. We are unable to retrieve your request."
                      "Please check your entry and try again.")

        try_again = input("Is there another city you would like to lookup? (y/n): \n").lower()
        if try_again not in ['yes', 'y']:
            print("Thank you, and goodbye.")
            quit()


if __name__ == "__main__":
    main()  # Call the renamed function