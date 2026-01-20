from solver import give_word

green = [None, None, None, None, None]
yellow = [[], [], [], [], []]
gray = []
guesses = 0

input("Are you ready to play Wordle? Press Enter to continue...")

while guesses < 6:
    print("Try this word:", give_word(green, yellow, gray))
    correct = input("Did I get it right? (y/n) ")
    if correct == 'y':
        break
    
    green_input = input('What letters were green? (Enter all 5 letters with "_" for letters that werent green) ').replace(" ", "").lower()
    yellow_input = input('What letters were yellow? (Enter all 5 letters with "_" for letters that werent yellow) ').replace(" ", "").lower()
    gray_input = input('Enter all the letters that were gray (separate with a comma): ').replace(" ", "").split(',')
    
    for i in range(0,5):
        if green_input[i] != "_":
            green[i] = green_input[i]
        if yellow_input[i] != "_" and yellow_input[i] not in yellow[i]:
            yellow[i].append(yellow_input[i])
    for letter in gray_input:
        if letter not in gray:
            gray.append(letter.lower())

    guesses += 1

if correct == 'y':
    print("Yay! I guessed your word in", str(guesses + 1), "guess(es)!")
else:
    print("Oh no! I couldn't guess your word :(")