import sys
import logging
import time


def getFreq(char, word):
    count = 0
    for letter in word:
        if char == letter:
            count += 1
    return count


def answer_generator(user_word, correctness):
    global ALL_WORDS
    for i in range(5):
        log.debug("Looking at letter:", user_word[i])
        for word in ALL_WORDS.keys():
            if correctness[i] == '_' and user_word[i] in word:
                log.debug("Removing: %s invalid letter: %s", word,
                          user_word[i])
                ALL_WORDS[word] = False
                for j in range(5):
                    if i != j and user_word[i] == user_word[j]:
                        if correctness[j] == '!':
                            ALL_WORDS[word] = word[j] == user_word[i] and (user_word[i] not in word[j+1:] and user_word[i] not in word[:j])
                            continue
                        elif correctness[j] == '?':
                            ALL_WORDS[word] = word[j] != user_word[i] and (user_word[i] in word[i+1:] or user_word[i] in word[:i])
                            continue
            elif correctness[i] == '!' and user_word[i] != word[i]:
                log.debug("Removing: %s missing correct letter: %s", word,
                          user_word[i])
                ALL_WORDS[word] = False
                continue
            elif correctness[i] == '?':
                if user_word[i] not in word or user_word[i] == word[i]:
                    log.debug("Removing: %s missing correct letter or in wrong postition: %s",
                              word, user_word[i])
                    ALL_WORDS[word] = False
                    continue
                else:
                    for j in range(5):
                        if i != j and user_word[i] == user_word[j]:
                            if correctness[j] == '!':
                                ALL_WORDS[word] = (word[i] != user_word[i] and word[j] == user_word[i]) and (user_word[i] in word[j+1:] or user_word[i] in word[:j])
                                continue
                            if correctness[j] == '?':
                                word_freq = getFreq(user_word[i], word)
                                user_freq = getFreq(user_word[i], user_word)
                                ALL_WORDS[word] = word[i] != user_word[i] and word[j] != user_word[i] and (word_freq == user_freq)
                                continue


def main():
    global ALL_WORDS
    guesses = 0
    print(len(sys.argv))
    if len(sys.argv) > 1 and str.lower(sys.argv[1]) == "debug":
        log.setLevel(logging.DEBUG)
    with open('words.txt') as f:
        ALL_WORDS = {w.strip(): True for w in f.readlines()}
    repeat = 'y'
    while (repeat != 'n'):
        print('You have {:d} guesses remaining'.format(6 - guesses))
        user_word = input("Enter your 5 letter word: ").strip().lower()
        correctness = input("Enter _ for not in word, ! for correct spot and ? if in wrong position: ").strip()
        if (correctness == "!!!!!"):
            print("The word is:", user_word + "!")
            exit(0)

        #start = time.time()
        answer_generator(user_word, correctness)
        #end = time.time()

        #diff = (end - start) * 1000
        #print("Execution time:", diff, "milliseconds")

        ALL_WORDS = dict(filter(lambda entry: entry[1], ALL_WORDS.items()))
        valid_word_count = len(ALL_WORDS.keys())
        if valid_word_count > 1:
            print("Valid Word(s): ", end="")
            for k in ALL_WORDS.keys():
                print(k, end=" ")
            print("")
        elif valid_word_count == 1:
            print("The answer is:", next(iter(ALL_WORDS.keys())) + "!")
            exit(0)
        else:
            print("No valid words, somethings wrong!!!")
            exit(1)
        repeat = input("Guess another word? y/n: ").strip()
        guesses += 1
        print("")


log = logging.getLogger('solver')
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] [%(levelname)s] %(name)s: %(message)s', dt_fmt)
handler.setFormatter(formatter)
log.addHandler(handler)
ALL_WORDS = dict()
main()
