from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
import time
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.select import Select
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import func
import re
from selenium.common.exceptions import TimeoutException
import sqlite3
from selenium.webdriver.chrome.service import Service as ChromeService
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import urllib3



genre_dic = {0:"スグ会いたい", 1:"スグじゃないけど"}
post_area_tokyo = ["千代田区", "中央区", "港区", "新宿区", "文京区", "台東区",
                   "品川区", "目黒区", "大田区", "世田谷区", "渋谷区", "中野区",
                   "杉並区", "豊島区", "北区", "荒川区", "板橋区", "練馬区",
                    "武蔵野市",  
                   ]
post_area_kanagawa = ["横浜市鶴見区", "横浜市神奈川区", "横浜市西区", "横浜市中区", "横浜市南区", "横浜市保土ｹ谷区", 
                      "横浜市磯子区", "横浜市金沢区", "横浜市港北区", "横浜市戸塚区", "横浜市港南区", "横浜市旭区",
                      "横浜市緑区", "横浜市瀬谷区", "横浜市栄区", "横浜市泉区", "横浜市青葉区", "横浜市都筑区", 
                      "川崎市川崎区", "川崎市幸区", "川崎市中原区", "川崎市高津区", "川崎市多摩区", "川崎市宮前区", 
                      "川崎市麻生区",]
post_area_saitama = ["さいたま市西区", "さいたま市北区", "さいたま市大宮区", "さいたま市見沼区", "さいたま市中央区",
                      "さいたま市桜区", "さいたま市浦和区", "さいたま市南区", "さいたま市緑区", "さいたま市岩槻区",
                      "川口市", "戸田市", "和光市",]
post_area_chiba = ["千葉市中央区", "千葉市花見川区", "千葉市稲毛区", "千葉市若葉区",
                    "千葉市緑区", "千葉市美浜区", "市川市", "船橋市",]

post_area_dic = {"東京都":post_area_tokyo, "神奈川県":post_area_kanagawa, "埼玉県":post_area_saitama, "千葉県":post_area_chiba}
# detail_post_area_list = [post_area_tokyo, post_area_kanagawa, post_area_saitama, post_area_chiba]

def login(driver, wait):
  login = None  # login変数の初期化
  try:
    try:
      driver.refresh()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
    except TimeoutException as e:
      print("<<<<<<<リロード>>>>>>>>>>")
      driver.refresh()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
    url = driver.current_url
    if url != "https://pcmax.jp/pcm/index.php":
      driver.get("https://pcmax.jp/pcm/index.php")
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # 利用制限中
    suspend = driver.find_elements(By.CLASS_NAME, value="suspend-title")
    if len(suspend):
      print('利用制限中です')
      return 
    login = driver.find_elements(By.CLASS_NAME, value="login")
    if len(login):    
      login[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
      submit = driver.find_element(By.NAME, value="login")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit)
      submit.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
  except TimeoutException as e:
    print("TimeoutException")
    driver.refresh()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    return login(driver, wait)
  
    
