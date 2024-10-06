import copy

from Constants import constants
from Domains.RandomAI import RandomAI
from Repository.GameRepository import GameRepository


class SmartAI(RandomAI):

    def __init__(self,repository: GameRepository):
        super().__init__()
        self.repository = repository
        self.memorised_table_responses = {}

    def convert_table_to_string_line(self):
        string_of_table = ""
        for line in self.repository.table.table:
            for pawn in line:
                string_of_table = string_of_table + str(int(pawn))
        return string_of_table

    def get_table_score(self):
        string_of_table = self.convert_table_to_string_line()
        if string_of_table not in self.memorised_table_responses:
            self.memorised_table_responses.update({string_of_table: self.repository.table.get_table_score_for_ai()})
            # print(string_of_table+str(self.memorised_table_responses[string_of_table]))
        return self.memorised_table_responses[string_of_table]

    def place_pawn_on_board_by_player(self, table=None,depth=0):
        if depth == 0:
            return 0,self.get_table_score()
        worst_position = constants.UNDEFINED_CODE
        worst_score = 1000
        for position in range(0,23):
            line = position//3
            column = position % 3
            if table.is_slot_empty(line,column):
                self.repository.table.change_table_element(line,column,constants.PLAYER_SLOT)
                removed_position = -1
                removed_line = 0
                removed_column = 0
                if self.repository.is_moara(line,column):
                    removed_position = self.remove_pawn_by_player()
                    removed_line = removed_position // 3
                    removed_column = removed_position % 3
                    self.repository.table.change_table_element(removed_line,removed_column,constants.EMPTY_SLOT)
                best_position, score = self.place_pawn_on_board(table,depth-1)
                if score < worst_score:
                    worst_score = score
                    worst_position = position
                if removed_position != -1:
                    self.repository.table.change_table_element(removed_line,removed_column,constants.AI_SLOT)
                table.change_table_element(line, column, constants.EMPTY_SLOT)
        if worst_position != -1:
            return worst_position,worst_score
        return super().place_pawn_on_board()

    def place_pawn_on_board(self, table=None,depth=0):
        if depth == 0:
            return 0,self.get_table_score()
        best_position = constants.UNDEFINED_CODE
        best_score = -constants.UNOPTAINABLE_SCORE
        for position in range(0,23):
            line = position//3
            column = position % 3
            if self.repository.table.is_slot_empty(line,column):
                self.repository.add_pawn_to_board(line,column,constants.AI_SLOT,for_ai=True)
                removed_position = -2
                removed_line = 0
                removed_column = 0
                if self.repository.is_moara(line,column):
                    removed_position = self.remove_pawn(self.repository.get_all_positions_of_player(constants.PLAYER_SLOT))
                    removed_line = removed_position//3
                    removed_column = removed_position % 3
                    self.repository.table.change_table_element(removed_line,removed_column,constants.EMPTY_SLOT)
                worst_position, score = self.place_pawn_on_board_by_player(table,depth-1)
                if score > best_score:
                    best_score = score
                    best_position = position
                if removed_position != -2:
                    self.repository.table.change_table_element(removed_line,removed_column,constants.PLAYER_SLOT)
                self.repository.table.change_table_element(line, column, constants.EMPTY_SLOT)
        if best_position != -1:
            return best_position,best_score
        return super().place_pawn_on_board()

    def move_pawn_on_board_by_player(self,pawns_position, table=None):
        worst_position = constants.UNDEFINED_CODE
        worst_score = constants.UNOPTAINABLE_SCORE
        worst_direction = 'r'
        for position in self.repository.get_all_positions_of_player(constants.PLAYER_SLOT):
            line = position // 3
            column = position % 3
            for direction in constants.DIRECTIONS_LIST:
                try:
                    new_line, new_column = table.get_new_available_position(line, column, direction)
                    self.repository.table.change_table_element(line, column, constants.EMPTY_SLOT)
                    self.repository.table.change_table_element(new_line, new_column, constants.PLAYER_SLOT)
                    removed_position = -1
                    removed_line = 0
                    removed_column = 0
                    if self.repository.is_moara(new_line, new_column):
                        removed_position = self.remove_pawn_by_player()
                        removed_line = removed_position // 3
                        removed_column = removed_position % 3
                        self.repository.table.change_table_element(removed_line, removed_column, constants.EMPTY_SLOT)
                    score = table.get_table_score_for_ai()
                    if score < worst_score:
                        worst_score = score
                        worst_position = position
                        worst_direction = direction
                    if removed_position != -1:
                        self.repository.table.change_table_element(removed_line, removed_column, constants.AI_SLOT)
                    self.repository.table.change_table_element(line, column, constants.PLAYER_SLOT)
                    self.repository.table.change_table_element(new_line, new_column, constants.EMPTY_SLOT)
                except ValueError as error:
                    pass
        if worst_position != -1:
            return worst_position, worst_direction, worst_score

        return super().move_pawn_on_board(pawns_position)

    def move_pawn_on_board(self, pawns_position, table=None):
        best_position = -1
        best_score = -999
        best_direction = 'r'
        for position in pawns_position:
            line = position//3
            column = position % 3
            for direction in constants.DIRECTIONS_LIST:
                try:
                    new_line, new_column = table.get_new_available_position(line, column, direction)
                    self.repository.table.change_table_element(line, column, constants.EMPTY_SLOT)
                    self.repository.table.change_table_element(new_line, new_column, constants.AI_SLOT)
                    removed_position = -1
                    removed_line = 0
                    removed_column = 0
                    if self.repository.is_moara(new_line, new_column):
                        removed_position = self.remove_pawn(self.repository.get_all_positions_of_player(constants.PLAYER_SLOT))
                        removed_line = removed_position // 3
                        removed_column = removed_position % 3
                        self.repository.table.change_table_element(removed_line, removed_column, constants.EMPTY_SLOT)
                    worst_position, worst_direction, score = self.move_pawn_on_board_by_player(pawns_position,table)
                    if score > best_score:
                        best_score = score
                        best_position = position
                        best_direction = direction
                    if removed_position != -1:
                        self.repository.table.change_table_element(removed_line, removed_column,constants.PLAYER_SLOT)
                    self.repository.table.change_table_element(line, column, constants.AI_SLOT)
                    self.repository.table.change_table_element(new_line, new_column, constants.EMPTY_SLOT)
                except ValueError as error:
                    pass
        if best_position != -1:
            return best_position,best_direction

        return super().move_pawn_on_board(pawns_position)

    def remove_pawn_by_player(self):
        worst_position = -1
        worst_score = 999
        for position in self.repository.get_all_positions_of_player(constants.AI_SLOT):
            line = position // 3
            column = position % 3
            try:
                self.repository.remove_pawn(line, column, constants.PLAYER_SLOT, for_ai=True)
                score = self.get_table_score()
                if score < worst_score:
                    worst_score = score
                    worst_position = position
                self.repository.add_pawn_to_board(line, column, constants.AI_SLOT, for_ai=True)
            except ValueError as error:
                pass
        if worst_position != -1:
            return worst_position
        return super().remove_pawn(self.repository.get_all_positions_of_player(constants.AI_SLOT))

    def remove_pawn(self,pawns_position,table=None):
        best_position = -1
        best_score = -999
        for position in pawns_position:
            line = position//3
            column = position % 3
            try:
                self.repository.remove_pawn(line,column,constants.AI_SLOT,for_ai=True)
                score = self.get_table_score()
                if score > best_score:
                    best_score = score
                    best_position = position
                self.repository.add_pawn_to_board(line,column,constants.PLAYER_SLOT,for_ai=True)
            except ValueError as error:
                pass
        if best_position != -1:
            return best_position
        return super().remove_pawn(pawns_position)
