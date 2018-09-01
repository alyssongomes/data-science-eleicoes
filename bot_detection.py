import threading
import botometer
import pandas as pd
import numpy as np
import time
import tweepy

mashape_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
twitter_app_auth = {
    'consumer_key': 'xxxxxxxxxxxxxxxxxxxxxxxxx',
    'consumer_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'access_token': 'xxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)
def worker(files):
    dt = None
    file_name = None

    def query(user_name):
        try:
            result = bom.check_account('@'+user_name)
            return float(result['scores']['universal']) #probabilidade de ser bot
        except botometer.NoTimelineError:
            return 0
        except tweepy.error.TweepError:
            print("No Autorized")
            dt.to_csv(file_name+'_location.csv',sep=',', encoding='utf-8', index=False)
            time.sleep(1200)

    for f in files:
        dt = pd.read_csv(f+'_location.csv',sep=',',encoding='utf8')
        file_name = f
        # dt['likely_bot'] = 0
        for z in zip(dt.user_screen_name, range(len(dt.user_screen_name))):
            if dt.loc[z[1],'likely_bot'] == 0:
                print(z)
                dt.loc[z[1],'likely_bot'] = query(z[0])
                print(dt.loc[z[1],'likely_bot'])
                dt.to_csv(f+'_location.csv',sep=',', encoding='utf-8', index=False)

ta = threading.Thread(target=worker,args=(['ALCKMIN'],))
tb = threading.Thread(target=worker,args=(['BOLSONARO'],))
tc = threading.Thread(target=worker,args=(['LULA'],))
td = threading.Thread(target=worker,args=(['CIRO'],))
te = threading.Thread(target=worker,args=(['MANUELA','BOULOS','MARINA'],))
tf = threading.Thread(target=worker,args=(['TEMER'],))
ta.start()
tb.start()
tc.start()
td.start()
te.start()
tf.start()
