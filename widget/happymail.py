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
from selenium.webdriver.support import expected_conditions as EC
import base64
import requests
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
import gc


# 警告画面
def catch_warning_screen(driver):
  wait = WebDriverWait(driver, 15)
  anno = driver.find_elements(By.CLASS_NAME, value="anno")
  warning = driver.find_elements(By.CLASS_NAME, value="warning screen")
  dialog = driver.find_elements(By.ID, value="_information_dialog")
  remodal = driver.find_elements(By.CLASS_NAME, value="remodal-image")
  remodal_wrapper = driver.find_elements(By.CLASS_NAME, value="remodal-wrapper")
  warinig_cnt =0
  while len(warning) or len(anno) or len(dialog) or len(remodal) or len(remodal_wrapper):
    driver.refresh()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
    warning = driver.find_elements(By.CLASS_NAME, value="warning screen")
    anno = driver.find_elements(By.CLASS_NAME, value="anno")
    dialog = driver.find_elements(By.ID, value="_information_dialog")
    remodal = driver.find_elements(By.CLASS_NAME, value="remodal-image")
    remodal_wrapper = driver.find_elements(By.CLASS_NAME, value="remodal-wrapper")
    warinig_cnt += 1
    if warinig_cnt > 2:
       return True
  return False
   
def re_post(name,  driver, wait, title, post_text):
  try:
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
    nav_list = driver.find_elements(By.ID, value='ds_nav')
    if not len(nav_list):
      print(f"{name}: 警告画面が出ている可能性があります。")
      return False
    mypage = nav_list[0].find_element(By.LINK_TEXT, "マイページ")
    try:
      mypage.click()
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
    except ElementClickInterceptedException as e:
      print(f"{name}:警告画面が出ている可能性があります")
      return
    # 画像チェック
    top_img_element = driver.find_elements(By.CLASS_NAME, value="ds_mypage_user_image")
    if len(top_img_element):
      top_img = top_img_element[0].get_attribute("style")
      if "noimage" in top_img:
          print(f"{name}のトップ画がNoImageの可能性があります。。。")
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
    # genre_dict = {0:"今すぐ会いたい", 1:"大人の出会い"}  
    genre = driver.find_elements(By.CLASS_NAME, value="ds_bd_none")
    road_cnt = 1
    while len(genre) <= 2:
      time.sleep(2)
      genre = driver.find_elements(By.CLASS_NAME, value="ds_bd_none")
      road_cnt += 1
      if road_cnt == 7:
          break
    genre = genre[1].text
    # print("<<<再投稿する掲示板のジャンル取得>>>")
    # print(genre)
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
          # print(area)
          if area not in list:
              list.append(area)
              area_cnt += 1
          else:
              # print("重複があった")
              # print(area_cnt)
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
          # print(area)
          if area in not_be_repost_areas:
            # print("リポストできなかったのでスキップ")
            # print(area)
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
                  # print(str(area) + "の再投稿に成功しました")
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
                  bulletin_board_history = menu_link[4]
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
  except WebDriverException as e:
    error_message = str(e)
    if "unexpectedly exited. Status code was: -9" in error_message:
        print("in repost")
        print("Chromedriverが予期せず終了しました。再起動して起動してください。")
        driver.quit()

def return_matching(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img, matching_cnt):
  return_matching_counted = 0
  mail_icon_cnt = 0
  user_icon = 0

  while return_matching_counted < matching_cnt:
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
      # print(f'送信履歴あり {user_name}　~ skip ~')
      mail_icon_cnt += 1
      user_icon += 1
      # # メールアイコンが5つ続いたら終了
      if mail_icon_cnt == 5:
        ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
        top_link = ds_logo.find_element(By.TAG_NAME, value="a")
        top_link.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        print("マッチングリストで送信履歴のあるユーザーが5回続きました")
        return return_matching_counted
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
      catch_warning_screen(driver)
      # fst_messageを入力
      text_area = driver.find_element(By.ID, value="text-message")
      # text_area.send_keys(fst_message)
      script = "arguments[0].value = arguments[1];"
      driver.execute_script(script, text_area, fst_message)
      # 送信
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
        upload_file.send_keys(return_foot_img)
        time.sleep(2)
        submit = driver.find_element(By.ID, value="submit_button")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit)
        driver.execute_script("arguments[0].click();", submit)
        while img_conform.is_displayed():
          time.sleep(2)
      mail_icon_cnt = 0
      user_icon = 0
      return_matching_counted += 1
      now = datetime.now().strftime('%m-%d %H:%M:%S')
      print(f'{name}:マッチング返し {user_name} ~ {str(return_matching_counted)} ~ {now}')
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
  return return_matching_counted

