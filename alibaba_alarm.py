from selenium import webdriver
from bs4 import BeautifulSoup
import os, time

#def input date
def InputDate(month):
    while True:
        try:
            input_value = int(input(f'{month}:'))
        except:
            print('enter right number')
        while month == 'month':
            if input_value in range(1, 13):
                return input_value
        while month == 'day':
            if input_value in range(1, 31):
                return input_value
    
#define a driver
op = webdriver.ChromeOptions()
op.add_argument("window-size=1500,800")
op.add_argument('headless')
driver = webdriver.Chrome(executable_path='F:\ChromeDriver\chromedriver.exe', options=op)
month = InputDate('month')
day = InputDate('day')
url = (f'https://www.alibaba.ir/train/THR-KER?adult=1&child=0&infant=0&departing=1400-{month}-{day}')
#scrape
stop = False
print('Searching for availble seat...')
while stop == False:
    try:
        driver.get(url)
        time.sleep(20)
        res = driver.page_source
        soup = BeautifulSoup(res, 'lxml')
    except:
        print('no internet')
        time.sleep(30)
    try:
        train_result = soup.find_all('div', class_='a-card available-card mb-3 cards-flip-item last:mb-0')
        if train_result != []:
            print('one seat is available')
            os.system("Demon_Slayer_Season_2_Opening_Full_Akeboshi_LiSA.mp3")
            stop = True
    except:
        pass
driver.close()
_ = input('\nHave a good day... :)\n\ndeveloped by ==Unes==')