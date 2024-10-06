import random

from Constants import constants
from Domains.DumbAI import DumbAI
from Domains.RandomAI import RandomAI
from Domains.SmartAI import SmartAI
from Repository.GameRepository import GameRepository


class Services:

    def __init__(self,game_mode):
        self.repository = GameRepository(constants.PLAYER_SLOT,constants.AI_SLOT)
        self.ai = RandomAI()
        self.__game_mode = game_mode
        pass

    def get_game_state(self):
        return self.repository.get_game_state()

    def can_player1_jump(self):
        return self.repository.can_player1_jump()

    def can_player2_jump(self):
        return self.repository.can_player2_jump()

    def get_table(self):
        return self.repository.get_table_string()

    def get_table_data(self) -> dict:
        return {
            "table_matrix": self.repository.get_table_list(),
            "player1_pawns":self.repository.get_player1_pawns(),
            "player2_pawns":self.repository.get_player2_pawns(),
        }

    def start_game(self,selected_ai:int):
        if selected_ai == constants.DUMB_AI:
            self.ai = DumbAI()
        elif selected_ai == constants.SMART_AI:
            self.ai = SmartAI(self.repository)
        self.repository.start_game()

    @staticmethod
    def is_position_valid(position: int):
        return 0 <= position <= 23

    @staticmethod
    def from_position_id_to_line_and_column(position: int):
        if not Services.is_position_valid(position):
            raise ValueError("Not a valid position!")
        line = position//3
        column = position % 3
        return line,column

    def add_pawn_to_board(self,position: int,player_slot=constants.PLAYER_SLOT):
        line,column = Services.from_position_id_to_line_and_column(position)
        self.repository.add_pawn_to_board(line,column,player_slot,for_ai=False)
        if self.__game_mode == constants.PLAYER_VS_PLAYER or self.repository.get_game_state() == constants.REMOVE_PIECES:
            return
        self.add_pawn_to_board_ai()

    def add_pawn_to_board_ai(self):
        position_ai,score = self.ai.place_pawn_on_board(self.repository.get_table(),depth=constants.AI_DEPTH)
        line,column = Services.from_position_id_to_line_and_column(position_ai)
        while not self.repository.is_slot_empty(line, column):
            position_ai,score = self.ai.place_pawn_on_board()
            line,column = Services.from_position_id_to_line_and_column(position_ai)
        self.repository.add_pawn_to_board(line, column, constants.AI_SLOT,for_ai=False)
        if self.repository.get_game_state() == constants.REMOVE_PIECES:
            self.remove_pawn_from_board_ai()

    def remove_pawn_from_board(self,position:int,player_slot=constants.PLAYER_SLOT):
        line,column = Services.from_position_id_to_line_and_column(position)
        self.repository.remove_pawn(line,column,player_slot,for_ai=False)
        if self.__game_mode == constants.PLAYER_VS_PLAYER:
            return
        if self.repository.get_game_state() == constants.FILL_THE_TABLE:
            self.add_pawn_to_board_ai()
        elif self.repository.get_game_state() == constants.MOVE_PIECES:
            self.move_pawn_ai()

    def remove_pawn_from_board_ai(self):
        position = self.ai.remove_pawn(self.repository.get_all_positions_of_player(constants.PLAYER_SLOT),self.repository.get_table())
        line = position//3
        column = position % 3
        try:
            self.repository.remove_pawn(line,column,constants.AI_SLOT,for_ai=False)
        except ValueError as error:
            self.remove_pawn_from_board_ai()

    def move_pawn(self,position:int,direction,player_slot=constants.PLAYER_SLOT):
        line = position//3
        column = position % 3
        self.repository.move_pawn_on_board(line,column,direction,player_slot)
        if self.repository.get_game_state() == constants.REMOVE_PIECES or self.__game_mode == constants.PLAYER_VS_PLAYER:
            return
        self.move_pawn_ai()

    def jump_pawn(self,position:int,new_position:int,player_slot=constants.PLAYER_SLOT):
        line, column = Services.from_position_id_to_line_and_column(position)
        new_line,new_column = Services.from_position_id_to_line_and_column(new_position)
        self.repository.jump_pawn_on_board(line,column,new_line,new_column,player_slot,for_ai=False)
        if self.repository.get_game_state() == constants.REMOVE_PIECES or self.__game_mode == constants.PLAYER_VS_PLAYER:
            return 
        self.move_pawn_ai()

    def move_pawn_ai(self):
        position,direction = self.ai.move_pawn_on_board(self.repository.get_all_positions_of_player(constants.AI_SLOT),self.repository.get_table())
        line, column = Services.from_position_id_to_line_and_column(position)
        try:
            self.repository.move_pawn_on_board(line, column, direction, constants.AI_SLOT)
            if self.repository.get_game_state() == constants.REMOVE_PIECES:
                self.remove_pawn_from_board_ai()
        except ValueError as error:
            self.move_pawn_ai()

    def get_possible_directions_from_position(self,position):
        line,column = Services.from_position_id_to_line_and_column(position)
        table = self.repository.get_table()
        positions_list = []
        for direction in constants.DIRECTIONS_LIST:
            try:
                new_line,new_column = table.get_new_available_position(line,column,direction)
                positions_list.append({
                    "direction":direction,
                    "position":new_line*3+new_column
                })
            except ValueError as error:
                pass
        return positions_list
