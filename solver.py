import sys;

def getFreq(char, word):
    count = 0;
    for letter in word:
        if char == letter:
            count += 1;
    return count;

def main():
    guesses = 0;
    debug = False;
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug = True;
    with open('words.txt') as f:
        ALL_WORDS = {w.strip() : True for w in f.readlines()};
    repeat = 'y';
    while (repeat != 'n'):
        print('You have {:d} guesses remaining'.format(6 - guesses));
        user_word = input("Enter your 5 letter word: ").strip();
        correctness = input("Enter _ for not in word, ! for correct spot and ? if in wrong position: ").strip();
        if (correctness == "!!!!!"):
            print("The word is:", user_word + "!");
            exit(0);
        for i in range(5):
            if debug:
                print("Looking at letter:", user_word[i])
            for word in ALL_WORDS.keys():
                if (ALL_WORDS[word]):
                    if correctness[i] == '_' and user_word[i] in word:
                        if debug:
                            print("Removing:", word, "invalid letter:", user_word[i])
                        ALL_WORDS[word] = False;
                        for j in range(5):
                            if i != j and user_word[i] == user_word[j]:
                                if correctness[j] == '!':
                                    ALL_WORDS[word] = word[j] == user_word[i] and (user_word[i] not in word[j+1:] and user_word[i] not in word[:j]);
                                    continue;
                                elif correctness[j] == '?':
                                    ALL_WORDS[word] = word[j] != user_word[i] and (user_word[i] in word[i+1:] or user_word[i] in word[:i]);
                                    continue;
                    elif correctness[i] == '!' and user_word[i] != word[i]:
                        if debug:
                            print("Removing:", word, "missing correct letter:", user_word[i])
                        ALL_WORDS[word] = False;
                        continue;
                    elif correctness[i] == '?':
                        if user_word[i] not in word or user_word[i] == word[i]:
                            if debug:
                                print("Removing:", word, "missing correct letter or in wrong postition:", user_word[i]);
                            ALL_WORDS[word] = False;
                            continue;
                        else:
                            for j in range(5):
                                if i != j and user_word[i] == user_word[j]:
                                    if correctness[j] == '!':
                                        ALL_WORDS[word] = (word[i] != user_word[i] and word[j] == user_word[i]) and (user_word[i] in word[j+1:] or user_word[i] in word[:j]);
                                        continue;
                                    if correctness[j] == '?':
                                        word_freq = getFreq(user_word[i], word);
                                        user_freq = getFreq(user_word[i], user_word);
                                        ALL_WORDS[word] = word[i] != user_word[i] and word[j] != user_word[i] and(word_freq == user_freq);
                                        continue;
        counter = 0;
        valid_words = []
        for k,v in ALL_WORDS.items():
            if v:
                counter += 1;
                valid_words.append(k);
        if counter > 1:
            print("Valid Word(s): ", end="");
            for x in valid_words:
                print(x, end=" ");
            print("");
        elif counter == 1:
            print("The answer is:", valid_words[0] + "!");
            exit(0);
        else:
            print("No valid words, somethings wrong!!!");
            exit(1);
        repeat = input("Guess another word? y/n: ").strip();
        guesses += 1;
        print("");
main();