def re_post(name, pcmax_windowhandle, driver, genre_flag):
  wait = WebDriverWait(driver, 15)
  if pcmax_windowhandle:
    handle_array = driver.window_handles
    driver.switch_to.window(pcmax_windowhandle)
  else:
    dbpath = 'firstdb.db'
    conn = sqlite3.connect(dbpath)
    # # SQLiteを操作するためのカーソルを作成
    cur = conn.cursor()
    # # 順番
    # # データ検索
    cur.execute('SELECT login_id, passward, post_title, post_article FROM pcmax WHERE name = ?', (name,))
    for row in cur:
        login_id = row[0]
        login_pass = row[1]
        post_title = row[2]
        post_contents = row[3] 
    driver.delete_all_cookies()
    driver.get("https://pcmax.jp/pcm/file.php?f=login_form")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    wait_time = random.uniform(3, 6)
    time.sleep(2)
    id_form = driver.find_element(By.ID, value="login_id")
    id_form.send_keys(login_id)
    pass_form = driver.find_element(By.ID, value="login_pw")
    pass_form.send_keys(login_pass)
    time.sleep(1)
    send_form = driver.find_element(By.NAME, value="login")
    try:
      send_form.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
    except TimeoutException as e:
      print("TimeoutException")
      driver.refresh()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)
      id_form = driver.find_element(By.ID, value="login_id")
      id_form.send_keys(login_id)
      pass_form = driver.find_element(By.ID, value="login_pw")
      pass_form.send_keys(login_pass)
      time.sleep(1)
      send_form = driver.find_element(By.NAME, value="login")
      send_form.click()
    # 利用制限中
    suspend = driver.find_elements(By.CLASS_NAME, value="suspend-title")
    if len(suspend):
      print(f'{name}pcmax利用制限中です')
      return  
  wait_time = random.uniform(3, 4)
  login(driver, wait)
  # MENUをクリック
  menu = driver.find_element(By.ID, value='sp_nav')
  menu.click()
  time.sleep(wait_time)
  # 掲示板履歴をクリック　
  bulletin_board_history = driver.find_element(By.CLASS_NAME, value="nav-content-list")
  bulletin_board_history = bulletin_board_history.find_elements(By.TAG_NAME, value="dd")
  
  for i in bulletin_board_history:
    if i.text == "投稿履歴・編集":
      bulletin_board_history = i.find_element(By.TAG_NAME, value="a")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", bulletin_board_history)
      bulletin_board_history.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      break
  # 掲示板履歴なし
  no_post = driver.find_elements(By.CLASS_NAME, value="write_text")
  if len(no_post):
    if no_post[0].text == "まだ掲示板への投稿はありません。":
      print(no_post[0].text)
      add_post = driver.find_elements(By.CLASS_NAME, value="white_last")
      add_post_button = add_post[0].find_elements(By.TAG_NAME, value="a")
      add_post_button[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      if genre_flag == 0:
          choices = driver.find_elements(By.CLASS_NAME, value="choice")
          for choice in choices:
            candidate_choice = choice.get_attribute('href')
            if candidate_choice is not None:
                if choice.text == "スグ会いたい":
                  add_post_link = candidate_choice
            else:
                continue
      driver.get(add_post_link)
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time) 
      for kanto_region, kanto_area in post_area_dic.items():
        # # アダルトを選択
        adult = driver.find_element(By.ID, value="genre2")
        adult.click()
        title = driver.find_element(By.ID, value="title1") 
        title.send_keys(post_title)
        time.sleep(1)
        post_text = driver.find_element(By.ID, value="textarea1") 
        post_text.send_keys(post_contents)
        time.sleep(1)
        # 投稿地域を選択
        area = driver.find_element(By.ID, "prech")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", area)
        time.sleep(1)
        select = Select(area)
        select.select_by_visible_text(kanto_region)
        time.sleep(1)
        # 詳細地域を選択
        detailed_area = driver.find_element(By.NAME, value="city_id")
        select = Select(detailed_area)
        detail_area = random.choice(kanto_area)
        print('今回の詳細地域 ~' + str(detail_area) + "~")
        select.select_by_visible_text(detail_area)
        time.sleep(1)
        # メール受付数を変更
        mail_reception = driver.find_element(By.NAME, "max_reception_count")
        select = Select(mail_reception)
        select.select_by_visible_text("5通")
        time.sleep(1)
        # チェック項目にチェック
        today_check = driver.find_element(By.ID, value="bty_4")
        today_check.click()
        ask_date = driver.find_element(By.ID, value="bty_5")
        ask_date.click()
        check3 = driver.find_element(By.ID, value="bty_6")
        check3.click()
        check4 = driver.find_element(By.ID, value="bty_7")
        check4.click()
        check5 = driver.find_element(By.ID, value="bty_8")
        check5.click()
        check6 = driver.find_element(By.ID, value="bty_9")
        check6.click()
        # 掲示板に書く 
        write_bulletin_board = driver.find_element(By.ID, value="bbs_write_btn")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", write_bulletin_board)
        write_bulletin_board.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        # 利用制限チェック
        usage_limit = driver.find_elements(By.CLASS_NAME, value="white_box")
        if len(usage_limit):
          print(f"{name}pcmax利用制限画面が出ました")
          break
        # https://pcmax.jp/pcm/index.php
        driver.get("https://pcmax.jp/pcm/index.php")
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        
        # MENUをクリック
        menu = driver.find_element(By.ID, value='sp_nav')
        menu.click()
        time.sleep(wait_time)
        # 掲示板書き込みをクリック　
        bulletin_board_history = driver.find_element(By.CLASS_NAME, value="nav-content-list")
        bulletin_board_history = bulletin_board_history.find_elements(By.TAG_NAME, value="dd")
        for i in bulletin_board_history:
          if i.text == "掲示板書込み":
            bulletin_board_history = i.find_element(By.TAG_NAME, value="a")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", bulletin_board_history)
            bulletin_board_history.click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(wait_time)
            break
      
      
    
  #掲示板4つ再投稿
  link_list = []
  posts = driver.find_elements(By.CLASS_NAME, value="bbs_posted_wrap")
  if not len(posts):
    return
  for i in range(len(posts)):

    copy = posts[i].find_elements(By.TAG_NAME, value="a")
    for a_element in copy:
      link_text = a_element.text
      if link_text == "コピーする":
        link = a_element.get_attribute("href")
        link_list.append(link)
  for i in link_list:
    driver.get(i)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    detail_selected = driver.find_elements(By.CLASS_NAME, value="back_in_box")
    detail_selected = detail_selected[2].find_element(By.CLASS_NAME, value="item_r")
    detail_selected = detail_selected.text.replace(' ', '')
    
    # 前回の都道府県を取得
    last_area = driver.find_elements(By.CLASS_NAME, value="back_in_box")
    last_area = last_area[1].find_element(By.CLASS_NAME, value="item_r")
    last_area = last_area.text.replace(' ', '')
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(last_area)
    print("前回の詳細地域 ~" + str(detail_selected) + "~" )
    # 編集するをクリック 
    edit_post = driver.find_element(By.ID, value="alink")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", edit_post)
    time.sleep(1)
    edit_post.click()
    wait = WebDriverWait(driver, 15)
    time.sleep(wait_time)
    # ジャンルを選択
    select_genre = driver.find_element(By.ID, value="selectb")
    select = Select(select_genre)
    select.select_by_visible_text(genre_dic[genre_flag])
    time.sleep(1)

    # 投稿地域を選択
    area = driver.find_element(By.ID, "prech")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", area)
    time.sleep(1)
    select = Select(area)
    select.select_by_visible_text(last_area)
    time.sleep(1)
    # 詳細地域を選択
    detailed_area = driver.find_element(By.NAME, value="city_id")
    select = Select(detailed_area)
    try:
      post_area_dic[last_area].remove(detail_selected)
    except ValueError:
      pass
    detail_area = random.choice(post_area_dic[last_area])
    print('今回の詳細地域 ~' + str(detail_area) + "~")
    select.select_by_visible_text(detail_area)
    time.sleep(1)
    # メール受付数を変更
    mail_reception = driver.find_element(By.NAME, "max_reception_count")
    select = Select(mail_reception)
    select.select_by_visible_text("5通")
    time.sleep(1)
    # 掲示板に書く 
    write_bulletin_board = driver.find_element(By.ID, value="bbs_write_btn")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", write_bulletin_board)
    write_bulletin_board.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    # 利用制限チェック
    usage_limit = driver.find_elements(By.CLASS_NAME, value="white_box")
    if len(usage_limit):
      print(f"{name}pcmax利用制限画面が出ました")
      top_logo = driver.find_elements(By.ID, value="top")
      a = top_logo[0].find_element(By.TAG_NAME, value="a")
      a.click()
      time.sleep(wait_time)
      # MENUをクリック
      menu = driver.find_element(By.ID, value='sp_nav')
      menu.click()
      time.sleep(wait_time)
      # 掲示板履歴をクリック　
      bulletin_board_history = driver.find_element(By.CLASS_NAME, value="nav-content-list")
      bulletin_board_history = bulletin_board_history.find_elements(By.TAG_NAME, value="dd")
      for i in bulletin_board_history:
        if i.text == "投稿履歴・編集":
          bulletin_board_history = i.find_element(By.TAG_NAME, value="a")
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", bulletin_board_history)
          bulletin_board_history.click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(wait_time)
          break
      #掲示板4つ再投稿
      link_list = []
      posts = driver.find_elements(By.CLASS_NAME, value="copy_title")
      if not len(posts):
        return
      for i in range(len(posts)):
        copy = posts[i].find_elements(By.TAG_NAME, value="a")
        for a_element in copy:
          link_text = a_element.text
          if link_text == "コピーする":
            link = a_element.get_attribute("href")
            link_list.append(link)
      repost_cnt = 1
      for i in link_list:
        try:
          driver.get(i)
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(wait_time)
        except TimeoutException as e:
          print("TimeoutException")
          driver.refresh()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(wait_time)
        submit = driver.find_element(By.CLASS_NAME, value="write_btn")
        submit.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        print(f"再投稿 {repost_cnt}件")
        repost_cnt += 1
      return
    # 掲示板投稿履歴をクリック
    bulletin_board_history = driver.find_element(By.XPATH, value="//*[@id='wrap']/div[2]/table/tbody/tr/td[3]/a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", bulletin_board_history)
    bulletin_board_history.click()
    time.sleep(1)
  driver.get("https://pcmax.jp/pcm/index.php")
  
