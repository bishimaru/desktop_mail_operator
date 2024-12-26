from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
import time
from selenium.webdriver.common.by import By
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import pcmax, happymail, func
from selenium.webdriver.support.ui import WebDriverWait
import traceback
from datetime import timedelta
import sqlite3
import base64
import requests

def sb_h_repost_returnfoot(happy_chara, matching_cnt, type_cnt, return_foot_cnt, headless): 
  name = happy_chara["name"]
  login_id = happy_chara["login_id"]
  login_pass = happy_chara["password"]
  post_title = happy_chara["post_title"]
  post_contents = happy_chara["post_contents"]
  return_foot_message = happy_chara["return_foot_message"]
  return_foot_img = happy_chara["chara_image"]
  fst_message = happy_chara["fst_message"]

  if not login_id:
    print(f"{name}：ログインIDが正しくありません")
    return
  driver,wait = func.get_driver(headless)
  driver.delete_all_cookies()
  driver.get("https://happymail.jp/login/")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  wait_time = random.uniform(2, 5)
  time.sleep(2)
  id_form = driver.find_element(By.ID, value="TelNo")
  id_form.send_keys(login_id)
  pass_form = driver.find_element(By.ID, value="TelPass")
  pass_form.send_keys(login_pass)
  time.sleep(1)
  send_form = driver.find_element(By.ID, value="login_btn")
  send_form.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  return_foot_counted = 0
  repost_flug = ""

  # try:
  #   repost_flug = happymail.re_post(name, driver, wait, post_title, post_contents)
  # except Exception as e:
  #   print(f"ハッピーメール掲示板エラー{name}")
  #   print(traceback.format_exc())
  #   func.send_error(f"ハッピーメール掲示板エラー{name}", traceback.format_exc())
  # time.sleep(2)
  try:
    return_foot_counted = happymail.return_footpoint(name, driver, wait, return_foot_message, matching_cnt, type_cnt, return_foot_cnt, return_foot_img, fst_message)
  except Exception as e:
    print(f"足跡返しエラー{name}")
    print(traceback.format_exc())
    func.send_error(f"足跡返しエラー{name}", traceback.format_exc())
  driver.quit()
  print(f"再投稿：{repost_flug}\nマッチング返し {return_foot_counted[0]}件\nタイプ返し {return_foot_counted[1]}件\n足跡返し {return_foot_counted[2]}件\n")
  return f"再投稿：{repost_flug}\nマッチング返し {return_foot_counted[0]}件\nタイプ返し {return_foot_counted[1]}件\n足跡返し {return_foot_counted[2]}件\n"


if __name__ == '__main__':
  if len(sys.argv) < 2:
    cnt = 20
  else:
    name = str(sys.argv[1])
    cnt = int(sys.argv[2])
    # matching_cnt = int(sys.argv[3])
    # type_cnt = int(sys.argv[4])
  happy_chara_list = func.get_user_data()["happymail"]
  for i in happy_chara_list:
    if i['name'] == "アスカ":
      happy_chara_list = i
  print(happy_chara_list)

  matching_cnt = 0
  type_cnt = 0
  headless = False
  sb_h_repost_returnfoot(happy_chara_list, matching_cnt, type_cnt, cnt, headless)


  