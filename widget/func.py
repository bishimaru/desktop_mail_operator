import time
import sqlite3
import random
import os
import sys
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import traceback
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from selenium.webdriver.common.by import By
from widget import pcmax
from selenium.webdriver.support.select import Select
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
import requests
import shutil
import unicodedata
import platform
from urllib3.exceptions import MaxRetryError
from webdriver_manager.core.driver_cache import DriverCacheManager
import tempfile
from stem import Signal
from stem.control import Controller

def get_the_temporary_folder(temp_dir):
  # スクリプトのディレクトリを基準にディレクトリを作成
  script_dir = os.path.dirname(os.path.abspath(__file__)) 
  tmp_dir = os.path.join(script_dir, "tmp")  # tmpフォルダのパスを作成
  if not os.path.exists(tmp_dir):
    os.makedirs(tmp_dir)
  # tmpフォルダ内に 引数で受け取った フォルダを作成
  dir = os.path.join(tmp_dir, temp_dir)  # h_footprintフォルダのパスを作成
  if not os.path.exists(dir):
    os.makedirs(dir)
  # デバック用ファイル作成
  # for i in range(1, 13):  # 3つのテストファイルを作成
  #       file_path = os.path.join(dir, f"test_file_{i}.txt")
  #       if not os.path.exists(file_path):
  #           with open(file_path, "w") as f:
  #               f.write(f"This is test file {i}.")
  #           print(f"Created: {file_path}")
  entries = os.listdir(dir)  # ディレクトリ内のエントリを取得
  # print(entries)
  # print(len(entries))  # エントリの数を
  # time.sleep(10)
  if len(entries) >= 10:
    print("キャッシュが複数存在するため、クリアします。起動中のマクロは再起動してください。。。")
    for entry in entries:
      entry_path = os.path.join(dir, entry)
      try:
        # エントリがファイルの場合
        if os.path.isfile(entry_path) or os.path.islink(entry_path):
            os.remove(entry_path)
            # print(f"Deleted file: {entry_path}")
        # エントリがフォルダの場合
        elif os.path.isdir(entry_path):
            shutil.rmtree(entry_path)
            # print(f"Deleted folder: {entry_path}")
      except Exception as e:
          print(f"Failed to delete {entry_path}: {e}")
  return dir

def clear_webdriver_cache():
    os_name = platform.system()
    
    # スクリプトの実行ディレクトリを取得
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 削除するキャッシュディレクトリ
    cache_dirs = []

    # macOS の場合
    if os_name == "Darwin":
        cache_dirs = [
            os.path.expanduser("~/.wdm/drivers"),  # WebDriverのキャッシュディレクトリ
            os.path.join(script_dir, "widget", "tmp", "h_footprint")  # スクリプトの実行ディレクトリに基づいたパス
        ]
    # Windows の場合
    elif os_name == "Windows":
        cache_dirs = [
            os.path.join(os.getenv('USERPROFILE'), '.wdm', 'drivers'),
            os.path.join(script_dir, "widget", "tmp", "h_footprint")
        ]
    else:
        return  # サポートしていないOSの場合は何もしない

    # キャッシュディレクトリの削除
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"Deleted: {cache_dir}")
            except Exception as e:
                print(f"Error clearing cache {cache_dir}: {e}")

# def get_driver(headless_flag, max_retries=3):
#     os_name = platform.system()
#     for attempt in range(max_retries):
#         try:
#           # ランダムなポートを割り当てる
#           port = random.randint(5000, 9000)
#           options = Options()
#           if headless_flag:
#             options.add_argument('--headless')
#             options.add_argument("--disable-gpu") 
#           options.add_argument("--disable-gpu")  # GPUアクセラレーションを無効化
#           options.add_argument("--disable-software-rasterizer")  # ソフトウェアラスタライズを無効化
#           options.add_argument("--disable-dev-shm-usage")  # 共有メモリの使用を無効化（仮想環境で役立つ）
#           options.add_argument("--incognito")
#           options.add_argument('--enable-unsafe-swiftshader')
#           options.add_argument('--log-level=3')  # これでエラーログが抑制されます
#           options.add_argument('--disable-web-security')
#           options.add_argument('--disable-extensions')
#           options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
#           options.add_argument("--no-sandbox")
#           options.add_argument("--window-size=456,912")
#           options.add_experimental_option("detach", True)
#           options.add_argument("--disable-cache")
#           options.add_argument("--disable-blink-features=AutomationControlled")  # 自動化検出回避のためのオプション

