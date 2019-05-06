import urllib3.request
import nltk
import ssl, os
import certifi
from collections import defaultdict
from heapq import nlargest
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from bs4 import BeautifulSoup
import requests

def getTextVerge(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content.decode('utf8'), 'lxml')
    return soup.find("div", {"class":"l-col__main"}).text.replace('\n', '')

def summarize(text, n):
    # Setup... Figure out whether or not ther are less sentences than the number of sentences we want
    sents = sent_tokenize(text)
    assert n <= len(sents)
    
    # Filter out stopwords
    _stopwords = set(stopwords.words('english') + list(punctuation))
    word_sent = [word for word in word_tokenize(text.lower()) if word not in _stopwords]
    
    # Construct a frequency distribution of the surviving words
    freq = FreqDist(word_sent)
    
    # Begin ranking logic
    ranking = defaultdict(int)
    for i,sent in enumerate(sents): 
        for w in word_tokenize(sent.lower()):
            if w in freq:
                ranking[i] += freq[w]
                
    # Prep results and return
    sents_idx = nlargest(4, ranking, key=ranking.get)
    return [sents[j] for j in sorted(sents_idx)]

def getVergeReport(url, n):
    verge = getTextVerge(url=url)
    summ = summarize(verge, n)
    return summ
