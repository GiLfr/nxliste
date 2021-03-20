from selenium import webdriver
import time
# import pandas as pd
from local.credentials import LoginId, password

driver=webdriver.Chrome()
driver.get('https://netflix.com')
time.sleep(4)
cookies = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[1]/div[1]/div[1]/button[1]').click()
time.sleep(2)
signIn = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div/div[1]/div/a').click()
time.sleep(4)
emailId = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div/div/label/input')
emailId.send_keys(LoginId)
passwordInput = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input')
passwordInput.send_keys([password])
signInButton = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div/div/div[1]/form/button').click()
time.sleep(4)
profileN3 = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[3]/div/a/div/div').click()
time.sleep(4)
maListeAccess = driver.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div/div/ul/li[6]/a').click()

print('Enregistrer la page avec le menu du navigateur et sauver sous Netflix.html')
# time.sleep(4)
# maListe = driver.page_source
# maListe = driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[1]/div[2]/div/div[2]/div/div/div[1]')
time.sleep(200)
# print(maListe)