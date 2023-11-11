from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime as default_datetime
from selenium.webdriver.firefox.options import Options
from datetime import timedelta
import pendulum
import datetime as scraper_datetime
import json, csv, os, requests, time
import pandas as pd

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
export_dir = os.path.join(current_dir, 'TASI120_data', 'BMKG')
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

options = Options()
options.headless = True

# driver = webdriver.Chrome(r"/home/sigurita/Downloads/SeleniumDriver/chromedriver")
driver = webdriver.Firefox(executable_path= r"/home/sigurita/Downloads/SeleniumDriver/geckodriver", options=options)


now = scraper_datetime.datetime.now()
tanggal_sekarang = now.strftime("%d-%m-%Y")

print('Start')

driver.get('https://www.bmkg.go.id/cuaca/prakiraan-cuaca-indonesia.bmkg#TabPaneCuaca1')
tab = driver.find_elements(by=By.XPATH, value='/html/body/div[1]/div[3]/div/div[1]/div/ul/li/a')
if len(tab) >= 3:
    tab_index = 1
else:
    tab_index = 2

def method_pagi():
    print("Metode pagi hari sedang dijalankan")

    tab_xpath = f'//*[@id="TabPaneCuaca{tab_index}"]'
    kolom = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody[1]/tr/td')
    if len(kolom) != 6:
        print("Jumlah kolom tidak sesuai, menghentikan pengambilan data...")
        driver.refresh()
        method_pagi()
        return

    kota =  driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[1]/a')
    siang = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[2]/span')
    malam = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[3]/span')
    dini = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[4]/span')
    suhu = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[5]')
    kelembapan = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[6]')

    result = []

    for i in range(len(kota)):
        data = {
            'Kota' : kota[i].text,
            'Prakiraan Cuaca Siang' : siang[i].text,
            'Prakiraan Cuaca Malam' : malam[i].text,
            'Prakiraan Cuaca Dini Hari': dini[i].text,
            'Suhu (°C)': suhu[i].text,
            'Kelembapan (%)': kelembapan[i].text
        }
        result.append(data)

    df = pd.DataFrame(result)
    print(df)
    df.to_csv(os.path.join(export_dir, f'bmkg_{str(tanggal_sekarang)}.csv'), index=False)

    time.sleep(2)
    driver.close()
    print("Data telah disimpan")

def method_siang():
    print("Metode siang hari sedang dijalankan")

    tab_xpath = f'//*[@id="TabPaneCuaca{tab_index}"]'
    kolom = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody[1]/tr/td')
    if len(kolom) != 5:
        print("Jumlah kolom tidak sesuai, menghentikan pengambilan data...")
        driver.refresh()
        method_pagi()
        return

    kota =  driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[1]/a')
    malam = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[2]/span')
    dini = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[3]/span')
    suhu = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[4]')
    kelembapan = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[5]')

    result = []

    for i in range(len(kota)):
        data = {
            'Kota' : kota[i].text,
            'Prakiraan Cuaca Malam' : malam[i].text,
            'Prakiraan Cuaca Dini Hari': dini[i].text,
            'Suhu (°C)': suhu[i].text,
            'Kelembapan (%)': kelembapan[i].text
        }

        result.append(data)
    
    df = pd.DataFrame(result)
    print(df)
    df.to_csv(os.path.join(export_dir, f'bmkg_{str(tanggal_sekarang)}.csv'), index=False)

    # close the browser  
    time.sleep(2)
    driver.close()
    print("Data telah disimpan") 

def method_malam():
    print("Metode malam hari sedang dijalankan")

    tab_xpath = f'//*[@id="TabPaneCuaca{tab_index}"]'
    kolom = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody[1]/tr/td')
    if len(kolom) != 4:
        print("Jumlah kolom tidak sesuai, menghentikan pengambilan data...")
        driver.refresh()
        method_pagi()
        return

    kota =  driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[1]/a')
    dini = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[2]/span')
    suhu = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[3]')
    kelembapan = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[4]')

    result = []
    for i in range(len(kota)):
        data = {
            'Kota' : kota[i].text,
            'Prakiraan Cuaca Dini Hari': dini[i].text,
            'Suhu (°C)': suhu[i].text,
            'Kelembapan (%)': kelembapan[i].text
        }
        result.append(data)

    df = pd.DataFrame(result)
    print(df)
    df.to_csv(os.path.join(export_dir, f'bmkg_{str(tanggal_sekarang)}.csv'), index=False)

    # close the browser  
    time.sleep(2)
    driver.close()
    print("Data telah disimpan")

def method_dini():
    print("Metode dini hari sedang dijalankan")

    tab_xpath = f'//*[@id="TabPaneCuaca{tab_index}"]'
    kolom = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody[1]/tr/td')
    if len(kolom) != 7:
        print("Jumlah kolom tidak sesuai, menghentikan pengambilan data...")
        driver.refresh()
        method_pagi()
        return

    kota =  driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[1]/a')
    pagi = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[2]/span')
    siang = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[3]/span')
    malam = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[4]/span')
    dini = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[5]/span')
    suhu = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[6]')
    kelembapan = driver.find_elements(by=By.XPATH, value=f'{tab_xpath}/div/table/tbody/tr/td[7]')

    result = []

    for i in range(len(kota)):
        data = {
            'Kota' : kota[i].text,
            'Prakiraan Cuaca Pagi Hari': pagi[i].text,
            'Prakiraan Cuaca Siang Hari': siang[i].text,
            'Prakiraan Cuaca Malam Hari': malam[i].text,
            'Prakiraan Cuaca Dini Hari': dini[i].text,
            'Suhu ( °C )': suhu[i].text,
            'Kelembapan (%)': kelembapan[i].text
        }

        result.append(data)

    df = pd.DataFrame(result)
    print(df)
    df.to_csv(os.path.join(export_dir, f'bmkg_{str(tanggal_sekarang)}.csv'), index=False)

    # close the browser  
    time.sleep(2)
    driver.close()
    print("Data telah disimpan")

def main():
    current_time = scraper_datetime.datetime.now().time()
    time.sleep(3)
    if current_time < scraper_datetime.time(hour=6):
        method_dini()
    elif current_time < scraper_datetime.time(hour=12):
        method_pagi()
    elif current_time < scraper_datetime.time(hour=18):
        method_siang()
    elif current_time < scraper_datetime.time(hour=23, minute=59):
        method_malam()

main()