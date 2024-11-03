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


def happymail_re_registration(headless, selected_name):
    user_data = func.get_user_data()
    if not user_data:
        return
    if user_data == 2:
        print("ユーザーデータを登録してください。")
        return
    if not user_data['user'][0]['check_mail_happymail']:
        print("有効期限が切れています")
        return
    for chara_datas in user_data['happymail']:
        if chara_datas['name'] == selected_name:
            chara_data = chara_datas
    
    driver, wait = func.get_driver(headless)
    if len(driver.window_handles) == 0:  # ウィンドウが閉じられたか確認
        print("ブラウザウィンドウが閉じられました。プロセスを終了します。")
        driver.quit()
        sys.exit(0)
    try: 
        happymail.re_registration(chara_data, driver, wait)
    except NoSuchWindowException:
        pass
    except Exception as e:
        print(f"{selected_name}:")
        print(traceback.format_exc())
    finally:
        if len(driver.window_handles) == 0:  # ウィンドウが閉じられたか確認
            print("ブラウザウィンドウが閉じられました。プロセスを終了します。")
            driver.quit()
            sys.exit(0)
    driver.quit()
    time.sleep(1)        
    

def run_script():
    selected_index = listbox.curselection()  # 選択されているインデックスを取得
    if not selected_index:
        messagebox.showwarning("警告", "キャラを選択してください。")
        return

    selected_name = listbox.get(selected_index)  # 選択されているキャラの名前を取得
    
    headless = check_var.get()
    
    root.withdraw()  # 実行ボタンを押した時にウィンドウを非表示にする
    root.update()  # Tkinterのイベントループを更新
    happymail_re_registration(headless, selected_name)
    root.quit()
    sys.exit(0)

def populate_user_listbox():
    user_data = func.get_user_data()
    if user_data == 2:
        return
    happy_user_list = []
    if not user_data:
        return
    for h_chara_data in user_data["happymail"]:
        happy_user_list.append(f"{h_chara_data['name']}")
    
    listbox.delete(0, tk.END)
    for user in happy_user_list:
        listbox.insert(tk.END, user)


# Tkinter ウィンドウの設定
root = tk.Tk()
root.title("ハピメアカウント登録")

# ユーザーリストの表示
listbox_label = tk.Label(root, text="キャラリスト:")
listbox_label.pack()

listbox = tk.Listbox(root, height=10, selectmode=tk.SINGLE)  # シングル選択モードに設定
listbox.pack()



# フレームの作成
frame = tk.Frame(root)
frame.pack()

# チェックボックスとラベルをフレーム内に配置
check_label = tk.Label(frame, text="ウィンドウを表示しない")
check_label.pack(side="left")

check_var = tk.BooleanVar(value=True)
check_button = tk.Checkbutton(frame, variable=check_var)
check_button.pack(side="left")

# 実行ボタン
run_button = tk.Button(root, text="実行", command=run_script)
run_button.pack()

# ユーザーリストの読み込み
populate_user_listbox()

# Tkinter メインループの開始
root.mainloop()