#           # キャッシュディレクトリを変更
#           # custom_cache_dir = os.path.join(os.getcwd(), "driver_cache")
#           # cache_manager = DriverCacheManager(custom_cache_dir)
#           if os_name == "Darwin":
#             service = Service(executable_path=ChromeDriverManager(cache_manager=DriverCacheManager(valid_range=0)).install())
#           elif os_name == "Windows":
#             service = Service(executable_path=ChromeDriverManager(cache_manager=DriverCacheManager(valid_range=0)).install())
#           service.command_line_args().append(f"--port={port}")
#           driver = webdriver.Chrome(options=options, service=service)
#           wait = WebDriverWait(driver, 18)

#           return driver, wait

#         except (WebDriverException, NoSuchElementException, MaxRetryError) as e:
#             print(f"WebDriverException発生: {e}")
#             print(f"再試行します ({attempt + 1}/{max_retries})")
#             clear_webdriver_cache()
#             time.sleep(5)
#             if attempt == max_retries - 1:
#                 raise

def test_get_driver(tmp_dir, headless_flag, max_retries=3):
    # os_name = platform.system()
    # print(tmp_dir)
    # tmpフォルダ内に一意のキャッシュディレクトリを作成
    temp_dir = os.path.join(tmp_dir, f"temp_cache_{os.getpid()}")  # 一意のディレクトリを生成（PIDベース）
    os.environ["WDM_CACHE"] = temp_dir
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)  # キャッシュディレクトリが存在しない場合は作成
    # print(f"WDM_CACHE is set to: {os.environ['WDM_CACHE']}")

    for attempt in range(max_retries):
      try:
        options = Options()
        if headless_flag:
          options.add_argument('--headless')
        options.add_argument("--disable-gpu") 
        options.add_argument("--disable-software-rasterizer")
        options.add_argument("--disable-dev-shm-usage")  # 共有メモリの使用を無効化（仮想環境で役立つ）
        options.add_argument("--incognito")
        options.add_argument('--enable-unsafe-swiftshader')
        options.add_argument('--log-level=3')  # これでエラーログが抑制されます
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-extensions')
        options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=456,912")
        options.add_experimental_option("detach", True)
        options.add_argument("--disable-cache")
        options.add_argument("--disable-blink-features=AutomationControlled")  # 自動化検出回避のためのオプション
        
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(options=options, service=service)
        wait = WebDriverWait(driver, 18)

        return driver, wait

      except (WebDriverException, NoSuchElementException, MaxRetryError, ConnectionError) as e:
        print(f"WebDriverException発生: {e}")
        print(f"再試行します ({attempt + 1}/{max_retries})")
        clear_webdriver_cache()
        time.sleep(5)
        if attempt == max_retries - 1:
            raise
      except ConnectionError as e:
        print(f"⚠️ ネットワークエラーが発生しました: {e}")
        print("3分後に再接続します...")
        clear_webdriver_cache()
        time.sleep(180)
        if attempt == max_retries - 1:
            raise


def timer(fnc, seconds, h_cnt, p_cnt):  
  start_time = time.time() 
  fnc(h_cnt, p_cnt)
  while True:
    elapsed_time = time.time() - start_time  # 経過時間を計算する
    if elapsed_time >= seconds:
      start_time = time.time() 
      break
    else:
      time.sleep(10)
  return True


