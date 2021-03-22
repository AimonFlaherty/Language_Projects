import sys
import syllablesCount

with open('train.txt') as in_file:
    words = set(in_file.read().split())

missing = []

for word in words:
    try:
        num_sylls = syllablesCount.syllablesCount(word)
        #print(word, num_sylls, end = '\n') #word counts
    except KeyError:
        missing.append(word)
print('Missing words: ', missing, file = sys.stderr)
