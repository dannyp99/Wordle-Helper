def main():
    guesses = 0;
    with open('words.txt') as f:
        ALL_WORDS = {w.strip() : True for w in f.readlines()};
    repeat = 'y'
    while (repeat != 'n'):
        print('You have {:d} guesses remaining'.format(6 - guesses))
        user_word = input("Enter your 5 letter word: ").strip()
        correctness = input("Enter _ for not in word, ! for correct spot and ? if in wrong position: ").strip();
        if (correctness == "!!!!!"):
            print("The word is:", user_word + "!")
            exit()
        for i in range(5):
            #print("Looking at letter:", user_word[i])
            for word in ALL_WORDS.keys():
                if (ALL_WORDS[word]):
                    if correctness[i] == '_' and user_word[i] in word:
                        #print("Removing:", word, "invalid letter:", user_word[i])
                        ALL_WORDS[word] = False;
                        continue;
                    elif correctness[i] == '!' and (user_word[i] != word[i] or user_word[i] not in word):
                        #print("Removing:", word, "missing correct letter:", user_word[i])
                        ALL_WORDS[word] = False;
                        continue;
                    elif correctness[i] == '?' and (user_word[i] not in word or user_word[i] == word[i]):
                        #print("Removing:", word, "missing correct letter or in wrong postition:", user_word[i])
                        ALL_WORDS[word] = False;
                        continue;
        print("Valid Words: ", end="")
        for x in ALL_WORDS.keys():
            if ALL_WORDS[x]:
                print(x, end=" ")
        print("");
        repeat = input("Guess another word? y/n: ").strip();
        guesses += 1
        print("")
main();