def return_type(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, return_foot_img, type_cnt):
  return_type_counted = 0
  mail_icon_cnt = 0
  user_icon_type = 0
  while return_type_counted < type_cnt:
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
      # print(f'送信履歴あり {user_name} ~ skip ~')
      mail_icon_cnt += 1
      user_icon_type += 1
      # # メールアイコンが5つ続いたら終了
      if mail_icon_cnt == 5:
        ds_logo = driver.find_element(By.CLASS_NAME, value="ds_logo")
        top_link = ds_logo.find_element(By.TAG_NAME, value="a")
        top_link.click()
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(wait_time)
        print("タイプリストで送信履歴のあるユーザーが５回続きました")
        return return_type_counted
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
      catch_warning_screen(driver)
      # fst_messageを入力
      text_area = driver.find_element(By.ID, value="text-message")
      text_area.send_keys(fst_message)
      # script = "arguments[0].value = arguments[1];"
      # driver.execute_script(script, text_area, fst_message)
      # 送信
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
      return_type_counted += 1
      now = datetime.now().strftime('%m-%d %H:%M:%S')
      print(f'{name}:タイプ返し {user_name} ~ {str(return_type_counted)} ~ {now}')
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
  return return_type_counted
      
def return_footpoint(name, driver, wait, return_foot_message, matching_cnt, type_cnt, return_foot_cnt, return_foot_img, fst_message):
    wait_time = random.uniform(2, 3)
    driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
    return_cnt = 0
    mail_icon_cnt = 0
    duplication_user = False
    user_name_list = []
    user_icon = 0
    if return_foot_img:
      # 画像データを取得してBase64にエンコード
      image_response = requests.get(return_foot_img)
      image_base64 = base64.b64encode(image_response.content).decode('utf-8')
      # ローカルに一時的に画像ファイルとして保存
      image_filename = f"{name}_image.png"
      with open(image_filename, 'wb') as f:
          f.write(base64.b64decode(image_base64))
      # 画像の保存パスを取得
      image_path = os.path.abspath(image_filename)
    else:
      image_path = ""
      image_filename = None 
    # マッチング返し
    matching_counted = 0
    try:
      matching_counted = return_matching(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, image_path, matching_cnt)
      print(f"マッチング返し総数 {matching_counted}")
    except Exception as e:  
      print("マッチング返しエラー")
      # print(traceback.format_exc())
      driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)
    # タイプ返し
    type_counted = 0
    try:
      type_counted = return_type(name, wait, wait_time, driver, user_name_list, duplication_user, fst_message, image_path, type_cnt)
      print(f"タイプ返し総数 {type_counted}")
    except Exception as e:  
      print("タイプ返しエラー")
      # print(traceback.format_exc())
      driver.get("https://happymail.co.jp/sp/app/html/mbmenu.php")
      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
      time.sleep(wait_time)      
    # print(f"メッセージ送信数　{return_cnt} {matching_counted} {type_counted}")
    # 足跡返し
    try:
      while return_foot_cnt >= return_cnt + 1:
        warning_pop = catch_warning_screen(driver)
        if warning_pop:
          print(f"{name}：警告画面が出ている可能性があります")
          return
        # マイページをクリック
        nav_list = driver.find_elements(By.ID, value='ds_nav')
        if not len(nav_list):
            print(f"{name}: 警告画面が出ている可能性があります。")
            return
        mypage = nav_list[0].find_element(By.LINK_TEXT, "マイページ")
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
        while len(f_user) < 19:
          # ページの最後までスクロール
          driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
          time.sleep(2)
          f_user = driver.find_elements(By.CLASS_NAME, value="ds_post_head_main_info")
        name_field = f_user[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
        user_name = name_field.text
        mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
        send_skip_cnt = 0
        while len(mail_icon) or user_name in user_name_list:
          if len(mail_icon):
            # print("***")
            # print(send_skip_cnt)
            user_icon += 1
            # print(f'送信履歴あり {user_name} ~ skip ~')
            send_skip_cnt += 1
            try:
              name_field = f_user[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
              user_name = name_field.text
              mail_icon = name_field.find_elements(By.TAG_NAME, value="img")
            except IndexError:
              print("送信可能なユーザーが見つかりませんでした")
              return return_cnt
            if send_skip_cnt > 19:
              print("送れないユーザーが20回続きました")
              return return_cnt
          elif len(user_name_list):
            while user_name in user_name_list:
                # print('重複ユーザー')
                # print("~~~")
                # print(send_skip_cnt)
                send_skip_cnt += 1
                user_icon = user_icon + 1
                if len(f_user) <= user_icon:
                  duplication_user = True
                  break
                name_field = f_user[user_icon].find_element(By.CLASS_NAME, value="ds_like_list_name")
                user_name = name_field.text
                if send_skip_cnt > 19:
                  print("送れないユーザーが20回続きました")
                  return return_cnt
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
              user_name_list.append(user_name)
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
          # 入力エリアが表示され、操作可能になるまで待機
          text_area = WebDriverWait(driver, 20).until(
              EC.visibility_of_element_located((By.ID, "text-message"))
          )
          # text_area = driver.find_element(By.ID, value="text-message")
          # 入力エリアをスクロールして中央に表示し、少し待機
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_area)
          time.sleep(1)  # 少し待機して安定させる
          script = "arguments[0].value = arguments[1];"
          driver.execute_script(script, text_area, return_foot_message)
          # 送信
          catch_warning_screen(driver)
          send_mail = driver.find_element(By.ID, value="submitButton")
          driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_mail)
          send_mail.click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(wait_time)
          send_msg_elem = driver.find_elements(By.CLASS_NAME, value="message__block__body__text--female")
          reload_cnt = 0
          while send_msg_elem[-1].text != return_foot_message:
            #  print(send_msg_elem[-1].text)
             driver.refresh()
             wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
             time.sleep(wait_time)
             send_msg_elem = driver.find_elements(By.CLASS_NAME, value="message__block__body__text--female")
             reload_cnt += 1
             if reload_cnt == 3:
                driver.refresh()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                break
          # 画像があれば送信
          if image_path:
            img_conform = driver.find_element(By.ID, value="media-confirm")
            plus_icon = driver.find_elements(By.ID, value="ds_js_media_display_btn")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", plus_icon[0])
            time.sleep(1)
            driver.execute_script("arguments[0].click();", plus_icon[0])         
            time.sleep(1)
            upload_file = driver.find_element(By.ID, "upload_file")
            # DEBUG
            # upload_file.send_keys("/Users/yamamotokenta/Desktop/myprojects/mail_operator/widget/picture/kumi_mizugi.jpeg")
            upload_file.send_keys(image_path)
            time.sleep(2)
            submit = driver.find_element(By.ID, value="submit_button")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", submit)
            driver.execute_script("arguments[0].click();", submit)
            while img_conform.is_displayed():
              time.sleep(2)
          return_cnt += 1
          mail_icon_cnt = 0
          user_icon = 0
          now = datetime.now().strftime('%m-%d %H:%M:%S')
          print(f'{name}:足跡返し  ~ {str(return_cnt)} ~ {user_name} {now}')
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

      # ファイルが存在しているか確認し、削除
      if image_filename:
        if os.path.exists(image_filename):
            os.remove(image_filename)
      if return_cnt == None:
        return_cnt = 0
      return return_cnt
    except WebDriverException as e:
      print("in return_footpoint")
      error_message = str(e)
      if "unexpectedly exited. Status code was: -9" in error_message:
          print("Chromedriverが予期せず終了しました。再起動して起動してください。")
          driver.quit()

    finally: 
      # ファイルが存在しているか確認し、削除
      if image_filename:
        if os.path.exists(image_filename):
            os.remove(image_filename)
      if return_cnt == None:
        return_cnt = 0
      return [matching_counted, type_counted, return_cnt]
       

