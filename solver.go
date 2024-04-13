package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"sort"
	"strings"
)

var all_words map[string] bool = make(map[string]bool)
var debug_logger *log.Logger

func get_freq(character string, word string) int {
    counter := 0
    for _, char := range word {
        if string(char) == character {
            counter++
        }
    }
    return counter
}

func load_word_list() {
    file, err := os.Open("words.txt")

    if err != nil {
        log.Fatal(err)
    }

    defer file.Close()

    scanner := bufio.NewScanner(file)

    for scanner.Scan() {
        all_words[scanner.Text()] = true
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }
}

func filter(word_map map[string] bool) map[string] bool {
    filtered_word_map := make(map[string] bool)
    for k, v := range word_map {
        if v { filtered_word_map[k] = v }
    }
    return filtered_word_map

}

func answer_generator(user_word string, correctness string) {
    for i := range 5 {
        checking_char := string(user_word[i])
        debug_logger.Printf("Loooking at letter %s\n", checking_char)
        for word := range all_words {
            if string(correctness[i]) == "_" && strings.Contains(word, checking_char) {
                debug_logger.Printf("Removing %s invalid letter: %s\n", word, checking_char)
                all_words[word] = false
                for j := range 5 {
                    correctness_char := string(correctness[j])
                    if i != j && checking_char == string(user_word[j]) {
                        if correctness_char == "!" {
                            all_words[word] = string(word[j]) == checking_char && (!strings.Contains(word[j+1:], checking_char) && !strings.Contains(word[:j], checking_char))
                            debug_logger.Println(word, "is:", all_words[word])
                            continue
                        } else if correctness_char == "?" {
                            all_words[word] = string(word[j]) != checking_char && (strings.Contains(word[i+1:], checking_char) || strings.Contains(word[:i], checking_char))
                            debug_logger.Println(word, "is:", all_words[word])
                            continue
                        }
                    }
                }
            } else if string(correctness[i]) == "!" && checking_char != string(word[i]) {
                debug_logger.Printf("Removing %s missing correct letter: %s\n", word, checking_char)
                all_words[word] = false
                continue
            } else if string(correctness[i]) == "?" { // ? case
                if !strings.Contains(word, checking_char) || checking_char == string(word[i]) {
                    debug_logger.Printf("Removing: %s missing correct letter or in wrong postition: %s\n", word, checking_char)
                    all_words[word] = false
                    continue
                } else {
                    var correctness_char string
                    for j := range 5 {
                        correctness_char = string(correctness[j])
                        if i != j && checking_char == string(user_word[j]) {
                            if correctness_char == "!" {
                                debug_logger.Printf("split char: %s, contains true? %t", word[:j], strings.Contains(word[:j], checking_char))
                                all_words[word] = (string(word[i]) != checking_char && string(word[j]) == checking_char) && (strings.Contains(word[j+1:], checking_char) || strings.Contains(word[:j], checking_char))
                                debug_logger.Println(word, "is:", all_words[word])
                                continue
                            } else if correctness_char == "?" {
                                word_freq := get_freq(checking_char, word)
                                user_freq := get_freq(checking_char, user_word)
                                all_words[word] = string(word[i]) != checking_char && string(word[j]) != checking_char && (word_freq == user_freq)
                                debug_logger.Println(word, "is:", all_words[word])
                                continue
                            }
                        }
                    }
                }
            }
        }
    }
}

func main() {
    reader := bufio.NewReader(os.Stdin)
    guesses := 0
    var argv []string = os.Args
    if len(argv) > 1 && strings.ToLower(argv[1]) == "debug" {
        debug_logger = log.New(os.Stdout, "DEBUG: ", log.Ldate|log.Ltime|log.Lshortfile)
    } else {
        debug_file, err := os.OpenFile("go-logs.log", os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0666)
        if err != nil {
            log.Fatal(err)
        }
        debug_logger = log.New(debug_file, "DEBUG: ", log.Ldate|log.Ltime|log.Lshortfile)
    }

    load_word_list()
    //for k := range all_words {
    //    delete(all_words, k)
    //}
    //all_words["arles"] = true

    repeat := "y"
    for guesses <= 6 && repeat != "n" {
        fmt.Printf("You have %d guesses remaining\n", 6 - guesses)
        fmt.Printf("Enter your 5 letter word: ")
        user_word, _ := reader.ReadString('\n')
        cleaned_user_word := strings.ToLower(strings.TrimSpace(user_word))
        fmt.Printf("Enter _ for not in word, ! for correct spot and ? if in wrong position: ")
        correctness, _ := reader.ReadString('\n')
        cleaned_correctness := strings.ToLower(strings.TrimSpace(correctness))
        if cleaned_correctness == "!!!!!" {
            fmt.Println("The word is:", cleaned_user_word, "!")
            os.Exit(0)
        }

        answer_generator(cleaned_user_word, cleaned_correctness)

        all_words = filter(all_words) 
        valid_word_count := len(all_words)
        if valid_word_count > 1 {
            keys := make([]string, 0, len(all_words))
            for k := range all_words {
                keys = append(keys, k)
            }
            sort.Strings(keys)
            fmt.Printf("Valid Word(s): ")
            for _, k := range keys {
                fmt.Printf("%s ", k)
            }
            fmt.Println()
        } else if valid_word_count == 1 {
            var answer string
            for k := range all_words { answer = k; break }
            fmt.Printf("The answer is: %s\n", answer)
            os.Exit(0)
        } else {
            fmt.Println("No valid words, something is wrong!!!")
            os.Exit(1)
        }
        fmt.Printf("Guess another word? y/n: ")
        repeat_read, _ := reader.ReadString('\n')
        repeat = strings.TrimSpace(repeat_read)
        guesses++ 
        fmt.Println()
    }

}
