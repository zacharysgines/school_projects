from db import get_all_wordle_answers, get_all_words
import string

wordle = get_all_wordle_answers()
words = get_all_words()

position_freq = [{letter: 0 for letter in string.ascii_lowercase} for i in range(0,5)]
for word in wordle:
    for i in range(0,5):
        position_freq[i][word[i].lower()] += 1

letter_totals = {}
for letter in string.ascii_lowercase:
    sum = 0
    for i in range(0,5):
        sum += position_freq[i][letter]
    letter_totals[letter] = sum

def give_word(green, yellow, gray):
    #Keep track of words that are in the dictionary but not in the wordle database so I don't get them again
    false_words = ['slaie']
    best = ["", 0]
    for word in words:
        word = word.lower()
        #Make sure that all the letters are actual letters, this hasn't been a wordle word before, and it's in the wordle database
        if all(c.isalpha() for c in word) and word not in wordle and word not in false_words:
            duplicate_count = 0
            letters = []
            positional_sum = 0
            overall_sum = 0
            score = 0
            valid_word = True
            #Loop for each letter in the word
            for i in range(0,5):
                #Check against all green, yellows and grays
                if (green[i] != None and word[i] != green[i]) or (word[i] in yellow[i]) or (word[i] in gray):
                    valid_word = False
                    break
                #Calculate sums based on letter frequency of past words used in wordle
                positional_sum += position_freq[i][word[i]]
                overall_sum += letter_totals[word[i]]
                #Track duplicate letters to penalize them later
                if word[i] in letters:
                    duplicate_count += 1
                letters.append(word[i])                
            #Make sure that all the yellow letters are accounted for
            if valid_word:
                for i in range(0,5):
                    if valid_word:
                        for letter in yellow[i]:
                            if letter not in (letters):
                                valid_word = False
                                break
            #Calcuate score for this word
            if valid_word:
                positional_sum *= 1 - (duplicate_count / 5)
                overall_sum /= 5
                score = positional_sum * 0.7 + overall_sum * 0.3
                #If this is the best word, store it
                if score > best[1]:
                    best[0] = word
                    best[1] = score
    return best[0]