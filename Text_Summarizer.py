from flask import Flask, render_template, url_for, request
import time
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from bs4 import BeautifulSoup
from urllib.request import urlopen

nlp = spacy.load("en_core_web_sm")
app = Flask(__name__)


def txt_summarizer(raw_docx):
    stopwords = list(STOP_WORDS)
    raw_text = raw_docx
    docx = nlp(raw_text)

   
    word_frequency = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequency.keys():
                word_frequency[word.text] = 1
            else:
                word_frequency[word.text] += 1
    maximum_frequncy = max(word_frequencies.values())
    for word in word_frequency.keys():
        word_frequency[word] = (word_frequency[word]/maximum_frequncy)
    
    
    sentence_list = [sentence for sentence in docx.sents]

    
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [w.text for w in summarized_sentences]
    summary = ' '.join(final_sentences)

    return summary


def readingT(mytext):
    total_words = len([token.text for token in nlp(mytext)])
    estimatedTime = total_words/200.0
    return estimatedTime

@app.route('/')
def index():
    return render_template('index.html')
