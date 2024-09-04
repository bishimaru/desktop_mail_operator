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


def sb_h_repost_returnfoot(happy_chara, cnt, headless): 
  name = happy_chara["name"]
  login_id = happy_chara["login_id"]
  login_pass = happy_chara["password"]
  post_title = happy_chara["post_title"]
  post_contents = happy_chara["post_contents"]
  return_foot_message = happy_chara["return_foot_message"]
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
  return_foot_cnt = 0
  repost_flug = ""
  try:
    repost_flug = happymail.re_post(name, driver, wait, post_title, post_contents)
  except Exception as e:
    print(f"ハッピーメール掲示板エラー{name}")
    print(traceback.format_exc())
    func.send_error(f"ハッピーメール掲示板エラー{name}", traceback.format_exc())
  time.sleep(2)
  try:
    return_foot_img = ""
    fst_message = ""
    return_foot_cnt = happymail.return_footpoint(name, driver, wait, return_foot_message, cnt, return_foot_img, fst_message)
  except Exception as e:
    print(f"足跡返しエラー{name}")
    print(traceback.format_exc())
    func.send_error(f"足跡返しエラー{name}", traceback.format_exc())
  driver.quit()
  print(f"再投稿：{repost_flug}\n足跡返し {return_foot_cnt}件")
  return f"再投稿：{repost_flug}\n足跡返し {return_foot_cnt}件\n"


if __name__ == '__main__':
  if len(sys.argv) < 2:
    cnt = 20
  else:
    name = str(sys.argv[1])
    cnt = int(sys.argv[2])
    # matching_cnt = int(sys.argv[3])
    # type_cnt = int(sys.argv[4])
  happy_chara_list = ['アスカ', '50086800553', 'ebbh7278', '3人でエッチを楽しめる方探してます♪', '初めまして( ＾∀＾)\r\nあすかです！友達のゆかとセフレさん探しの為に始めてみました♪♪\r\n\r\n2人とも都内のメンズ専門の脱毛サロンで働いてるんですけど、VIOの脱毛専門で施術中にエッチな気分になっちゃてるちょっと変態な2人組です(⸝⸝⸝´꒳`⸝⸝⸝)ﾃﾚｯ\r\n\r\n私もゆかもちょっと刺激が欲しいなって思ってて、、\r\n折角セフレさんになってもらうなら3人でエッチを楽しめる人を探してます！\r\n\r\n3Pとかに興味ある方は連絡くださいね♪♪\r\n因みに、2人ともエッチで人懐っこい性格なので会って損はしないと思います♪笑', "足跡が付いてたので気になってご連絡しちゃいました♪\r\nあすかです٩( 'ω’ )و\r\n友達のゆかと3人でエッチを楽しめるセフレさんを見つけたくてサイトに登録しました！\r\n\r\n2人ともメンズ専門の脱毛サロンで働いてるんですけど、毎回VIOの施術中にエッチな気分になっちゃって(//ω照♥\r\n\r\n私もゆかも今は特定の相手もいないし、折角なら3人でエッチを楽しめるセフレさんが出来たらなって思ってるんですけど今ってそういうお相手探してたりしませんか？？"]
  
  headless = False
  sb_h_repost_returnfoot(happy_chara_list, cnt, headless)


  