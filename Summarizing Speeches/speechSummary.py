
import re
import requests
import bs4
import nltk
from nltk.corpus import stopwords
from collections import Counter

def main():
    url = 'http://www.analytictech.com/mb021/mlk.htm'
    page = requests.get(url)
    page.raise_for_status()
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    p_elems = [element.text for element in soup.find_all('p')]

    speech = ''.join(p_elems)
    speech = speech.replace(')mowing', 'knowing')
    speech = re.sub('\s+', ' ', speech)
    speech_edit = re.sub('[^a-zA-Z]', ' ', speech)
    speech_edit = re.sub('\s', ' ', speech_edit)

    while True:
        max_words = input('Enter the max number of words per sentence: ')
        num_sens = input('Enter the number of sentences: ')
        if max_words.isdigit() and num_sens.isdigit():
            break
        else:
            print('\nPlease enter a whole number\n')

    speech_edit_no_stop = removeStopWords(speech_edit)
    word_freq = wordFreq(speech_edit_no_stop)
    sen_scores = scoreSens(speech, word_freq, max_words)

    counts = Counter(sen_scores)
    summary = counts.most_common(int(num_sens))
    print('\nSummary:\n')
    for i in summary:
        print(i[0])


def removeStopWords(speech_edit):
    stop_words = set(stopwords.words('english'))
    speech_edit_no_stop = ''
    for word in nltk.word_tokenize(speech_edit):
        if word.lower() not in stop_words:
            speech_edit_no_stop += word + ' '
    return speech_edit_no_stop


def wordFreq(speech_edit_no_stop):
    word_freq = nltk.FreqDist(nltk.word_tokenize(speech_edit_no_stop.lower()))
    return word_freq


def scoreSens(speech, word_freq, max_words):
    sen_scores = dict()
    sentences = nltk.sent_tokenize(speech)
    for sen in sentences:
        sen_scores[sen] = 0
        words = nltk.word_tokenize(sen.lower())
        sen_word_count = len(words)
        if sen_word_count <= int(max_words):
            for word in words:
                if word in word_freq.keys():
                    sen_scores[sen] += word_freq[word]
            sen_scores[sen] = sen_scores[sen] / sen_word_count
    return sen_scores


if __name__ == '__main__':
    main()
