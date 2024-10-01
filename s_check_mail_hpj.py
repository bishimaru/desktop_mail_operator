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
from selenium.common.exceptions import WebDriverException
import urllib3



def wait_if_near_midnight():
    # 現在時刻を取得
    now = datetime.now()
    # 現在時刻の時間と分を取得
    current_hour = now.hour
    current_minute = now.minute
    # もし現在時刻が23:55を過ぎていたら
    if current_hour == 23 and 55 <= current_minute:
        print("現在時刻は0時に近づいています。処理を一時中断します。")
        #     # ここに実行したい動作を追加
        time.sleep(600)
        print("処理を再開します。")
    return

def check_mail(user_data, driver, wait):
  happymail_list = user_data['happymail']
  pcmax_list = user_data['pcmax']
  conn = sqlite3.connect('user_data.db')
  c = conn.cursor()
  c.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
  chara_data = c.fetchone()
  mailaddress = chara_data[4]
  password = chara_data[5]
  receiving_address = chara_data[6]

  try:
    send_flug = True
    while True:
        start_time = time.time() 
        current_datetime = datetime.utcfromtimestamp(int(start_time))
        # ハッピーメール
        print(f'~~ハピメ:新着メールチェック開始~~')
        for happy_info in happymail_list:
            new_mail_lists = []
            try:
                happymail_new = happymail.check_new_mail(happy_info, driver, wait)
                if happymail_new:
                    new_mail_lists.append(happymail_new)
                # メール送信
                smtpobj = None
                if len(new_mail_lists) == 0:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f'{happy_info["name"]}チェック完了  {now}')
                    pass
                else:
                    if mailaddress and password and receiving_address:
                        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f'チェック完了　要確認メールあり  {now}')
                        print(new_mail_lists)
                        text = ""
                        subject = "新着メッセージ"
                    
                        for new_mail_list in new_mail_lists:
                            # print('<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>')
                            # print(new_mail_list)
                            for new_mail in new_mail_list:

                                text = text + new_mail + ",\n"
                                if "警告" in text:
                                    subject = "メッセージ"
                    try:
                        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
                        smtpobj.starttls()
                        smtpobj.set_debuglevel(0)
                        smtpobj.login(mailaddress, password)
                        msg = MIMEText(text)
                        msg['Subject'] = subject
                        msg['From'] = mailaddress
                        msg['To'] = receiving_address
                        msg['Date'] = formatdate()
                        smtpobj.send_message(msg)
                    except smtplib.SMTPDataError as e:
                        print(f"SMTPDataError: {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")
                    finally:
                        if smtpobj: 
                            smtpobj.close()   
            except Exception as e:
                print(f"<<<<<<<<<<メールチェックエラー：ハッピーメール{happy_info['name']}>>>>>>>>>>>")
                print(traceback.format_exc())
                traceback.print_exc() 
                func.send_error(f"メールチェックエラー：ハッピーメール{happy_info['name']}", traceback.format_exc())    
            wait_if_near_midnight()
        # pcmax
        print(f"<<PCMAX:新着メール 足あとチェック開始>>")
        for pcmax_info in pcmax_list:
            new_mail_lists = []
            pcmax_new, return_foot_cnt = pcmax.check_new_mail(pcmax_info, driver, wait)
        
            if pcmax_new != 1:
                new_mail_lists.append(pcmax_new)
            # メール送信
            smtpobj = None 
            if len(new_mail_lists) == 0:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f'{pcmax_info["name"]}チェック完了  {now}')
                pass
            else:
                print("~~~~~~~~~~~~")
                print(f"{mailaddress} {password} {receiving_address}")
                if mailaddress and password and receiving_address:
                    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f'チェック完了 要確認メールあり  {now}')
                    print(new_mail_lists)
                    
                    text = ""
                    subject = "新着メッセージ"
                
                    for new_mail_list in new_mail_lists:
                        # print('<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>')
                        # print(new_mail_list)
                        for new_mail in new_mail_list:

                            text = text + new_mail + ",\n"
                            if "警告" in text:
                                subject = "メッセージ"
                try:
                    smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
                    smtpobj.starttls()
                    smtpobj.set_debuglevel(0)
                    smtpobj.login(mailaddress, password)
                    msg = MIMEText(text)
                    msg['Subject'] = subject
                    msg['From'] = mailaddress
                    msg['To'] = receiving_address
                    msg['Date'] = formatdate()
                    smtpobj.send_message(msg)
                except smtplib.SMTPDataError as e:
                    print(f"SMTPDataError: {e}")
                except Exception as e:
                    print(f"An error occurred: {e}")
                finally:
                    if smtpobj: 
                        smtpobj.close()   
    
            if return_foot_cnt:     
                continue
                # for r_f_user in pcmax_return_foot_count_dic:
                #     if order_info[0] == r_f_user:
                #         # print(777)
                #         # print(return_foot_count_dic[r_f_user])
                #         pcmax_return_foot_count_dic[r_f_user] = pcmax_return_foot_count_dic[r_f_user] + return_foot_cnt
                #         # print(return_foot_count_dic[r_f_user])
            wait_if_near_midnight()
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
  except (WebDriverException, urllib3.exceptions.MaxRetryError) as e:
    print(f"接続エラーが発生しました: {e}")
    
    print("20秒後に再接続します。")
    print(driver.session_id)

    driver.quit()
    time.sleep(20)  # 10秒待機して再試行
    print(999)
    driver, wait = func.get_driver(1)
    check_mail(user_data, headless)
