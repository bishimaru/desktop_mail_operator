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

def pcmax_reregistration(name):
  options = Options()
  # options.add_argument("--headless")  # 必要に応じてheadlessモードを使用
  options.add_argument("--disable-gpu")  # headlessモードの時はこのオプションを追加
  options.add_argument("--incognito")
  options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
  options.add_argument("--no-sandbox")
  options.add_argument("--window-size=456,912")
  options.add_experimental_option("detach", True)
  options.add_argument("--disable-cache")
  service = Service(executable_path=ChromeDriverManager().install())
  driver = webdriver.Chrome(options=options, service=service)
  wait = WebDriverWait(driver, 15)
  
  
  try:
    pcmax.re_registration(name, driver)
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
    pcmax_reregistration(name)
  