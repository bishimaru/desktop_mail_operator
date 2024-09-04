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
import traceback
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import func
from selenium.webdriver.support.select import Select
import sqlite3
import re
from datetime import datetime, timedelta
import difflib
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
import base64
import json


# 警告画面
def catch_warning_screen(driver):
  wait = WebDriverWait(driver, 15)
  anno = driver.find_elements(By.CLASS_NAME, value="anno")
  warning = driver.find_elements(By.CLASS_NAME, value="warning screen")
  dialog = driver.find_elements(By.ID, value="_information_dialog")
  remodal = driver.find_elements(By.CLASS_NAME, value="remodal-image")
  warinig_cnt =0
  while len(warning) or len(anno) or len(dialog) or len(remodal):
    driver.refresh()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    warning = driver.find_elements(By.CLASS_NAME, value="warning screen")
    anno = driver.find_elements(By.CLASS_NAME, value="anno")
    dialog = driver.find_elements(By.ID, value="_information_dialog")
    remodal = driver.find_elements(By.CLASS_NAME, value="remodal-image")
    warinig_cnt += 1
    if warinig_cnt > 2:
       return True
  return False
   
def re_post(name,  driver, wait, title, post_text):
  area_list = ["東京都", "千葉県", "埼玉県", "神奈川県", "栃木県", "静岡県"]
  repost_flug_list = []  
  wait_time = random.uniform(2, 3)
  # TOPに戻る
  driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
  driver.delete_cookie("outbrain_cid_fetch")
  # 警告画面が出たらスキップ
  warning_flug = catch_warning_screen(driver)
  if warning_flug:
     print(f"{name}：警告画面が出ている可能性があります")
     return False
  
  # マイページをクリック
  nav_list = driver.find_element(By.ID, value='ds_nav')
  mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
  try:
    mypage.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  except ElementClickInterceptedException as e:
    print(f"{name}:警告画面が出ている可能性があります")
    return
  # マイリストをクリック
  common_list = driver.find_element(By.CLASS_NAME, "ds_common_table")
  common_table = common_list.find_elements(By.CLASS_NAME, "ds_mypage_text")
  for common_table_elem in common_table:
     if "マイリスト" in common_table_elem.text:
        mylist = common_table_elem
  driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", mylist)
  time.sleep(wait_time)
  mylist.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # 掲示板履歴をクリック
  menu_list = driver.find_element(By.CLASS_NAME, "ds_menu_link_list")
  menu_link = menu_list.find_elements(By.CLASS_NAME, "ds_next_arrow")
  bulletin_board_history = menu_link[4]
  bulletin_board_history.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  warning_flug = catch_warning_screen(driver)
  #その他掲示板をクリック
  link_tab = driver.find_elements(By.CLASS_NAME, "ds_link_tab_text")
  others_bulletin_board = link_tab[1]
  others_bulletin_board.click()
  time.sleep(1)
 
  # ジャンル選択
  genre_dict = {0:"今すぐ会いたい", 1:"大人の出会い"}  
  genre = driver.find_elements(By.CLASS_NAME, value="ds_bd_none")
  road_cnt = 1
  while len(genre) <= 2:
     time.sleep(2)
     genre = driver.find_elements(By.CLASS_NAME, value="ds_bd_none")
     road_cnt += 1
     if road_cnt == 7:
        break
  genre = genre[1].text
  print("<<<再投稿する掲示板のジャンル取得>>>")
  print(genre)
  # 1日に書き込めるのは五回まで
 
    # for i, kanto in enumerate(area_list):
    #   # 掲示板重複を削除する
    #   driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    #   time.sleep(2)
    #   area_texts = driver.find_elements(By.CLASS_NAME, value="ds_write_bbs_status")
    #   area_texts_list = []
    #   for area in area_texts:
    #     shaping_area = area.text.replace(" ", "").replace("\n", "")
    #     area_texts_list.append(shaping_area)
    #   area_cnt = 0
    #   list = []
    #   for area_text in area_texts_list:
    #     if area_text not in list:
    #         list.append(area_text)
    #         area_cnt += 1
    #     else:
    #         print("重複があった")
    #         duplication_area = driver.find_elements(By.CLASS_NAME, value="ds_round_btn_red")[area_cnt]
    #         driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", duplication_area)
    #         time.sleep(2)
    #         duplication_area.click()
    #         wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #         time.sleep(wait_time)
    #         delete = driver.find_element(By.CLASS_NAME, "modal-confirm")
    #         delete.click()
    #         time.sleep(2)

    #   #  掲示板をクリック
    #   nav_list = driver.find_element(By.ID, value='ds_nav')
    #   bulletin_board = nav_list.find_element(By.LINK_TEXT, "募集")
    #   bulletin_board.click()
    #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #   time.sleep(wait_time)
    #   # 書き込みをクリック
    #   write = driver.find_element(By.CLASS_NAME, value="icon-header_kakikomi")
    #   write.click()
    #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #   time.sleep(wait_time)
    #   # 書き込み上限に達したらスキップ
    #   adult = driver.find_elements(By.CLASS_NAME, value="remodal-wrapper")
    #   print(len(adult))
    #   if len(adult):
    #       print("24時間以内の掲示板書き込み回数の上限に達しています(1日5件まで)")
    #       cancel = driver.find_element(By.CLASS_NAME, value="modal-cancel")
    #       cancel.click()
    #       driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
    #       continue
    #   # その他掲示板をクリック
    #   link_tab = driver.find_elements(By.CLASS_NAME, "ds_link_tab_text")
    #   others_bulletin_board = link_tab[1]
    #   others_bulletin_board.click()
    #   time.sleep(2)
    #   # ジャンルを選択
    #   select_genre = driver.find_element(By.ID, value="keijiban_adult_janl")
    #   select = Select(select_genre)
    #   select.select_by_visible_text(genre_dict[genre_flag])
    #   time.sleep(1)
    #   # タイトルを書き込む
    #   input_title = driver.find_element(By.NAME, value="Subj")
    #   driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", input_title)
    #   input_title.send_keys(title)
    #   time.sleep(1)
    #   # 本文を書き込む
    #   text_field = driver.find_element(By.ID, value="text-message")
    #   driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_field)
    #   text_field.send_keys(post_text)
    #   time.sleep(1)
    #   # 書き込みエリアを選択
    #   select_area = driver.find_element(By.NAME, value="wrtarea")
    #   select = Select(select_area)
    #   select.select_by_visible_text(kanto)
    #   time.sleep(1)
    #   mail_rep =driver.find_element(By.NAME, value="Rep")
    #   select = Select(mail_rep)
    #   select.select_by_visible_text("10件")
    #   time.sleep(1)
    #   # 書き込む
    #   writing = driver.find_element(By.ID, value="billboard_submit")
    #   writing.click()
    #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #   time.sleep(wait_time)
    #   # 書き込み成功画面の判定
    #   success = driver.find_elements(By.CLASS_NAME, value="ds_keijiban_finish")
    #   if len(success):
    #     print(f"{name}: {i + 1} の書き込みに成功しました")
    #     # マイページをクリック
    #     nav_list = driver.find_element(By.ID, value='ds_nav')
    #     mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
    #     mypage.click()
    #     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #     time.sleep(wait_time)
    #     # マイリストをクリック
    #     common_list = driver.find_element(By.CLASS_NAME, "ds_common_table")
    #     common_table = common_list.find_elements(By.CLASS_NAME, "ds_mypage_text")
    #     mylist = common_table[4]
    #     driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", mylist)
    #     time.sleep(wait_time)
    #     mylist.click()
    #     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #     time.sleep(wait_time)
    #     # 掲示板履歴をクリック
    #     menu_list = driver.find_element(By.CLASS_NAME, "ds_menu_link_list")
    #     menu_link = menu_list.find_elements(By.CLASS_NAME, "ds_next_arrow")
    #     bulletin_board_history = menu_link[5]
    #     bulletin_board_history.click()
    #   else:
    #     print(str(i +1) + "の書き込みに失敗しました")
    #     driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
        
  
    
  # 掲示板重複を削除する
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  time.sleep(2)
  area_texts = driver.find_elements(By.CLASS_NAME, value="ds_write_bbs_status")
  area_texts_list = []
  for area in area_texts:
    area = area.text.replace(" ", "").replace("\n", "")
    area_texts_list.append(area)
  area_cnt = 0
  list = []
  
  for area_text in area_texts_list:
    for area in area_list:
      if area in area_text:
        # print(888)
        # print(area)
        if area not in list:
            list.append(area)
            area_cnt += 1
        else:
            print("重複があった")
            print(area_cnt)
            if area_cnt >= 4:
                continue
            duplication_area = driver.find_elements(By.CLASS_NAME, value="ds_round_btn_red")[area_cnt]
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", duplication_area)
            time.sleep(2)
            duplication_area.click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(wait_time)
            delete = driver.find_element(By.CLASS_NAME, "modal-confirm")
            delete.click()
            time.sleep(2)
  # 再掲載をクリック
  # for repost_cnt in range(4):
  repost_cnt = 0
  not_be_repost_areas = []
  blue_round_buttons = driver.find_elements(By.CLASS_NAME, "ds_round_btn_blue2")
  while len(blue_round_buttons):
    blue_round_button = blue_round_buttons[0]
    # 再掲載できなかった場合はスキップ
    js_parent_script = "return arguments[0].parentNode;"
    parent_blue_round_button = driver.execute_script(js_parent_script, blue_round_button)
    # area_text = driver.find_elements(By.CLASS_NAME, value="ds_write_bbs_status")
    area_text = parent_blue_round_button.text.replace(" ", "").replace("\n", "")
    skip_flug = False
    this_area = ""
    for area in area_list:
      if area in area_text:
        # print("今回のエリア")
        this_area = area
        print(area)
        if area in not_be_repost_areas:
          print("リポストできなかったのでスキップ")
          print(area)
          skip_flug = True
    if skip_flug:
        break   
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", blue_round_button)
    time.sleep(wait_time)
    driver.execute_script('arguments[0].click();', blue_round_button)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    # 再掲載する
    re_posting = driver.find_element(By.CLASS_NAME, "modal-confirm")
    re_posting.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    if this_area:
      print(str(this_area) + "の再投稿に成功しました")
      repost_flug_list.append(str(this_area) + "◯")
    # id=modalの要素が出たら失敗 class=remodal-wrapperが4つともdiplay:noneなら成功
    warning = driver.find_elements(By.CLASS_NAME, value="remodal-wrapper ")
    if len(warning):
        display_property = driver.execute_script("return window.getComputedStyle(arguments[0]).getPropertyValue('display');", warning[0])
        if display_property == 'block':
          # ２時間経ってない場合は終了
          modal_text = warning[0].find_element(By.CLASS_NAME, value="modal-content")
          if modal_text.text == "掲載から2時間以上経過していない為、再掲載できません":
              print("掲載から2時間以上経過していない為、再掲載できません")
              cancel = driver.find_element(By.CLASS_NAME, value="modal-cancel")
              cancel.click()
              driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
              break
          # リモーダルウィンドウを閉じる
          print("再投稿に失敗したので新規書き込みします")
          cancel = driver.find_element(By.CLASS_NAME, value="modal-cancel")
          cancel.click()
          time.sleep(wait_time)
          # 都道府県を取得
          js_parent_script = "return arguments[0].parentNode;"
          parent_blue_round_button = driver.execute_script(js_parent_script, blue_round_button)
          # area_text = driver.find_elements(By.CLASS_NAME, value="ds_write_bbs_status")
          area_text = parent_blue_round_button.text.replace(" ", "").replace("\n", "")
          for area in area_list:
            if area in area_text:
              #  掲示板をクリック
              nav_list = driver.find_element(By.ID, value='ds_nav')
              bulletin_board = nav_list.find_element(By.LINK_TEXT, "募集")
              bulletin_board.click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(wait_time)
              catch_warning_screen(driver)
              # 書き込みをクリック
              write = driver.find_element(By.CLASS_NAME, value="icon-kakikomi_float")
              # write = driver.find_element(By.CLASS_NAME, value="icon-header_kakikomi")
              write.click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(wait_time)
              # 書き込み上限に達したらスキップ
              adult = driver.find_elements(By.CLASS_NAME, value="remodal-wrapper")
              print(len(adult))
              if len(adult):
                  print("24時間以内の掲示板書き込み回数の上限に達しています(1日5件まで)")
                  cancel = driver.find_element(By.CLASS_NAME, value="modal-cancel")
                  cancel.click()
                  driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
                  continue
              # その他掲示板をクリック
              link_tab = driver.find_elements(By.CLASS_NAME, "ds_link_tab_text")
              others_bulletin_board = link_tab[1]
              others_bulletin_board.click()
              time.sleep(2)
              # タイトルを書き込む
              input_title = driver.find_element(By.NAME, value="Subj")
              driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", input_title)
              script = "arguments[0].value = arguments[1];"
              driver.execute_script(script, input_title, title)
              # input_title.send_keys(title)
              time.sleep(1)
              # 本文を書き込む
              text_field = driver.find_element(By.ID, value="text-message")
              driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_field)
              script = "arguments[0].value = arguments[1];"
              driver.execute_script(script, text_field, post_text)
              # text_field.send_keys(post_text)
              time.sleep(1)
              # 書き込みエリアを選択
              select_area = driver.find_element(By.NAME, value="wrtarea")
              select = Select(select_area)
              select.select_by_visible_text(area)
              time.sleep(1)
              mail_rep =driver.find_element(By.NAME, value="Rep")
              select = Select(mail_rep)
              select.select_by_visible_text("10件")
              time.sleep(1)
              # 書き込む
              writing = driver.find_element(By.ID, value="billboard_submit")
              writing.click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(wait_time)
              # 書き込み成功画面の判定
              success = driver.find_elements(By.CLASS_NAME, value="ds_keijiban_finish")
              if len(success):
                print(str(area) + "の再投稿に成功しました")
                repost_flug_list.append(str(area) + ":◯")
                # マイページをクリック
                nav_list = driver.find_element(By.ID, value='ds_nav')
                mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
                mypage.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                # マイリストをクリック
                common_list = driver.find_element(By.CLASS_NAME, "ds_common_table")
                common_table = common_list.find_elements(By.CLASS_NAME, "ds_mypage_text")
                for common_table_elem in common_table:
                  if common_table_elem.text == "マイリスト":  
                    mylist = common_table_elem
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", mylist)
                time.sleep(wait_time)
                mylist.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                # 掲示板履歴をクリック
                menu_list = driver.find_element(By.CLASS_NAME, "ds_menu_link_list")
                menu_link = menu_list.find_elements(By.CLASS_NAME, "ds_next_arrow")
                bulletin_board_history = menu_link[5]
                bulletin_board_history.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
              else:
                print(str(area) + "の再投稿に失敗しました")
                repost_flug_list.append(str(area) + "：×")
                not_be_repost_areas.append(str(area))
                driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
                # マイページをクリック
                nav_list = driver.find_element(By.ID, value='ds_nav')
                mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
                mypage.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                # マイリストをクリック
                common_list = driver.find_element(By.CLASS_NAME, "ds_common_table")
                common_table = common_list.find_elements(By.CLASS_NAME, "ds_mypage_text")
                mylist = common_table[4]
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", mylist)
                time.sleep(wait_time)
                mylist.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                # 掲示板履歴をクリック
                menu_list = driver.find_element(By.CLASS_NAME, "ds_menu_link_list")
                menu_link = menu_list.find_elements(By.CLASS_NAME, "ds_next_arrow")
                bulletin_board_history = menu_link[5]
                bulletin_board_history.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                
    blue_round_buttons = driver.find_elements(By.CLASS_NAME, "ds_round_btn_blue2")
    # print(f"「{name}」ハッピーメールの掲示板書き込みに成功しました")
    repost_cnt += 1
    if repost_cnt == 4:
        break
  if repost_flug_list == False:
    repost_flug_list = "0件"
  return repost_flug_list