def return_footpoint(name, pcmax_windowhandle, driver, return_foot_message, cnt, return_foot_img):
  if cnt == 0:
    return
  wait = WebDriverWait(driver, 15)
  driver.switch_to.window(pcmax_windowhandle)
  wait_time = random.uniform(2, 3)
  time.sleep(1)
  login(driver, wait)
  # 新着メッセージの確認
  have_new_massage_users = []
  new_message = driver.find_element(By.CLASS_NAME, value="message")
  new_message.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  user_info = driver.find_elements(By.CLASS_NAME, value="user_info")
  print(len(user_info))
  # 新着ありのユーザーをリストに追加
  for usr_info in user_info:
    unread = usr_info.find_elements(By.CLASS_NAME, value="unread1")
    if len(unread):
      name = usr_info.find_element(By.CLASS_NAME, value="name").text
      if len(name) > 7:
        name = name[:7] + "…"
      have_new_massage_users.append(name)
  print("新着メッセージリスト")
  print(have_new_massage_users)
  driver.get("https://pcmax.jp/pcm/index.php")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  # 右下のキャラ画像をクリック
  chara_img = driver.find_element(By.XPATH, value="//*[@id='sp_footer']/a[5]")
  chara_img.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # //*[@id="contents"]/div[2]/div[2]/ul/li[5]/a
  # 足あとをクリック
  footpoint = driver.find_element(By.XPATH, value="//*[@id='contents']/div[2]/div[2]/ul/li[5]/a")
  footpoint.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # ページの高さを取得
  last_height = driver.execute_script("return document.body.scrollHeight")
  while True:
    # ページの最後までスクロール
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # ページが完全に読み込まれるまで待機
    time.sleep(1)
    # 新しい高さを取得
    new_height = driver.execute_script("return document.body.scrollHeight")
    # ページの高さが変わらなければ、すべての要素が読み込まれたことを意味する
    if new_height == last_height:
        break
    last_height = new_height
  # ユーザーを取得
  user_list = driver.find_element(By.CLASS_NAME, value="list-content")
  div = user_list.find_elements(By.XPATH, value='./div')
  # リンクを取得
  user_cnt = 1
  mail_history = 0
  send_count = 0
  link_list = []
  while user_cnt <= 40:
    # 新着リストの名前ならスキップ
    name = div[user_cnt].find_element(By.CLASS_NAME, value="user-name")
    if name.text in have_new_massage_users:
      user_cnt += 1
    else:
      a_tags = div[user_cnt].find_elements(By.TAG_NAME, value="a")
      # print("aタグの数：" + str(len(a_tags)))
      if len(a_tags) > 1:
        link = a_tags[1].get_attribute("href")
        # print(link)
        link_list.append(link)
      user_cnt += 1
  for i in link_list:
    if mail_history == 7:
      break
    driver.get(i)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')

    # タイプありがとう
    like_return = driver.find_elements(By.CLASS_NAME, value="tbtn2")
    if len(like_return):
      like_return[0].click()
      time.sleep(2)
    sent = driver.find_elements(By.XPATH, value="//*[@id='profile-box']/div/div[2]/p/a/span")
    if len(sent):
      print('送信履歴があります')
      time.sleep(2)
      mail_history += 1
      continue  
    # 自己紹介文をチェック
    self_introduction = driver.find_elements(By.XPATH, value="/html/body/main/div[4]/div/p")
    if len(self_introduction):
      self_introduction = self_introduction[0].text.replace(" ", "").replace("\n", "")
      if '通報' in self_introduction or '業者' in self_introduction:
        print('自己紹介文に危険なワードが含まれていました')
        refusal_elems = driver.find_elements(By.CLASS_NAME, value="flex_btn_container")
        for candidate_elem in refusal_elems:
          if "お断り" in candidate_elem.text:
            refusal_elem = candidate_elem
            refusal_elem.click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(wait_time)
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
      continue
    time.sleep(1)
    # メッセージをクリック
    message = driver.find_elements(By.ID, value="message1")
    if len(message):
      message[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(3)
    else:
      continue
    # 画像があれば送付
    if return_foot_img:
      picture_icon = driver.find_elements(By.CLASS_NAME, value="mail-menu-title")
      picture_icon[0].click()
      time.sleep(1)
      picture_select = driver.find_element(By.ID, "my_photo")
      select = Select(picture_select)
      select.select_by_visible_text(return_foot_img)
      
    # メッセージを入力
    text_area = driver.find_element(By.ID, value="mdc")
    text_area.send_keys(return_foot_message)
    time.sleep(4)
    print("マジ送信 " + str(maji_soushin) + " ~" + str(send_count + 1) + "~")
    # メッセージを送信
    if maji_soushin:
      send = driver.find_element(By.CLASS_NAME, value="maji_send")
      send.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
      send_link = driver.find_element(By.ID, value="link_OK")
      send_link.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      send_count += 1
      mail_history = 0
      
    else:
      send = driver.find_element(By.ID, value="send_n")
      send.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      send_count += 1
      mail_history = 0

    if send_count == cnt:
      break
  driver.get("https://pcmax.jp/pcm/index.php")

def make_footprints(name, pcmax_id, pcmax_pass, driver, wait, select_areas, youngest_age, oldest_age,):
  driver.delete_all_cookies()
  driver.get("https://pcmax.jp/pcm/file.php?f=login_form")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  wait_time = random.uniform(3, 6)
  time.sleep(2)
  id_form = driver.find_element(By.ID, value="login_id")
  id_form.send_keys(pcmax_id)
  pass_form = driver.find_element(By.ID, value="login_pw")
  pass_form.send_keys(pcmax_pass)
  time.sleep(1)
  send_form = driver.find_element(By.NAME, value="login")
  send_form.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(1)
  # 利用制限中
  suspend = driver.find_elements(By.CLASS_NAME, value="suspend-title")
  if len(suspend):
    print(f'{name}利用制限中です')  
  #プロフ検索をクリック
  footer_icons = driver.find_element(By.ID, value="sp_footer")
  search_profile = footer_icons.find_element(By.XPATH, value="./*[1]")
  search_profile.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(1)
  # 検索条件を設定
  search_elem = driver.find_element(By.ID, value="search1")
  search_elem.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(1)
  # 地域選択
  select_area = driver.find_elements(By.CLASS_NAME, value="pref-select-link")
  if len(select_area):
    select_link = select_area[0].find_elements(By.TAG_NAME, value="a")
    select_link[0].click()
  else:
    # 都道府県の変更、リセット
    reset_area = driver.find_elements(By.CLASS_NAME, value="reference_btn")
    reset_area[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(1)
    reset_area_orange = driver.find_elements(By.CLASS_NAME, value="btn-orange")
    reset_area_orange[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(1)
    ok_button = driver.find_element(By.ID, value="link_OK")
    ok_button.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(1)
    select_area = driver.find_elements(By.CLASS_NAME, value="pref-select-link")
    # たまにエラー
    select_area_cnt = 0
    while not len(select_area):
      time.sleep(1)
      print("select_areaが取得できません")
      select_area = driver.find_elements(By.CLASS_NAME, value="pref-select-link")
      select_area_cnt += 1
      if select_area_cnt == 10:
        break
    select_link = select_area[0].find_elements(By.TAG_NAME, value="a")
    select_link[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(1)
  area_id_dict = {"静岡県":27, "新潟県":13, "山梨県":17, "長野県":18, "茨城県":19, "栃木県":20, "群馬県":21, "東京都":22, "神奈川県":23, "埼玉県":24, "千葉県":25}
  area_ids = []
  for select_area in select_areas:
    if area_id_dict.get(select_area):
      area_ids.append(area_id_dict.get(select_area))
  for area_id in area_ids:
    if 19 <= area_id <= 25:
      region = driver.find_elements(By.CLASS_NAME, value="select-details-area")[1]
    elif 13 <= area_id <= 18:
      region = driver.find_elements(By.CLASS_NAME, value="select-details-area")[2]
    elif 26 <= area_id <= 29:
      region = driver.find_elements(By.CLASS_NAME, value="select-details-area")[4]
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", region)
    check = region.find_elements(By.ID, value=int(area_id))
    time.sleep(1)
    driver.execute_script("arguments[0].click();", check[0])
  save_area = driver.find_elements(By.NAME, value="change")
  time.sleep(1)
  save_area[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(1)
  # 年齢
  if youngest_age:
    if 17 < int(youngest_age) < 59:
      str_youngest_age = youngest_age + "歳"
    elif 60 <= int(youngest_age):
      str_youngest_age = "60歳以上"
    from_age = driver.find_element(By.NAME, value="from_age")
    select_from_age = Select(from_age)
    select_from_age.select_by_visible_text(str_youngest_age)
    time.sleep(1)
  else:
    youngest_age = ""
  if oldest_age:
    if 17 < int(oldest_age) < 59:
      str_oldest_age = oldest_age + "歳"
    elif 60 <= int(oldest_age):
      str_oldest_age = "60歳以上" 
    to_age = driver.find_element(By.ID, "to_age")
    select = Select(to_age)
    select.select_by_visible_text(str_oldest_age)
    time.sleep(1)
  else:
    youngest_age = ""
  

  # ページの高さを取得
  last_height = driver.execute_script("return document.body.scrollHeight")
  while True:
    # ページの最後までスクロール
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # ページが完全に読み込まれるまで待機
    time.sleep(2)
    # 新しい高さを取得
    new_height = driver.execute_script("return document.body.scrollHeight")
    # ページの高さが変わらなければ、すべての要素が読み込まれたことを意味する
    if new_height == last_height:
        break
    last_height = new_height
  # 履歴あり、なしの設定
  mail_history = driver.find_elements(By.CLASS_NAME, value="thumbnail-c")
  check_flag = driver.find_element(By.ID, value="opt3") 
  is_checked = check_flag.is_selected()
  if is_checked:
      print("送信履歴にチェックあり")
  else:
      mail_history[2].click()
      time.sleep(1)
  enter_button = driver.find_elements(By.ID, value="search1")
  enter_button[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  # ページの高さを取得
  last_height = driver.execute_script("return document.body.scrollHeight")
  while True:
    # ページの最後までスクロール
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # ページが完全に読み込まれるまで待機
    time.sleep(2)
    user_list = driver.find_element(By.CLASS_NAME, value="content_inner")
    users = user_list.find_elements(By.XPATH, value='./div')
    # print(len(users))
    if len(users) > 50:
       print('ユーザー件数50　OVER')
       break
    # 新しい高さを取得
    new_height = driver.execute_script("return document.body.scrollHeight")
    # ページの高さが変わらなければ、すべての要素が読み込まれたことを意味する
    if new_height == last_height:
        break
    last_height = new_height
  # https://pcmax.jp/mobile/profile_detail.php?user_id=" + user_id + "&search=prof&condition=648ac5f23df62&page=1&sort=&stmp_counter=13&js=1
  # リンクを取得
  user_cnt = 1
  link_list = []
  for user_cnt in range(len(users)):
    # # 実行確率（80%の場合）
    # execution_probability = 0.80
    # # ランダムな数値を生成し、実行確率と比較
    # if random.random() < execution_probability:
    user_id = users[user_cnt].get_attribute("id")
    if user_id == "loading":
      print('id=loading')
      while user_id != "loading":
        time.sleep(2)
        user_id = users[user_cnt].get_attribute("id")
    link = "https://pcmax.jp/mobile/profile_detail.php?user_id=" + user_id + "&search=prof&condition=648ac5f23df62&page=1&sort=&stmp_counter=13&js=1"
    link_list.append(link)
    # else:
      #  print('無双RUSH終了')
  print(f"ユーザー件数：{len(link_list)}")
  for i, link_url in enumerate(link_list):
      like_flag = False
      driver.get(link_url)
      time.sleep(wait_time)
      # いいね
      # ランダムな数値を生成し、実行確率と比較
      # 実行確率
      # execution_probability = 0.40
      # if random.random() < execution_probability:
      #   like_flag = True
      #   like = driver.find_elements(By.ID, value="type_maru")
      #   like[0].click()
      # time.sleep(wait_time)
      # if like_flag:
      #   print(f"{name}: pcmax、足ペタ件数: {i + 1} いいね")
      # else:
      #   print(f"{name}: pcmax、足ペタ件数: {i + 1}")
      # if i == 21:
      #    break
      print(f"{name}: pcmax、足ペタ件数: {i + 1}")
  driver.refresh()

def send_fst_mail(name, maji_soushin, select_areas, youngest_age, oldest_age, ng_words,):
  options = Options()
  options.add_argument('--headless')
  options.add_argument("--incognito")
  options.add_argument("--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1")
  options.add_argument("--no-sandbox")
  options.add_argument("--window-size=456,912")
  options.add_experimental_option("detach", True)
  options.add_argument("--disable-cache")
  driver = func.get_firefox_driver()
  # service = Service(executable_path="./chromedriver")
  # driver = webdriver.Chrome(service=service, options=options)
  wait = WebDriverWait(driver, 15)
  
  try:
    driver.delete_all_cookies()
    driver.get("https://pcmax.jp/pcm/file.php?f=login_form")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  except TimeoutException as e:
    print("TimeoutException")
    driver.refresh()
  wait_time = random.uniform(2, 5)
  time.sleep(wait_time)
  
  id_form = driver.find_element(By.ID, value="login_id")
  id_form.send_keys(login_id)
  pass_form = driver.find_element(By.ID, value="login_pw")
  pass_form.send_keys(login_pass)
  time.sleep(1)
  send_form = driver.find_element(By.NAME, value="login")
  send_form.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  try:
    send_cnt = 1
    while True:
      # 利用制限中
      suspend = driver.find_elements(By.CLASS_NAME, value="suspend-title")
      if len(suspend):
        print('利用制限中です')
        break
      #プロフ検索をクリック
      footer_icons = driver.find_element(By.ID, value="sp_footer")
      search_profile = footer_icons.find_element(By.XPATH, value="./*[1]")
      search_profile.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # 検索条件を設定
      search_elem = driver.find_element(By.ID, value="search1")
      search_elem.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
      # 地域選択
      select_area = driver.find_elements(By.CLASS_NAME, value="pref-select-link")
      if len(select_area):
        select_link = select_area[0].find_elements(By.TAG_NAME, value="a")
        select_link[0].click()
      else:
        # 都道府県の変更、リセット
        reset_area = driver.find_elements(By.CLASS_NAME, value="reference_btn")
        reset_area[0].click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(1)
        reset_area_orange = driver.find_elements(By.CLASS_NAME, value="btn-orange")
        reset_area_orange[0].click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(1)
        ok_button = driver.find_element(By.ID, value="link_OK")
        ok_button.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(1)
        select_area = driver.find_elements(By.CLASS_NAME, value="pref-select-link")
        select_link = select_area[0].find_elements(By.TAG_NAME, value="a")
        select_link[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
      area_id_dict = {"東京都":22, "神奈川県":23, "埼玉県":24, "千葉県":25}
      area_ids = []
      for select_area in select_areas:
        if area_id_dict.get(select_area):
          area_ids.append(area_id_dict.get(select_area))
      for area_id in area_ids:
        kanto_selects = driver.find_elements(By.CLASS_NAME, value="select-details-area")[1]
        check = kanto_selects.find_elements(By.ID, value=int(area_id))
        time.sleep(1)
        driver.execute_script("arguments[0].click();", check[0])
      save_area = driver.find_elements(By.NAME, value="change")
      time.sleep(1)
      save_area[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
      # 年齢
      if youngest_age:
        if 17 < int(youngest_age) < 59:
          str_youngest_age = youngest_age + "歳"
        elif 60 <= int(youngest_age):
          str_youngest_age = "60歳以上"
        from_age = driver.find_element(By.NAME, value="from_age")
        select_from_age = Select(from_age)
        select_from_age.select_by_visible_text(str_youngest_age)
        time.sleep(1)
      else:
        youngest_age = ""
      if oldest_age:
        if 17 < int(oldest_age) < 59:
          str_oldest_age = oldest_age + "歳"
        elif 60 <= int(oldest_age):
          str_oldest_age = "60歳以上" 
        to_age = driver.find_element(By.ID, "to_age")
        select = Select(to_age)
        select.select_by_visible_text(str_oldest_age)
        time.sleep(1)
      else:
        youngest_age = ""
      # ページの高さを取得
      last_height = driver.execute_script("return document.body.scrollHeight")
      while True:
        # ページの最後までスクロール
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # ページが完全に読み込まれるまで待機
        time.sleep(2)
        # 新しい高さを取得
        new_height = driver.execute_script("return document.body.scrollHeight")
        # ページの高さが変わらなければ、すべての要素が読み込まれたことを意味する
        if new_height == last_height:
            break
        last_height = new_height
      # 履歴あり、なしの設定
      mail_history = driver.find_elements(By.CLASS_NAME, value="thumbnail-c")
      check_flag = driver.find_element(By.ID, value="opt3") 
      is_checked = check_flag.is_selected()
      if not is_checked:
          mail_history[2].click()
          time.sleep(1)
      enter_button = driver.find_elements(By.ID, value="search1")
      enter_button[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      # ユーザーを取得
      user_list = driver.find_element(By.CLASS_NAME, value="content_inner")
      users = user_list.find_elements(By.XPATH, value='./div')
      # ページの高さを取得
      last_height = driver.execute_script("return document.body.scrollHeight")
      while True:
        # ページの最後までスクロール
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # ページが完全に読み込まれるまで待機
        time.sleep(2)
        user_list = driver.find_element(By.CLASS_NAME, value="content_inner")
        users = user_list.find_elements(By.XPATH, value='./div')
        # print(len(users))
        if len(users) > 100:
          #  print('ユーザー件数200　OVER')
          break
        # 新しい高さを取得
        new_height = driver.execute_script("return document.body.scrollHeight")
        # ページの高さが変わらなければ、すべての要素が読み込まれたことを意味する
        if new_height == last_height:
            break
        last_height = new_height
      # ユーザーのhrefを取得
      user_cnt = 1
      link_list = []
      for user_cnt in range(len(users)):
        # 実行確率（80%の場合）
        execution_probability = 0.80
        # ランダムな数値を生成し、実行確率と比較
        if random.random() < execution_probability:
          user_id = users[user_cnt].get_attribute("id")
          if user_id == "loading":
            # print('id=loading')
            while user_id != "loading":
              time.sleep(2)
              user_id = users[user_cnt].get_attribute("id")
          link = "https://pcmax.jp/mobile/profile_detail.php?user_id=" + user_id + "&search=prof&condition=648ac5f23df62&page=1&sort=&stmp_counter=13&js=1"
          link_list.append(link)
      # メール送信
      for i, link_url in enumerate(link_list):
        send_status = True
        driver.get(link_url)
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(1)
        # 名前を取得
        user_name = driver.find_elements(By.CLASS_NAME, value="page_title")
        if len(user_name):
          user_name = user_name[0].text
        else:
          user_name = ""
        # 年齢,活動地域を取得
        profile_data = driver.find_elements(By.CLASS_NAME, value="data")
        span_cnt = 0
        while not len(profile_data):
          time.sleep(1)
          profile_data = driver.find_elements(By.CLASS_NAME, value="data")
          span_cnt += 1
          if span_cnt == 10:
            print("年齢と活動地域の取得に失敗しました")
            break
        if not len(profile_data):
          user_age = ""
          area_of_activity = ""
        else:
          span_elem = profile_data[0].find_elements(By.TAG_NAME, value="span")
          user_age = span_elem[0].text
          area_of_activity = span_elem[1].text 
        # 自己紹介文をチェック
        self_introduction = driver.find_elements(By.XPATH, value="/html/body/main/div[4]/div/p")
        if len(self_introduction):
          self_introduction = self_introduction[0].text.replace(" ", "").replace("\n", "")
          for ng_word in ng_words:
            if ng_word in self_introduction:
              print('自己紹介文に危険なワードが含まれていました')
              time.sleep(wait_time)
              send_status = False
              continue
            if send_status == False:
              break
        # 残ポイントチェック
        if maji_soushin:
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
            continue
          time.sleep(1)
        # メッセージをクリック
        message = driver.find_elements(By.ID, value="message1")
        if len(message):
          # タイムアウト発生
          message[0].click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(3)
        else:
          continue
        # 画像があれば送付
        if fst_message_img:
          picture_icon = driver.find_elements(By.CLASS_NAME, value="mail-menu-title")
          picture_icon[0].click()
          time.sleep(1)
          picture_select = driver.find_element(By.ID, "my_photo")
          select = Select(picture_select)
          select.select_by_visible_text(fst_message_img)
          
        # メッセージを入力
        text_area = driver.find_element(By.ID, value="mdc")
        text_area.send_keys(fst_message)
        time.sleep(4)
        print(str(name) + ": pcmax、マジ送信 " + str(maji_soushin) + " ~" + str(send_cnt) + "~ " + str(user_age) + " " + str(area_of_activity) + " " + str(user_name))
        # メッセージを送信
        if send_status:
          send_cnt += 1
          if maji_soushin:
            send = driver.find_elements(By.CLASS_NAME, value="maji_send")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send[0])
            send[0].click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(1)
            send_link = driver.find_element(By.ID, value="link_OK")
            send_link.click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(wait_time)
          else:
            send = driver.find_element(By.ID, value="send_n")
            send.click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(wait_time)
          time.sleep(wait_time)
        if i == 15:
            break
      try:
        driver.get("https://pcmax.jp/pcm/index.php")
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
      except TimeoutException as e:
        print("TimeoutException")
        driver.refresh()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)

  # 何らかの処理
  except KeyboardInterrupt:
    print("Ctl + c")
    driver.quit()  

def check_new_mail(pcmax_info, driver, wait):
  return_list = []
  login_id = pcmax_info["login_id"]
  login_pass = pcmax_info["password"]
  fst_message = pcmax_info["fst_mail"]
  mail_img = pcmax_info["mail_img"]
  second_message = pcmax_info["second_message"]
  return_foot_message = pcmax_info["return_foot_message"]
  condition_message = pcmax_info["condition_message"]
  mail_address = pcmax_info["mail_address"]
  gmail_password = pcmax_info["gmail_password"]
  
  name = pcmax_info["name"]
  if login_id == None or login_id == "":
    print(f"{name}のpcmaxキャラ情報を取得できませんでした")
    return 1, 0
  try:
    driver.delete_all_cookies()
    driver.get("https://pcmax.jp/pcm/file.php?f=login_form")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  except TimeoutException as e:
    print("TimeoutException")
    driver.refresh()
  except (WebDriverException, urllib3.exceptions.MaxRetryError) as e:
    print(f"接続エラーが発生しました: {e}")
    print("10秒後に再接続します。")
    print(driver.session_id)

    driver.quit()
    time.sleep(10)  # 10秒待機して再試行
    driver, wait = func.get_driver(1)
    
  time.sleep(2)
  id_form = driver.find_element(By.ID, value="login_id")
  id_form.send_keys(login_id)
  pass_form = driver.find_element(By.ID, value="login_pw")
  pass_form.send_keys(login_pass)
  time.sleep(1)
  send_form = driver.find_element(By.NAME, value="login")
  try:
    send_form.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(3)
  except TimeoutException as e:
    print("TimeoutException")
    driver.refresh()
  warning = driver.find_elements(By.CLASS_NAME, value="caution-title")
  warning2 = driver.find_elements(By.CLASS_NAME, value="suspend-title")
  warning3 = driver.find_elements(By.CLASS_NAME, value="mail-setting-title")
  number_lock = driver.find_elements(By.ID, value="content_header2")
  if len(warning) or len(warning2) or len(warning3) or len(number_lock):
    print(f"PCMAX {name}に警告画面が出ている可能性があります")
    # return_list.append(f"{name}pcmaxに警告画面が出ている可能性があります")
    if len(return_list):
      return return_list, 0
    else:
      return 1, 0
  # 新着があるかチェック
  have_new_massage_users = []
  new_message_elem = driver.find_elements(By.CLASS_NAME, value="message")
  if len(new_message_elem):
    new_message = new_message_elem[0]
  else:
    new_message = ""
    # print('新着メール取得に失敗しました')
  # if 1 == 1: #dev
  if new_message:
    # if 1 == 1: #dev
    if new_message.text[:2] == "新着":
      # print('新着があります')
      message = driver.find_elements(By.CLASS_NAME, value="message")[0]
      message.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)
      # 未読だけを表示
      new_message_display = driver.find_elements(By.CLASS_NAME, value="msg-display_change")
      new_message_display[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)
      # 新着ありのユーザーをリストに追加
      message_list = driver.find_elements(By.CLASS_NAME, value="receive_user")
      for usr_info in message_list:
          new_mail_user = usr_info.find_element(By.CLASS_NAME, value="name").text
          if len(new_mail_user) > 7:
            new_mail_user = new_mail_user[:7] + "…"
          have_new_massage_users.append(new_mail_user)
      print(f"新着メッセージ数 {len(message_list)}")
      # メッセージ一覧を取得      
      while len(message_list):
        try:
            message_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "receive_user")))   
        except TimeoutException:
            print("タイムアウトしました")
            break
        arrival_date = message_list[-1].find_elements(By.CLASS_NAME, value="date")
        date_numbers = re.findall(r'\d+', arrival_date[0].text)
        # datetime型を作成
        arrival_datetime = datetime(int(date_numbers[0]), int(date_numbers[1]), int(date_numbers[2]), int(date_numbers[3]), int(date_numbers[4])) 
        now = datetime.today()
        elapsed_time = now - arrival_datetime
        # print(f"メール到着からの経過時間{elapsed_time}")
        if elapsed_time >= timedelta(minutes=4):
          # print("4分以上経過しています。")
          taikai = False
          # dev
          # user_photo = message_list[5].find_element(By.CLASS_NAME, value="user_photo")
          try:
            element = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "receive_user")))
          except TimeoutException:
              print("要素が見つかりませんでした。")
          user_photo = element[-1].find_element(By.CLASS_NAME, value="user_photo")
          # 退会してるか判定
          out = element[-1].find_elements(By.CLASS_NAME, value="out")
          
          if len(out):
            next_element = element[-1].find_elements(By.XPATH, value='following-sibling::*')
            script_code = next_element[0].get_attribute("innerHTML")
            # 取得したJavaScriptコードを表示
            # 正規表現パターン
            pattern = r"mail_recive_detail\.php\?mail_id=(.*?);"
            match = re.search(pattern, script_code)
            result = match.group(1)
            print(result)
            
            taikai_user_url = f"https://pcmax.jp/mobile/mail_recive_detail.php?mail_id={result}"
            driver.get(taikai_user_url)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            driver.get("https://pcmax.jp/mobile/mail_recive_list.php?receipt_status=0")
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            continue
          user_link = user_photo.find_element(By.TAG_NAME, value="a").get_attribute("href")
          start_index = user_link.find("user_id=")
          # print(777)
          # print(start_index)
          if start_index != -1:
              user_id = user_link[start_index + len("user_id="):]
              # print("取得した文字列:", user_id)
          elif "void" in str(start_index):
            user_page = user_photo.find_element(By.TAG_NAME, value="a")
            if user_page.is_enabled():
              driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", user_page)
              user_page.click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(2)
              driver.back()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(2)
              # 未読だけを表示
              new_message_display = driver.find_elements(By.CLASS_NAME, value="msg-display_change")
              new_message_display[0].click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(2)
              # メッセージ一覧を取得
              message_list = driver.find_elements(By.CLASS_NAME, value="receive_user")
              continue
          else:
              # user info にIDが載ってる　i1167384264
              # https://pcmax.jp/mobile/mail_recive_detail.php?mail_id=1167384264&user_id=16164934
              print("user_idが見つかりませんでした。")
              if len(element):
                user_photo = element[-1].find_element(By.CLASS_NAME, value="user_photo")
                user_link = user_photo.find_element(By.TAG_NAME, value="a").get_attribute("href")
                start_index = user_link.find("user_id=")
                print(type(start_index))
                # print(start_index)
                if start_index != -1:
                  user_id = user_link[start_index + len("user_id="):]
                  # print("取得した文字列:", user_id)
                  taikai = False
                else:
                  taikai = True
          try:
            message_list = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "receive_user")))   
          except TimeoutException:
              print("要素が見つかりませんでした。")
              break
          #dev # mail_id = message_list[5].find_element(By.TAG_NAME, value="input").get_attribute("value")
          mail_id = message_list[-1].find_element(By.TAG_NAME, value="input").get_attribute("value")
          new_mail_link = "https://pcmax.jp/mobile/mail_recive_detail.php?mail_id=" + str(mail_id) + "&user_id=" + str(user_id)
          driver.get(new_mail_link)
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(3)
          all_mail = driver.find_elements(By.ID, value="all_mail")
          if len(all_mail):
            all_mail[0].click()
            time.sleep(1)
            sent_by_me = driver.find_elements(By.CLASS_NAME, value="right_balloon_w")
            sent_by_me_maji = driver.find_elements(By.CLASS_NAME, value="right_balloon-maji")
          else:
            sent_by_me = driver.find_elements(By.CLASS_NAME, value="right_balloon_w")
            sent_by_me_maji = driver.find_elements(By.CLASS_NAME, value="right_balloon-maji")
          no_history_second_mail = True
          # 受信メッセージにメールアドレスが含まれているか
          received_mail_elem = driver.find_elements(By.CLASS_NAME, value="left_balloon_m")
          if len(received_mail_elem):
            received_mail = received_mail_elem[-1].text
          else:
            received_mail = ""
          
          # ＠を@に変換する
          if "＠" in received_mail:
            received_mail = received_mail.replace("＠", "@")

          # メールアドレスを抽出する正規表現
          email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
          # email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
          email_list = re.findall(email_pattern, received_mail)
          if email_list:
            # print("メールアドレスが含まれています")
            # print(email_list)
            # print(name)

            # icloudの場合
            if "icloud.com" in received_mail:
              print("icloud.comが含まれています")
              icloud_text = "メール送ったんですけど、ブロックされちゃって届かないのでこちらのアドレスにお名前添えて送ってもらえますか？"
              icloud_text = icloud_text + "\n" + mail_address
              text_area = driver.find_elements(By.ID, value="mdc")
              if len(text_area):
                script = "arguments[0].value = arguments[1];"
                driver.execute_script(script, text_area[0], icloud_text)
                # text_area[0].send_keys(icloud_text)
                time.sleep(4)
                send = driver.find_element(By.ID, value="send_n")
                send.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(2)
                # 連続防止で失敗
                waiting = driver.find_elements(By.CLASS_NAME, value="banned-word")
                if len(waiting):
                  print("<<<<<<<<<<<<<<<<<<<連続防止で失敗>>>>>>>>>>>>>>>>>>>>")
                  time.sleep(6)
                  send = driver.find_element(By.ID, value="send_n")
                  send.click()
                  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                  time.sleep(2)
              # 戻って見ちゃいや登録
              back = driver.find_element(By.ID, value="back3")
              back.click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(2)
            else:
              name_elem = driver.find_elements(By.CLASS_NAME, value="content_header_center")
              user_name = name_elem[0].text
              for user_address in email_list:
                site = "pcmax"
                func.send_conditional(user_name, user_address, mail_address, gmail_password, condition_message, site)
                print("アドレス内1stメールを送信しました")
            # 見ちゃいや登録
            latest_mail = driver.find_element(By.ID, value="dlink")
            latest_mail.click()
            time.sleep(2)
            dont_look_elems= driver.find_elements(By.CLASS_NAME, value="line-menu-inbox")
            dont_look = None
            for dont_look_elem in dont_look_elems:
              if "見ちゃいや" in dont_look_elem.text:
                dont_look = dont_look_elem
            if dont_look:
              driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", dont_look)
              time.sleep(1)
              dont_look.click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(1)
            dont_look_registration = driver.find_elements(By.CLASS_NAME, value="del")
            if len(dont_look_registration):
              dont_look_registration[0].click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            driver.get("https://pcmax.jp/mobile/mail_recive_list.php?receipt_status=0")
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(2)
            
            continue

            # received_mail_elem = driver.find_elements(By.CLASS_NAME, value="left_balloon_m")
            # received_mail = received_mail_elem[-1].text
            # return_message = f"{name}pcmax,{user_name}:{received_mail}"
            # print(return_message)
            # return_list.append(return_message)
            # no_history_second_mail = False
          
          # メッセージ送信一件もなし
          elif len(sent_by_me) == 0 and len(sent_by_me_maji) == 0:
            text_area = driver.find_elements(By.ID, value="mdc")
            if len(text_area):
              script = "arguments[0].value = arguments[1];"
              driver.execute_script(script, text_area[0], fst_message)
              # text_area[0].send_keys(fst_message)
              time.sleep(6)
              send = driver.find_element(By.ID, value="send_n")
              send.click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(2)
              # 連続防止で失敗
              waiting = driver.find_elements(By.CLASS_NAME, value="banned-word")
              if len(waiting):
                print("<<<<<<<<<<<<<<<<<<<連続防止で失敗>>>>>>>>>>>>>>>>>>>>")
                time.sleep(6)
                send = driver.find_element(By.ID, value="send_n")
                send.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(2)
          # メッセージ送信一件だけ
          elif len(sent_by_me) == 1 or len(sent_by_me_maji) == 1:
            sent_by_me_list = []
            if len(sent_by_me):
              for sent_list in sent_by_me:
                sent_by_me_list.append(sent_list)
            elif len(sent_by_me_maji):
              for sent_list in sent_by_me_maji:
                sent_by_me_list.append(sent_list)
            for send_my_text in sent_by_me_list:
              # second_mailを既に送っているか
              if send_my_text.text == second_message:
                # print("second_mail履歴あり")
                name_elem = driver.find_elements(By.CLASS_NAME, value="content_header_center")
                user_name = name_elem[0].text
                received_mail_elem = driver.find_elements(By.CLASS_NAME, value="left_balloon_m")
                received_mail = received_mail_elem[-1].text
                return_message = f"{name}pcmax,{login_id}:{login_pass}\n{user_name}「{received_mail}」"
                return_list.append(return_message)
                no_history_second_mail = False
            # secondメッセージを入力
            if no_history_second_mail:
              text_area = driver.find_elements(By.ID, value="mdc")
              if len(text_area):
                script = "arguments[0].value = arguments[1];"
                driver.execute_script(script, text_area[0], second_message)
                # text_area[0].send_keys(second_message)
                time.sleep(6)
                send = driver.find_element(By.ID, value="send_n")
                send.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(2)
                # 連続防止で失敗
                waiting = driver.find_elements(By.CLASS_NAME, value="banned-word")
                if len(waiting):
                  print("<<<<<<<<<<<<<<<<<<<連続防止で失敗>>>>>>>>>>>>>>>>>>>>")
                  time.sleep(6)
                  send = driver.find_element(By.ID, value="send_n")
                  send.click()
                  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                  time.sleep(2)

          elif func.normalize_text(second_message) == func.normalize_text(sent_by_me[-1].text):
            # 受信メールにアドレスがあるか
            print('やり取り中')
            print(sent_by_me[-1].text)
            name_elem = driver.find_elements(By.CLASS_NAME, value="content_header_center")
            user_name = name_elem[0].text
            # print(user_name)
            # print(received_mail)
            return_message = f"{name}pcmax,{login_id}:{login_pass}\n{user_name}「{received_mail}」"
            return_list.append(return_message)
       
          # https://pcmax.jp/mobile/mail_recive_list.php?receipt_status=0
          driver.get("https://pcmax.jp/mobile/mail_recive_list.php?receipt_status=0")
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(2)
          # メッセージ一覧を取得
          message_list = driver.find_elements(By.CLASS_NAME, value="receive_user")
        else:
          break
  # 足跡返し
  try:
    driver.get("https://pcmax.jp/pcm/index.php")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  except TimeoutException as e:
    print("TimeoutException")
    driver.refresh()
  time.sleep(2)
  warning = driver.find_elements(By.CLASS_NAME, value="caution-title")
  warning2 = driver.find_elements(By.CLASS_NAME, value="suspend-title")
  warning3 = driver.find_elements(By.CLASS_NAME, value="setting-title")
  if len(warning) or len(warning2) or len(warning3):
    print(f"{name}pcmaxに警告画面が出ている可能性があります")
    # return_list.append(f"{name}pcmaxに警告画面が出ている可能性があります")
    if len(return_list):
      return return_list, 0
    else:
      return 1, 0
  # 右下のキャラ画像をクリック
  chara_img = driver.find_elements(By.XPATH, value="//*[@id='sp_footer']/a[5]")
  reload_cnt = 1
  while not len(chara_img):
    time.sleep(5)
    # print("右下のキャラ画像が見つかりません")
    chara_img = driver.find_elements(By.XPATH, value="//*[@id='sp_footer']/a[5]")
    reload_cnt += 1
    if reload_cnt == 5:
      break
  chara_img[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  # //*[@id="contents"]/div[2]/div[2]/ul/li[5]/a
  # 足あとをクリック
  footpoint = driver.find_element(By.CLASS_NAME, value="visit1")
  # footpoint = driver.find_element(By.XPATH, value="//*[@id='contents']/div[2]/div[2]/ul/li[5]/a")
  footpoint.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  # ページの高さを取得
  last_height = driver.execute_script("return document.body.scrollHeight")
  while True:
    # ページの最後までスクロール
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # ページが完全に読み込まれるまで待機
    time.sleep(1)
    
    # ユーザーを取得
    user_list = driver.find_element(By.CLASS_NAME, value="list-content")
    div = user_list.find_elements(By.XPATH, value='./div')
    if len(div) > 40:
      # print(666)
      # print(len(div))
      break
    # 新しい高さを取得
    new_height = driver.execute_script("return document.body.scrollHeight")
    # ページの高さが変わらなければ、すべての要素が読み込まれたことを意味する
    if new_height == last_height:
      break
    last_height = new_height
  # リンクを取得
  user_cnt = 1
  mail_history = 0
  send_count = 0
  link_list = []
  while user_cnt < len(div):
    # 新着リストの名前ならスキップ
    span= div[user_cnt].find_elements(By.TAG_NAME, value="span")
    user_name = ""
    for i in span:
      if i.get_attribute("class") == "user-name":
        user_name = i.text    
    like = div[user_cnt].find_elements(By.CLASS_NAME, value="type1")
    # name = div[user_cnt].find_element(By.CLASS_NAME, value="user-name")
    # print(1111111111111111)
    # print(user_name)
    if user_name in have_new_massage_users:
      # print('新着リストのユーザーです')
      user_cnt += 1
    elif not len(like):
      user_cnt += 1
    else:
      a_tags = div[user_cnt].find_elements(By.TAG_NAME, value="a")
      # print("aタグの数：" + str(len(a_tags)))
      if len(a_tags) > 1:
        link = a_tags[1].get_attribute("href")
        # print(link)
        link_list.append(link)
      user_cnt += 1
  # print(len(link_list))
  for i in link_list:
    # if mail_history == 7:
    #   break
    driver.get(i)
    # //*[@id="profile-box"]/div/div[2]/p/a/span
    sent = driver.find_elements(By.XPATH, value="//*[@id='profile-box']/div/div[2]/p/a/span")
    if len(sent):
      # print('送信履歴があります')
      # いいねする
      with_like = driver.find_elements(By.CLASS_NAME, value="type1")
      if len(with_like):
        with_like[0].click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(1)
      time.sleep(2)
      mail_history += 1
      continue  
    # 自己紹介文をチェック
    self_introduction = driver.find_elements(By.XPATH, value="/html/body/main/div[4]/div/p")
    if len(self_introduction):
      self_introduction = self_introduction[0].text.replace(" ", "").replace("\n", "")
      if '通報' in self_introduction or '業者' in self_introduction:
        print('自己紹介文に危険なワードが含まれていました')
        # お断り登録
        refusal_elems = driver.find_elements(By.CLASS_NAME, value="flex_btn_container")
        refusal_elems = refusal_elems[0].find_elements(By.TAG_NAME, value="a")
        refusal_elem = ""
        for candidate_elem in refusal_elems:
          if "お断り" in candidate_elem.text:
            refusal_elem = candidate_elem
        if refusal_elem:
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", refusal_elem)
          time.sleep(1)
          refusal_elem.click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(2)
          refusal_registration = driver.find_elements(By.CLASS_NAME, value="del")
          refusal_registration[0].click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(2)
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
      time.sleep(4)
      continue
    time.sleep(1)
    # いいねする
    with_like = driver.find_elements(By.CLASS_NAME, value="type1")
    if len(with_like):
      time.sleep(1)
      with_like[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(1)
    # メッセージをクリック
    message = driver.find_elements(By.ID, value="message1")
    if len(message):
      message[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(3)
    else:
      continue
    # 画像があれば送付
    if mail_img:
      picture_icon = driver.find_elements(By.CLASS_NAME, value="mail-menu-title")
      picture_icon[0].click()
      time.sleep(1)
      picture_select = driver.find_element(By.ID, "my_photo")
      select = Select(picture_select)
      select.select_by_visible_text(mail_img)
      
    # メッセージを入力
    text_area = driver.find_element(By.ID, value="mdc")
    script = "arguments[0].value = arguments[1];"
    driver.execute_script(script, text_area, return_foot_message)
    # text_area.send_keys(return_foot_message)
    time.sleep(6)
    # print("マジ送信 " + str(maji_soushin) + " ~" + str(send_count + 1) + "~")
    print(f"{name}pcmax 足跡返し マジ送信:{maji_soushin} {send_count + 1}件送信")

    # メッセージを送信
    if maji_soushin:
      send = driver.find_element(By.CLASS_NAME, value="maji_send")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send)
      # send.click()
      driver.execute_script("arguments[0].click();", send)
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)
      send_link = driver.find_elements(By.ID, value="link_OK")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_link[0])
      send_link[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)
      send_count += 1
      mail_history = 0
      
    else:
      send = driver.find_element(By.ID, value="send_n")
      send.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(2)
      send_count += 1
      mail_history = 0
  # if send_count:
  #   return_list.append(f'{name}pcmax 足跡返し{send_count}件')

  if len(return_list):
    return return_list, send_count
  else:
    return 1, send_count

  
