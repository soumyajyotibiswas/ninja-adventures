import string, random, os

# Game variables
intro_message='''
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/    


Welcome to the hangman game.
You have to guess the correct word, before you loose
all your lives. As you loose a life, a body will start
to appear on the noose. If you can guess the word,
before your life hits 0, you win. All the letters are
from the english dictionary, and are greater or equal to
7 letters and less or equal to 10 letters.
You have 7 lives if you enter a wrong alphabet, and 3 
retries if you enter anything other than an aplhabet.

Pro Tip: Try starting with a vowel first.
Note: The prorgam depends on the file /usr/share/dict/words.
'''
alphabets_list=list(string.ascii_lowercase)
word_length=random.randint(7,10)
count=3
lives=6
dict_location='/usr/share/dict/words'
# This is for systems with the file available
def random_word_generator():
    word_dictionary=open(dict_location,'r').read().split('\n')
    return(random.choice([word.lower() for word in word_dictionary if word.isalpha() and len(word) == word_length]))
random_word=random_word_generator()
display_list=['_' for char in random_word]
def is_game_over():
    if count == 0:
        print("You entered 3 choices that were not alphabets. Sorry. Try again!")
        return True
    elif lives == 0:
        print(f"You are out of extra lives. Sorry. Try Again!. The word was {random_word}.")
        return True
    elif '_' not in display_list:
        print(f"You have won with {lives} left. The word was {random_word}.")
        return True
    else:
        return False
def show_game_stat():
    print(f"No of lives left: {lives}")
    print(f"No of retries left: {count}")
    print(f"The word is: ",*display_list)
# Game start
while(True):
    print(intro_message)
    show_game_stat()
    user_input=input("Enter a letter of your choice: ").lower()
    print("***** Processing *****")
    if user_input not in alphabets_list:
        print(f"Entered value {user_input} is not a valid alphabet.Try Again!")
        count-=1
    else:
        index_user_choice=[i for i in range(0,len(random_word)) if random_word[i] == user_input]
        if len(index_user_choice) == 0:
            print(f"Uh Oh! Wrong choice.")
            lives-=1
        else:
            if user_input in display_list:
                print(f"Your have already chosen '{user_input}' once.")
            else:
                for i in index_user_choice:
                    display_list[int(i)]=user_input
    show_game_stat()
    input("Press any key to continue..")
    os.system('clear')
    game_stat=is_game_over()
    if game_stat:
        show_game_stat()
        break