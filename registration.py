import tkinter as tk
from tkinter import messagebox
import sqlite3

# データベース接続とテーブル作成
conn = sqlite3.connect('user_data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL,
        h_schedule_time TEXT,
        gmail_address TEXT,
        gmail_password TEXT,
        receiving_address TEXT        
    )
''')
conn.commit()

# データベースから最新のユーザー情報を取得する関数
def get_latest_user_data():
    c.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    return c.fetchone()

# データをデータベースに保存する関数
def save_data():
    user_name = entry_user_name.get().strip().replace(" ", "").replace("　", "")
    password = entry_password.get().strip().replace(" ", "").replace("　", "")
    gmail = entry_gmail_address.get().strip().replace(" ", "").replace("　", "")
    gmail_pass = entry_gmail_pass.get().strip().replace(" ", "").replace("　", "")
    receiving_address = entry_receiving_address.get().strip().replace(" ", "").replace("　", "")

    if user_name and password:
        c.execute("INSERT INTO users (user_name, password, gmail_address, gmail_password, receiving_address) VALUES (?,?,?,?,?)", (user_name, password, gmail, gmail_pass, receiving_address))
        conn.commit()
        messagebox.showinfo("情報", "データが保存されました！")
        entry_user_name.delete(0, tk.END)
        entry_password.delete(0, tk.END)
        root.quit()  # メインループを終了
    else:
        messagebox.showwarning("警告", "ユーザー名とパスワードを入力してください！")

# パスワードの表示/非表示を切り替える関数
def toggle_password():
    if show_password_var.get():
        entry_password.config(show='')
    else:
        entry_password.config(show='*')

# ウィンドウの作成
root = tk.Tk()
root.title("ユーザー情報入力")

# データベースから最新のユーザー情報を取得して、エントリの初期値に設定
latest_user_data = get_latest_user_data()

# ラベルとエントリの作成
label_user_name = tk.Label(root, text="ユーザー名(必須):")
label_user_name.grid(row=0, column=0, padx=10, pady=10)
entry_user_name = tk.Entry(root)
entry_user_name.grid(row=0, column=1, padx=10, pady=10)

label_password = tk.Label(root, text="パスワード（必須):")
label_password.grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show='*')
entry_password.grid(row=1, column=1, padx=10, pady=10)

# パスワード表示/非表示のチェックボックス
show_password_var = tk.BooleanVar()
show_password_check = tk.Checkbutton(root, text="パスワードを表示", variable=show_password_var, command=toggle_password)
show_password_check.grid(row=2, column=1, padx=10, pady=10, sticky='w')

label_gmail_address = tk.Label(root, text="自動送信サーバーアドレス:")
label_gmail_address.grid(row=3, column=0, padx=10, pady=10)
entry_gmail_address = tk.Entry(root)
entry_gmail_address.grid(row=3, column=1, padx=10, pady=10)

label_gmail_pass = tk.Label(root, text="Gmailアプリパスワード:")
label_gmail_pass.grid(row=4, column=0, padx=10, pady=10)
entry_gmail_pass = tk.Entry(root)
entry_gmail_pass.grid(row=4, column=1, padx=10, pady=10)

label_receiving_address = tk.Label(root, text="受信メールアドレス:")
label_receiving_address.grid(row=5, column=0, padx=10, pady=10)
entry_receiving_address = tk.Entry(root)
entry_receiving_address.grid(row=5, column=1, padx=10, pady=10)


# 取得したデータが存在すれば、それを入力欄の初期値に設定

if latest_user_data:
    entry_user_name.insert(0, latest_user_data[1])
    entry_password.insert(0, latest_user_data[2])
    if len(latest_user_data) > 4:
        entry_gmail_address.insert(0, latest_user_data[4])
    if len(latest_user_data) > 5:
        entry_gmail_pass.insert(0, latest_user_data[5])
    if len(latest_user_data) > 6:
        entry_receiving_address.insert(0, latest_user_data[6])
    

# 保存ボタンの作成
save_button = tk.Button(root, text="保存", command=save_data)
save_button.grid(row=6, column=1, pady=10)

# メインループ開始
root.mainloop()

# データベース接続を閉じる
conn.close()
