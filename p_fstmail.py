import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import pcmax, func
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import traceback
import random
from datetime import datetime



def main(maji_soushin, chara_name_list, end_hour, end_minute):
  # 〜〜〜〜〜〜検索設定〜〜〜〜〜〜
  # メール送信数（上限なしは0）
  limit_send_cnt = 15
  
  # 年齢選択（最小18歳、最高60以上）
  youngest_age = "19"
  oldest_age = "37"
  # NGワード（複数、追加可能）
  ng_words = [
    "通報",
    "業者",
    # "食事",
    # "お茶",
    # "円",
    # "パパ",
    # "援",
    # "援交",
    # "お金のやり取り",
  ]

  user_sort = [
    "ログイン順",
    # "登録順", 
    # "自己PR更新順"
  ]
  # user_data = func.get_user_data()
  # print(user_data["pcmax"][0]['name'])
  # print(f"キャラ数　{len(chara_name_list)}")
  
  
  while True:
    for order_count in range(len(chara_name_list)):
      # 現在時刻を取得
      current_time = datetime.now()
      if current_time.hour > int(end_hour) or (current_time.hour == int(end_hour) and current_time.minute >= int(end_minute)):
          print("終了時刻を過ぎました。")
          return
      else:
          print("現在時刻:", current_time)
      # 地域選択（3つまで選択可能）
      areas = [
        "東京都",
        "千葉県",
        "埼玉県",
        "神奈川県",
        "静岡県",
        # "新潟県",
        # "山梨県",
        # "長野県",
        # "茨城県",
        "栃木県",
        # "群馬県",
      ]
      areas.remove("東京都")
      select_areas = random.sample(areas, 2)
      select_areas.append("東京都")
      print(f"キャラ:{chara_name_list[order_count]['name']}、選択地域:{select_areas}")
      try:
        pcmax.send_fst_mail(chara_name_list[order_count]['name'], chara_name_list[order_count]['login_id'], chara_name_list[order_count]['password'], chara_name_list[order_count]['fst_mail'], chara_name_list[order_count]['mail_img'], chara_name_list[order_count]['second_message'], maji_soushin, select_areas, youngest_age, oldest_age, ng_words, limit_send_cnt, user_sort)
      except Exception as e:
        print(traceback.format_exc())
   

if __name__ == '__main__':
  maji_soushin = False
  if sys.argv[1] == str(1):
      maji_soushin = True
  end_hour = sys.argv[2]
  end_minute = sys.argv[3]
    
  chara_name_list = {
    "アスカ":{},"彩香":{},"えりか":{},"きりこ":{},
    "さな":{},"すい":{},  "つむぎ":{},"なお":{},
    "はづき":{}, "ハル":{}, "めあり":{},"りこ":{}, 
    "りな":{}, "ゆっこ":{},"ゆかり":{}, "ゆうな":{},
    
  }
  # chara_name_list = {
  #   "つむぎ":{},
    
  # }
  
  main(maji_soushin, chara_name_list, end_hour, end_minute)
  