from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
from selenium.webdriver.common.by import By
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import pcmax, happymail, func
from selenium.webdriver.support.ui import WebDriverWait
import traceback
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import sqlite3
import time 
from datetime import datetime, timedelta, time as dt_time  
import socket
order_list = [
   ["アスカ", "asuka414510@gmail.com"],
#    ["あやか", "ayaka414510@gmail.com"],
   ["いおり", "iori547253@gmail.com"],
   ["えりか", "k.erika414510@gmail.com"],
   ["きりこ", "kiriko414510@gmail.com"],
   ["くみ", "kumi414510@gmail.com"],
   ["さな", "sana.cnfwijl@gmail.com"],
   ["すい", "sui187586@gmail.com"],
   ["つむぎ", "tumtum.jpwa@gmail.com"],
   ["なお", "n414510a@gmail.com"],
#    ["ハル", "haruru414510@gmail.com"],
#    ["はづき", "k.haru414510@gmail.com"], 
#    ["めあり", "meari414510@gmail.com"],
#    ["りこ", "riko414510@gmail.com"],
#    ["りな", "k.rina414510@gmail.com"],
#    ["ゆうな", "y8708336@gmail.com"],
#    ["ゆっこ", "yuko414510@gmail.com"], 
#    ["ゆかり", "y216154@gmail.com"],
  
]
# order_list = [
#      ["すい", "sui187586@gmail.com"],

#    ]

def wait_if_near_midnight():
    current_time = datetime.now().time()
    
    # 現在時刻が23:50を越えているかをチェック
    if current_time >= dt_time(23, 55):
        print("23:55を過ぎたので、0:05まで待機します。")
        # 0:05までの残り時間を計算
        target_time = datetime.combine(datetime.date.today(), dt_time(0, 5))
        if current_time.hour == 23:
            target_time += timedelta(days=1)  # 翌日の0:05を設定
        time_to_wait = (target_time - datetime.datetime.now()).total_seconds()
        
        # 残り時間を待機
        time.sleep(time_to_wait)
        print("待機終了、処理を再開します。")
    return

