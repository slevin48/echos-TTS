import streamlit as st
import urllib.request as urllib2
from bs4 import BeautifulSoup
from gtts import gTTS 
import pandas as pd

def get_echos_articles():
    # "https://www.lesechos.fr/"
    f = urllib2.urlopen("https://www.lesechos.fr/")
    res = f.read()
    soup = BeautifulSoup(res, 'html.parser')
    # articles = [i.text for i in soup.find_all("h3")]
    list = soup.find_all("a",class_= "sc-1560xb1-0 fUqzcK sc-1ttlxdz-2 bxQRWI")
    articles = [i['title'] for i in list]
    links = [i['href'] for i in list]
    dict = {'articles': articles, 'links': links} 
    df = pd.DataFrame(dict)

    return df

def get_echos_title(article):
    # "https://www.lesechos.fr/"
    f = urllib2.urlopen("https://www.lesechos.fr"+article)
    res = f.read()
    soup = BeautifulSoup(res, 'html.parser')
    title = soup.find("h1",class_= "sc-AxirZ sc-1ohdft1-0 leQiFa").text
    return title

def get_echos_abstract(article):
    f = urllib2.urlopen("https://www.lesechos.fr"+article)
    res = f.read()
    soup = BeautifulSoup(res, 'html.parser')
    abstract = soup.find("p",class_= "sc-AxirZ sc-1ohdft1-0 ejcVmy").text
    return abstract

def tts(mytext,desc):
    # text to speech conversion 

    # mytext = 'Welcome to geeksforgeeks!'
    
    # Language in which you want to convert 
    language = 'fr'
    
    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    myobj = gTTS(text=mytext, lang=language, slow=False) 
    
    # Saving the converted audio in a mp3 file named 
    # welcome  
    myobj.save("audio/"+desc+".mp3")

df = get_echos_articles()
select = st.selectbox("Article",[i for i in range(len(df))],format_func=lambda x: df.loc[x].articles)
# https://discuss.streamlit.io/t/label-and-values-in-in-selectbox/1436/3


st.markdown("# "+str(select+1)+") "+get_echos_title(df.loc[select].links))
st.markdown('[lien vers l\'article sur les Echos.fr](https://www.lesechos.fr'+df.loc[select].links+')')

tts(get_echos_title(df.loc[select].links),"article_"+str(select+1))
title_file = open('audio/article_'+str(select+1)+'.mp3', 'rb')
title_bytes = title_file.read()
st.markdown("## Title")
st.audio(title_bytes, format='audio/ogg')

tts(get_echos_abstract(df.loc[select].links),"abstract_"+str(select+1))

st.markdown("## Abstract")
abstract_file = open('audio/abstract_'+str(select+1)+'.mp3', 'rb')
abstract_bytes = abstract_file.read()
st.audio(abstract_bytes, format='audio/ogg')