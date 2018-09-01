from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient
import json

# Credenciais
consumer_key = "xxxxxxxxxxxxxxxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
acess_token = "xxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
acess_token_secret = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Autenticação e token de acesso a API
auth = OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(acess_token,acess_token_secret)

# Listener de captura do Tweet e de registro no MongoDB
class Listener(StreamListener):
    qtd = 0
    def on_data(self,dados):
        tweet = json.loads(dados)
        collection.insert_one(tweet)
        self.qtd += 1
        if self.qtd % 100 == 0:
            print("Salvou mais 100 ...")
        return True

listener = Listener()
stream = Stream(auth,listener=listener)

client = MongoClient('localhost',27017) #Criando conexão
db = client.politica #criando banco
collection = db.tweets_eleicoes #criando coleção

# Lista de hashtags
keywords =["eleicoes", "eleicoes2018"]

#Iniciar a filtragem de tweets
stream.filter(track=keywords)