def send_conditional(user_name, user_address, mailaddress, password, text, site):
  subject = f'{site}でやり取りしてた{user_name}さんでしょうか？'
  text = text
  address_from = mailaddress
  address_to = user_address
  smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
  smtpobj.set_debuglevel(0)
  smtpobj.starttls()
  smtpobj.login(mailaddress, password)
  msg = MIMEText(text)
  msg['Subject'] = subject
  msg['From'] = address_from
  msg['To'] = address_to
  msg['Date'] = formatdate()
  smtpobj.send_message(msg)
  smtpobj.close()  

def send_error(chara, error_message):
  # print("エラー送信＞＞＞＜＜＜＜＜＜＜")
  # print(f"{chara}  :  {error_message}")
  mailaddress = 'kenta.bishi777@gmail.com'
  password = 'rjdzkswuhgfvslvd'
  text = f"キャラ名:{chara} \n {error_message}"
  subject = "サイト回しエラーメッセージ"
  address_from = 'kenta.bishi777@gmail.com'
  # address_to = "ryapya694@ruru.be"
  address_to = "gifopeho@kmail.li"
  smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
  smtpobj.set_debuglevel(1) 
  smtpobj.starttls()
  smtpobj.login(mailaddress, password)
  msg = MIMEText(text)
  msg['Subject'] = subject
  msg['From'] = address_from
  msg['To'] = address_to
  msg['Date'] = formatdate()
  try:
    smtpobj.send_message(msg)
  except smtplib.SMTPDataError as e:
    print(f"SMTPDataError: {e}")
  except Exception as e:
    print(f"An error occurred: {e}")
  
  smtpobj.close()

def send_mail(message, mail_info, title):
  mailaddress = mail_info[1]
  password = mail_info[2]
  text = message
  subject = title
  address_from = mail_info[1]
  address_to = mail_info[0]
  smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
  # smtpobj.set_debuglevel(1) 
  smtpobj.set_debuglevel(0)  # デバッグログをオフにする
  smtpobj.starttls()
  smtpobj.login(mailaddress, password)
  msg = MIMEText(text)
  msg['Subject'] = subject
  msg['From'] = address_from
  msg['To'] = address_to
  msg['Date'] = formatdate()
  smtpobj.send_message(msg)
  smtpobj.close()



