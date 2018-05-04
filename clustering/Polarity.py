'''
    Classe que calcula a polaridade dos tweets
'''
import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords

class Polarity(object):

    base_lexica = None
    
    @staticmethod
    def load():
        Polarity.base_lexica = pd.read_csv('../SEMANTICSCLASSIFICATION/SentiLex.csv', sep=';')

    @staticmethod
    def preProcessor(tweet):
        t = tweet
        t = t.lower() # removendo letras maiúsculas
        t = re.sub(r'(\b)?@\w+','',t) #removendo referências a outros perfis
        # t = re.sub(r'(\b)?#\w+','',t) #removendo hashtags
        t = re.sub(r'http\S+','',t,flags=re.MULTILINE) #removendo links
        t = re.sub(r'https\S+','',t,flags=re.MULTILINE) #removendo links
        t = re.sub(r'(\w+)?\d(\w+)?','',t) # removendo números
        t = re.sub(r',|\"|!|\n|:|\.|\?|;|\(|\)',' ',t) #removendo pontuações

        # removendo stopwords
        nsw = ''
        for word in t.split(' '):
            if word not in stopwords.words('portuguese'):
                nsw += word+' '
        t = nsw.strip()

        t = re.sub(r' +',' ',t) # removendo espaços duplos
        t = t.strip() # remover espaços vazios no início e no fim
        return t

    @staticmethod
    def searchWord(word):
        k = 0
        for p in Polarity.base_lexica.palavra:
            if word in p:
                return int(Polarity.base_lexica.pol[k].split('=')[1])
            k += 1
        return 0


