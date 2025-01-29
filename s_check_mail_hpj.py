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
import gc
from requests import exceptions
import requests
from stem import Signal
from stem.control import Controller
import shutil
import traceback


def wait_if_near_midnight():
    now = datetime.now()
    current_hour = now.hour
    current_minute = now.minute
    # もし現在時刻が23:55を過ぎていたら
    if current_hour == 23 and 55 <= current_minute:
        print("現在時刻は0時に近づいています。処理を一時中断します。")
        #     # ここに実行したい動作を追加
        time.sleep(600)
        print("処理を再開します。")
    return

def check_mail(user_data, headless):
  happymail_list = user_data['happymail']
  pcmax_list = user_data['pcmax']
  jmail_list = user_data['jmail']
  mailaddress = user_data['user'][0]['gmail_account']
  gmail_password = user_data['user'][0]['gmail_account_password']
  receiving_address = user_data['user'][0]['user_email']
  


#   print(f"*****{mailaddress}*****{gmail_password}*****{receiving_address}")
  while True:
        send_flug = True
        start_time = time.time() 
        current_datetime = datetime.utcfromtimestamp(int(start_time))
        # ハッピーメール
        print(f'~~~~~~~~~~~~ハピメ:新着メールチェック開始~~~~~~~~~~~~')
        driver = None
        temp_dir = func.get_the_temporary_folder("check_mail")
        driver,wait = func.test_get_driver(temp_dir, headless)
        for happy_info in happymail_list:
            new_mail_lists = []
            # if happy_info["name"] != "ゆっこ":
            #     continue
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
                    
                    if mailaddress and gmail_password and receiving_address:
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
                    else:
                        print("~~~~~~~~~~~~")
                        print(f"自動送信に必要な情報が不足しています。　{mailaddress} {gmail_password} {receiving_address}")
                        
                    try:
                        smtpobj = smtplib.SMTP('smtp.gmail.com', 587)
                        smtpobj.starttls()
                        smtpobj.set_debuglevel(0)
                        smtpobj.login(mailaddress, gmail_password)
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
            except (smtplib.SMTPException, socket.gaierror) as e:
                print(f"メール送信中にエラーが発生しました: {e}")
                print("5分間待機して再試行します...")
                driver.quit()
                shutil.rmtree(temp_dir)
                time.sleep(300) 
                check_mail(user_data, headless)
            except (WebDriverException, urllib3.exceptions.MaxRetryError) as e:
                tb = traceback.format_exc()  # トレースバック情報を取得
                print(f"接続エラーが発生しました: {e}")
                print(f"エラー発生行: {tb}")
                print("20秒後に再接続します。")
                driver.quit()
                shutil.rmtree(temp_dir)
                time.sleep(20) 
                check_mail(user_data, headless)
            except exceptions.ConnectionError as e:
                print(f"ネットワーク回線がオフラインの可能性があります. {360 // 60} 分後にリトライします。")
                time.sleep(360)
                check_mail(user_data, headless)
            except Exception as e:
                print(f"<<<<<<<<<<メールチェックエラー：ハッピーメール{happy_info['name']}>>>>>>>>>>>")
                print(traceback.format_exc())
                func.send_error(f"メールチェックエラー：ハッピーメール{happy_info['name']}", traceback.format_exc())    
            wait_if_near_midnight()
            # driver.refresh()
        if driver is not None:
            driver.quit()
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
        time.sleep(2)
        temp_dir = func.get_the_temporary_folder("check_mail")
        driver,wait = func.test_get_driver(temp_dir, headless)
        # pcmax
        print(f"<<<<<<<<<<<<PCMAX:新着メール開始>>>>>>>>>>>>")
        for pcmax_info in pcmax_list:  
            func.change_tor_ip()  
            new_mail_lists = []
            try:
                result = pcmax.check_new_mail(pcmax_info, driver, wait)
                if result is not None:
                    pcmax_new, return_foot_cnt = result
                else:
                    pcmax_new, return_foot_cnt = 1, 0
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
                    print(f"{mailaddress} {gmail_password} {receiving_address}")
                    if mailaddress and gmail_password and receiving_address:
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
                        smtpobj.login(mailaddress, gmail_password)
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
            except (smtplib.SMTPException, socket.gaierror) as e:
                print(f"メール送信中にエラーが発生しました: {e}")
                print("5分間待機して再試行します...")
                driver.quit()
                shutil.rmtree(temp_dir)
                time.sleep(300)  # 300秒（5分）間待機
                check_mail(user_data, headless)
            except (WebDriverException, urllib3.exceptions.MaxRetryError) as e:
                print(f"タイムアウトエラーが発生しました: {e}")      
                print("30秒後に再接続します。")
                time.sleep(30)  # 30秒待機して再試行
                check_mail(user_data, headless)
              
            except Exception as e:
                print(f"<<<<<<<<<<PCMAX{pcmax_info['name']}>>>>>>>>>>>")
                print(traceback.format_exc())
                traceback.print_exc() 
                func.send_error(f"PCMAX{pcmax_info['name']}", traceback.format_exc())    
            wait_if_near_midnight()
            if return_foot_cnt:     
                continue
                # for r_f_user in pcmax_return_foot_count_dic:
                #     if order_info[0] == r_f_user:
                #         # print(777)
                #         # print(return_foot_count_dic[r_f_user])
                #         pcmax_return_foot_count_dic[r_f_user] = pcmax_return_foot_count_dic[r_f_user] + return_foot_cnt
                #         # print(return_foot_count_dic[r_f_user])
        wait_if_near_midnight()
        # driver.refresh()
            # jmail
            # try:
            #     driver, wait = get_driver(debug)
            #     jmail_new, return_foot_cnt = jmail.check_new_mail(driver, wait, jmail_list)
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
        driver.quit()
        shutil.rmtree(temp_dir)
        time.sleep(1)
        gc.collect()
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
    # except (smtplib.SMTPException, socket.gaierror) as e:
    #     print(f"メール送信中にエラーが発生しました: {e}")
    #     print("5分間待機して再試行します...")
    #     driver.quit()
    #     time.sleep(300)  # 300秒（5分）間待機
    #     driver, wait = func.get_driver(1)
    #     check_mail(user_data, driver, wait)
    