def h_p_return_footprint(name, h_w, p_w, driver, return_foot_message, cnt, h_return_foot_img, p_return_foot_img):
  start_time = time.time() 
  wait = WebDriverWait(driver, 10)
  wait_time = random.uniform(1, 3)
  history_user_list = []
  p_w = ""
  # wait_time = 2
  # ハッピーメールの足跡リストまで
  driver.switch_to.window(h_w)
  driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # マイページをクリック
  nav_list = driver.find_element(By.ID, value='ds_nav')
  mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
  mypage.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 足あとをクリック
  return_footpoint = driver.find_element(By.CLASS_NAME, value="icon-ico_footprint")
  return_footpoint.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 足跡ユーザーを取得
  happy_foot_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")
  while len(happy_foot_user) == 0:
      time.sleep(2)
      happy_foot_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")  
  mail_icon_cnt = 0
  name_field = happy_foot_user[0].find_element(By.CLASS_NAME, value="ds_like_list_name")
  user_name = name_field.text
  mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
  mail_icon_cnt = 0
  if len(mail_icon):
    if not user_name in history_user_list:
        # print(history_user_list)
        mail_icon_cnt = 0
        history_user_list.append(user_name)
        happy_foot_user[0].click()
    else:
      # print('ハッピーメール：メールアイコンがあります')
      mail_icon_cnt += 1
      # print(f'メールアイコンカウント{mail_icon_cnt}')
      name_field = happy_foot_user[mail_icon_cnt].find_element(By.CLASS_NAME, value="ds_like_list_name")
      user_name = name_field.text
      mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
      # # メールアイコンが7つ続いたら終了
      if mail_icon_cnt == 5:
        print("ハッピーメール：メールアイコンが5続きました")
      # ユーザークリック
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", happy_foot_user[mail_icon_cnt])
      time.sleep(1)
      happy_foot_user[mail_icon_cnt].click()
  else:
    happy_foot_user[0].click()

  # PCMAXの足跡リストまで
  if p_w:
    driver.switch_to.window(p_w)
    pcmax.login(driver, wait)
    # 新着メッセージの確認
    have_new_massage_users = []
    new_message = driver.find_element(By.CLASS_NAME, value="message")
    new_message.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    user_info = driver.find_elements(By.CLASS_NAME, value="user_info")
    # 新着ありのユーザーをリストに追加
    for usr_info in user_info:
      unread = usr_info.find_elements(By.CLASS_NAME, value="unread1")
      if len(unread):
        new_mail_pcmax_name = usr_info.find_element(By.CLASS_NAME, value="name").text
        if len(new_mail_pcmax_name) > 7:
          new_mail_pcmax_name = new_mail_pcmax_name[:7] + "…"
        have_new_massage_users.append(new_mail_pcmax_name)
    print("新着メッセージリスト")
    print(have_new_massage_users)
    driver.get("https://pcmax.jp/pcm/index.php")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(1)
    # 右下のキャラ画像をクリック
    chara_img = driver.find_elements(By.XPATH, value="//*[@id='sp_footer']/a[5]")
    if len(chara_img):
      chara_img[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
    else: #番号確認画面
      return
    # //*[@id="contents"]/div[2]/div[2]/ul/li[5]/a
    # 足あとをクリック
    footpoint = driver.find_element(By.XPATH, value="//*[@id='contents']/div[2]/div[2]/ul/li[5]/a")
    footpoint.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    for i in range(3):
      # ページの最後までスクロール
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      # ページが完全に読み込まれるまで待機
      time.sleep(1)
    # ユーザーを取得
    user_list = driver.find_element(By.CLASS_NAME, value="list-content")
    div = user_list.find_elements(By.XPATH, value='./div')
    # ユーザーのlinkをリストに保存
    link_list = []
    user_cnt = 0
    # print(len(div))
    while user_cnt + 1 < len(div) - 1:
      # 新着リストの名前ならスキップ
      new_mail_name = div[user_cnt].find_element(By.CLASS_NAME, value="user-name")
      if new_mail_name.text in have_new_massage_users:
        user_cnt += 1
      else:
        a_tags = div[user_cnt].find_elements(By.TAG_NAME, value="a")
        # print("aタグの数：" + str(len(a_tags)))
        if len(a_tags) > 1:
          link = a_tags[1].get_attribute("href")
          # print(link)
          link_list.append(link)
        user_cnt += 1
  # メッセージを送信
  pcmax_return_message_cnt = 1
  pcmax_transmission_history = 0
  pcmax_send_flag = True
  foot_cnt = 0
  p_foot_cnt = 0
  p_send_cnt = 0
  while cnt > foot_cnt:
    # happymail
    driver.switch_to.window(h_w)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    happy_send_status = True
    m = driver.find_elements(By.XPATH, value="//*[@id='ds_main']/div/p")
    if len(m):
      print(m[0].text)
      if m[0].text == "プロフィール情報の取得に失敗しました": 
          continue
    # 自己紹介文に業者、通報が含まれているかチェック
    if len(driver.find_elements(By.CLASS_NAME, value="translate_body")):
      contains_violations = driver.find_element(By.CLASS_NAME, value="translate_body")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", contains_violations)
      self_introduction_text = contains_violations.text.replace(" ", "").replace("\n", "")
      if '通報' in self_introduction_text or '業者' in self_introduction_text:
          print('ハッピーメール：自己紹介文に危険なワードが含まれていました')
          happy_send_status = False
    # メッセージ履歴があるかチェック
    mail_field = driver.find_element(By.ID, value="ds_nav")
    mail_history = mail_field.find_element(By.ID, value="mail-history")
    display_value = mail_history.value_of_css_property("display")
    if display_value != "none":
        print('ハッピーメール：メール履歴があります')
        # print(user_name)
        # user_name_list.append(user_name) 
        happy_send_status = False
        mail_icon_cnt += 1
    # メールするをクリック
    if happy_send_status:
      send_mail = mail_field.find_element(By.CLASS_NAME, value="ds_profile_target_btn")
      send_mail.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # 足跡返しを入力
      text_area = driver.find_element(By.ID, value="text-message")
      text_area.send_keys(return_foot_message)
      # 送信
      send_mail = driver.find_element(By.ID, value="submitButton")
      send_mail.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # 画像があれば送信
      if h_return_foot_img:
        img_conform = driver.find_element(By.ID, value="media-confirm")
        plus_icon = driver.find_element(By.CLASS_NAME, value="icon-message_plus")
        plus_icon.click()
        time.sleep(1)
        upload_file = driver.find_element(By.ID, "upload_file")
        upload_file.send_keys(h_return_foot_img)
        time.sleep(1)
        submit = driver.find_element(By.ID, value="submit_button")
        submit.click()
        while img_conform.is_displayed():
            time.sleep(1)
      foot_cnt += 1
      print(name + ':ハッピーメール：'  + str(foot_cnt) + "件送信")
      mail_icon_cnt = 0
      driver.get("https://happymail.co.jp/sp/app/html/ashiato.php")
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      # https://happymail.co.jp/sp/app/html/ashiato.php
    else:
      driver.get("https://happymail.co.jp/sp/app/html/ashiato.php")
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
    # 足跡ユーザーを取得
    time.sleep(1)
    happy_foot_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")
    while len(happy_foot_user) == 0:
        time.sleep(1)
        happy_foot_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")    
    name_field = happy_foot_user[0].find_element(By.CLASS_NAME, value="ds_like_list_name")
    user_name = name_field.text
    
    # print(user_name)
    # print(history_user_list)
    mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
    if len(mail_icon):
      while len(mail_icon):
        if not user_name in history_user_list:
          
          mail_icon_cnt = 0
          history_user_list.append(user_name)
          happy_foot_user[0].click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(2)
          driver.get("https://happymail.co.jp/sp/app/html/ashiato.php")
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(wait_time)
          happy_foot_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")
          name_field = happy_foot_user[0].find_element(By.CLASS_NAME, value="ds_like_list_name")
          mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
        else:
          # print('ハッピーメール：メールアイコンがあります')
          mail_icon_cnt += 1
          # print(f'メールアイコンカウント{mail_icon_cnt}')
          name_field = happy_foot_user[mail_icon_cnt].find_element(By.CLASS_NAME, value="ds_like_list_name")
          user_name = name_field.text
          mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
          # # メールアイコンが7つ続いたら終了
          if mail_icon_cnt == 5:
            print("ハッピーメール：メールアイコンが5続きました")
      # ユーザークリック
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", happy_foot_user[mail_icon_cnt])
      time.sleep(1)
      happy_foot_user[mail_icon_cnt].click()
    else:
      happy_foot_user[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)


    # pcmax
    if p_w and pcmax_send_flag:
      transmission_history = 0
      driver.switch_to.window(p_w)
      time.sleep(1)
      driver.get(link_list[p_foot_cnt])
      time.sleep(wait_time)
      # お相手のご都合により表示できませんはスキップ
      main = driver.find_elements(By.TAG_NAME, value="main")
      if not len(main):
        p_foot_cnt += 1
        continue

      # 送信履歴が連続で続くと終了
      sent = driver.find_elements(By.XPATH, value="//*[@id='profile-box']/div/div[2]/p/a/span")
      if len(sent):
        pcmax_transmission_history += 1
        if pcmax_transmission_history == 5:
          pcmax_send_flag = False
        print('pcmax:送信履歴があります')
        print(f"送信履歴カウント：{pcmax_transmission_history}" )
        p_foot_cnt += 1
        time.sleep(1)
        continue
      # 自己紹介文をチェック
      self_introduction = driver.find_elements(By.XPATH, value="/html/body/main/div[4]/div/p")
      if len(self_introduction):
        self_introduction = self_introduction[0].text.replace(" ", "").replace("\n", "")
        if '通報' in self_introduction or '業者' in self_introduction:
          print('pcmax:自己紹介文に危険なワードが含まれていました')
          p_foot_cnt += 1
          continue
      # 残ポイントチェック
      point = driver.find_elements(By.ID, value="point")
      if len(point):
        point = point[0].find_element(By.TAG_NAME, value="span").text
        pattern = r'\d+'
        match = re.findall(pattern, point)
        if int(match[0]) > 1:
          maji_soushin = True
        else:
          maji_soushin = False
      else:
        time.sleep(wait_time)
        print(' 相手の都合により表示できません')
        p_foot_cnt += 1
        continue
      # メッセージをクリック
      message = driver.find_elements(By.ID, value="message1")
      if len(message):
        message[0].click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(3)
      else:
        continue
      # 画像があれば送付
      if p_return_foot_img:
        picture_icon = driver.find_elements(By.CLASS_NAME, value="mail-menu-title")
        picture_icon[0].click()
        time.sleep(1)
        picture_select = driver.find_element(By.ID, "my_photo")
        select = Select(picture_select)
        select.select_by_visible_text(p_return_foot_img)
      # メッセージを入力
      text_area = driver.find_element(By.ID, value="mdc")
      text_area.send_keys(return_foot_message)
      time.sleep(1)
      p_foot_cnt += 1
      p_send_cnt += 1
      print("pcmax:マジ送信 " + str(maji_soushin) + " ~" + str(p_send_cnt) + "~")
      # メッセージを送信
      if maji_soushin:
        send = driver.find_element(By.CLASS_NAME, value="maji_send")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send)
        send.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(1)
        send_link = driver.find_element(By.ID, value="link_OK")
        send_link.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        # time.sleep(wait_time)
        pcmax_transmission_history = 0
      else:
        send = driver.find_element(By.ID, value="send_n")
        send.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        # time.sleep(wait_time)
        # mail_history = 0
  # timedeltaオブジェクトを作成してフォーマットする
  elapsed_time = time.time() - start_time  # 経過時間を計算する
  elapsed_timedelta = timedelta(seconds=elapsed_time)
  elapsed_time_formatted = str(elapsed_timedelta)
  print(f"<<<<<<<<<<<<<h_p_foot 経過時間 {elapsed_time_formatted}>>>>>>>>>>>>>>>>>>")
  print(f"pcmax足跡返し　{name}、{p_send_cnt}件")