def check_mail(user_data, driver, wait):
  happymail_list = user_data['happymail']
  print(happymail_list)
  pcmax_list = user_data['pcmax']
  try:
    pcmax_return_foot_count_dic = {
            "アスカ": 0,
            "いおり": 0,
            "えりか": 0,
            "きりこ": 0,
            "くみ": 0,
            "さな": 0,
            "すい": 0,
            "つむぎ": 0,
            "なお": 0,
            "ハル": 0,
            "はづき": 0,
            "めあり": 0,
            "りこ": 0,
            "りな": 0,
            "ゆうな": 0,
            "ゆっこ": 0,
            "ゆかり": 0,   
            "わかな": 0,   
        }
    
    send_flug = True
    while True:
        start_time = time.time() 
        current_datetime = datetime.utcfromtimestamp(int(start_time))
    
        for happy_info in happymail_list:
            new_mail_lists = []
            debug = False
            # ハッピーメール
            try:
                
                happymail_new = happymail.check_new_mail(driver, wait, happy_info)
                if happymail_new:
                    new_mail_lists.append(happymail_new)
                
            except Exception as e:
                # print(f"<<<<<<<<<<メールチェックエラー：ハッピーメール{order_info[0]}>>>>>>>>>>>")
                print(traceback.format_exc())
                # func.send_error(f"メールチェックエラー：ハッピーメール{order_info[0]}", traceback.format_exc())    
            wait_if_near_midnight()
        # pcmax
        # try:
            
        #     pcmax_new, return_foot_cnt = pcmax.check_new_mail(driver, wait, order_info[0])
            
        #     if pcmax_new != 1:
        #         new_mail_lists.append(pcmax_new)
        
        #     if return_foot_cnt:     
        #         for r_f_user in pcmax_return_foot_count_dic:
        #             if order_info[0] == r_f_user:
        #                 # print(777)
        #                 # print(return_foot_count_dic[r_f_user])
        #                 pcmax_return_foot_count_dic[r_f_user] = pcmax_return_foot_count_dic[r_f_user] + return_foot_cnt
        #                 # print(return_foot_count_dic[r_f_user])
        #     driver.quit()
        # except Exception as e:
        #     # print(f"<<<<<<<<<<メールチェックエラー：pcmax{order_info[0]}>>>>>>>>>>>")
        #     print(traceback.format_exc())
        #     # func.send_error(f"メールチェックエラー：pcmax{order_info[0]}", traceback.format_exc())

        #     driver.quit()
        # wait_if_near_midnight()
            # jmail
            # try:
            #     driver, wait = get_driver(debug)
            #     jmail_new, return_foot_cnt = jmail.check_new_mail(driver, wait, order_info[0])
            #     if jmail_new == 2:
            #         new_mail_lists.append(f"jmail:{order_info[0]} ログインできませんでした")
            #     elif jmail_new != 1:
            #         new_mail_lists.append(jmail_new)
            #     if return_foot_cnt:     
            #         for r_f_user in jmail_return_foot_count_dic:
            #             if order_info[0] == r_f_user:
            #                 # print(777)
            #                 # print(jmail_return_foot_count_dic[r_f_user])
            #                 # print(return_foot_cnt)
            #                 jmail_return_foot_count_dic[r_f_user] = jmail_return_foot_count_dic[r_f_user] + return_foot_cnt
            #                 # print(jmail_return_foot_count_dic[r_f_user])
            #     driver.quit()
            # except Exception as e:
            #     print(f"<<<<<<<<<<メールチェックエラー：jmail{order_info[0]}>>>>>>>>>>>")
            #     print(traceback.format_exc())
            #     func.send_error(f"メールチェックエラー：jmail{order_info[0]}", traceback.format_exc())
            #     driver.quit()
            
            
            # メール送信
            if len(new_mail_lists) == 0:
                # print(f'{order_info[0]}新着チェック完了手動メールなし')
                pass
            else:
                # print(f'{order_info[0]}新着チェック完了手動メールあり')
                print(new_mail_lists)
                mailaddress = 'kenta.bishi777@gmail.com'
                password = 'rjdzkswuhgfvslvd'
                text = ""
                subject = "新着メッセージ"
            
                for new_mail_list in new_mail_lists:
                    # print('<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>')
                    # print(new_mail_list)
                    for new_mail in new_mail_list:

                        text = text + new_mail + ",\n"
                        if "警告" in text:
                            subject = "メッセージ"
                address_from = 'kenta.bishi777@gmail.com'
                # address_to = 'bidato@wanko.be'
                address_to = "ryapya694@ruru.be"
                # address_to = 'misuzu414510@gmail.com'

                try:
                    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
                    smtpobj.starttls()
                    smtpobj.login(mailaddress, password)
                    msg = MIMEText(text)
                    msg['Subject'] = subject
                    msg['From'] = address_from
                    msg['To'] = address_to
                    msg['Date'] = formatdate()
                    smtpobj.send_message(msg)
                except smtplib.SMTPDataError as e:
                    print(f"SMTPDataError: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                smtpobj.close()
        elapsed_time = time.time() - start_time  
        elapsed_timedelta = timedelta(seconds=elapsed_time)
        elapsed_time_formatted = str(elapsed_timedelta)
        # print(f"<<<<<<<<<<<<<<<<<<<<足跡返し総数　　開始時間{current_datetime}, 経過時間{elapsed_time_formatted}>>>>>>>>>>>>>>>>>>>>")
        # print(pcmax_return_foot_count_dic)
        # print("<<<<<<<<<<<<<<<jmail>>>>>>>>>>>>>>>>>>>>>>>")
        # print(jmail_return_foot_count_dic)

        # 現在時刻を取得
        # now = datetime.now()
        # 現在時刻の時間と分を取得
        # current_hour = now.hour
        # current_minute = now.minute
        # もし現在時刻が10:00から10:20の間だったら
        # if current_hour == 10 and 0 <= current_minute <= 20 and send_flug:
        #     print("現在時刻は10:00から10:20の間です。特定の動作を実行します。")
        #     # ここに実行したい動作を追加
        #     mailaddress = 'kenta.bishi777@gmail.com'
        #     password = 'rjdzkswuhgfvslvd'
        #     text = str(jmail_return_foot_count_dic)  # 辞書を文字列に変換
        #     subject = "jメール足跡返し件数"
        #     address_from = 'kenta.bishi777@gmail.com'
        #     # address_to = 'bidato@wanko.be'
        #     address_to = "ryapya694@ruru.be"
        #     # address_to = 'misuzu414510@gmail.com'
        #     try:
        #         smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
        #         smtpobj.set_debuglevel(0)
        #         smtpobj.starttls()
        #         smtpobj.login(mailaddress, password)
        #         msg = MIMEText(text)
        #         msg['Subject'] = subject
        #         msg['From'] = address_from
        #         msg['To'] = address_to
        #         msg['Date'] = formatdate()
        #         smtpobj.send_message(msg)
        #     except smtplib.SMTPDataError as e:
        #         print(f"SMTPDataError: {e}")
        #     except Exception as e:
        #         print(f"An error occurred: {e}")
        #     smtpobj.close()
        #     send_flug = False
        # if current_hour == 11:
        #     send_flug = True
  except (smtplib.SMTPException, socket.gaierror) as e:
    print(f"メール送信中にエラーが発生しました: {e}")
    print("5分間待機して再試行します...")
    driver.quit()
    time.sleep(300)  # 300秒（5分）間待機
    driver, wait = func.get_driver(1)
    check_mail(user_data, driver, wait)
