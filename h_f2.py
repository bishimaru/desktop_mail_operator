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
import signal

user_data = func.get_user_data()
def run_script():
    # 選択されたキャラクターを取得
    selected_users = [name for name, var in check_vars.items() if var.get()]
    print(selected_users)
    if not selected_users:
        messagebox.showwarning("警告", "キャラクターを選択してください。")
        return

    foot_cnt = entry.get()
    if not foot_cnt.isdigit():
        messagebox.showwarning("警告", "足跡数には半角で正の整数を入力してください。")
        return

    foot_cnt = int(foot_cnt)
    headless = check_var.get()

    # Tkinterウィンドウを非表示にする
    root.withdraw()
    root.update()

    # 選択されたキャラクターで足跡付けを実行
    happymail_footprints(headless, foot_cnt, selected_users)

def happymail_footprints(headless, foot_cnt, selected_users):
    if not user_data:
        print("ユーザーデータを取得できませんでした。")
        return

    happy_user_list = [
        [h_chara_data['name'], h_chara_data['login_id'], h_chara_data['password']]
        for h_chara_data in user_data["happymail"]
        if h_chara_data['name'] in selected_users  # 選択されたキャラクターのみ対象
    ]

    if not happy_user_list:
        print("選択されたキャラクターに該当するユーザーデータがありません。")
        return
    for i in range(9999):
      driver,wait = func.get_driver(headless)
      for user_list in happy_user_list:
          print(f"キャラクター: {user_list[0]} の処理を開始します。")
          if user_list[1] is None or user_list[1] == "":
              print(f"{user_list[0]}:ログインIDが正しくありません")
              continue
          try:      
              happymail.make_footprints(user_list[0], user_list[1], user_list[2], driver, wait, foot_cnt)
          except NoSuchWindowException:
              pass
          
          except Exception as e:
              print(f"{user_list[0]}:")
              print(traceback.format_exc())
          finally:
              if len(driver.window_handles) == 0:  # ウィンドウが閉じられたか確認
                  print("ブラウザウィンドウが閉じられました。プロセスを終了します。")
                  driver.quit()
                  sys.exit(0)
      driver.quit()
      time.sleep(1)        
      
     

def toggle_all_characters():
    """全キャラのチェックを切り替える"""
    select_all = select_all_var.get()  # チェックボックスの状態を取得
    for var in check_vars.values():
        var.set(select_all)  # チェックボックスの状態を一括変更

def populate_user_checkboxes():
    global select_all_var
    select_all_var = tk.BooleanVar(value=False)  # 初期状態は未選択
    select_all_button = tk.Checkbutton(
        checkbox_frame, text="全キャラを選択", variable=select_all_var, command=toggle_all_characters
    )
    select_all_button.grid(row=1, column=0, columnspan=2, pady=5, sticky="w")  # 全幅で配置

    if user_data == 2:
        return
    happy_user_list = []
    if not user_data:
        return
    for h_chara_data in user_data["happymail"]:
        happy_user_list.append(f"{h_chara_data['name']}")

    # キャラを2列に分けて表示
    for idx, user in enumerate(happy_user_list):
        var = tk.BooleanVar(value=False)  # 初期状態は選択されていない
        row = idx // 2 + 2  # ラベルと「全キャラを選択」チェックボックスが1行目まで使用しているので+2
        col = idx % 2       # 列のインデックス（2列で表示）
        checkbox = tk.Checkbutton(checkbox_frame, text=user, variable=var)
        checkbox.grid(row=row, column=col, padx=10, pady=2)  # 均等に余白を設定
        check_vars[user] = var

# Tkinter ウィンドウの設定
root = tk.Tk()
root.title("ハピメ足跡付け")

# チェックボックスを配置するフレーム
checkbox_frame = tk.Frame(root)
checkbox_frame.pack()

# チェックボックス用の変数を保持する辞書
check_vars = {}

# キャラリストのチェックボックスを生成
populate_user_checkboxes()

# 入力フォーム
entry_label = tk.Label(root, text="一度につける足跡数:")
entry_label.pack()
entry = tk.Entry(root, width=5)
entry.pack()

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

# Tkinterのイベントループ
try:
    root.mainloop()
except KeyboardInterrupt:
    print("\nKeyboardInterrupt in mainloop. Exiting...")
    root.quit()