def re_registration(name, driver):
  print(name)
  wait = WebDriverWait(driver, 15)  
  dbpath = 'firstdb.db'
  conn = sqlite3.connect(dbpath)
  # # SQLiteを操作するためのカーソルを作成
  cur = conn.cursor()
  # # 順番
  # # データ検索
  cur.execute('SELECT * FROM pcmax WHERE name = ?', (name,))
  for row in cur:
      print(6666)
      print(row)
      login_id = row[2]
      login_pass = row[3]
      date_of_birth = row[13]
      self_promotion = row[14]
      height = row[15]
      body_shape = row[16]
      blood_type = row[17]
      activity_area = row[18]
      detail_activity_area = row[19]
      profession = row[20]
      freetime = row[21]
      car_ownership = row[22]
      smoking = row[23]
      ecchiness_level = row[24]
      sake = row[25]
      process_before_meeting = row[26]
      first_date_cost = row[27]

  driver.delete_all_cookies()
  driver.get("https://pcmax.jp/pcm/file.php?f=login_form")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  wait_time = random.uniform(4, 6)
  time.sleep(2)
  id_form = driver.find_element(By.ID, value="login_id")
  id_form.send_keys(login_id)
  pass_form = driver.find_element(By.ID, value="login_pw")
  pass_form.send_keys(login_pass)
  time.sleep(1)
  send_form = driver.find_element(By.NAME, value="login")
  try:
    send_form.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(1)
  except TimeoutException as e:
    print("TimeoutException")
    driver.refresh()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    id_form = driver.find_element(By.ID, value="login_id")
    id_form.send_keys(login_id)
    pass_form = driver.find_element(By.ID, value="login_pw")
    pass_form.send_keys(login_pass)
    time.sleep(1)
    send_form = driver.find_element(By.NAME, value="login")
    send_form.click()
  # 利用制限中
  suspend = driver.find_elements(By.CLASS_NAME, value="suspend-title")
  if len(suspend):
    print(f'{name}pcmax利用制限中です')
    return  
  wait_time = random.uniform(4,5)
  login(driver, wait)
  # MENUをクリック
  menu = driver.find_element(By.ID, value='sp_nav')
  menu.click()
  time.sleep(wait_time)
  # プロフィール編集をクリック　
  bulletin_board_history = driver.find_element(By.CLASS_NAME, value="nav-content-list")
  bulletin_board_history = bulletin_board_history.find_elements(By.TAG_NAME, value="dd")
  for i in bulletin_board_history:
    if i.text == "プロフィール編集":
      edit_profile = i.find_element(By.TAG_NAME, value="a")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", edit_profile)
      edit_profile.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      break
  # 名前を変更
  info_change = driver.find_elements(By.CLASS_NAME, value="info_change")
  name_change = info_change[0].find_elements(By.TAG_NAME, value="a")[0]
  name_change.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  nick_name = driver.find_elements(By.CLASS_NAME, value="textbox")
  nick_name[0].clear()
  nick_name[0].send_keys(name)
  time.sleep(2)
  set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
  set_button[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 生年月日を変更
  info_change = driver.find_elements(By.CLASS_NAME, value="info_change")
  birthdate_change = info_change[0].find_elements(By.TAG_NAME, value="a")[1]
  birthdate_change.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  birth_date = driver.find_elements(By.CLASS_NAME, value="textbox")
  birth_date[0].clear()
  birth_date[0].send_keys(date_of_birth)
  time.sleep(2)
  set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
  set_button[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 自己PR
  if self_promotion:
    print("自己紹介ぶん")
  # 身長
  prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
  height_link = prof_list[0].find_elements(By.TAG_NAME, value="a")
  driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", height_link[0])
  time.sleep(1)
  height_link[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  height_select = driver.find_elements(By.CLASS_NAME, value="s_select")
  select = Select(height_select[0])
  select.select_by_value(height)
  time.sleep(1)
  set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
  set_button[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 体型
  if body_shape:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    body_shape_link = prof_list[1].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", body_shape_link[0])
    time.sleep(1)
    body_shape_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    body_shape_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(body_shape_select[0])
    select.select_by_visible_text(body_shape)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 血液型
  if blood_type:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    blood_type_link = prof_list[2].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", blood_type_link[0])
    time.sleep(1)
    blood_type_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    blood_type_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(blood_type_link_select[0])
    select.select_by_visible_text(blood_type)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 活動エリア
  prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
  activity_area_link = prof_list[5].find_elements(By.TAG_NAME, value="a")
  driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", activity_area_link[0])
  time.sleep(1)
  activity_area_link[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  activity_area_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
  select = Select(activity_area_link_select[0])
  select.select_by_visible_text(activity_area)
  time.sleep(1)
  set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
  set_button[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 活動詳細エリア
  if detail_activity_area:
    # prech
    activity_area_link_select = driver.find_elements(By.ID, value="prech")
    select = Select(activity_area_link_select[0])
    select.select_by_visible_text(activity_area)
    time.sleep(2)
    detail_activity_area_link_select = driver.find_elements(By.ID, value="city_id_1")
    select = Select(detail_activity_area_link_select[0])
    select.select_by_visible_text(detail_activity_area)
  time.sleep(1)
  set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
  set_button[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 職業
  if profession:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    profession_link = prof_list[6].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", profession_link[0])
    time.sleep(1)
    profession_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    profession_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(profession_link_select[0])
    select.select_by_visible_text(profession)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)

  # ヒマな時間帯
  if freetime:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    freetime_link = prof_list[9].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", freetime_link[0])
    time.sleep(1)
    freetime_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    freetime_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(freetime_link_select[0])
    select.select_by_visible_text(freetime)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 車の所有
  if car_ownership:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    car_ownership_link = prof_list[10].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", car_ownership_link[0])
    time.sleep(1)
    car_ownership_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    car_ownership_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(car_ownership_link_select[0])
    select.select_by_visible_text(car_ownership)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 喫煙
  if smoking:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    smoking_link = prof_list[11].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", smoking_link[0])
    time.sleep(1)
    smoking_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    smoking_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(smoking_link_select[0])
    select.select_by_visible_text(smoking)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # エッチ度
  if ecchiness_level:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    ecchiness_level_link = prof_list[12].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", ecchiness_level_link[0])
    time.sleep(1)
    ecchiness_level_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    ecchiness_level_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(ecchiness_level_link_select[0])
    select.select_by_visible_text(ecchiness_level)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # お酒
  if sake:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    sake_link = prof_list[13].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", sake_link[0])
    time.sleep(1)
    sake_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    sake_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(sake_link_select[0])
    select.select_by_visible_text(sake)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 会うまでのプロセス
  if process_before_meeting:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    process_before_meeting_link = prof_list[14].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", process_before_meeting_link[0])
    time.sleep(1)
    process_before_meeting_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    process_before_meeting_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(process_before_meeting_link_select[0])
    select.select_by_visible_text(process_before_meeting)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 初回デート費用
  if first_date_cost:
    prof_list = driver.find_elements(By.CLASS_NAME, value="prof_lst")
    first_date_cost_link = prof_list[15].find_elements(By.TAG_NAME, value="a")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", first_date_cost_link[0])
    time.sleep(1)
    first_date_cost_link[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    first_date_cost_link_select = driver.find_elements(By.CLASS_NAME, value="s_select")
    select = Select(first_date_cost_link_select[0])
    select.select_by_visible_text(first_date_cost)
    time.sleep(1)
    set_button = driver.find_elements(By.CLASS_NAME, value="basic_btn")
    set_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 旅行・宿泊
  # 出身地
  # 学歴
  # 年収
  # 同居人
  # 結婚
  # 子供
  # 家事・育児
  # 社交性

  registration_button = driver.find_elements(By.CLASS_NAME, value="btn")
  registration_button[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)

  