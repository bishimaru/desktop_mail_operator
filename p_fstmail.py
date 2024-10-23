import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import pcmax, func
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import traceback
import random
from datetime import datetime
import time


def main(maji_soushin, chara_name_list, end_hour, end_minute, headless):
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
      if end_hour and end_minute:
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
        # "静岡県",
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
      driver = None
      try:
        driver,wait = func.get_driver(headless)
        pcmax.send_fst_mail(chara_name_list[order_count]['name'], chara_name_list[order_count]['login_id'], chara_name_list[order_count]['password'], chara_name_list[order_count]['fst_mail'], chara_name_list[order_count]['mail_img'], chara_name_list[order_count]['second_message'], maji_soushin, select_areas, youngest_age, oldest_age, ng_words, limit_send_cnt, user_sort, driver,wait)
      except Exception as e:
        print(traceback.format_exc())
      finally:
         if driver is not None:
          driver.quit()
         time.sleep(1)
   

if __name__ == '__main__':
  maji_soushin = True
  headless = False      
  end_hour = sys.argv[1]
  end_minute = sys.argv[2]
    
  chara_name_list = [
     {'id': 4, 'name': 'きりこ', 'login_id': '20973857', 'password': '5556', 'fst_mail': 'はじめまして(*\'ω\'*)\r\nカーディーラーの受付嬢として働いている『きりこ』です(*´ω｀)\r\n\u3000\r\n今お仕事とかで悩んでいることがあって・・・\r\n営業の人とかお客さんをおもてなしするのが仕事なんですけど\r\n「接客マナー」とか「気配り」をすごい求められる職業ですっごいストレスがたまっちゃうんです(´;ω;｀)\r\n\r\n休みの日でも営業の人から連絡きたりもするし、そんな仕事だけの毎日から解放されたくて.....\r\nついでにあっちのほうもご無沙汰だしストレスと欲求不満を解消できるセフレさんを探そうと思ってサイトをはじめてみました(@_@。\r\n\r\n少しMっけのある男性のほうが相性いいかもです(*´ω｀)\r\n\r\n同じ感じでセフレ探してるなら返信もらえると嬉しいです"(-""-)"', 'mail_img': None, 'post_title': 'Mっけある人◎/カーディーラーの受付嬢', 'post_content': "はじめまして(*'ω'*)\r\n某企業のカーディーラーの受付嬢として働いている『きりこ』です(*´ω｀)\r\n\u3000\r\n今お仕事とか出会いで悩んでることがあって......\r\n営業の人とかお客さんをおもてなしするのが仕事なんですけど\r\n「接客マナー」とか「気配り」をすごい求められる職業ですっごいストレスがたまっちゃうんです(´;ω;｀)\r\n\r\n休みの日でも営業の人から連絡きたりもするし、そんな仕事だけの毎日から解放されたくて.....\r\nついでにあっちのほうもご無沙汰だしストレスと欲求不満を解消できるセフレさんを探そうと思ってサイトをはじめてみました(@_@。\r\n\r\n普段は気配りとかして相手に尽くすようなお仕事をしてるんですけど実は私Sなんです(#^^#)\r\n\r\nなので少しMっけのある男性のほうが相性いいかもです(*´ω｀)", 'second_message': 'メッセージありがとうございます٩(ˊᗜˋ*)و\r\n\r\nこういう場所だし連絡もらえるか不安だったので、連絡もらえて嬉しいです！\r\n\r\n早速会う時のお話しして行きたいんですけど、ここでのやり取りあんまり慣れてないのでメアド交換してメールでお話ししたいのでメアド教えてもらえると嬉しいです(*´ω｀)', 'condition_message': 'PCMAXでやりとりしてたきりこです！\r\nメアド交換ありがとうございます○o。.\r\n\r\n単刀直入なんですけど、やり逃げとかのリスクもあるし最初はホテル別の2万円でホテルデートしませんか？？\r\nストレスとか欲求不満をちゃんと解消するためにこれだけお願いしたいです(´;ω;｀)\r\n\r\n1ヶ月間会ってみて、お互いに2ヶ月目も会いたいってなった場合はお金とか無しで関係を続行したいです♪\r\n\r\n沢山の方とメールしても埒が明かないので、まずはこれで決めてくれる人に絞りたいなって思いますー！\r\nお返事もらえたらまた私から連絡したいので、お返事待ってます！', 'return_foot_message': 'はじめまして(*\'ω\'*)\r\nカーディーラーの受付嬢として働いている『きりこ』です(*´ω｀)\r\n\u3000\r\n今お仕事とかで悩んでいることがあって・・・\r\n営業の人とかお客さんをおもてなしするのが仕事なんですけど\r\n「接客マナー」とか「気配り」をすごい求められる職業ですっごいストレスがたまっちゃうんです(´;ω;｀)\r\n\r\n休みの日でも営業の人から連絡きたりもするし、そんな仕事だけの毎日から解放されたくて.....\r\nついでにあっちのほうもご無沙汰だしストレスと欲求不満を解消できるセフレさんを探そうと思ってサイトをはじめてみました(@_@。\r\n\r\n少しMっけのある男性のほうが相性いいかもです(*´ω｀)\r\n\r\n同じ感じでセフレ探してるなら返信もらえると嬉しいです"(-""-)"', 'mail_address': 'kiriko414510@gmail.com', 'gmail_password': 'wqhpalqgwdgfrdmh', 'date_of_birth': None, 'self_promotion': '', 'height': None, 'body_shape': None, 'blood_type': None, 'activity_area': None, 'detail_activity_area': None, 'profession': '', 'freetime': None, 'car_ownership': None, 'smoking': None, 'ecchiness_level': None, 'sake': None, 'process_before_meeting': None, 'first_date_cost': None, 'is_active': True, 'memo': None, 'user_id': 4},
  ]
  # chara_name_list = {
  #   "つむぎ":{},
    
  # }
  
  main(maji_soushin, chara_name_list, end_hour, end_minute, headless)
  