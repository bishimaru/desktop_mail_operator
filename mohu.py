import tkinter as tk
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
from widget import happymail, func
import sqlite3
from selenium.webdriver.chrome.service import Service
from datetime import timedelta
from tkinter import messagebox
from selenium.common.exceptions import NoSuchWindowException
import signal
import shutil


user_data = func.get_user_data()["happymail"]
base_path = "./chrome_profiles/h_footprint"
headless = False
drivers = {}
for i in user_data:
  print(i["name"])
  if i["name"] != "アスカ" and i["name"] != "めあり":
    continue
  profile_path = os.path.join(base_path, i["name"])
  if os.path.exists(profile_path):
    shutil.rmtree(profile_path)  # フォルダごと削除
    print(f"{profile_path} を削除しました")
    os.makedirs(profile_path, exist_ok=True)  
  driver,wait = func.get_multi_driver(profile_path, headless)
  drivers[i["name"]] = {"driver": driver, "wait": wait}

  for name, data in drivers.items():
    print(f"{name} のページタイトル: {data['driver'].title}")
    happymail.login(i["name"], i["login_id"], i["password"], drivers[name]["driver"], drivers[name]["wait"],)
    warning = happymail.catch_warning_screen(drivers[name]["driver"])
    if warning:
      print(warning)
    else:
      print(f"{i["name"]}のログインに成功しました")


# 例: すべての `driver` を適切に閉じる
# for name, data in drivers.items():
#     data["driver"].quit()
#     print(f"{name} のブラウザを閉じました")