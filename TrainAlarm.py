import requests, jdatetime, time, os

##### defs #####
################

# def for posting info
def PostInfo(date, destination, origin, passengers):
    api = 'https://ws.alibaba.ir/api/v2/train/available'  # api for post request
    payload = {
        "departureDate": f"{date}",
        "destination": f"{destination}",
        "isExclusiveCompartment": 'false',
        "origin": f"{origin}",
        "passengerCount": f'{passengers}',
        "ticketType": "Family", }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.9,fa;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'content-type': 'application/json',
        'Content-Length': '137',
        'ab-channel': 'WEB-NEW,PRODUCTION,CSR,www.alibaba.ir',
        'Origin': 'https://www.alibaba.ir',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'Referer': 'https://www.alibaba.ir/',
        'Connection': 'keep-alive'}
    try:
        res = requests.post(api, json=payload, headers=headers, timeout=10)
        if res.status_code == 500:
            print('Server problem')
            return None
        elif res.status_code != 200:
            print('Internet problems or Bad request!')
            return None
        req_id = res.json()['result']['requestId']
        time.sleep(1)
        return req_id
    except:
        print('POST connection lost')

# def for get information
def GetInfo(id):
    api = f'https://ws.alibaba.ir/api/v1/train/available/{id}' # api for get request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        'accept': 'application/json',
        'ab-channel': 'WEB-NEW,PRODUCTION,CSR,www.alibaba.ir',
        'Referer': 'https://www.alibaba.ir/', }
    try:
        res = requests.get(api, headers=headers, timeout=10)
        if res.status_code == 500:
            print('Server problem!')
            return None
        elif res.status_code != 200:
            print('Internet problems or Bad request!')
            return None 
        return res.json()
    except:
        print('GET conneection lost')

# def input date
def InputDate(month):
    while True:
        try:
            input_value = int(input(f'{month}: '))
            while month == 'Month':
                if input_value in range(1, 13):
                    return input_value
                else:
                    break
            while month == 'Day':
                if input_value in range(1, 31):
                    return input_value
                else:
                    break
            print('Not in range..try again..')
        except:
            print('enter right number')

# def for select and return the city tag
def CityName(some_str,city_dict):
    while True:
        try:
            input_name = input(f'{some_str}')
            city_tag = city_dict[f'{input_name.lower()}']
            return city_tag
        except:
            print('Wrong input!')

#def for printing city names
def PrintCityName(city_dict):
    print('city:', end=' ')
    for city in list(city_dict.keys()):
        print(city, end=', ')

# def for Passenger input
def PassengerNum():
    while True:
        try:
            num = int(input('Number of passengers: '))
            return num
        except:
            print('Wrong input!')

################
##### main #####
################
city_dictionary ={'tehran':'THR', 'kerman':'KER', 'mashhad':'MHD', 'shiraz':'SYZ',
                'esfehan':'IFN', 'zahedan':'ZAH', 'bandar-abas':'BND', 'yazd':'AZD',
                } 

day = InputDate('Day')
month = InputDate('Month')
PrintCityName(city_dictionary)      # print ciy names
origin = CityName('\nFrom:', city_dictionary)
destination = CityName('To:', city_dictionary)
passengers = PassengerNum()
gregorian_date = jdatetime.date(1400, month, day).togregorian()     # convert jalili date to gregorian date

print('\nWait for availble seat...')
stop, i = False, 1
while stop == False:        # Loop for finding available seat and alarm
    try:
        req_id = PostInfo(gregorian_date, destination.upper(), origin.upper(), passengers)   # get requestId
        if req_id != None:
            all_info = GetInfo(req_id)      # get info with requestId from Alibaba
            if all_info['result']['departing'] != []:      # list of availble train
                i = 1       
                for seat in range(len(all_info['result']['departing'])):    #loop for finding availble seats
                    availble_seat = all_info['result']['departing'][seat]['seat']
                    if availble_seat >= passengers:
                        print(f'{passengers} available seat/seats! :)')
                        os.system("Alarm.mp3")      # play the alarm soundtrack
                        stop = True
                        break
            else:
                print('No train is available..:(')
                stop = True
        
        if stop == True:
            break
        time.sleep(20)
    except:
        i += 1
        time.sleep(6)
        if i == 5:
            stop = True

input('\nHave a good day... :)\nDeveloped by ==Unes==\n[telegram:t.me/unes_h]')