def check_new_mail_gmail(driver, wait, name, mail_address):
  if not mail_address:
    return None
  return_list = []
  dbpath = 'firstdb.db'
  conn = sqlite3.connect(dbpath)
  cur = conn.cursor()
  cur.execute('SELECT window_Handle FROM gmail WHERE mail_address = ?', (mail_address,))
  w_h = ""
  for row in cur:
      w_h = row[0]
  if not w_h:
    return None
  cur.execute('SELECT login_id, passward FROM pcmax WHERE name = ?', (name,))
  login_id = ""
  passward = ""
  for row in cur:
    login_id = row[0]
    passward = row[1]
  try:
      driver.switch_to.window(w_h)
      time.sleep(2)
      driver.get("https://mail.google.com/mail/mu")
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)  
  except TimeoutException as e:
      print("TimeoutException")
      driver.refresh()
  except Exception as e:
      print(f"<<<<<<<<<<エラー：{mail_address}>>>>>>>>>>>")
      print(traceback.format_exc())
      driver.quit()
  # メニューをクリック
  # カスタム属性の値を持つ要素をXPathで検索
  custom_value = "メニュー"
  xpath = f"//*[@aria-label='{custom_value}']"
  element = driver.find_elements(By.XPATH, value=xpath)
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2) 
  element[0].click()
  time.sleep(1) 
  custom_value = "toggleaccountscallout+21"
  xpath = f"//*[@data-control-type='{custom_value}']"
  element = driver.find_elements(By.XPATH, value=xpath)
  if len(element):
      time.sleep(2)
      element = driver.find_elements(By.XPATH, value=xpath)
  address = element[0].text
  # メインボックスのチェック
  menuitem_element = driver.find_elements(By.XPATH, '//*[@role="menuitem"]')
  main_box = menuitem_element[0]
  main_box.click()
  time.sleep(1)
  emails = driver.find_elements(By.XPATH, value='//*[@role="listitem"]')
  for email in emails:
    new_email = email.find_elements(By.TAG_NAME, value="b")
    if len(new_email):
      child_elements = email.find_elements(By.CLASS_NAME, value="Rk")
      if child_elements[0].text:  # テキストが空でない場合
          # print(f"この子要素にテキストが含まれています: {child_elements[0].text}")
          return_list.append(f"{address},{login_id}:{passward}\n「{child_elements[0].text}」")
      email.click()
      time.sleep(2)
      driver.back()
      time.sleep(1)
    else:
      continue
      
  # 迷惑メールフォルダーをチェック
  custom_value = "メニュー"
  xpath = f"//*[@aria-label='{custom_value}']"
  element = driver.find_elements(By.XPATH, value=xpath)
  element[0].click()
  time.sleep(2) 
  menu_list = driver.find_elements(By.XPATH, value="//*[@role='menuitem']")
  spam = menu_list[-1]
  driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", spam)
  spam.click()
  time.sleep(1) 
  emails = driver.find_elements(By.XPATH, value='//*[@role="listitem"]')
  for email in emails:
    new_email = email.find_elements(By.TAG_NAME, value="b")
    if len(new_email):
      child_elements = email.find_elements(By.CLASS_NAME, value="Rk")
      if child_elements[0].text:  # テキストが空でない場合
          # print(f"この子要素にテキストが含まれています: {child_elements[0].text}")
          return_list.append(f"{address}:迷惑フォルダ,{login_id}:{passward}\n「{child_elements[0].text}」")
      email.click()
      time.sleep(2)
      driver.back()
      time.sleep(1)
    else:
      continue
  custom_value = "メニュー"
  xpath = f"//*[@aria-label='{custom_value}']"
  element = driver.find_elements(By.XPATH, value=xpath)
  element[0].click()
  # window_handles = driver.window_handles
  # for window_handle in window_handles:
  #   driver.switch_to.window(window_handle)
  #   current_url = driver.current_url
  #   if current_url.startswith("https://mail.google.com/mail/mu"):
  #       print("URLがhttps://mail.google.com/mail/muから始まります。")
  #   else:
  #       print("URLがhttps://mail.google.com/mail/muから始まりません。")
  if len(return_list):
    return return_list
  else:
    return None

