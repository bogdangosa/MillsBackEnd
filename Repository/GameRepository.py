from Constants import constants
from Domains.DumbAI import DumbAI
from Domains.Game import Game
from Domains.Table import Table


class GameRepository:

    def __init__(self,player1_slot,player2_slot):
        self.game = Game(player1_slot,player2_slot)
        self.table = Table()

    def get_game_state(self):
        return self.game.get_game_state()

    def get_table(self):
        return self.table

    def can_player1_jump(self):
        return self.game.player1_can_jump

    def can_player2_jump(self):
        return self.game.player2_can_jump

    def get_player1_pawns(self):
        return self.game.get_player1_pawns()

    def get_player2_pawns(self):
        return self.game.get_player2_pawns()

    def get_table_string(self):
        return f"""
        player1:{self.game.get_player1_pawns()}
        player2:{self.game.get_player2_pawns()}
        {self.table}
        """

    def get_table_dict(self) -> dict:
        return self.table.to_dict()

    def get_table_list(self) -> list:
        return self.table.to_list()

    def start_game(self):
        self.game.start_game()

    def jump_pawn_on_board(self,line,column,new_line,new_column,player_slot,for_ai=False):
        if self.table.table[line][column] != player_slot:
            raise ValueError("There isn't your pawn on that position!")
        if not self.table.is_slot_empty(new_line,new_column):
            raise ValueError("Not an empty slot")
        self.table.change_table_element(line,column,constants.EMPTY_SLOT)
        self.table.change_table_element(new_line,new_column,player_slot)
        if self.is_moara(new_line, new_column):
            self.game.game_state = constants.REMOVE_PIECES

    def add_pawn_to_board(self,line,column,player_slot,for_ai=False):
        if not self.table.is_slot_empty(line,column):
            raise ValueError("Not an empty slot")
        self.table.change_table_element(line,column,player_slot)
        if not for_ai:
            self.game.add_pawn_to_board(player_slot)
            if self.is_moara(line,column):
                self.game.game_state = constants.REMOVE_PIECES

    def is_slot_empty(self,line,column):
        return self.table.is_slot_empty(line,column)

    def is_column_the_same(self,column: list[tuple]) -> bool:
        first_position = column[0]
        first_line = first_position[0]
        first_column = first_position[1]
        first_sign = self.table.table[first_line][first_column]
        for position in column:
            line = position[0]
            column = position[1]
            if self.table.table[line][column] != first_sign:
                return False
        return True

    def is_moara(self,line,column) -> bool:
        if self.table.table[line][column] == constants.EMPTY_SLOT:
            return False
        if self.table.table[line][0] == self.table.table[line][1] == self.table.table[line][2]:
            return True

        for a_column in constants.COLUMNS:
            if (line,column) in a_column:
                if self.is_column_the_same(a_column):
                    return True
        return False

    def remove_pawn(self,line,column,player_slot,for_ai=False):
        can_player_jump = self.game.can_opposite_player_jump(player_slot)
        if self.table.table[line][column] == player_slot or self.table.is_slot_empty(line,column) or (self.is_moara(line,column) and not can_player_jump):
            raise ValueError("Not a valid position to remove!")
        self.table.make_slot_empty(line,column)
        if not for_ai:
            self.game.remove_pawn_from_board(player_slot)
            if self.is_game_over():
                self.game.game_state = constants.GAME_ENDED

    def move_pawn_on_board(self,line,column,direction,player_slot):
        if self.table.table[line][column] != player_slot:
            raise ValueError("There isn't your pawn on that position!")
        new_line,new_column = self.table.get_new_available_position(line,column,direction)
        self.table.change_table_element(line,column,constants.EMPTY_SLOT)
        self.table.change_table_element(new_line,new_column,player_slot)
        if self.is_moara(new_line, new_column):
            self.game.game_state = constants.REMOVE_PIECES

    def get_all_positions_of_player(self,player_slot):
        return self.table.get_all_positions_of_slot(player_slot)

    def is_game_over(self):
        if self.game.player1_pawns_removed > 6 or self.game.player2_pawns_removed > 6:
            return True