def return_matching(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img):
  return_matching_cnt = 0
  mail_icon_cnt = 0
  user_icon = 0

  while return_matching_cnt < 5:
    send_status = True
    #  タイプをクリック
    nav_list = driver.find_element(By.ID, value='ds_nav')
    type = nav_list.find_element(By.LINK_TEXT, "タイプ")
    type.click() 
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    # 「マッチング」をクリック
    from_myself = driver.find_elements(By.CLASS_NAME, value="ds_common_tab_item")[2]
    from_myself.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    matching_list = driver.find_element(By.ID , value="list_reciprocal")
    matching_users = matching_list.find_elements(By.CLASS_NAME, value="ds_user_post_link_item_r")
    while len(matching_users) == 0:
        time.sleep(2)
        matching_users = driver.find_elements(By.CLASS_NAME, value="ds_user_post_link_item_r")
    name_field = matching_users[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
    user_name = name_field.text
    mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
    while len(mail_icon):
      print(f'送信履歴あり {user_name}　~ skip ~')
      mail_icon_cnt += 1
      user_icon += 1
      # # メールアイコンが4つ続いたら終了
      if mail_icon_cnt == 4:
        ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
        top_link = ds_logo.find_element(By.TAG_NAME, value="a")
        top_link.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        print("マッチングリストでメールアイコンが4回続きました")
        return return_matching_cnt
      name_field = matching_users[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
      user_name = name_field.text
      mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
    # ユーザー重複チェック
    if len(user_name_list):
      while user_name in user_name_list:
          print('重複ユーザー')
          user_icon = user_icon + 1
          if len(matching_users) <= user_icon:
              duplication_user = True
              break
          name_field = matching_users[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
          user_name = name_field.text
    # マッチングユーザーをクリック
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", matching_users[user_icon])
    time.sleep(1)
    # print(f"ユーザーカウント{user_icon}")
    if duplication_user:
      name_field = matching_users[user_icon+1].find_element(By.CLASS_NAME, value="ds_like_list_name")
      user_name = name_field.text
      user_name_list.append(user_name) 
      message_button = matching_users[user_icon+1].find_elements(By.CLASS_NAME, value="message_button")
      message_button[0].click()
    else:
      message_button = matching_users[user_icon].find_elements(By.CLASS_NAME, value="message_button")
      message_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    catch_warning_screen(driver)
    # プロフィールをチェック
    prof_text = driver.find_elements(By.ID, value="first_m_profile_introduce")
    if len(prof_text):
      if prof_text[0].text == "プロフィール情報の取得に失敗しました":
          user_icon += 1
      # 自己紹介文に業者、通報が含まれているかチェック
      else:
        contains_violations = prof_text[0]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", contains_violations)
        self_introduction_text = contains_violations.text.replace(" ", "").replace("\n", "")
        if '通報' in self_introduction_text or '業者' in self_introduction_text:
          print(f'自己紹介文に危険なワードが含まれていました {user_name}')
          send_status = False
          user_icon += 1
    # メールするをクリック
    if send_status:
      # fst_messageを入力
      text_area = driver.find_element(By.ID, value="text-message")
      # text_area.send_keys(fst_message)
      script = "arguments[0].value = arguments[1];"
      driver.execute_script(script, text_area, fst_message)
      # 送信
      catch_warning_screen(driver)
      send_mail = driver.find_element(By.ID, value="submitButton")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_mail)
      send_mail.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # 画像があれば送信
      if return_foot_img:
        img_conform = driver.find_element(By.ID, value="media-confirm")
        plus_icon = driver.find_elements(By.ID, value="ds_js_media_display_btn")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", plus_icon[1])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", plus_icon[1])
        time.sleep(1)
        upload_file = driver.find_element(By.ID, "upload_file")
        upload_file.send_keys(return_foot_img)
        time.sleep(2)
        submit = driver.find_element(By.ID, value="submit_button")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit)
        driver.execute_script("arguments[0].click();", submit)
        while img_conform.is_displayed():
          time.sleep(2)
      mail_icon_cnt = 0
      user_icon = 0
      return_matching_cnt += 1
      print(f'{name}:マッチング返し send_status = {str(send_status)} ~ {str(return_matching_cnt)} ~ {user_name}')
      # TOPに戻る
      driver.execute_script("window.scrollTo(0, 0);")
      ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", ds_logo)
      top_link = ds_logo.find_element(By.TAG_NAME, value="a")
      time.sleep(1)
      driver.execute_script("arguments[0].click();", top_link)
      # top_link.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
    else:
      user_name_list.append(user_name) 
      # TOPに戻る
      ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
      top_link = ds_logo.find_element(By.TAG_NAME, value="a")
      driver.execute_script("arguments[0].click();", top_link)
      # top_link.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
  user_icon = 0
  return return_matching_cnt