def get_user_data_ken2():
  # APIエンドポイントURL
  api_url = "https://meruopetyan.com/api/user-data/"
  # DEBUG
  # api_url = "http://127.0.0.1:8000/api/user-data/"
  max_retries = 3
  retry_count = 0
  wait_time = 300  # 5分（300秒）

  # POSTリクエストのペイロード
  data = {
      'name': "ken2",
      'password': "7234"
  }
  while retry_count < max_retries:

    try:
      # POSTリクエストを送信してデータを取得
      response = requests.post(api_url, data=data)
      
      # レスポンスのステータスコードを確認
      if response.status_code == 200:
          # レスポンスのJSONデータを取得
          user_data = response.json()

          # Happymailデータを表示
          # print("Happymailのデータ:")
          # for data in user_data.get('userprofile', []):
          #     print(f"Name: {data['gmail_account']}, ")

          # # PCMaxデータを表示
          # print("PCMaxのデータ:")
          # for data in user_data.get('pcmax', []):
          #     print(f"Name: {data['name']}, ")
          return user_data
      elif response.status_code == 204:
        print(f"有効期限が切れている可能性があります。")
        return 0
      elif response.status_code == 404:
        print(f"ユーザー名が見つかりません。")
        return 0
      elif response.status_code == 400:
        print(f"パスワードが正しくありません。")
        return 0
      
      else:
        print(f"Error: {response.status_code}, データの取得に失敗しました。")
        return 0
    except requests.exceptions.ConnectionError as e:
      retry_count += 1
      print(f"接続エラーが発生しました。リトライ回数: {retry_count}/{max_retries}")
      if retry_count >= max_retries:
          print("最大リトライ回数に達しました。エラーを終了します。")
          raise e
      print(f"{wait_time}秒後にリトライします...")
      time.sleep(wait_time)  # 5分間待機
  # すべてのリトライが失敗した場合のエラーメッセージ
  raise Exception("サーバーへの接続に失敗しました。")

