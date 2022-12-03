import common_config as cc

def does_player_want_to_play():
    cc.display_table()
    if not cc.player_cards_total >= 21 and not cc.player_stand:
        player_choice=input(f"\nEnter hit or stand. If you enter hit, a card will be dealt to you and added to the total of your cards. Your current card total is '{cc.player_cards_total}' and your cards are '{cc.player_cards}' --> ").lower()
        if player_choice not in ['hit','stand']:
            raise Exception(f"Invalid choice of '{player_choice}' when asked played to 'hit' or 'stand'. Try again!")
        elif player_choice == 'stand':
            cc.player_stand=True
        else:
            cc.player_cards.append(cc.hit_me(whom="player"))
            does_player_want_to_play()
    else:
        cc.player_stand=True

def who_won():
    (x,y)=cc.is_game_over()
    cc.display_table()
    if x:
        if y == 'p':
            cc.player_winnings(what='won')
            print(f"\n****You Won****.\nCongratulations. Your total earnings '${cc.total_player_winnings}'.")
        elif y == 'de':
            cc.player_winnings(what='lost')
            print(f"\n****Dealer Won****.\nYour total earnings '${cc.total_player_winnings}'.")
        else:
            print(f"\n****It's a draw****.")
    else:
        raise Exception("Invalid state hit. Cannot determine who won.")

def play_game():
    does_player_want_to_play()
    if not cc.is_player_bust():
        cc.dealer_plays()
    else:
        cc.dealer_stand=True

def main():
    cc.os.system('clear')
    to_continue=current_total=0
    game_count=1
    while(True):
        cc.initial_setup()
        if to_continue == 'yes':
            cc.total_player_winnings=current_total
        (x,y)=cc.is_game_over('initial')
        if (x,y) == cc.player_wins:
            cc.player_winnings(when='initial',what='won')
            print(f"\n****BLACKJACK****\nYou won even before the match started. You win '${cc.total_player_winnings}'.")
        else:
            play_game()
        who_won()
        to_continue=input("\nDo you want to continue playing the same game? enter yes or no. If you enter anything other than 'yes', you will have a choice to exit the game or reset the game. [eg: yes] --> ").lower()
        print(f"\nEnd of round '{game_count}'.")
        if to_continue != 'yes':
            to_reset=input("\nDo you want to exit the game? If you enter anything other than 'yes', the game will reset. [eg: yes] --> ").lower()
            if to_reset != 'yes':
                main()
            else:
                print("\nThank you for playing Blackjack. Bye.")
                break
        else:
            current_total=cc.total_player_winnings
            game_count += 1

main()