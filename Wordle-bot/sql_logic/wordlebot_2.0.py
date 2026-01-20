import pyodbc

driver = '{ODBC Driver 17 for SQL Server}'
server = 'LIAM\\SQLEXPRESS'
database = 'Dictionary'
trusted_connection = 'yes'

connection_string = (
    f"DRIVER={driver};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection={trusted_connection};"
)

with pyodbc.connect(connection_string) as conn:
    cursor = conn.cursor()

    green1 = ''
    green2 = ''
    green3 = ''
    green4 = ''
    green5 = ''
    yellow1 = []
    yellow2 = []
    yellow3 = []
    yellow4 = []
    yellow5 = []
    missing = []
    included_letters = []

    i = 0
    while i <= 6:
        cursor.execute("{CALL Wordlebot (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)}", 
                    (green1, green2, green3, green4, green5,
                        ','.join(yellow1), ','.join(yellow2), ','.join(yellow3), ','.join(yellow4), ','.join(yellow5),
                        ','.join(missing)))
        
        row = cursor.fetchone()
        if not row:                    
            correct = 'na'
            break
        else:
            print("Here, try this word:")
            print(row[0])

            correct = input("Did you get it correct? (y/n) ")
            if correct == 'y':
                break
            else:
                greens = input("Enter green letters (use _ for unknowns): ")
                yellows = input("Enter yellow letters (use _ for unknowns): ")
                grays = input("Enter all gray letters here (no commas or spaces): ")
                
                if greens[0] != '_' and greens[0] not in green1:
                    green1 = greens[0]
                    included_letters.append(greens[0])
                if greens[1] != '_' and greens[1] not in green2:
                    green2 = greens[1]
                    included_letters.append(greens[1])
                if greens[2] != '_' and greens[2] not in green3:
                    green3 = greens[2]
                    included_letters.append(greens[2])
                if greens[3] != '_' and greens[3] not in green4:
                    green4 = greens[3]
                    included_letters.append(greens[3])
                if greens[4] != '_' and greens[4] not in green5:
                    green5 = greens[4]
                    included_letters.append(greens[4])

                if yellows[0] != '_' and yellows[0] not in yellow1:
                    yellow1.append(yellows[0])
                    included_letters.append(yellows[0])
                if yellows[1] != '_' and yellows[1] not in yellow2:
                    yellow2.append(yellows[1])
                    included_letters.append(yellows[1])
                if yellows[2] != '_' and yellows[2] not in yellow3:
                    yellow3.append(yellows[2])
                    included_letters.append(yellows[2])
                if yellows[3] != '_' and yellows[3] not in yellow4:
                    yellow4.append(yellows[3])
                    included_letters.append(yellows[3])
                if yellows[4] != '_' and yellows[4] not in yellow5:
                    yellow5.append(yellows[4])
                    included_letters.append(yellows[4])

                        
                for letter in grays:
                    if letter not in missing and letter not in included_letters:
                        missing.append(letter)

                i += 1

    if correct == 'y':
        print("Yay! I guessed your word in", i+1, "guesses!")
    elif correct == 'n':
        print("Oh no, I wasn't able to guess your word :()")
    else:
        new_word = input("Oops! Looks like I ran out of words! Can you tell me what your word was? (input with no spaces or special charachters) ")
        insert_word_query = '''
            INSERT INTO words (word)
            VALUES (?)
        '''

        cursor.execute(insert_word_query, (new_word,))
        conn.commit()

        new_word_query = 'SELECT word FROM words WHERE word = ?'

        cursor.execute(new_word_query, (new_word,))
        row = cursor.fetchone()
        if row:
            print("Got it! I added your word to the dictionary")
        else:
            print("Oops! I wasn't able to add your word to the dictionary.")