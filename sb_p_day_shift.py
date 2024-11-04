from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random
import time
from selenium.webdriver.common.by import By
import os
import sys
from widget import pcmax, happymail, func
from selenium.webdriver.support.ui import WebDriverWait
import traceback
from datetime import timedelta
# from sb_p_repost import pcmax_repost
from h_repost_returnfoot import sb_h_repost_returnfoot
import p_fstmail


def sb_p_all_do(pcmax_chara_list, headless):
  verification_flug = func.get_user_data()
  if not verification_flug:
      return
  
  def timer(sec, functions):
    start_time = time.time() 
    for func in functions:
      try:
        return_func = func()
      except Exception as e:
        print(e)
        return_func = 0
    elapsed_time = time.time() - start_time  # 経過時間を計算する
    while elapsed_time < sec:
      time.sleep(30)
      elapsed_time = time.time() - start_time  # 経過時間を計算する
      # print(f"待機中~~ {elapsed_time} ")
    return return_func
  wait_cnt = 3600 / len(pcmax_chara_list)

  # メール送信数（上限なしは0）
  limit_send_cnt = 10

  # 年齢選択（最小18歳、最高60以上）
  youngest_age = "19"
  oldest_age = "29"
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
  maji_soushin = True
  start_one_rap_time = time.time() 

  print(len(pcmax_chara_list))
  # print(pcmax_chara_list)
  for i in range(99):
    for pcmax_chara in pcmax_chara_list:
      # 地域選択（3つまで選択可能）
      areas = [
        "東京都",
        # "千葉県",
        # "埼玉県",
        # "神奈川県",
        # "静岡県",
        # "新潟県",
        # "山梨県",
        # "長野県",
        # "茨城県",
        # "栃木県",
        # "群馬県",
      ]
      if len(areas) > 1:
        areas.remove("東京都")
        select_areas = random.sample(areas, 2)
        select_areas.append("東京都")
      elif len(areas) == 1:
        select_areas = areas
      print(f"キャラ:{pcmax_chara['name']}、選択地域:{select_areas}") 
      
      try:
        driver,wait = func.get_driver(headless)
        return_func = timer(wait_cnt, [lambda: pcmax.send_fst_mail(pcmax_chara['name'], pcmax_chara['login_id'], pcmax_chara['password'], pcmax_chara['fst_mail'], pcmax_chara['mail_img'], pcmax_chara['second_message'], maji_soushin, select_areas, youngest_age, oldest_age, ng_words, limit_send_cnt, user_sort, driver, wait)])
        # if isinstance(return_func, str):
        #   return_cnt_list.append(f"{happy_chara['name']}: {return_func}")
        # elif isinstance(return_func, list):
        #   return_cnt_list.append(f"{happy_chara['name']}: {return_func}")
      except Exception as e:
        print(f"エラー{pcmax_chara[0]}")
        print(traceback.format_exc())
      finally:
        if driver is not None:
          driver.quit()
        time.sleep(1)
    elapsed_time = time.time() - start_one_rap_time  
    elapsed_timedelta = timedelta(seconds=elapsed_time)
    elapsed_time_formatted = str(elapsed_timedelta)
    print(f"<<<<<<<<<<<<<PCMAX回し一周タイム： {elapsed_time_formatted}>>>>>>>>>>>>>>>>>>")
    # return_cnt_list.append(f"PCMAX回し一周タイム： {elapsed_time_formatted}")
    # str_return_cnt_list = ",\n".join(return_cnt_list)
    
    # if len(mail_info) and mail_info[0] != "" and mail_info[1] != "" and mail_info[2] != "":
    #   func.send_mail(str_return_cnt_list, mail_info)

if __name__ == '__main__':

  pcmax_chara_list = [
#  ['アスカ', '50086800553', 'ebbh7278', '3人でエッチを楽しめる方探してます♪', '初めまして( ＾∀＾)\r\nあすかです！友達のゆかとセフレさん探しの為に始めてみました♪♪\r\n\r\n2人とも都内のメンズ専門の脱毛サロンで働いてるんですけど、VIOの脱毛専門で施術中にエッチな気分になっちゃてるちょっと変態な2人組です(⸝⸝⸝´꒳`⸝⸝⸝)ﾃﾚｯ\r\n\r\n私もゆかもちょっと刺激が欲しいなって思ってて、、\r\n折角セフレさんになってもらうなら3人でエッチを楽しめる人を探してます！\r\n\r\n3Pとかに興味ある方は連絡くださいね♪♪\r\n因みに、2人ともエッチで人懐っこい性格なので会って損はしないと思います♪笑', "足跡が付いてたので気になってご連絡しちゃいました♪\r\nあすかです٩( 'ω’ )و\r\n友達のゆかと3人でエッチを楽しめるセフレさんを見つけたくてサイトに登録しました！\r\n\r\n2人ともメンズ専門の脱毛サロンで働いてるんですけど、毎回VIOの施術中にエッチな気分になっちゃって(//ω照♥\r\n\r\n私もゆかも今は特定の相手もいないし、折角なら3人でエッチを楽しめるセフレさんが出来たらなって思ってるんですけど今ってそういうお相手探してたりしませんか？？"],
  # ['えりか', '50010903495', 'ebbh72781', 'セクシー女優に偏見ない人。長期せふれさん', '〜\u3000Profile\u3000〜\r\n・えりか/25歳/Dcup/セクシー女優\r\n・AV女優のお仕事がない時は会員制のデリヘルで働いてます！\r\n・温泉巡りが趣味でたまに連休とって体を休めています◎\r\n\r\n投稿見てくれてありがとうございます♪\r\nまずは簡単にプロフィール書いてみました！\r\n\r\nAVのお仕事もデリヘルのお仕事もえっちが好きで人と関わるのが大好きな私にとってはすっごく楽しいです♪( ´θ｀)ノ\r\nとはいえプライベートはプライベートで大事にしたいと思ってます！\r\n\r\nここではプライベートを一緒に楽しめる方を探しています◎\r\nえっちについては私自身プロだし仕事柄プロの男優さんとか会ってきたので上手さとかそういうのは逆に気にしないですm(__)m\r\nその代わりに長期的な関係ってのがあまりないので、経験少ない人とどんどん相性良くなっていける関係が理想かなって思ってます！\r\n\r\n私の職業に偏見なくて長期的な関係でも大丈夫って方いたらメッセージもらえると嬉しいです(*ﾟ▽ﾟ*)', '足跡からです！m(__)m\r\nセクシー女優と会員制のデリヘルでお仕事しています◎\r\n\r\nプライベートでえっちなことができるせふれさんを探しています！\r\n仕事ではプロの男優さんとかと会うので上手さとかは逆に気にしないですm(__)m\r\nその代わりに長期的な関係ってのがあまりないので、経験少ない人とどんどん相性良くなっていける関係が理想かなって思ってます♪( ´▽｀)\r\n\r\nもし仕事に偏見なく会ってくれる人いたら連絡もらいたいです！']
  ]
  pcmax_chara_list = func.get_user_data()['pcmax']
  headless = True
  sb_p_all_do(pcmax_chara_list, headless)