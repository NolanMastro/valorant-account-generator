import os
import random
import traceback
import requests
import datetime
import random
import string
import discord
import threading
import random_word
from discord import SyncWebhook
from selenium import webdriver
from random_word import RandomWords
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from dotenv import load_dotenv
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


load_dotenv()
count = 0


r = RandomWords()


if not os.environ["webhook"]:
    raise Exception("Please enter a webhook url in the .env file to send the accounts.")
else:
    discord_webhook_url = os.environ["webhook"]

if not os.environ["catchall"]:
    raise Exception("Please enter a catchall email in the .env file.")
else:
    catchall = os.environ["catchall"]

if not os.environ["password"]:
    raise Exception("Please enter a password to use for the accounts in the .env file.")
else:
    password = os.environ["password"]

def get_to_login_page(driver):
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#gatsby-focus-wrapper > section.section.dark.HomeHero-module--homeHero--2qpBZ.in-view > div.sectionWrapper.border-left.HomeHero-module--sectionWrapper--lvg6e > button > div > span.PrimaryButton-module--label-text--qK7Ui"))).click()
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.DetachedModal-module--popupBackdrop--lNSL8 > div > div > div > div.SignupModal-module--popupCTAWrapper--LsBuF > div:nth-child(1) > button > div > span.PrimaryButton-module--label-text--qK7Ui'))).click()
    except:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#riotbar-account-bar > div > div'))).click()
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#riotbar-account-dropdown-links > a:nth-child(3) > p'))).click()
        get_to_login_page(driver)


def create_account(driver, catchall, password, count):
    #get random email and input it
    temp_email_and_username = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'email')))
    elem = driver.find_element(By.NAME, 'email')
    elem.send_keys(temp_email_and_username + catchall)
    #next button
    elem.send_keys(Keys.ENTER)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'date_of_birth_month'))).send_keys('03')
    driver.find_element(By.NAME, 'date_of_birth_day').send_keys('20')
    elem = driver.find_element(By.NAME, 'date_of_birth_year')
    elem.send_keys('2000')
    elem.send_keys(Keys.ENTER)
    #username
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'username')))
    elem = driver.find_element(By.NAME, 'username')
    elem.send_keys(temp_email_and_username)
    elem.send_keys(Keys.ENTER)
    #password
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'password'))).send_keys(password)
    elem = driver.find_element(By.NAME, 'confirm_password')
    elem.send_keys(password)
    elem.send_keys(Keys.ENTER)
    #captcha/finish
    wait = WebDriverWait(driver, 300)
    element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#gatsby-focus-wrapper > section > div.sectionWrapper.DownloadClient-module--sectionWrapper--AQPfD > div > button > div > span.PrimaryButton-module--label-text--qK7Ui")))
    webhook = SyncWebhook.from_url(discord_webhook_url)
    webhook.send(f"Username:{temp_email_and_username}\nPassword:{password}")
    count = count+1
    os.system('cls')
    print(f'Accounts created this session: {count}')

    

def main():
    options = webdriver.ChromeOptions()
    driver = driver = webdriver.Chrome(service=Service(ChromeDriverManager(cache_valid_range=30).install()),options=options)
    os.system('cls')
    print(f'Accounts created this session: {count}')
    while True:
        driver.get("https://playvalorant.com/en-us/")
        get_to_login_page(driver)
        create_account(driver, catchall, password, count)
        
        
        

main()
