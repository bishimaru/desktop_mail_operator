from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
import time
from selenium.webdriver.common.by import By
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from selenium.webdriver.support.ui import WebDriverWait
import traceback
from widget import pcmax, happymail, func
import sqlite3
from selenium.webdriver.chrome.service import Service
from datetime import timedelta

def happymail_reregistration(name, headress):
  driver, wait = func.get_driver(headress)
  
  try:
    happymail.re_registration(name, driver, wait)
    driver.quit() 
  except Exception as e:
    print(f"{name}:エラー")
    print(traceback.format_exc())
    driver.quit() 
  

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("引数エラー")
  elif len(sys.argv) >= 2:
    name = str(sys.argv[1])
    headress = str(sys.argv[2])
    print(headress)
    if headress == "0":
      headress = False
    else:
      headress = True
    happymail_reregistration(name, headress)
  