def return_type(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img):
  return_type_cnt = 0
  mail_icon_cnt = 0
  user_icon_type = 0
  while return_type_cnt < 5:
    send_status = True
    #  タイプをクリック
    nav_list = driver.find_element(By.ID, value='ds_nav')
    type = nav_list.find_element(By.LINK_TEXT, "タイプ")
    type.click() 
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    # 「相手から」をクリック
    from_other = driver.find_elements(By.CLASS_NAME, value="ds_common_tab_item")[0]
    from_other.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    type_list = driver.find_element(By.ID , value="list_myself")
    type_users = type_list.find_elements(By.CLASS_NAME, value="ds_user_post_link_item_r")
    while len(type_users) == 0:
        time.sleep(2)
        type_users = driver.find_elements(By.CLASS_NAME, value="ds_user_post_link_item_r")
    name_field = type_users[user_icon_type].find_element(By.CLASS_NAME, value="ds_like_list_name")
    user_name = name_field.text
    mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
    while len(mail_icon):
      print(f'送信履歴あり {user_name} ~ skip ~')
      mail_icon_cnt += 1
      user_icon_type += 1
      # # メールアイコンが4つ続いたら終了
      if mail_icon_cnt == 4:
        ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
        top_link = ds_logo.find_element(By.TAG_NAME, value="a")
        top_link.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        print("タイプリストでメールアイコンが4回続きました")
        return return_type_cnt
      name_field = type_users[user_icon_type].find_element(By.CLASS_NAME, value="ds_like_list_name")
      user_name = name_field.text
      mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
    # ユーザー重複チェック
    if len(user_name_list):
      while user_name in user_name_list:
          print('重複ユーザー')
          user_icon_type = user_icon_type + 1
          if len(type_users) <= user_icon_type:
              duplication_user = True
              break
          name_field = type_users[user_icon_type].find_element(By.CLASS_NAME, value="ds_like_list_name")
          user_name = name_field.text
    # タイプユーザーをクリック
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", type_users[user_icon_type])
    time.sleep(1)
    # print(f"ユーザーカウント{user_icon}")
    if duplication_user:
      name_field = type_users[user_icon_type+1].find_element(By.CLASS_NAME, value="ds_like_list_name")
      user_name = name_field.text
      user_name_list.append(user_name) 
      message_button = type_users[user_icon_type+1].find_elements(By.CLASS_NAME, value="type_button")
      message_button[0].click()
    else:
      message_button = type_users[user_icon_type].find_elements(By.CLASS_NAME, value="type_button")
      message_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    type_confirm = driver.find_elements(By.CLASS_NAME, value="modal-confirm")
    while len(type_confirm) == 0:
      time.sleep(2)
      type_confirm = driver.find_elements(By.CLASS_NAME, value="modal-confirm")
    time.sleep(1)
    type_confirm[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    # プロフ画面の下のメッセージを送信をクリック
    send_mail = driver.find_elements(By.CLASS_NAME, value="ds_profile_target_btn")
    if "履歴あり" in send_mail[0].text:
       send_status = False
    else:
      send_mail[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # プロフィールをチェック
      prof_text = driver.find_elements(By.ID, value="first_m_profile_introduce")
      if len(prof_text):
        if prof_text[0].text == "プロフィール情報の取得に失敗しました":
            user_icon_type += 1
        # 自己紹介文に業者、通報が含まれているかチェック
        else:
          contains_violations = prof_text[0]
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", contains_violations)
          self_introduction_text = contains_violations.text.replace(" ", "").replace("\n", "")
          if '通報' in self_introduction_text or '業者' in self_introduction_text:
            print(f'自己紹介文に危険なワードが含まれていました {user_name}')
            send_status = False
            user_icon_type += 1
    # メールするをクリック
    if send_status:
      # fst_messageを入力
      text_area = driver.find_element(By.ID, value="text-message")
      # text_area.send_keys(fst_message)
      script = "arguments[0].value = arguments[1];"
      driver.execute_script(script, text_area, fst_message)
      # 送信
      catch_warning_screen(driver)
      send_mail = driver.find_element(By.ID, value="submitButton")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_mail)
      send_mail.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # 画像があれば送信
      if return_foot_img:
        img_conform = driver.find_element(By.ID, value="media-confirm")
        plus_icon = driver.find_elements(By.ID, value="ds_js_media_display_btn")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", plus_icon[1])
        time.sleep(1)
        driver.execute_script("arguments[0].click();", plus_icon[1])
        time.sleep(1)
        upload_file = driver.find_element(By.ID, "upload_file")
        # DEBUG用
        # upload_file.send_keys("/Users/yamamotokenta/Desktop/myprojects/mail_operator/widget/picture/chara_img01.jpg")
        upload_file.send_keys(return_foot_img)
        time.sleep(1)
        submit = driver.find_element(By.ID, value="submit_button")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit)
        driver.execute_script("arguments[0].click();", submit)
        while img_conform.is_displayed():
          time.sleep(2)
      mail_icon_cnt = 0
      user_icon_type = 0
      return_type_cnt += 1
      print(f'{name}:タイプ返し send_status = {str(send_status)} ~ {str(return_type_cnt)} ~) {user_name}')
      # TOPに戻る
      driver.execute_script("window.scrollTo(0, 0);")
      ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", ds_logo)
      top_link = ds_logo.find_element(By.TAG_NAME, value="a")
      time.sleep(1)
      driver.execute_script("arguments[0].click();", top_link)
      # top_link.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
    else:
      user_name_list.append(user_name) 
      # TOPに戻る
      ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
      top_link = ds_logo.find_element(By.TAG_NAME, value="a")
      driver.execute_script("arguments[0].click();", top_link)
      # top_link.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
  user_icon_type = 0
  return return_type_cnt
      