def make_footprints(name, happymail_id, happymail_pass, driver, wait, foot_count):
   driver.delete_all_cookies()
   driver.get("https://happymail.jp/login/")
   # loaderが消えるのを待つ
   WebDriverWait(driver, 10).until(
      EC.invisibility_of_element_located((By.CLASS_NAME, "loader"))
   )
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
   nav_list = driver.find_elements(By.ID, value='ds_nav')
   if not len(nav_list):
      print(f"{name}: 警告画面が出ている可能性があります。")
      return
   mypage = nav_list[0].find_element(By.LINK_TEXT, "プロフ検索")
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
      warinig_flug = catch_warning_screen(driver)
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
      catch_warning_screen(driver)
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
      catch_warning_screen(driver)
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


def send_fst_message(happy_user_list, driver, wait):
  for user_info in happy_user_list:
    name,login_id, passward, fst_message, mail_img = user_info
    limit_cnt = 1
    
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
  

def check_new_mail(happy_info, driver, wait):
  return_list = []
  name = happy_info["name"]
  login_id = happy_info["login_id"]
  login_pass = happy_info["password"]
  fst_message = happy_info["fst_message"]
  conditions_message = happy_info["second_message"]   
  return_foot_message = happy_info["return_foot_message"]   
  print(f"{name} チェック開始")
  if not login_id:
    print(f"{name}のログインIDを取得できませんでした")
    return
  driver.delete_all_cookies()
  # driver.implicitly_wait(15)
  try:
    driver.get("https://happymail.jp/login/")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  except TimeoutException:
    print("Timeout reached, retrying...")
    driver.refresh()  # ページをリフレッシュして再試行
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    
  wait_time = random.uniform(2, 5)
  time.sleep(wait_time)
  id_form = driver.find_element(By.ID, value="TelNo")
  id_form.send_keys(login_id)
  pass_form = driver.find_element(By.ID, value="TelPass")
  pass_form.send_keys(login_pass)
  time.sleep(wait_time)
  send_form = driver.find_element(By.ID, value="login_btn")
  try:
    send_form.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
  except TimeoutException:
    print("Timeout reached, retrying...")
    driver.refresh()  # ページをリフレッシュして再試行
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    
    
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
  # 画像チェック
  top_img_element = driver.find_elements(By.CLASS_NAME, value="ds_mypage_user_image")
  if len(top_img_element):
     top_img = top_img_element[0].get_attribute("style")
     if "noimage" in top_img:
        print(f"{name}のトップ画の設定がNoImageです")
        return_list.append(f"{name},{login_id}:{login_pass} ハッピーメールのトップ画像がNOIMAGEの可能性があります.....")
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
    #  only_new_message = driver.find_elements(By.CLASS_NAME, value="ds_message_tab_item")[2]
     only_new_message = driver.find_elements(By.CLASS_NAME, value="ds_message_tab_item")[1]
     only_new_message.click()
     time.sleep(1)
    #  ds_message_list_mini
     new_mail = driver.find_elements(By.CLASS_NAME, value="ds_message_list_mini")  
     if not len(new_mail):
         list_load = driver.find_elements(By.ID, value="load_bL")
         if len(list_load):
          list_load[0].click()
         time.sleep(2)
     #新着がある間はループ
    #  b = 0
    #  while b == 0:
    #     b+= 1  
     
     while len(new_mail):
        # parent_element = new_mail[0].find_element(By.XPATH, value="..")
        # next_element = parent_element.find_element(By.XPATH, value="following-sibling::*")
        date = new_mail[0].find_elements(By.CLASS_NAME, value="ds_message_date") 
        # print(date[0].text)       
        date_numbers = re.findall(r'\d+', date[0].text)
        # print(date_numbers)
        if not len(date_numbers):
           for_minutes_passed = True
        else:
          now = datetime.today()
          arrival_datetime = datetime(
            year=now.year,
            month=now.month,
            day=now.day,
            hour=int(date_numbers[0]),
            minute=int(date_numbers[1])
          )
          elapsed_time = now - arrival_datetime
          # print(f"メール到着からの経過時間{elapsed_time}")
          # 4分経過しているか
          # if True:
          if elapsed_time >= timedelta(minutes=4):
             for_minutes_passed = True
          else:
             for_minutes_passed = False
        if for_minutes_passed:
          print("4分以上経過しているメッセージあり。")
          # s = driver.find_elements(By.CLASS_NAME, value="ds_message_list_top")
          # s[0].click()
          new_mail[0].click()
          wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
          time.sleep(2)
          catch_warning_screen(driver)
          send_message = driver.find_elements(By.CLASS_NAME, value="message__block--send")    

          if len(send_message):
            send_text = send_message[-1].find_elements(By.CLASS_NAME, value="message__block__body__text")[0].text
            if not send_text:
                send_text = send_message[-2].find_elements(By.CLASS_NAME, value="message__block__body__text")[0].text
            # print("<<<<<<<<<<<send_text>>>>>>>>>>>>>")
            # print(send_text)
            # print("<<<<<<<<<<<fst_message>>>>>>>>>>>>>")
            # print(fst_message)
            # print("<<<<<<<<<<<return_foot_message>>>>>>>>>>>>>")
            # print(return_foot_message)
            # 改行と空白を削除
            send_text_clean = func.normalize_text(send_text)
            fst_message_clean = func.normalize_text(fst_message)
            return_foot_message_clean = func.normalize_text(return_foot_message)
            conditions_message_clean = func.normalize_text(conditions_message)
            
            # 変換後のデバッグ表示
            # print("---------------------------------------")
            # print(f"変換後のsend_text: {repr(send_text_clean)}")
            # print("---------------------------------------")
            # print(f"変換後のfst_message: {repr(fst_message_clean)}")
            # print("---------------------------------------")
            # print(f"変換後のreturn_foot_message: {repr(return_foot_message_clean)}")
            
            # print("---------------------------------------")
            # print(fst_message_clean == send_text_clean)
            # print("---------------------------------------")
            # print(return_foot_message_clean == send_text_clean)
            # print("---------------------------------------")
            # print("募集メッセージ" in send_text)

            if fst_message_clean == send_text_clean or return_foot_message_clean == send_text_clean or "募集メッセージ" in send_text_clean:
              if conditions_message:
                text_area = driver.find_element(By.ID, value="text-message")
                driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", text_area)
                # text_area.send_keys(return_foot_message)
                script = "arguments[0].value = arguments[1];"
                driver.execute_script(script, text_area, conditions_message)
                # text_area.send_keys(conditions_message)
                # 送信
                send_mail = driver.find_element(By.ID, value="submitButton")
                send_mail.click()
                wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                time.sleep(wait_time)
                send_msg_elem = driver.find_elements(By.CLASS_NAME, value="message__block__body__text--female")
                reload_cnt = 0
                send_text_clean = func.normalize_text(send_msg_elem[-1].text)
                while send_text_clean != conditions_message_clean:
                  
                  driver.refresh()
                  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                  time.sleep(5)
                  send_msg_elem = driver.find_elements(By.CLASS_NAME, value="message__block__body__text--female")
                  reload_cnt += 1
                  if reload_cnt == 3:
                      driver.refresh()
                      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                      time.sleep(wait_time)
                      break
              else:
                # print('やり取りしてます')
                user_name = driver.find_elements(By.CLASS_NAME, value="app__navbar__item--title")[1]
                user_name = user_name.text
                receive_contents = driver.find_elements(By.CLASS_NAME, value="message__block--receive")[-1]
                return_message = f"{name}happymail,{login_id}:{login_pass}\n{user_name}「{receive_contents.text}」"
                return_list.append(return_message)
                # みちゃいや
                plus_icon_parent = driver.find_elements(By.CLASS_NAME, value="message__form__action")
                plus_icon = plus_icon_parent[0].find_elements(By.CLASS_NAME, value="icon-message_plus")
                
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
                  # print('<<<<<<<<<<<<<<<<<みちゃいや登録>>>>>>>>>>>>>>>>>>>')
                  mityaiya.click()
                  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                  time.sleep(2)
                  mityaiya_send = driver.find_elements(By.CLASS_NAME, value="input__form__action__button__send")
                  if len(mityaiya_send):
                    mityaiya_send[0].click()
                    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                    time.sleep(1)
                  
            else:
              # print('やり取りしてます')
              user_name = driver.find_elements(By.CLASS_NAME, value="app__navbar__item--title")[1]
              user_name = user_name.text
              receive_contents = driver.find_elements(By.CLASS_NAME, value="message__block--receive")[-1]
              return_message = f"{name}happymail,{login_id}:{login_pass}\n{user_name}「{receive_contents.text}」"
              return_list.append(return_message)

              # みちゃいや
              plus_icon_parent = driver.find_elements(By.CLASS_NAME, value="message__form__action")
              plus_icon = plus_icon_parent[0].find_elements(By.CLASS_NAME, value="icon-message_plus")
              
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
                # print('<<<<<<<<<<<<<<<<<みちゃいや登録>>>>>>>>>>>>>>>>>>>')
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
            script = "arguments[0].value = arguments[1];"
            driver.execute_script(script, text_area, fst_message)
            # text_area.send_keys(fst_message)
            # 送信
            send_mail = driver.find_element(By.ID, value="submitButton")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", send_mail)
            send_mail.click()
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
            time.sleep(wait_time)
            send_msg_elem = driver.find_elements(By.CLASS_NAME, value="message__block__body__text--female")
            reload_cnt = 0
            while send_msg_elem[-1].text != fst_message:
                  driver.refresh()
                  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                  time.sleep(5)
                  send_msg_elem = driver.find_elements(By.CLASS_NAME, value="message__block__body__text--female")
                  # print(send_msg_elem[-1].text)
                  reload_cnt += 1
                  if reload_cnt == 3:
                      driver.refresh()
                      wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
                      time.sleep(wait_time)
                      break
           
        else:
          if len(return_list):
              return return_list
          else:
              return None
        driver.get("https://happymail.co.jp/sp/app/html/message_list.php")
        wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
        time.sleep(2)
        new_mail = driver.find_elements(By.CLASS_NAME, value="happy_blue_10")
        print(777)
        print(len(new_mail))
     
  if len(return_list):
    return return_list
  else:
    return None
  
