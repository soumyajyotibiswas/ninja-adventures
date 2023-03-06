import random,os

def set_global_variables():
    global complete_eight_deck_of_cards,dealer_cards,dealer_cards_total,dealer_stand,dealer_wins,initial_message,match_draw,one_deck_of_cards,player_bet,player_cards,player_cards_total,player_stand,player_wins,rules,shuffle_threshold,total_player_winnings
    initial_message='''
    _     _            _    _            _    
    | |   | |          | |  (_)          | |   
    | |__ | | __ _  ___| | ___  __ _  ___| | __
    | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /
    | |_) | | (_| | (__|   <| | (_| | (__|   < 
    |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\
                        _/ |                
                        |__/                 

    Welcome to the game of blackjack.
    This is a simple game, player vs the computer (dealer).
    The deck has a set of 8 sets. Splits, early surrender,
    soft 17 and doubling down is not allowed. If you win,
    you get 2 times your bet as return. So if you bet $100,
    you will get $200.
    '''
    rules='''
    1. 2 through 10 count at face value, i.e. a 2 counts as two, a 9 counts as nine.
    2. Face cards (J,Q,K) count as 10.
    3. Ace can count as a 1 or an 11 depending on which value helps the hand the most.

    ****How do you beat the dealer?****

    By drawing a hand value that is higher than the dealer's hand value
    By the dealer drawing a hand value that goes over 21.
    By drawing a hand value of 21 on your first two cards, when the dealer does not.

    ****How do you lose to the dealer?****

    Your hand value exceeds 21.
    The dealers hand has a greater value than yours at the end of the round
    '''
    one_deck_of_cards=[2,3,4,5,6,7,8,9,10,10,10,10,[1,11]]
    complete_eight_deck_of_cards=32*one_deck_of_cards
    player_cards=[]
    dealer_cards=['_']
    shuffle_threshold=104
    player_bet=0
    player_cards_total=0
    dealer_cards_total=0
    player_wins=(True,'p')
    dealer_wins=(True,'d')
    match_draw=(False,'d')
    total_player_winnings=0
    player_stand=False
    dealer_stand=False

def print_intro_message():
    print(initial_message)

def print_rules():
    print(rules)

def shuffle_decks():
    global complete_eight_deck_of_cards
    complete_eight_deck_of_cards=32*one_deck_of_cards
    random.shuffle(complete_eight_deck_of_cards)

def deal_card(when='',whom=''):
    if len(complete_eight_deck_of_cards) < shuffle_threshold:
        shuffle_decks()
    choice_of_card=random.choice(complete_eight_deck_of_cards)
    complete_eight_deck_of_cards.remove(choice_of_card)
    if isinstance(choice_of_card,list):
        choice_of_card=deal_with_ace(when,whom)
    return choice_of_card

def add_cards():
    global dealer_cards_total
    global player_cards_total
    dealer_cards_total=0
    for i in dealer_cards:
        if isinstance(i,int):
            dealer_cards_total += i
    player_cards_total=0
    for i in player_cards:
        if isinstance(i,int):
            player_cards_total += i

def deal_with_ace(when='',whom=''):
    add_cards()
    if whom == 'player':
        if when == 'initial':
            print("Hey! you got an ACE to start with.")
        print(f"Your current cards are:",*player_cards)
        print(f"Your cards total is {player_cards_total}.")
        player_choice=int(input("\nDo you want to consider this ACE as 1 or 11? [eg: 1] --> "))
        if player_choice not in [1,11]:
            raise Exception(f"Invalid choice of '{player_choice}' while picking a value for ACE.")
        return player_choice
    else:
        if when == 'initial':
            return 11
        else:
            return 1

def hit_me(whom=''):
    if whom == 'player':
        return deal_card(whom='player')
    else:
        return deal_card()

def place_bets():
    global player_bet
    player_choice=int(input("Enter your bet between $1 to $100: [eg: 1 denotes $1 ] --> "))
    if player_choice not in list(range(1,101)):
        raise Exception(f"Your bet of '${player_choice}' is invalid. It has to be between $1 to $100.")
    else:
        player_bet=player_choice

def dealer_plays():
    global dealer_stand    
    while(True):
        add_cards()
        if dealer_cards_total < 17:
            if dealer_cards[0] == '_':
                dealer_cards[0]=hit_me(whom='dealer')
            else:
                dealer_cards.append(hit_me(whom='dealer'))
        else:
            dealer_stand=True
            break

def player_winnings(when='',what=''):
    global total_player_winnings
    if what=='won':
        if when == 'initial':
            total_player_winnings += 2.5 * player_bet
        else:
            total_player_winnings += 2 * player_bet
    else:
        total_player_winnings -= player_bet

def is_player_bust():
    add_cards()
    if player_cards_total > 21:
        return True
    else:
        return False

def is_game_over(when=''):
    add_cards()
    if when == 'initial':
        if player_cards_total == 21:
            return True,'p'
        else:
            return False,'n'
    else:
        if player_stand and dealer_stand:
            if (player_cards_total == 21 or dealer_cards_total < player_cards_total or dealer_cards_total > 21) and not (player_cards_total > 21):
                return True,'p'
            elif dealer_cards_total == player_cards_total:
                return True,'dr'
            elif (dealer_cards_total == 21 or dealer_cards_total > player_cards_total or player_cards_total > 21) and not (dealer_cards_total > 21):
                return True,'de'
            else:
                return False,'n'
        else:
                return False,'n'

def initial_setup():
    set_global_variables()
    print_intro_message()
    print_rules()
    shuffle_decks()
    dealer_cards.append(deal_card(when='initial'))
    place_bets()
    for _ in range(0,2):
        player_cards.append(deal_card(whom='player'))
    display_table('i')

def display_table(when=''):
    input("\nPress any key to continue..")
    os.system('clear')
    add_cards()
    print("\nThe dealer's cards are: ",*dealer_cards,f" | Total of dealer's cards is '{dealer_cards_total}'.")
    print("The player's cards are: ",*player_cards,f" | Total of player's cards is '{player_cards_total}'.")
    print(f"Player bet is '${player_bet}'.\n")
    if when!='i':
        print(f"Player total winnings till now '${total_player_winnings}'")