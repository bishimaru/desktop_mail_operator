import requests
from stem import Signal
from stem.control import Controller
import time

# TorのIPアドレスを取得する関数
def get_ip_with_tor():
    proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050",
    }
    try:
        response = requests.get("http://ip-api.com/json/", proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            print(f"Current IP: {data['query']} ({data['country']})")
        else:
            print(f"Failed to fetch IP. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# Torの回路を再構築する関数
def change_tor_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # デフォルト設定の場合は認証不要
        controller.signal(Signal.NEWNYM)

# メイン処理
for i in range(5):  # 5回IPアドレスを変更して確認
    change_tor_ip()  # IPアドレスを変更
    time.sleep(5)  # 回路が安定するまで待機（5秒程度推奨）
    get_ip_with_tor()