# def re_registration(name, driver):
  
#   func.get_user_data()
#       login_id = row[2]
#       login_pass = row[3]
     
     
#   if not login_id:
#     return

#   driver.delete_all_cookies()
#   wait = WebDriverWait(driver, 15)  
#   driver.get("https://happymail.jp/login/")
#   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#   # wait_time = random.uniform(2, 5)
#   time.sleep(2)
#   id_form = driver.find_element(By.ID, value="TelNo")
#   id_form.send_keys(login_id)
#   pass_form = driver.find_element(By.ID, value="TelPass")
#   pass_form.send_keys(login_pass)
#   time.sleep(1)
#   send_form = driver.find_element(By.ID, value="login_btn")
#   send_form.click()
#   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#   time.sleep(2)

#   # 警告画面が出たらスキップ
#   warning = driver.find_elements(By.CLASS_NAME, value="ds_main_header_text")
#   if warning:
#      print("警告画面が出ました")
#      return
#   # マイページをクリック
#   nav_list = driver.find_element(By.ID, value='ds_nav')
#   mypage = nav_list.find_element(By.LINK_TEXT, "マイページ")
#   mypage.click()
#   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#   time.sleep(2)
#   # プロフィールをクリック
#   common_list = driver.find_element(By.CLASS_NAME, "ds_common_table")
#   common_table = common_list.find_elements(By.CLASS_NAME, "ds_mypage_text")
#   for common_table_elem in common_table:
#      if "プロフィール" in common_table_elem.text:
#         mylist = common_table_elem
#   driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", mylist)
#   time.sleep(2)
#   mylist.click()
#   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#   time.sleep(2)
  
