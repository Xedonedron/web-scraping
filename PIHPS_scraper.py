from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime as default_datetime
from datetime import timedelta
import pendulum
import datetime as scraper_datetime
import json, csv, os, requests, time
import pandas as pd
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

now = scraper_datetime.datetime.now()
tanggal_sekarang = now.strftime("%d-%m-%Y")

print('Start')

# chromedriver
# driver = webdriver.Chrome(r"/home/sigurita/Downloads/SeleniumDriver/chromedriver")
driver = webdriver.Firefox(executable_path= r"/home/sigurita/Downloads/SeleniumDriver/geckodriver", options=options)

# navigate to the url -> Pasar Tradisional Berdasarkan Daerah
driver.get('https://www.bi.go.id/hargapangan/TabelHarga/PasarModernDaerah')

time.sleep(10)

# table
row = driver.find_elements(by=By.XPATH, value='//*[@id="grid1"]/div/div[6]/div[2]/table/tbody/tr/td[2]')
lenRow = len(row)
iterDate = len(driver.find_elements(by=By.XPATH, value='//*[@id="grid1"]/div/div[6]/div[1]/div/div[1]/div/table/tbody/tr[1]/td'))
# infoDate = driver.find_element(by=By.XPATH, value='//*[@id="info"]/tr[1]/td[2]').text
# infoDate = str(infoDate[2:]).replace(" ", "")

result = {}

for j in range(1, lenRow): # iterasi luar untuk komoditas
    data = {}
    for k in range(3, iterDate + 1): # iterasi dalam untuk tanggal
        current_col_number = k + 5 # mulai dari 8 karena xpath nya di 8
        perDate = driver.find_element(by=By.XPATH, value=f'//*[contains(@id, "dx-col-{current_col_number}")]/div[2]').text # ngecek kolom tanggal
        varTanggal = f"{perDate}" # bikin variabel sejumlah dengan iterasi dengan penamaan tanggal
        tanggal = driver.find_element(by=By.XPATH, value=f'//*[@id="grid1"]/div/div[6]/div/div/div[1]/div/table/tbody/tr[{j}]/td[{k}]') # find_element gak pake s karena hanya untuk ngecek 1 XPATH
        data[varTanggal] = tanggal.text
    result[row[j-1].text] = data

df = pd.DataFrame(result).T
df.index.name = 'Komoditas'
df.columns.name = 'Tanggal'
print(df)

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
export_dir = os.path.join(current_dir, 'TASI120_data', 'PIHPS', 'modern')
if not os.path.exists(export_dir):
    os.makedirs(export_dir)

df.to_csv(os.path.join(export_dir, f'pihps_modern_daerah_{tanggal_sekarang}.csv'), index=True, float_format='%.3f', sep=";")

time.sleep(2)

# close the browser  
driver.close()

print('Data telah disimpan')