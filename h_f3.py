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
from selenium.common.exceptions import NoSuchWindowException, WebDriverException


user_data = func.get_user_data()["happymail"]
base_path = "./chrome_profiles/h_footprint"
headless = False
drivers = {}

# """ すべての WebDriver を終了する関数 """
def close_all_drivers():
  for name, data in drivers.items():
    try:
      data["driver"].quit()
      print(f"{name} のブラウザを正常に閉じました")
    except WebDriverException as e:
      print(f"{name} のブラウザを閉じる際にエラーが発生: {e}")
  drivers.clear()  # ドライバーリストを空にする

# Ctrl+C で中断した時に WebDriver を閉じる
def signal_handler(sig, frame):
  print("SIGINT (Ctrl+C) を検出しました。WebDriver を閉じます...")
  close_all_drivers()
  sys.exit(0)
# SIGINT (Ctrl+C) をキャッチする
signal.signal(signal.SIGINT, signal_handler)

try:
  # driver起動,ログイン
  for i in user_data:
    # if i["name"] != "アスカ" and i["name"] != "めあり":
    #   continue
    profile_path = os.path.join(base_path, i["name"])
    if os.path.exists(profile_path):
      shutil.rmtree(profile_path)  # フォルダごと削除
      print(f"{profile_path} を削除しました")
      os.makedirs(profile_path, exist_ok=True)  
    driver,wait = func.get_multi_driver(profile_path, headless)
    happymail.login(i["name"], i["login_id"], i["password"], driver, wait)
    warning = happymail.catch_warning_screen(driver)
    if warning:
      print(warning)
    else:
      print(f"{i['name']}のログインに成功しました")
    drivers[i["name"]] = {"driver": driver, "wait": wait}
  time.sleep(1)
  # 足跡付けSET
  for name, data in drivers.items():
    nav_flug = happymail.nav_item_click("プロフ検索", drivers[name]["driver"], drivers[name]["wait"])
    if not nav_flug:
      break
    happymail.set_mutidriver_make_footprints(drivers[name]["driver"], drivers[name]["wait"])
  # 足跡付けループ
  while True:
    for name, data in drivers.items():
      happymail.mutidriver_make_footprints(name,drivers[name]["driver"], drivers[name]["wait"])

except KeyboardInterrupt:
  # Ctrl+C が押された場合
  print("プログラムが Ctrl+C により中断されました。")
  close_all_drivers()
  sys.exit(0)
except Exception as e:
  # 予期しないエラーが発生した場合
  print("エラーが発生しました:", e)
  traceback.print_exc()
  close_all_drivers()
  sys.exit(1)
finally:
  # 正常終了時・エラー終了時を問わず、最後に WebDriver を閉じる
  close_all_drivers()