#   # 名前
#   links = driver.find_elements(By.CLASS_NAME, value="input__form__input__block")
#   name_link = links[5].click()
#   wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#   time.sleep(2)
#   name_textarea = driver.find_elements(By.CLASS_NAME, value="text_content")
#   name_textarea_value = name_textarea[0].get_attribute("value")
#   if name == name_textarea_value:
#     driver.back()
#     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#     time.sleep(2)
#   else:
#     name_textarea[0].clear()
#     name_textarea[0].send_keys(name)
#     save_button = driver.find_elements(By.ID, value="save")
#     save_button[0].click()
#     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#     time.sleep(2)
#     save_confirmation = driver.find_elements(By.CLASS_NAME, value="modal-confirm")
#     save_confirmation[0].click()
#     wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
#     time.sleep(20)
#   # 年齢
#   age_select = driver.find_elements(By.ID, value="age")
#   select = Select(age_select[0])
#   select.select_by_visible_text(age)
#   time.sleep(1)

def re_registration(chara_data, driver, wait):
  driver.delete_all_cookies()
  try:
    driver.get("https://happymail.jp/login/")
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  except TimeoutException:
    print("Timeout reached, retrying...")
    driver.refresh()  # ページをリフレッシュして再試行
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    
  wait_time = random.uniform(2, 3)
  time.sleep(wait_time)
  id_form = driver.find_element(By.ID, value="TelNo")
  id_form.send_keys(chara_data["login_id"])
  pass_form = driver.find_element(By.ID, value="TelPass")
  pass_form.send_keys(chara_data["password"])
  time.sleep(wait_time)
  send_form = driver.find_element(By.ID, value="login_btn")
  try:
    send_form.click()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(2)
  except TimeoutException:
    print("Timeout reached, retrying...")
    driver.refresh()  # ページをリフレッシュして再試行
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  remodal = driver.find_elements(By.CLASS_NAME,value="remodal-close")
  if len(remodal):
     remodal[0].click()
     time.sleep(2)
  warning = driver.find_elements(By.CLASS_NAME, value="information__dialog")
  if len(warning):
     print(f"{chara_data['name']},{chara_data['login_id']}:{chara_data['password']} ハッピーメールに警告画面が出ている可能性があります")
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
     print(f"{chara_data['name']},{chara_data['login_id']}:{chara_data['password']} ハッピーメールに警告画面が出ている可能性があります")
  # 画像チェック
  top_img_element = driver.find_elements(By.CLASS_NAME, value="ds_mypage_user_image")
  if len(top_img_element):
     top_img = top_img_element[0].get_attribute("style")
     if "noimage" in top_img:
        print(f"{chara_data['name']}のトップ画の設定がNoImageです")
  # マイページをクリック
  nav_list = driver.find_elements(By.ID, value='ds_nav')
  if not len(nav_list):
      print(f"{chara_data['name']}: 警告画面が出ている可能性があります。")
      return
  mypage = nav_list[0].find_element(By.LINK_TEXT, "マイページ")
  mypage.click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # プロフィールをクリック 
  profile = driver.find_element(By.CLASS_NAME, value="icon-ico_profile ")
  driver.execute_script("arguments[0].click();", profile)
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # name 
  name_form = driver.find_elements(By.ID, value="nickname_frame")
  driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", name_form[0])
  name_form[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(wait_time)
  # text_content
  name_text_area = driver.find_elements(By.CLASS_NAME, value="text_content")
  print(name_text_area[0].get_attribute("value"))
  if name_text_area[0].get_attribute("value") != chara_data["name"]:
    name_text_area[0].clear()
    name_text_area[0].send_keys(chara_data["name"])
    time.sleep(1)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # save
    save_button = driver.find_elements(By.ID, value="save")
    save_button[0].click()
    time.sleep(2)
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # modal-button-blue
    modal_save_button = driver.find_elements(By.CLASS_NAME, value="modal-button-blue")
    modal_save_button[0].click()
    time.sleep(2)
  else:
    driver.back()
    wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    time.sleep(wait_time)
  # 年齢
  if chara_data["age"]:
    age_text_area = driver.find_elements(By.ID, value="age")
    select = Select(age_text_area[0])
    select.select_by_visible_text(chara_data["age"])
    time.sleep(2)
    if age_text_area[0].get_attribute("value") != chara_data["age"]:
      select.select_by_visible_text(chara_data["age"])
      time.sleep(2)

  # 居住地
  if chara_data["activity_area"]:
    activity_area_text_area = driver.find_elements(By.ID, value="area")
    select = Select(activity_area_text_area[0])
    select.select_by_visible_text(chara_data["activity_area"])
    time.sleep(2)
    if activity_area_text_area[0].get_attribute("value") != chara_data["activity_area"]:
      select.select_by_visible_text(chara_data["activity_area"])
      time.sleep(2)
  # 詳細エリア
  if chara_data["detail_activity_area"]:
    
    detail_activity_area_text_area = driver.find_elements(By.ID, value="city")
    print(len(detail_activity_area_text_area))
    select = Select(detail_activity_area_text_area[0])
    select.select_by_visible_text(chara_data["detail_activity_area"])
    time.sleep(2)
    if detail_activity_area_text_area[0].get_attribute("value") != chara_data["detail_activity_area"]:
      select.select_by_visible_text(chara_data["detail_activity_area"])
      time.sleep(2)
  # member_birth_area 
  if chara_data["birth_place"]:
    member_birth_area_text_area = driver.find_elements(By.NAME, value="member_birth_area")
    select = Select(member_birth_area_text_area[0])
    
    select.select_by_visible_text(chara_data["birth_place"])
    time.sleep(2)
    if member_birth_area_text_area[0].get_attribute("value") != chara_data["birth_place"]:
      select.select_by_visible_text(chara_data["birth_place"])
      time.sleep(2)
  # blood_type
  if chara_data["blood_type"]:
    blood_type_text_area = driver.find_elements(By.NAME, value="blood_type")
    select = Select(blood_type_text_area[0])
    select.select_by_visible_text(chara_data["blood_type"])
    time.sleep(2)
    if blood_type_text_area[0].get_attribute("value") != chara_data["blood_type"]:
      select.select_by_visible_text(chara_data["blood_type"])
      time.sleep(2)
  # constellation
  if chara_data["constellation"]:
    constellation_text_area = driver.find_elements(By.NAME, value="constellation")
    select = Select(constellation_text_area[0])
    select.select_by_visible_text(chara_data["constellation"])
    time.sleep(2)
    if constellation_text_area[0].get_attribute("value") != chara_data["constellation"]:
      select.select_by_visible_text(chara_data["constellation"])
      time.sleep(2)
  # height
  if chara_data["height"]:
    height_text_area = driver.find_elements(By.NAME, value="height")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", height_text_area[0])
    driver.execute_script("arguments[0].click();", height_text_area[0])
    time.sleep(2)
    height_choicises_elem = driver.find_elements(By.ID, value="height_choice")
    height_choices = height_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in height_choices:
      if i.text == chara_data["height"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # menu_modal_cancel
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # スタイル
  if chara_data["style"]:
    style_text_area = driver.find_elements(By.NAME, value="style")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", style_text_area[0])
    driver.execute_script("arguments[0].click();", style_text_area[0])
    time.sleep(1)
    style_choicises_elem = driver.find_elements(By.ID, value="style_choice")
    style_choices = style_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in style_choices:
      if i.text == chara_data["style"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # menu_modal_cancel
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # ルックス
  if chara_data["looks"]:
    looks_text_area = driver.find_elements(By.NAME, value="type")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", looks_text_area[0])
    driver.execute_script("arguments[0].click();", looks_text_area[0])
    time.sleep(1)
    looks_choicises_elem = driver.find_elements(By.ID, value="type_choice")
    looks_choices = looks_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in looks_choices:
      if i.text == chara_data["looks"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # menu_modal_cancel
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # カップ
  if chara_data["cup"]:
    cup_text_area = driver.find_elements(By.NAME, value="bust_size")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", cup_text_area[0])
    driver.execute_script("arguments[0].click();", cup_text_area[0])
    time.sleep(1)
    cup_choicises_elem = driver.find_elements(By.ID, value="bust_size_choice")
    cup_choices = cup_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in cup_choices:
      if i.text == chara_data["cup"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # menu_modal_cancel
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # 職業
  if chara_data["job"]:
    job_text_area = driver.find_elements(By.NAME, value="job")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", job_text_area[0])
    driver.execute_script("arguments[0].click();", job_text_area[0])
    time.sleep(1)
    job_choicises_elem = driver.find_elements(By.ID, value="job_choice")
    job_choices = job_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in job_choices:
      if i.text == chara_data["job"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    # menu_modal_cancel
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # educational_background
  if chara_data["education"]:
    education_text_area = driver.find_elements(By.NAME, value="educational_background")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", education_text_area[0])
    driver.execute_script("arguments[0].click();", education_text_area[0])
    time.sleep(1)
    education_choicises_elem = driver.find_elements(By.ID, value="educational_background_choice")
    education_choices = education_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in education_choices:
      if i.text == chara_data["education"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # holiday
  if chara_data["holiday"]:
    holiday_text_area = driver.find_elements(By.NAME, value="holiday")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", holiday_text_area[0])
    driver.execute_script("arguments[0].click();", holiday_text_area[0])
    time.sleep(1)
    holiday_choicises_elem = driver.find_elements(By.ID, value="holiday_choice")
    holiday_choices = holiday_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in holiday_choices:
      if i.text == chara_data["holiday"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # child
  if chara_data["having_children"]:
    child_text_area = driver.find_elements(By.NAME, value="child")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", child_text_area[0])
    driver.execute_script("arguments[0].click();", child_text_area[0])
    time.sleep(1)
    child_choicises_elem = driver.find_elements(By.ID, value="child_choice")
    child_choices = child_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in child_choices:
      if i.text == chara_data["having_children"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # intention_to_marry
  if chara_data["intention_to_marry"]:
    intention_to_marry_text_area = driver.find_elements(By.NAME, value="child")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", intention_to_marry_text_area[0])
    driver.execute_script("arguments[0].click();", intention_to_marry_text_area[0])
    time.sleep(1)
    intention_to_marry_choicises_elem = driver.find_elements(By.ID, value="intention_to_marry_choice")
    intention_to_marry_choices = intention_to_marry_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in intention_to_marry_choices:
      if i.text == chara_data["intention_to_marry"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # tobacco
  if chara_data["smoking"]:
    tobacco_text_area = driver.find_elements(By.NAME, value="tobacco")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", tobacco_text_area[0])
    driver.execute_script("arguments[0].click();", tobacco_text_area[0])
    time.sleep(1)
    tobacco_choicises_elem = driver.find_elements(By.ID, value="tobacco_choice")
    tobacco_choices = tobacco_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in tobacco_choices:
      if i.text == chara_data["smoking"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # liquor
  if chara_data["sake"]:
    liquor_text_area = driver.find_elements(By.NAME, value="liquor")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", liquor_text_area[0])
    driver.execute_script("arguments[0].click();", liquor_text_area[0])
    time.sleep(1)
    liquor_choicises_elem = driver.find_elements(By.ID, value="liquor_choice")
    liquor_choices = liquor_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in liquor_choices:
      if i.text == chara_data["sake"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # car
  if chara_data["car_ownership"]:
    car_text_area = driver.find_elements(By.NAME, value="car")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", car_text_area[0])
    driver.execute_script("arguments[0].click();", car_text_area[0])
    time.sleep(1)
    car_choicises_elem = driver.find_elements(By.ID, value="car_choice")
    car_choices = car_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in car_choices:
      if i.text == chara_data["car_ownership"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # housemate
  if chara_data["roommate"]:
    housemate_text_area = driver.find_elements(By.NAME, value="housemate")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", housemate_text_area[0])
    driver.execute_script("arguments[0].click();", housemate_text_area[0])
    time.sleep(1)
    housemate_choicises_elem = driver.find_elements(By.ID, value="housemate_choice")
    housemate_choices = housemate_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in housemate_choices:
      if i.text == chara_data["roommate"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # brother
  if chara_data["brothers_and_sisters"]:
    brother_text_area = driver.find_elements(By.NAME, value="brother")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", brother_text_area[0])
    driver.execute_script("arguments[0].click();", brother_text_area[0])
    time.sleep(1)
    brother_choicises_elem = driver.find_elements(By.ID, value="brother_choice")
    brother_choices = brother_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in brother_choices:
      if i.text == chara_data["brothers_and_sisters"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # hope_before_meet
  if chara_data["until_we_met"]:
    hope_before_meet_text_area = driver.find_elements(By.NAME, value="hope_before_meet")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", hope_before_meet_text_area[0])
    driver.execute_script("arguments[0].click();", hope_before_meet_text_area[0])
    time.sleep(1)
    hope_before_meet_choicises_elem = driver.find_elements(By.ID, value="hope_before_meet_choice")
    hope_before_meet_choices = hope_before_meet_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in hope_before_meet_choices:
      if i.text == chara_data["until_we_met"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
  # first_date_cost
  if chara_data["date_expenses"]:
    first_date_cost_text_area = driver.find_elements(By.NAME, value="first_date_cost")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", first_date_cost_text_area[0])
    driver.execute_script("arguments[0].click();", first_date_cost_text_area[0])
    time.sleep(1)
    first_date_cost_choicises_elem = driver.find_elements(By.ID, value="first_date_cost_choice")
    first_date_cost_choices = first_date_cost_choicises_elem[0].find_elements(By.TAG_NAME, value="span")
    for i in first_date_cost_choices:
      if i.text == chara_data["date_expenses"]:
          classes = i.get_attribute("class")
          if not "chose" in classes.split():
            i.click()
            time.sleep(2)
            wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    modal_cancel = driver.find_elements(By.CLASS_NAME, value="menu_modal_cancel")
    modal_cancel[0].click()
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 0);")
  # profile_confirmation
  profile_save = driver.find_elements(By.ID, value="profile_confirmation")
  profile_save[0].click()
  wait.until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
  time.sleep(2)


  
     



