import random

from Domains.Table import Table

DIRECTION_OPTIONS = [['r','b'],['l','r','b'],['l','b'],
                     ['r','b'],['l','r','b','t'],['l','b'],
                     ['r','b'],['l','r','t'],['l','b'],
                     ['t','b','r'],['t','b','r','l'],['t','b','l'],
                     ['t','b','r'],['t','b','r','l'],['t','b','l'],
                     ['r','t'],['l','r','b'],['l','t'],
                     ['r', 't'], ['l', 'r', 'b', 't'], ['l', 't'],
                     ['r', 't'], ['l', 'r', 't'], ['l', 't']]


class RandomAI:

    def __init__(self):
        pass

    def place_pawn_on_board(self, table=None):
        if table is None:
            table = []
        return random.randint(0,23)

    def move_pawn_on_board(self,pawns_positions,table=None):
        random_pawn = random.choice(pawns_positions)
        direction = random.choice(DIRECTION_OPTIONS[random_pawn])
        print(str(random_pawn)+direction)
        return random_pawn,direction

    def remove_pawn(self,pawns_position,table=None):
        random_pawn = random.choice(pawns_position)
        return random_pawn