def get_user_data():
  # APIエンドポイントURL
  api_url = "https://meruopetyan.com/api/user-data/"
  # DEBUG
  # api_url = "http://127.0.0.1:8000/api/user-data/"
  max_retries = 3
  retry_count = 0
  wait_time = 300  # 5分（300秒）

  try:
    # ユーザーのnameとpasswordを設定
    conn = sqlite3.connect('user_data.db')
    c = conn.cursor()
    # 最新のユーザーデータを取得
    c.execute("SELECT user_name, password FROM users ORDER BY id DESC LIMIT 1")
    user_data = c.fetchone()
    conn.close()
  except sqlite3.OperationalError as e:
        print(f"ユーザーデータを登録してください。")
        return 2
  if not user_data[0] or not user_data[1]:
    print("ユーザーデータがありません")
    return 2
      
  user_name = user_data[0]
  password = user_data[1]
  # POSTリクエストのペイロード
  data = {
      'name': user_name,
      'password': password
  }

  while retry_count < max_retries:
    try:
      # POSTリクエストを送信してデータを取得
      response = requests.post(api_url, data=data)
      # レスポンスのステータスコードを確認
      if response.status_code == 200:
          # レスポンスのJSONデータを取得
          user_data = response.json()

          # Happymailデータを表示
          # print("Happymailのデータ:")
          # for data in user_data.get('userprofile', []):
          #     print(f"Name: {data['gmail_account']}, ")

          # # PCMaxデータを表示
          # print("PCMaxのデータ:")
          # for data in user_data.get('pcmax', []):
          #     print(f"Name: {data['name']}, ")
          return user_data
      elif response.status_code == 204:
        print(f"有効期限が切れている可能性があります。")
        return 0
      elif response.status_code == 404:
        print(f"ユーザー名が見つかりません。")
        return 0
      elif response.status_code == 400:
        print(f"パスワードが正しくありません。")
        return 0
      
      else:
        print(f"Error: {response.status_code}, データの取得に失敗しました。")
        return 0
    except requests.exceptions.ConnectionError as e:
      retry_count += 1
      print(f"接続エラーが発生しました。リトライ回数: {retry_count}/{max_retries}")
      if retry_count >= max_retries:
          print("最大リトライ回数に達しました。エラーを終了します。")
          raise e
      print(f"{wait_time}秒後にリトライします...")
      time.sleep(wait_time)  # 5分間待機
  # すべてのリトライが失敗した場合のエラーメッセージ
  raise Exception("サーバーへの接続に失敗しました。")

# 文字列を正規化する関数
def normalize_text(text):
    # Unicodeの互換正規化（NFKC）を使って、全角・半角や記号を統一
    return unicodedata.normalize('NFKC', text).replace("\n", "").replace("\r", "").replace(" ", "").replace("　", "").replace("〜", "~")

def change_tor_ip():
  with Controller.from_port(port=9051) as controller:
      controller.authenticate()  # デフォルト設定の場合は認証不要
      controller.signal(Signal.NEWNYM)
