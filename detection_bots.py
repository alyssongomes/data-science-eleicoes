import botometer
import pandas as pd
import numpy as np
import time
import tweepy

'''
mashape_key: chave obtida no site onde a API BotOrNot é gerenciada
link: https://market.mashape.com/OSoMe/botometer

twitter_app_auth: chaves obtidas no site do Twitter App
link: https://apps.twitter.com/
'''

mashape_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
twitter_app_auth = {
    'consumer_key': 'xxxxxxxxxxxxxxxxxxxx',
    'consumer_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'access_token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
    'access_token_secret': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
  }
bom = botometer.Botometer(wait_on_ratelimit=True,
                          mashape_key=mashape_key,
                          **twitter_app_auth)


df = pd.read_csv('SCREEN_NAME_BOT.csv',sep=',')

def qtd(x):
	i = 0
	for j in x:
		if np.isnan(j) == False:
			i += 1
	return i

names = list(df.screen_name)
names_analyses = qtd(df.bot.values)

i = names_analyses
for n in names[names_analyses:]:
	print(n)
	try:
		result = bom.check_account('@'+n)
		print(float(result['scores']['universal']))
		df.bot[i] = float(result['scores']['universal']) #probabilidade de ser bot
	except botometer.NoTimelineError:
		df.bot[i] = 0
	except tweepy.error.TweepError:
		print("No Autorized")
		df.bot[i] = 0
		time.sleep(1200)
		continue
	finally:
		df.to_csv('SCREEN_NAME_BOT.csv',sep=';',encoding='utf-8', index=False)

	if i % 90 == 0:
		df.to_csv('SCREEN_NAME_BOT.csv',sep=';',encoding='utf-8', index=False)
		time.sleep(900) #espera 15 minutos
		print("Mais 120 registrados...")

	i += 1

df.to_csv('SCREEN_NAME_BOT.csv',sep=';',encoding='utf-8', index=False)

