from base_bot import BaseBot
from collections import Counter

class Player(BaseBot):
    def choose_card(self, top_card):
        # checking for valid plays based on color or value matching
        # matching R5: playing R7 (color) or B5 (value)
        def can_play_card(card, top_card):
            return (card[0] == top_card[0] or  # matching colors
                   card[1:] == top_card[1:])   # matching values
        
        # determining optimal color for wild cards
        # analyzing hand: R4 R7 B2 R1 -> selecting R (3 reds)
        def my_best_color():
            my_colors = Counter()
            for card in self.hand:
                if card[0] in 'RGBY':  # counting standard colors
                    my_colors[card[0]] += 1
            
            # handling empty hand scenario
            if not my_colors:
                return 'R'
            
            # selecting most frequent color
            return my_colors.most_common(1)[0][0]
        
        # searching for matching standard cards first
        # considering hand=[B4, WC], top=R4: playing B4
        for card in self.hand:
            if card in ['WC', 'PC']:  # reserving wilds
                continue
            if can_play_card(card, top_card):
                return card
        
        # proceeding to wild card options
        # examining hand=[WC, G2], top=R5: playing WG
        if 'WC' in self.hand:
            return f'W{my_best_color()}'
        
        # considering +4 wild as final option
        # evaluating hand=[PC, B3], top=R5: playing PB
        if 'PC' in self.hand:
            return f'P{my_best_color()}'
        
        # drawing card when no plays available
        # noting hand=[B2, B3], top=R5: drawing
        return None

    
    
# For local testing only
    
if __name__ == "__main__":
    bot = Player(player_id=0)

    # Example input
    bot.hand = input("Enter your hand as space-separated cards: ").strip().split()
    top_card = input("Enter the top card: ").strip()

    move = bot.choose_card(top_card)
    print(f"Chosen card: {move}")