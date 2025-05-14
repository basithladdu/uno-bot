from game_engine import Game
from playerBot import Player as PlayerBot
from practice_bot import PracticeBot
import random


def main():
    game = Game()

    bots = {
        0: PlayerBot(0),
        1: PracticeBot(1),
        2: PracticeBot(2),
        3: PracticeBot(3)
    }

    for pid, bot in bots.items():
        bot.receive_cards([game.deck.draw_card() for _ in range(7)])
        game.players[pid] = bot

    game.turn_order = list(bots.keys())
    game.current_player = game.turn_order[0]
    # Draw initial top card (must not be a Wild, +4 or action card)
    while True:
        first_card = game.deck.draw_card()
        if first_card and (
                first_card[0] in ['R', 'G', 'B', 'Y'] and  # Valid color
                first_card[1:].isdigit()  # Must be a number (not action)
        ):
            game.played_cards.append(first_card)
            break
        else:
            # Put invalid card back and reshuffle
            game.deck.cards.insert(0, first_card)
            random.shuffle(game.deck.cards)

    round_counter = 0
    while True:
        current_player = game.current_player
        bot = game.players[current_player]
        top_card = game.played_cards[-1]

        # Only log Player 0's moves in submission format
        if current_player == 0:
            print(f"Top card: {top_card}")
            print(f"Bot hand: {bot.hand}")

        move = bot.choose_card(top_card)
        
        if current_player == 0:
            print(f"Chosen move: {move}\n")

        if move:
            winner = game.play_turn(current_player, move)
            if winner is not None:
                break
        else:
            winner = game.play_turn(current_player, None)
            if winner is not None:
                break

        round_counter += 1
        if round_counter > 200:
            break


if __name__ == "__main__":
    main()
