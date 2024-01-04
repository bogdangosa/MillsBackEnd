from Constants import constants


class Game:
    def __init__(self,player1_slot,player2_slot):
        self.game_state = constants.GAME_HASNT_STARTED
        self.player1_slot = player1_slot
        self.player2_slot = player2_slot
        self.player1_pawns = 0
        self.player2_pawns = 0
        self.player1_pawns_removed = 0
        self.player2_pawns_removed = 0

    def start_game(self):
        self.game_state = constants.FILL_THE_TABLE

    def get_player1_pawns(self):
        return self.player1_pawns

    def get_player2_pawns(self):
        return self.player2_pawns

    def get_game_state(self):
        return self.game_state

    def are_all_pieces_on_the_board(self):
        return self.player1_pawns+self.player1_pawns_removed == constants.MAXIMUM_NUMBER_OF_PAWNS and self.player2_pawns+self.player2_pawns_removed == constants.MAXIMUM_NUMBER_OF_PAWNS

    def add_pawn_to_board(self,player_slot):
        if player_slot == self.player1_slot:
            self.player1_pawns += 1
        elif player_slot == self.player2_slot:
            self.player2_pawns += 1
        if self.are_all_pieces_on_the_board():
            self.game_state = constants.MOVE_PIECES

    def remove_pawn_from_board(self,player_slot):
        if player_slot == self.player1_slot:
            self.player1_pawns_removed += 1
            self.player1_pawns -= 1
        if player_slot == self.player2_slot:
            self.player2_pawns_removed += 1
            self.player2_pawns -= 1

        if self.are_all_pieces_on_the_board():
            self.game_state = constants.MOVE_PIECES
        else:
            self.game_state = constants.FILL_THE_TABLE
