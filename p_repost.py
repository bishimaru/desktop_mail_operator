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
import setting

def pcmax_repost(headless):
  driver,wait = func.get_driver(headless)
  try:
    name ="777"
    pcmax.re_post(name, driver, wait)
    driver.quit() 
  except Exception as e:
    print(f"{name}:エラー")
    print(traceback.format_exc())
    driver.quit() 
  

if __name__ == '__main__':
  if len(sys.argv) < 2:
    print("引数エラー")
  elif len(sys.argv) >= 2:
    headless = str(sys.argv[1])
    
    pcmax_repost(headless )
  