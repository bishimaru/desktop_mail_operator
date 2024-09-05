import tkinter as tk
from tkinter import messagebox
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sb_h_day_shift import sb_h_all_do
from widget import func
from sb_h_day_shift import sb_h_all_do
import sqlite3

conn = sqlite3.connect('user_data.db')
c = conn.cursor()
# グローバル変数の宣言
global user_data
user_data = func.get_user_data()

# フォームを追加するためのカウンタ
form_count = 0
max_forms = 6

# Tkinter ウィンドウの設定
root = tk.Tk()
root.title("スケジューラ設定")

driver = None  # グローバルにドライバを定義

def start_scheduler(schedule_data, happy_chara_list, headless):
    verification_flug = func.get_user_data()
    if not verification_flug:
        return
    global driver

    user_profile_list = []
    user_info = user_data.get("user", None)
    
    # print('<<<<<<<<<<<<<>>>>>>>>>>>>>')
    # print(happy_chara_list)
    mail_info = [
        user_data["user"][0]["user_email"],
        user_data["user"][0]["gmail_account"],
        user_data["user"][0]["gmail_account_password"],
    ]
    scheduler = BlockingScheduler()
    combined_string = ""
    for element in schedule_data:
        if combined_string:
            combined_string = combined_string + "," +",".join(element)
        else:
            combined_string = combined_string +",".join(element)
    c.execute("INSERT INTO users (user_name, password, h_schedule_time) VALUES (?, ?, ?)", (user_data["user"][0]["username"], user_data["user"][0]["password"], combined_string))
    conn.commit()
    mail_info = []
    for data in schedule_data:
        hour, minute, args = data
        scheduler.add_job(
            sb_h_all_do, 
            'cron', 
            hour=int(hour), 
            minute=int(minute), 
            args=[int(args), happy_chara_list, headless, mail_info], 
            max_instances=1, 
            misfire_grace_time=60*60
        )
        print(f"スケジュール設定: {hour}時{minute}分, 足跡返し件数{args}件")
    print("Ctrl+{0} を押すと終了します。".format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        if driver:
            driver.quit()
            print("Chromedriver has been closed.")

def run_scheduler():
    global user_data  
    schedule_data = []
    happy_chara_list = [listbox.get(i) for i in range(listbox.size())]  # リストボックスからキャラリストを取得
    headless = check_var.get()  # チェックボックスの値を取得
    
    # happy_chara_list の順番に基づいて user_data["happymail"] を並べ替える
    sorted_happymail = []
    for chara_name in happy_chara_list:
        for h_chara_data in user_data["happymail"]:
            if h_chara_data['name'] == chara_name:
                sorted_happymail.append(h_chara_data)
                break    
    for i in range(form_count):
        hour = hour_entries[i].get()
        minute = minute_entries[i].get()
        args = args_entries[i].get()

        if not hour.isdigit() or not minute.isdigit() or not args.isdigit():
            tk.messagebox.showerror("入力エラー", "スペースなど数字以外は入力しないでください")
            return

        schedule_data.append((hour, minute, args))

    root.withdraw()  # 実行ボタンを押した時にウィンドウを非表示にする
    root.update()  # Tkinterのイベントループを更新
    start_scheduler(schedule_data, sorted_happymail, headless)

def add_form(user_info):
    global form_count

    if form_count >= max_forms:
        return  

    # 新しい入力フォームを追加
    hour_entry = tk.Entry(frame, width=3)
    hour_entry.grid(row=form_count, column=0)
    hour_entries.append(hour_entry)
    hour_label = tk.Label(frame, text="時")
    hour_label.grid(row=form_count, column=1)
    hour_labels.append(hour_label)

    minute_entry = tk.Entry(frame, width=3)
    minute_entry.grid(row=form_count, column=2)
    minute_entries.append(minute_entry)
    minute_label = tk.Label(frame, text="分")
    minute_label.grid(row=form_count, column=3)
    minute_labels.append(minute_label)

    args_entry = tk.Entry(frame, width=3)
    args_entry.grid(row=form_count, column=4)
    args_entries.append(args_entry)
    args_label = tk.Label(frame, text="件（足跡返し）")
    args_label.grid(row=form_count, column=5)
    args_labels.append(args_label)

    # 初期値を設定
    hour_entry.insert(0, user_info_list[form_count][0] if user_info_list[form_count][0] is not None else "")   
    minute_entry.insert(0, user_info_list[form_count][1] if user_info_list[form_count][1] is not None else "")  
    args_entry.insert(0, user_info_list[form_count][2] if user_info_list[form_count][2] is not None else "") 

    form_count += 1  # カウンタを更新

def remove_form():
    global form_count

    if form_count <= 1:
        return
    form_count -= 1  # カウンタを更新
    # 最後のフォームを削除
    hour_entries.pop().grid_forget()
    minute_entries.pop().grid_forget()
    args_entries.pop().grid_forget()

    # 最後のラベルを削除
    hour_labels.pop().grid_forget()
    minute_labels.pop().grid_forget()
    args_labels.pop().grid_forget()

    

def populate_user_listbox():
    global user_data  # グローバル変数に代入
    
    happy_chara_list = []
    
    if not user_data:
        return
    for h_chara_data in user_data["happymail"]:
        happy_chara_list.append(f"{h_chara_data['name']}")
    
    listbox.delete(0, tk.END)
    for user in happy_chara_list:
        listbox.insert(tk.END, user)

def on_drag_start(event):
    widget = event.widget
    widget.start_index = widget.nearest(event.y)

def on_drag_motion(event):
    widget = event.widget
    widget.activate(widget.nearest(event.y))

def on_drag_end(event):
    widget = event.widget
    end_index = widget.nearest(event.y)
    if end_index != widget.start_index:
        # 元の位置と新しい位置のアイテムを入れ替える
        item = widget.get(widget.start_index)
        widget.delete(widget.start_index)
        widget.insert(end_index, item)

# ユーザーリストの表示
listbox_label = tk.Label(root, text="キャラリスト:")
listbox_label.grid(row=0, column=0, columnspan=6)

listbox = tk.Listbox(root, height=10)
listbox.grid(row=1, column=0, columnspan=6)

# リストボックスでドラッグアンドドロップを有効にする
listbox.bind('<Button-1>', on_drag_start)
listbox.bind('<B1-Motion>', on_drag_motion)
listbox.bind('<ButtonRelease-1>', on_drag_end)

# 入力フォームとラベルを横に並べるフレーム
frame = tk.Frame(root)
frame.grid(row=2, column=0, columnspan=6, pady=10)

hour_entries = []
minute_entries = []
args_entries = []

hour_labels = []
minute_labels = []
args_labels = []

def get_latest_user_data(c):
    c.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    return c.fetchone()

user_info = get_latest_user_data(c)
user_info_list = [["", "", ""] for _ in range(6)]  
if user_info[3] is not None:
    string = user_info[3].split(",")
    for i in range(len(string)):
        user_info_list[i // 3][i % 3] = string[i]

# 最初の入力フォームを作成
add_form(user_info_list)

# プラスボタンを追加
add_button = tk.Button(root, text="+", command=lambda: add_form(user_info_list))
# add_button = tk.Button(root, text="+", command=add_form)
add_button.grid(row=3, column=1, pady=10)

# マイナスボタンを追加
remove_button = tk.Button(root, text="-", command=remove_form)
remove_button.grid(row=3, column=2, pady=10)

# 新しいフレームにチェックボックスとラベルを配置
check_frame = tk.Frame(root)
check_frame.grid(row=4, column=0, columnspan=6, pady=10)

check_label = tk.Label(check_frame, text="ウィンドウを表示しない")
check_label.pack(side="left")

check_var = tk.BooleanVar(value=True)
check_button = tk.Checkbutton(check_frame, variable=check_var)
check_button.pack(side="left")

# 実行ボタン
run_button = tk.Button(root, text="実行", command=run_scheduler)
run_button.grid(row=5, column=0, columnspan=6, pady=10)

# ユーザーリストの読み込み
populate_user_listbox()

# Tkinter メインループの開始
root.mainloop()
