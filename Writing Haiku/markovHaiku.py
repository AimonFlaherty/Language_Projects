import sys
import logging
import random
from collections import defaultdict
from syllablesCount import syllablesCount


# use logging to debug program
logging.disable(logging.CRITICAL) # comment out to enable debugging
logging.basicConfig(level = logging.DEBUG, format = '%(message)s')


# read data from file
def loadTrainingFile(file):
    with open(file) as f:
        rawData = f.read()
        return rawData


# replace newline with spaces, splits the words into lists
def prepTraining(rawData):
    corpus = rawData.replace('\n', ' ').split()
    return corpus


# map word to trailing word
def mapWordToWord(corpus):
    limit = len(corpus) - 1
    dict_to1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            suffix = corpus[index + 1]
            dict_to1[word].append(suffix)
    logging.debug("map word to word results for \"sake\" = %s\n", dict_to1['sake'])
    return dict_to1


# map 2 words to trailing word
def map2WordsToWord(corpus):
    limit = len(corpus) - 2
    dict2_to1 = defaultdict(list)
    for index, word in enumerate(corpus):
        if index < limit:
            key = word + ' ' + corpus[index + 1]
            suffix = corpus[index + 2]
            dict2_to1[key].append(suffix)
    logging.debug("map 2 word to word results for \"sake two\" = %s\n", dict2_to1['sake two'])
    return dict2_to1


# pick random word and return word with syllable count
def randWord(corpus):
    word = random.choice(corpus)
    num_sylls = syllablesCount(word)
    if num_sylls > 4:
        randWord(corpus)
    else:
        logging.debug("random word & syllables: %s %s\n", word, num_sylls)
        return (word, num_sylls)


# return acceptable words after target word
def wordAfterSingle(prefix, suffix_map_1, current_sylls, target_sylls):
    accepted_words = []
    suffixes = suffix_map_1.get(prefix)
    if suffixes != None:
        for candidate in suffixes:
            num_sylls = syllablesCount(candidate)
            if current_sylls + num_sylls <= target_sylls:
                accepted_words.append(candidate)
    logging.debug("accepted words after \"%s\" = %s\n", prefix, set(accepted_words))
    return accepted_words


# return acceptable words after word pair
def wordAfterDouble(prefix, suffix_map_2, current_sylls, target_sylls):
    accepted_words = []
    suffixes = suffix_map_2.get(prefix)
    if suffixes != None:
        for candidate in suffixes:
            num_sylls = syllablesCount(candidate)
            if current_sylls + num_sylls <= target_sylls:
                accepted_words.append(candidate)
    logging.debug("accepted words after \"%s\" = %s\n", prefix, set(accepted_words))
    return accepted_words


# build a haiku line
def haikuLine(suffix_map_1, suffix_map_2, corpus, end_prev_line, target_sylls):
    line = '2/3'
    line_sylls = 0
    current_line = []
    if len(end_prev_line) == 0:
        line = '1'
        word, num_sylls = randWord(corpus)
        current_line.append(word)
        line_sylls += num_sylls
        word_choices = wordAfterSingle(word, suffix_map_1, line_sylls, target_sylls)
        while len(word_choices) == 0:
            prefix = random.choice(corpus)
            logging.debug('new random prefix = %s', prefix)
            word_choices = wordAfterSingle(prefix, suffix_map_1, line_sylls, target_sylls)
        word = random.choice(word_choices)
        num_sylls = syllablesCount(word)
        logging.debug('word & syllables = %s %s', word, num_sylls)
        line_sylls += num_sylls
        current_line.append(word)
        if line_sylls == target_sylls:
            end_prev_line.extend(current_line[-2:])
            return current_line, end_prev_line
    else:
        current_line.extend(end_prev_line)

    while True:
        logging.debug('line = %s\n', line)
        prefix = current_line[-2] + ' ' + current_line[-1]
        word_choices = wordAfterDouble(prefix, suffix_map_2, line_sylls, target_sylls)

        while len(word_choices) == 0:
            index = random.randint(0, len(corpus) - 2)
            prefix = corpus[index] + ' ' + corpus[index + 1]
            logging.debug('new random prefix = %s', prefix)
            word_choices = wordAfterDouble(prefix, suffix_map_2, line_sylls, target_sylls)

        word = random.choice(word_choices)
        num_sylls = syllablesCount(word)
        logging.debug('word & syllables = %s %s', word, num_sylls)

        if line_sylls + num_sylls > target_sylls:
            continue
        elif line_sylls + num_sylls < target_sylls:
            current_line.append(word)
            line_sylls += num_sylls
        elif line_sylls + num_sylls == target_sylls:
            current_line.append(word)
            break

    end_prev_line = []
    end_prev_line.extend(current_line[-2:])
    if line == '1':
        final_line = current_line[:]
    else:
        final_line = current_line[2:]
    return final_line, end_prev_line


# user interface
def main():
    print("\nSometimes a computer can write a haiku\n")

    raw_haiku = loadTrainingFile('train.txt')
    corpus = prepTraining(raw_haiku)
    suffix_map_1 = mapWordToWord(corpus)
    suffix_map_2 = map2WordsToWord(corpus)
    final = []

    choice = None
    while choice != 0:
        print("""
        Haiku Generator

        0 - Quit
        1 - Generate a haiku
        2 - Regenerate line 2
        3 - Regenerate line 3
        """)
        choice = input("Choice: ")
        print()

        if choice == '0':
            print('Exit')
            sys.exit()

        elif choice == '1':
            final = []
            end_prev_line = []
            first_line, end_prev_line1 = haikuLine(suffix_map_1, suffix_map_2, corpus, end_prev_line, 5)
            final.append(first_line)
            line, end_prev_line2 = haikuLine(suffix_map_1, suffix_map_2, corpus, end_prev_line1, 7)
            final.append(line)
            line, end_prev_line3 = haikuLine(suffix_map_1, suffix_map_2, corpus, end_prev_line2, 5)
            final.append(line)

        elif choice == '2':
            if not final:
                print('Generate a full haiku first')
                continue
            else:
                print(end_prev_line1)
                line, end_prev_line2 = haikuLine(suffix_map_1, suffix_map_2, corpus, end_prev_line1, 7)
                final[1] = line

        elif choice == '3':
            if not final:
                print('Generate a full haiku first')
                continue
            else:
                line, end_prev_line3 = haikuLine(suffix_map_1, suffix_map_2, corpus, end_prev_line2, 5)
                final[2] = line

        else:
            print('\nNot a valid choice', file = sys.stderr)
            continue

        # Results
        print()
        print('', end = '')
        print(' '.join(final[0]), file = sys.stderr)
        print('', end = '')
        print(' '.join(final[1]), file = sys.stderr)
        print('', end = '')
        print(' '.join(final[2]), file = sys.stderr)
        print("                            -Python")


if __name__ == '__main__':
    main()
