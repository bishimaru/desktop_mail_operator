from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime, time, timedelta
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from widget import pcmax, happymail, func
import p_fstmail
from datetime import datetime, timedelta



def tick():
    print("Tick! The time is : %s'" % datetime.now())

if __name__ == '__main__':
    headless = True
    scheduler = BlockingScheduler()  # スケジューラを作る
    user_data = func.get_user_data()
    
    # chara_order_list = [
    # "アスカ","いおり","えりか","きりこ",
    # "さな","すい","つむぎ","なお",
    # # "はづき":{}, "ハル":{}, "めあり":{},"りこ":{}, 
    # # "りな":{}, "ゆっこ":{},"ゆかり":{}, "ゆうな":{},
    # ]
    chara_list = []
    for i in user_data["pcmax"]:
        chara_list.append(i)
        # if i["name"] in chara_order_list:
        #     print(i["name"])
        #     chara_list.append(i)
        print(i["name"])
    
    # 朝のジョブ
    scheduler.add_job(p_fstmail.main, 'cron', hour=5, minute=30, args=[1, chara_list, 11, 5, headless],  misfire_grace_time=60*60)
    # # 昼のジョブ
    scheduler.add_job(p_fstmail.main, 'cron', hour=14, minute=15, args=[1, chara_list, 16, 15, headless],  misfire_grace_time=60*60)
    # # 夜のジョブ
    scheduler.add_job(p_fstmail.main, 'cron', hour=18, minute=0, args=[1, chara_list, 22, 10, headless], misfire_grace_time=60*60)
    print("Press Ctrl+{0} to exit.".format('Break' if os.name == 'nt' else 'C'))
    
    try:
        scheduler.start()  # スタート
    except (KeyboardInterrupt, SystemExit):
        pass