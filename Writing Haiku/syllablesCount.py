import sys
import json
from string import punctuation
from nltk.corpus import cmudict

with open('missing_words.json') as f:
    missing_words = json.load(f)

cmudict = cmudict.dict()

def syllablesCount(words):
    words= words.replace('-', ' ')
    words = words.lower().split()
    num_sylls = 0
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]
        if word in missing_words:
            num_sylls += missing_words[word]
        else:
            for phonemes in cmudict[word][0]:
                for phoneme in phonemes:
                    if phoneme[-1].isdigit():
                        num_sylls += 1
    return num_sylls


def main():
    while True:
        print('Counting Syllables')
        word = input('Enter word or phrase or press enter to exit: ')
        if word  == '':
            sys.exit()
        try:
            syllables_count = syllablesCount(word)
            print('number of syllables in {} is: {}'.format(word, syllables_count))
            print()
        except KeyError:
            print('Word not found. \n', file = sys.stderr)


if __name__ == '__main__':
    main()