def return_footpoint(name, driver, wait, return_foot_message, cnt, return_foot_img, fst_message):
    wait_time = random.uniform(3, 4)
    driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    return_cnt = 0
    mail_icon_cnt = 0
    duplication_user = False
    user_name_list = []
    user_icon = 0
    # debug
    # if name == "えりか":
    #   # マッチング返し
    #   matching_cnt = return_matching(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img)
    #   print(f"マッチング返し総数 {matching_cnt}")
    #   return_cnt = return_cnt + matching_cnt
    #   # タイプ返し
    #   type_cnt = return_type(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img)
    #   print(f"タイプ返し総数 {mail_icon_cnt}")
    #   return_cnt = return_cnt + type_cnt
    #   print(f"メッセージ送信数　{return_cnt}")
    # elif name == "アスカ" or name == "いおり":
    #   # マッチング返し
    #   matching_cnt = return_matching(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img)
    #   print(f"マッチング返し総数 {matching_cnt}")
    #   # タイプ返し
    #   type_cnt = return_type(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img)
    #   print(f"タイプ返し総数 {type_cnt}")
    # マッチング返し
    # try:
    #   matching_cnt = return_matching(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img)
    #   print(f"マッチング返し総数 {matching_cnt}")
    # except Exception as e:  
    #   print("マッチ返しエラー")
    #   print(traceback.format_exc())
    #   driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
    #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #   time.sleep(wait_time)
    # # タイプ返し
    # try:
    #   type_cnt = return_type(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img)
    #   print(f"タイプ返し総数 {type_cnt}")
    # except Exception as e:  
    #   print("タイプ返しエラー")
    #   print(traceback.format_exc())
    #   driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
    #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    #   time.sleep(wait_time)      

    # 足跡返し
    while cnt >= return_cnt:
      warning_pop = catch_warning_screen(driver)
      if warning_pop:
         print(f"{name}：警告画面が出ている可能性があります")
         return
      # マイページをクリック
      nav_list = driver.find_element(By.ID, value='ds_nav')
      mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
      mypage.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # 足あとをクリック
      return_footpoint = driver.find_element(By.CLASS_NAME, value="icon-ico_footprint")
      driver.execute_script("arguments[0].click();", return_footpoint)
      # return_footpoint.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      send_status = True
      time.sleep(1)
      # ページの最後までスクロール
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      # ページが完全に読み込まれるまで待機
      time.sleep(1)
      f_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")
      while len(f_user) == 0:
         time.sleep(2)
         f_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")

      name_field = f_user[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
      user_name = name_field.text
      mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
      send_skip_cnt = 0
      while len(mail_icon) or user_name in user_name_list:
        if len(mail_icon):
          user_icon += 1
          print(f'送信履歴あり {user_name} ~ skip ~')
          send_skip_cnt += 1
          try:
            name_field = f_user[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
            user_name = name_field.text
            mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
          except IndexError:
            print("送信可能なユーザーが見つかりませんでした")
            return return_cnt
          if send_skip_cnt > 8:
            print("送れないユーザーが9回続きました")
            return return_cnt
        elif len(user_name_list):
          while user_name in user_name_list:
              print('重複ユーザー')
              send_skip_cnt += 1
              user_icon = user_icon + 1
              if len(f_user) <= user_icon:
                duplication_user = True
                break
              name_field = f_user[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
              user_name = name_field.text
              if send_skip_cnt > 9:
                print("送れないユーザーが10回続きました")
                return return_cnt

      # 年齢で返信する確率を調整する
      # user_age = f_user[user_icon].find_elements(By.CLASS_NAME, value="ds_like_list_age")
      # if not len(user_age):
      #    send_status = False
      # if user_age[0].text[:2] == "ナイ" or user_age[0].text == "":
      #    print("年齢不詳")
      #    user_age = 31
      # else:
      #   user_age = int(user_age[0].text[:2])
      # if user_age >= 40:
      #   #  print(f'〜〜{user_age}代〜〜')
      #    # 実行確率（80%の場合）
      #    execution_probability = 0.20
      #    # ランダムな数値を生成し、実行確率と比較
      #    if random.random() < execution_probability:
      #       send_status = False
    
      # 足跡ユーザーをクリック
     
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", f_user[user_icon])
      time.sleep(1)
      if duplication_user:
        name_field = f_user[user_icon+1].find_element(By.CLASS_NAME, value="ds_like_list_name")
        user_name = name_field.text
        user_name_list.append(user_name) 

        f_user[user_icon+1].click()
      else:
        f_user[user_icon].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      catch_warning_screen(driver)
      m = driver.find_elements(By.XPATH, value="//*[@id='ds_main']/div/p")
      if len(m):
        print(m[0].text)
        if m[0].text == "プロフィール情報の取得に失敗しました":
            user_icon += 1
            continue
      # 自己紹介文に業者、通報が含まれているかチェック
      if len(driver.find_elements(By.CLASS_NAME, value="translate_body")):
        contains_violations = driver.find_element(By.CLASS_NAME, value="translate_body")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", contains_violations)
        self_introduction_text = contains_violations.text.replace(" ", "").replace("\n", "")
        if '通報' in self_introduction_text or '業者' in self_introduction_text:
            print(f'自己紹介文に危険なワードが含まれていました {user_name}')
            send_status = False
      # メッセージ履歴があるかチェック
      mail_field = driver.find_element(By.ID, value="ds_nav")
      mail_history = mail_field.find_element(By.ID, value="mail-history")
      display_value = mail_history.value_of_css_property("display")
      if display_value != "none":
          # print('メール履歴があります')
          # print(user_name)
          user_name_list.append(user_name) 
          send_status = False
          mail_icon_cnt += 1
      # メールするをクリック
      if send_status:
        send_mail = mail_field.find_element(By.CLASS_NAME, value="ds_profile_target_btn")
        send_mail.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        # 足跡返しを入力
        text_area = driver.find_element(By.ID, value="text-message")
        # text_area.send_keys(return_foot_message)
        script = "arguments[0].value = arguments[1];"
        driver.execute_script(script, text_area, return_foot_message)
        # 送信
        catch_warning_screen(driver)
        send_mail = driver.find_element(By.ID, value="submitButton")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_mail)
        send_mail.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        # 画像があれば送信
        if return_foot_img:
          img_conform = driver.find_element(By.ID, value="media-confirm")
          plus_icon = driver.find_elements(By.ID, value="ds_js_media_display_btn")
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", plus_icon[0])
          time.sleep(1)
          driver.execute_script("arguments[0].click();", plus_icon[0])         
          time.sleep(1)
          upload_file = driver.find_element(By.ID, "upload_file")
          # DEBUG
          # upload_file.send_keys("/Users/yamamotokenta/Desktop/myprojects/mail_operator/widget/picture/kumi_mizugi.jpeg")
          upload_file.send_keys(return_foot_img)
          time.sleep(2)
          submit = driver.find_element(By.ID, value="submit_button")
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit)
          driver.execute_script("arguments[0].click();", submit)
          while img_conform.is_displayed():
             time.sleep(2)
        return_cnt += 1
        mail_icon_cnt = 0
        user_icon = 0
        print(f'{name}:足跡返し  ~ {str(return_cnt)} ~ {user_name} ')
        # TOPに戻る
        driver.execute_script("window.scrollTo(0, 0);")
        ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", ds_logo)
        top_link = ds_logo.find_element(By.TAG_NAME, value="a")
        time.sleep(1)
        driver.execute_script("arguments[0].click();", top_link)
        # top_link.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
      else:
        user_name_list.append(user_name) 
        # TOPに戻る
        ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
        top_link = ds_logo.find_element(By.TAG_NAME, value="a")
        driver.execute_script("arguments[0].click();", top_link)
        # top_link.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
    if return_cnt == None:
      return_cnt = 0
    return return_cnt

def make_footprints(name, happymail_id, happymail_pass, driver, wait, foot_count):
   driver.delete_all_cookies()
   driver.get("https://happymail.jp/login/")
   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
   wait_time = random.uniform(2, 5)
   time.sleep(2)
   id_form = driver.find_element(By.ID, value="TelNo") 
   id_form.send_keys(happymail_id)
   pass_form = driver.find_element(By.ID, value="TelPass")
   pass_form.send_keys(happymail_pass)
   time.sleep(wait_time)
   send_form = driver.find_element(By.ID, value="login_btn")
   send_form.click()
   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
   time.sleep(2)
   #リモーダル画面が開いていれば閉じる
   warinig_flug = catch_warning_screen(driver)
   if warinig_flug:
      print(f"{name}:警告画面が出ている可能性があります")
      return
   # プロフ検索をクリック
   nav_list = driver.find_element(By.ID, value='ds_nav')
   mypage = nav_list.find_element(By.LINK_TEXT, "プロフ検索")
   mypage.click()
   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
   time.sleep(wait_time)
   # 並びの表示を設定
   sort_order = driver.find_elements(By.ID, value="kind_select")
   select = Select(sort_order[0])
   select.select_by_visible_text("プロフ一覧")
   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
   time.sleep(wait_time)
   for i in range(foot_count):
      if warinig_flug:
        print(f"{name}:警告画面が出ている可能性があります")
        return
      user_list = driver.find_elements(By.CLASS_NAME, value="ds_user_post_link_item_r")
      no_history_user = False
      #  メールアイコン（送信履歴）があるかチェック
      mail_icon_flag = True
      mail_icon_try_cnt = 0
      while mail_icon_flag:
        # インデックスがリストの範囲外でないか確認
        if i >= len(user_list):
            print("ユーザーリストの終わりに達しました。")
            break
        user = user_list[i]
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", user)
        mail_icon_parent = user.find_elements(By.CLASS_NAME, value="text-male")
        mail_icon = mail_icon_parent[0].find_elements(By.TAG_NAME, value="img")
        if  not len(mail_icon):
          mail_icon_flag = False
          break
        i += 1
        mail_icon_try_cnt += 1
        if mail_icon_try_cnt == 10:
           break
      user_link = user.find_elements(By.TAG_NAME, value="a")
      user_link[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # ユーザ名を取得
      user_name = driver.find_elements(By.CLASS_NAME, value="ds_user_display_name")
      user_name = user_name[0].text
      # タイプ
      # ランダムな数値を生成し、実行確率と比較
      type_flag = False
      # 実行確率
      probability = 0.01
      
      execution_probability = probability
      if random.random() < execution_probability:
        type_button = driver.find_element(By.ID, value="btn-type")
        type_button.click()
        type_flag = True
        time.sleep(2)
      # いいね
      # # ランダムな数値を生成し、実行確率と比較
      # like_flag = False
      # # 実行確率
      # execution_probability = probability
      # if random.random() < execution_probability:
      #   others_icon = driver.find_elements(By.CLASS_NAME, value="icon-profile_other_on")
      #   others_icon[0].click()
      #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      #   time.sleep(1)
      #   like_icon = driver.find_elements(By.ID, value="btn-like")
      #   like_icon_classes = like_icon[0].get_attribute("class")
      #   if not "disabled" in like_icon_classes:
      #     like_flag = True
      #     # footer_menu-list-item-link
      #     like = like_icon[0].find_elements(By.CLASS_NAME, value="footer_menu-list-item-link")
      #     like[0].click()
      #     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      #     time.sleep(2)
      #     like_cancel = driver.find_elements(By.CLASS_NAME, value="modal-cancel")
      #     while not len(like_cancel):
      #        time.sleep(1)
      #        like_cancel = driver.find_elements(By.CLASS_NAME, value="modal-cancel")
      #     like_cancel[0].click()
      #     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      #     time.sleep(2)
      # print(f'{name}:足跡付け{i+1}件, いいね:{like_flag}、タイプ{type_flag}  {user_name}')
      # print(f'{name}:足跡付け{i+1}件, タイプ{type_flag}  {user_name}')
      print(f'{name}:足跡付け{i+1}件,  {user_name}')

      # 戻る
      back = driver.find_elements(By.CLASS_NAME, value="ds_prev_arrow")
      back[0].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # たまに変なページに遷移するのでurl確認
      current_url = driver.current_url
      # 特定の文字列で始まっているか確認
      if not current_url.startswith("https://happymail.co.jp/sp/app/html/profile_list.php"):
          print("URLは指定した文字列で始まっていません。")
          driver.get("https://happymail.co.jp/sp/app/html/profile_list.php")
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(wait_time)


  #  no_history_user_list = []
#    # ページの高さを取得
#    last_height = driver.execute_script("return document.body.scrollHeight")
#    while True:
#     # ページの最後までスクロール
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     # ページが完全に読み込まれるまで待機
#     time.sleep(2)
#     user_list = driver.find_elements(By.CLASS_NAME, value="ds_user_post_link_item_r")
#     for user in user_list:
#        user_class = user.get_attribute('class')
#        if not "ds_ribbon" in user_class:
#           # user_name = user.find_elements(By.CLASS_NAME, value="ds_post_body_name_small")
#           user_link = user.find_elements(By.TAG_NAME, value="a")
#           onclick_value = user_link[0].get_attribute('onclick')
#           # 正規表現パターンを定義
#           pattern = r'happymail\.co\.jp.*?idx=(\d+)'
#           match = re.search(pattern, onclick_value)
#           if match:
#             result = match.group(0)
#           no_history_user_list.append(result)
# # https://happymail.jp/login/
#     if len(no_history_user_list) > 33:
#       print('ユーザー件数33　OVER')
#       print(len(no_history_user_list))
#       break
#     # 新しい高さを取得
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     # ページの高さが変わらなければ、すべての要素が読み込まれたことを意味する
#     if new_height == last_height:
#         break
#     last_height = new_height
#    for i, no_history_user in enumerate(no_history_user_list):
#       driver.get(f"https://{no_history_user}")
#       wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#       time.sleep(wait_time)
#       #リモーダル画面が開いていれば閉じる
#       catch_warning_screen(driver)
#       # userのidxを取得（タイプボタン取得のため）
#       #  正規表現パターンを定義
#       pattern = r'idx=(\d+)'
#       # 正規表現でマッチングを行う
#       matches = re.findall(pattern, no_history_user)
#       # idxを目印にユーザーのディスプレイを取得
#       inputs = driver.find_elements(By.NAME, value="idx")
#       type_flag = False
#       # タイプ
#       # ランダムな数値を生成し、実行確率と比較
#       # 実行確率
#       execution_probability = 0.70
#       if random.random() < execution_probability:
#         for input in inputs:
#           if input.get_attribute('value') == matches[0]:
#             user_profile = input.find_element(By.XPATH, 'following-sibling::div[contains(@class, "ds_profile_picture")]')
#             type_btn = user_profile.find_elements(By.CLASS_NAME, value="icon-type_off")
#             if len(type_btn):
#               type_btn[0].click()
#               type_flag = True
#               time.sleep(2)
#       # いいね
#       # ランダムな数値を生成し、実行確率と比較
#          # 実行確率
#       execution_probability = 0.70
#       like_flag = False
#       if random.random() < execution_probability:
#         catch_warning_screen(driver)
#         others_icon = driver.find_elements(By.CLASS_NAME, value="icon-profile_other_on")
#         others_icon[0].click()
#         wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#         time.sleep(1)
#         like_icon = driver.find_elements(By.ID, value="btn-like")
#         like_icon_classes = like_icon[0].get_attribute("class")
#         if not "disabled" in like_icon_classes:
#           like_flag = True
#           # footer_menu-list-item-link
#           like = like_icon[0].find_elements(By.CLASS_NAME, value="footer_menu-list-item-link")
#           like[0].click()
#           wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#           time.sleep(2)
#           like_cancel = driver.find_elements(By.CLASS_NAME, value="modal-cancel")
#           while not len(like_cancel):
#              time.sleep(1)
#              like_cancel = driver.find_elements(By.CLASS_NAME, value="modal-cancel")
#           like_cancel[0].click()
#           wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#           time.sleep(2)
#       # driver.get("https://happymail.co.jp/sp/app/html/profile_list.php")
#       # driver.back()
#       print(f'{name}:足跡付け{i+1}件, いいね:{like_flag}、タイプ{type_flag}')
#       wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#       time.sleep(wait_time)
#       if i == 40:
#          break
#    driver.refresh()

def send_fst_message(happy_user_list, driver, wait):
  
  for user_info in happy_user_list:
    name,login_id, passward, fst_message, mail_img = user_info
    limit_cnt = 1
    if name == "きりこ":
      limit_cnt = 0
    driver.delete_all_cookies()
    driver.get("https://happymail.jp/login/")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    wait_time = random.uniform(3, 6)
    time.sleep(wait_time)
    id_form = driver.find_element(By.ID, value="TelNo")
    id_form.send_keys(login_id)
    pass_form = driver.find_element(By.ID, value="TelPass")
    pass_form.send_keys(passward)
    time.sleep(wait_time)
    send_form = driver.find_element(By.ID, value="login_btn")
    send_form.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    #リモーダル画面が開いていれば閉じる
    catch_warning_screen(driver)
    # # プロフ検索をクリック
    nav_list = driver.find_element(By.ID, value='ds_nav')
    seach_profile = nav_list.find_element(By.LINK_TEXT, "プロフ検索")
    seach_profile.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    send_cnt = 0
    user_colum = 0
    # 並びの表示を設定
    sort_order = driver.find_elements(By.ID, value="kind_select")
    select = Select(sort_order[0])
    select.select_by_visible_text("プロフ一覧")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    
    while send_cnt < limit_cnt:
      # ユーザーをクリック
      users = driver.find_elements(By.CLASS_NAME, value="ds_thum_contain")
      # print('取得したユーザー数')
      # print(len(users))
      styles = users[user_colum].get_attribute('style')
      e = driver.find_elements(By.CLASS_NAME, value="ds_mb2p")
      age_text = e[user_colum].find_elements(By.CLASS_NAME, value="ds_post_body_age_small")
      while not "20" in age_text[0].text:
        user_colum += 1
        e = driver.find_elements(By.CLASS_NAME, value="ds_mb2p")
        age_text = e[user_colum].find_elements(By.CLASS_NAME, value="ds_post_body_age_small")
        if user_colum == len(users):
          break
          
      # 画像なしのユーザーを探す
      # while "noimage" not in styles:
      #   user_colum += 1
      #   print(user_colum)
      #   styles = users[user_colum].get_attribute('style')
      
      driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", users[user_colum])
      users[user_colum].click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      send_status = True
      m = driver.find_elements(By.XPATH, value="//*[@id='ds_main']/div/p")
      if len(m):
        print(m[0].text)
        if m[0].text == "プロフィール情報の取得に失敗しました":
            send_status = False
            user_colum += 1
      # 自己紹介文に業者、通報が含まれているかチェック
      if len(driver.find_elements(By.CLASS_NAME, value="translate_body")):
        contains_violations = driver.find_element(By.CLASS_NAME, value="translate_body")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", contains_violations)
        self_introduction_text = contains_violations.text.replace(" ", "").replace("\n", "")
        if '通報' in self_introduction_text or '業者' in self_introduction_text:
            print('自己紹介文に危険なワードが含まれていました')
            send_status = False
            user_colum += 1
      # メッセージ履歴があるかチェック
      mail_field = driver.find_element(By.ID, value="ds_nav")
      mail_history = mail_field.find_element(By.ID, value="mail-history")
      display_value = mail_history.value_of_css_property("display")
      if display_value != "none":
          print('メール履歴があります')
          send_status = False
          user_colum += 1
      # メール送信
      if send_status:
        do_mail_icon = driver.find_elements(By.CLASS_NAME, value="ds_profile_target_btn")
        do_mail_icon[0].click()
        # 初めましてメッセージを入力
        text_area = driver.find_element(By.ID, value="text-message")
        text_area.send_keys(fst_message)
        # 送信
        send_mail = driver.find_element(By.ID, value="submitButton")
        send_mail.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        # 画像があれば送信
        # mail_img = setting.debug_img
        if mail_img:
          img_conform = driver.find_element(By.ID, value="media-confirm")
          plus_icon = driver.find_element(By.CLASS_NAME, value="icon-message_plus")
          plus_icon.click()
          time.sleep(1)
          upload_file = driver.find_element(By.ID, "upload_file")
          upload_file.send_keys(mail_img)
          time.sleep(2)
          submit = driver.find_element(By.ID, value="submit_button")
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit)
          driver.execute_script("arguments[0].click();", submit)
          while img_conform.is_displayed():
              time.sleep(2)
        send_cnt += 1
        user_colum += 1
        print(f"fst_message {name}~{send_cnt}~")
      driver.get("https://happymail.co.jp/sp/app/html/profile_list.php")
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
      # リモーダル画面が出たら閉じる
      remodal = driver.find_elements(By.CLASS_NAME, value="remodal-close")
      if len(remodal):
        print('リモーダル画面')
        remodal[0].click()
        time.sleep(wait_time)
    
  print("fstmail end")
  

def check_new_mail(driver, wait, name):
  return_list = []
  dbpath = 'firstdb.db'
  conn = sqlite3.connect(dbpath)
  cur = conn.cursor()
  cur.execute('SELECT login_id, passward, fst_message, return_foot_message, conditions_message FROM happymail WHERE name = ?', (name,))
  login_id = None
  for row in cur:
      login_id = row[0]
      login_pass = row[1]
      fst_message = row[2]
      return_foot_message = row[3]
      conditions_message = row[4]   
  if not login_id:
    print(f"{name}のhappymailキャラ情報を取得できませんでした")
    return
  driver.delete_all_cookies()
  driver.get("https://happymail.jp/login/")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  wait_time = random.uniform(2, 5)
  time.sleep(wait_time)
  id_form = driver.find_element(By.ID, value="TelNo")
  id_form.send_keys(login_id)
  pass_form = driver.find_element(By.ID, value="TelPass")
  pass_form.send_keys(login_pass)
  time.sleep(wait_time)
  send_form = driver.find_element(By.ID, value="login_btn")
  send_form.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  remodal = driver.find_elements(By.CLASS_NAME,value="remodal-close")
  if len(remodal):
     remodal[0].click()
     time.sleep(1)
  warning = driver.find_elements(By.CLASS_NAME, value="information__dialog")
  if len(warning):
     return_list.append(f"{name},{login_id}:{login_pass} ハッピーメールに警告画面が出ている可能性があります")
     return return_list
  name_elem = ""
  try:
    name_elem = driver.find_element(By.CLASS_NAME, "ds_user_display_name")
  except NoSuchElementException:
      time.sleep(7)
      name_elem = driver.find_elements(By.CLASS_NAME, "ds_user_display_name")
      if len(name_elem):
        name_elem = name_elem[0]
      pass
  if not name_elem:
     return_list.append(f"{name},{login_id}:{login_pass} ハッピーメールに警告画面が出ている可能性があります.....")
     return return_list
  name = name_elem.text  
  message_icon_candidates = driver.find_elements(By.CLASS_NAME, value="ds_nav_item")
  message_icon = ""
  for message_icon_candidate in message_icon_candidates:
     if "メッセージ" in message_icon_candidate.text:
        message_icon = message_icon_candidate
  if message_icon:
    new_message = message_icon.find_elements(By.CLASS_NAME, value="ds_red_circle")
    
  else:
     print("message_iconが見つかりません")
     return
  # 新着があった
  # if True:
  if len(new_message):
     link = message_icon.find_elements(By.TAG_NAME, value="a")
     link[0].click()
     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
     time.sleep(2)
     #  未読のみ表示
     only_new_message = driver.find_elements(By.CLASS_NAME, value="ds_message_tab_item")[1]
     only_new_message.click()
     time.sleep(1)
    
     new_mail = driver.find_elements(By.CLASS_NAME, value="ds_list_r_kidoku")  
     if not len(new_mail):
         list_load = driver.find_elements(By.ID, value="load_bL")
         if len(list_load):
          list_load[0].click()
         time.sleep(2)
     #新着がある間はループ
    #  while True:  
     while len(new_mail):
        parent_element = new_mail[0].find_element(By.XPATH, value="..")
        next_element = parent_element.find_element(By.XPATH, value="following-sibling::*")
        date = next_element.find_elements(By.CLASS_NAME, value="ds_message_date")
        date_numbers = re.findall(r'\d+', date[0].text)
        arrival_datetime = datetime(int(datetime.now().year), int(date_numbers[0]), int(date_numbers[1]), int(date_numbers[2]), int(date_numbers[3])) 
        now = datetime.today()
        elapsed_time = now - arrival_datetime
        # print(f"メール到着からの経過時間{elapsed_time}")
        # 4分経過しているか
        # if True:
        if elapsed_time >= timedelta(minutes=4):
          print("4分以上経過しています。")
          # s = driver.find_elements(By.CLASS_NAME, value="ds_js_hide_arrow")
          # s[0].click()
          new_mail[0].click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(2)
          catch_warning_screen(driver)
          print(11111111)
          send_message = driver.find_elements(By.CLASS_NAME, value="message__block--send")    

          # send_message = driver.find_elements(By.CLASS_NAME, value="message__block__body__text--female")   
          # print(len(send_message))  
          # if len(send_message) == 0:
          #   #  1st
          #   text_area = driver.find_element(By.ID, value="text-message")
          #   driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_area)
          #   text_area.send_keys(fst_message)
          #   # 送信
          #   send_mail = driver.find_element(By.ID, value="submitButton")
          #   driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_mail)
          #   send_mail.click()
          #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          #   time.sleep(wait_time)
          # elif len(send_message) == 1:
          #   # 2st
          #   text_area = driver.find_element(By.ID, value="text-message")
          #   driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_area)
          #   text_area.send_keys(conditions_message)
          #   # 送信
          #   send_mail = driver.find_element(By.ID, value="submitButton")
          #   send_mail.click()
          #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          #   time.sleep(wait_time)
          # else:
          #   #  通知
          #   print('やり取りしてます')
          #   user_name = driver.find_elements(By.CLASS_NAME, value="app__navbar__item--title")[0]
          #   user_name = user_name.text
          #   receive_contents = driver.find_elements(By.CLASS_NAME, value="message__block--receive")[-1]
          #   #  print(f"{user_name}:{receive_contents.text}")
          #   return_message = f"{name}happymail,{login_id}:{login_pass}\n{user_name}「{receive_contents.text}」"
          #   return_list.append(return_message)
          #   # みちゃいや
          #   plus_icon_parent = driver.find_elements(By.CLASS_NAME, value="message__form__action")
          #   plus_icon = plus_icon_parent[0].find_elements(By.CLASS_NAME, value="icon-message_plus")
          #   print(567)
          #   print(len(plus_icon))
          #   driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", plus_icon[0])
          #   plus_icon[0].click()
          #   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          #   time.sleep(2)
          #   # ds_message_txt_media_text
          #   mityaiya = ""
          #   candidate_mityaiya = driver.find_elements(By.CLASS_NAME, value="ds_message_txt_media_text")
          #   for c_m in candidate_mityaiya:
          #     if c_m.text == "見ちゃいや":
          #         mityaiya = c_m
          #   if mityaiya:
          #     #  print('<<<<<<<<<<<<<<<<<みちゃいや登録>>>>>>>>>>>>>>>>>>>')
          #     mityaiya.click()
          #     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          #     time.sleep(2)
          #     mityaiya_send = driver.find_elements(By.CLASS_NAME, value="input__form__action__button__send")
          #     if len(mityaiya_send):
          #       mityaiya_send[0].click()
          #       wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          #       time.sleep(1)

          if len(send_message):
            send_text = send_message[-1].find_elements(By.CLASS_NAME, value="message__block__body__text")[0].text
            if not send_text:
                send_text = send_message[-2].find_elements(By.CLASS_NAME, value="message__block__body__text")[0].text
            
            print("<<<<<<<<<<<>>>>>>>>>>>>>")
            print(send_text)
            print("---------------------------------------")
            print(fst_message == send_text)
            print("---------------------------------------")
            print(return_foot_message == send_text)
            print("---------------------------------------")
            print("募集メッセージ" in send_text)

            if fst_message == send_text or return_foot_message == send_text or "募集メッセージ" in send_text:
                text_area = driver.find_element(By.ID, value="text-message")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_area)
                text_area.send_keys(conditions_message)
                # 送信
                send_mail = driver.find_element(By.ID, value="submitButton")
                send_mail.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                
            else:
              print('やり取りしてます')
              user_name = driver.find_elements(By.CLASS_NAME, value="app__navbar__item--title")[0]
              user_name = user_name.text
              receive_contents = driver.find_elements(By.CLASS_NAME, value="message__block--receive")[-1]
              #  print(f"{user_name}:{receive_contents.text}")
              return_message = f"{name}happymail,{login_id}:{login_pass}\n{user_name}「{receive_contents.text}」"
              return_list.append(return_message)
              # みちゃいや
              plus_icon_parent = driver.find_elements(By.CLASS_NAME, value="message__form__action")
              plus_icon = plus_icon_parent[0].find_elements(By.CLASS_NAME, value="icon-message_plus")
              print(567)
              print(len(plus_icon))
              driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", plus_icon[0])
              plus_icon[0].click()
              wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
              time.sleep(2)
              # ds_message_txt_media_text
              mityaiya = ""
              candidate_mityaiya = driver.find_elements(By.CLASS_NAME, value="ds_message_txt_media_text")
              for c_m in candidate_mityaiya:
                if c_m.text == "見ちゃいや":
                    mityaiya = c_m
              if mityaiya:
                #  print('<<<<<<<<<<<<<<<<<みちゃいや登録>>>>>>>>>>>>>>>>>>>')
                mityaiya.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(2)
                mityaiya_send = driver.find_elements(By.CLASS_NAME, value="input__form__action__button__send")
                if len(mityaiya_send):
                  mityaiya_send[0].click()
                  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                  time.sleep(1)
                 
          else:
            text_area = driver.find_element(By.ID, value="text-message")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_area)
            text_area.send_keys(fst_message)
            # 送信
            send_mail = driver.find_element(By.ID, value="submitButton")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_mail)
            send_mail.click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(wait_time)
        else:
           if len(return_list):
              return return_list
           else:
              return None
        driver.get("https://happymail.co.jp/sp/app/html/message_list.php")
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        new_mail = driver.find_elements(By.CLASS_NAME, value="ds_list_r_kidoku")
  if len(return_list):
    return return_list
  else:
    return None
  
def re_registration(name, driver):
  dbpath = 'firstdb.db'
  conn = sqlite3.connect(dbpath)
  cur = conn.cursor()
  cur.execute('SELECT * FROM happymail WHERE name = ?', (name,))
  login_id = ""
  for row in cur:
     
      login_id = row[2]
      login_pass = row[3]
     
     
  if not login_id:
    return

  driver.delete_all_cookies()
  wait = WebDriverWait(driver, 15)  
  driver.get("https://happymail.jp/login/")
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  # wait_time = random.uniform(2, 5)
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

  # 警告画面が出たらスキップ
  warning = driver.find_elements(By.CLASS_NAME, value="ds_main_header_text")
  if warning:
     print("警告画面が出ました")
     return
  # マイページをクリック
  nav_list = driver.find_element(By.ID, value='ds_nav')
  mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
  mypage.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  # プロフィールをクリック
  common_list = driver.find_element(By.CLASS_NAME, "ds_common_table")
  common_table = common_list.find_elements(By.CLASS_NAME, "ds_mypage_text")
  for common_table_elem in common_table:
     if "プロフィール" in common_table_elem.text:
        mylist = common_table_elem
  driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", mylist)
  time.sleep(2)
  mylist.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  
  # 名前
  links = driver.find_elements(By.CLASS_NAME, value="input__form__input__block")
  name_link = links[5].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)
  name_textarea = driver.find_elements(By.CLASS_NAME, value="text_content")
  name_textarea_value = name_textarea[0].get_attribute("value")
  if name == name_textarea_value:
    driver.back()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
  else:
    name_textarea[0].clear()
    name_textarea[0].send_keys(name)
    save_button = driver.find_elements(By.ID, value="save")
    save_button[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    save_confirmation = driver.find_elements(By.CLASS_NAME, value="modal-confirm")
    save_confirmation[0].click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(20)
  # 年齢
  age_select = driver.find_elements(By.ID, value="age")
  select = Select(age_select[0])
  select.select_by_visible_text(age)
  time.sleep(1)