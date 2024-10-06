import random

from Constants import constants
from Domains.RandomAI import RandomAI
from Domains.Table import Table

DIRECTION_OPTIONS = [['r','b'],['l','r','b'],['l','b'],
                     ['r','b'],['l','r','b','t'],['l','b'],
                     ['r','b'],['l','r','t'],['l','b'],
                     ['t','b','r'],['t','b','r','l'],['t','b','l'],
                     ['t','b','r'],['t','b','r','l'],['t','b','l'],
                     ['r','t'],['l','r','b'],['l','t'],
                     ['r', 't'], ['l', 'r', 'b', 't'], ['l', 't'],
                     ['r', 't'], ['l', 'r', 't'], ['l', 't']]


class DumbAI(RandomAI):

    def __init__(self):
        super().__init__()

    def place_pawn_on_board(self,table=None,depth=None):
        blocking_position = -1
        if table is not None:
            for index1,line in enumerate(table.table):
                ai_slots_per_line = 0
                player_slots_per_line = 0
                index_of_empty_slot = -1
                for index2,slot in enumerate(line):
                    if slot == constants.AI_SLOT:
                        ai_slots_per_line += 1
                    elif slot == constants.EMPTY_SLOT:
                        index_of_empty_slot = index2
                    elif slot == constants.PLAYER_SLOT:
                        player_slots_per_line += 1
                if ai_slots_per_line == 2 and index_of_empty_slot != -1:
                    position = index1*3+index_of_empty_slot
                    return position,0
                elif player_slots_per_line == 2 and index_of_empty_slot !=-1:
                    blocking_position = index1 * 3 + index_of_empty_slot

            for column in constants.COLUMNS:
                ai_slots_per_line = 0
                player_slots_per_line = 0
                line_of_empty_slot = -1
                column_of_empty_slot = -1
                for slot_position in column:
                    current_line = slot_position[0]
                    current_column = slot_position[1]
                    if table.table[current_line][current_column] == constants.AI_SLOT:
                        ai_slots_per_line += 1
                    elif table.table[current_line][current_column] == constants.EMPTY_SLOT:
                        line_of_empty_slot = current_line
                        column_of_empty_slot = current_column
                    elif table.table[current_line][current_column] == constants.PLAYER_SLOT:
                        player_slots_per_line += 1
                if ai_slots_per_line == 2 and line_of_empty_slot != -1:
                    position = line_of_empty_slot * 3 + column_of_empty_slot
                    return position,0
                elif player_slots_per_line == 2 and line_of_empty_slot != -1:
                    blocking_position = line_of_empty_slot * 3 + column_of_empty_slot
        if blocking_position != -1:
            return blocking_position,0
        return super().place_pawn_on_board()

    def move_pawn_on_board(self,pawns_positions,table=None):
        if table is not None:
            empty_position = -1
            blocking_position = -1
            for index1, line in enumerate(table.table):
                ai_slots_per_line = 0
                player_slots_per_line = 0
                index_of_empty_slot = -1

                for index2, slot in enumerate(line):
                    if slot == constants.AI_SLOT:
                        ai_slots_per_line += 1
                    elif slot == constants.EMPTY_SLOT:
                        index_of_empty_slot = index2
                    elif slot == constants.PLAYER_SLOT:
                        player_slots_per_line += 1

                if ai_slots_per_line == 2 and index_of_empty_slot != -1:
                    empty_position = index1 * 3 + index_of_empty_slot
                    line, column = index1,index_of_empty_slot
                    try:
                        line,column = table.get_new_position(index1,index_of_empty_slot,constants.DIRECTION_TOP)
                        if table.get_table_element(line,column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_BOTTOM
                    except ValueError as error:
                        pass
                    try:
                        line,column = table.get_new_position(index1,index_of_empty_slot,constants.DIRECTION_BOTTOM)
                        if table.get_table_element(line,column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_TOP
                    except ValueError as error:
                        pass
                    # print("empty position:" + str(empty_position+1))
                elif player_slots_per_line == 2 and index_of_empty_slot != -1:
                    line, column = index1,index_of_empty_slot
                    blocking_position = index1 * 3 + index_of_empty_slot
                    try:
                        line, column = table.get_new_position(index1, index_of_empty_slot, constants.DIRECTION_TOP)
                        if table.get_table_element(line, column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_BOTTOM
                    except ValueError as error:
                        pass
                    try:
                        line, column = table.get_new_position(index1, index_of_empty_slot, constants.DIRECTION_BOTTOM)
                        if table.get_table_element(line, column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_TOP
                    except ValueError as error:
                        pass
                    # print("blocking position"+str(blocking_position + 1))

            for column in constants.COLUMNS:
                ai_slots_per_line = 0
                player_slots_per_line = 0
                line_of_empty_slot = -1
                column_of_empty_slot = -1

                for slot_position in column:
                    current_line = slot_position[0]
                    current_column = slot_position[1]
                    if table.table[current_line][current_column] == constants.AI_SLOT:
                        ai_slots_per_line += 1
                    elif table.table[current_line][current_column] == constants.EMPTY_SLOT:
                        line_of_empty_slot = current_line
                        column_of_empty_slot = current_column
                    elif table.table[current_line][current_column] == constants.PLAYER_SLOT:
                        player_slots_per_line += 1

                if ai_slots_per_line == 2 and line_of_empty_slot != -1:
                    empty_position = line_of_empty_slot * 3 + column_of_empty_slot
                    try:
                        line,column = table.get_new_position(line_of_empty_slot,column_of_empty_slot,constants.DIRECTION_RIGHT)
                        if table.get_table_element(line,column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_LEFT
                    except ValueError as error:
                        pass
                    try:
                        line,column = table.get_new_position(line_of_empty_slot,column_of_empty_slot,constants.DIRECTION_LEFT)
                        if table.get_table_element(line,column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_RIGHT
                    except ValueError as error:
                        pass
                    # print("empty position:" + str(empty_position+1))
                elif player_slots_per_line == 2 and line_of_empty_slot != -1:
                    blocking_position = line_of_empty_slot * 3 + column_of_empty_slot
                    try:
                        line, column = table.get_new_position(line_of_empty_slot, column_of_empty_slot, constants.DIRECTION_RIGHT)
                        if table.get_table_element(line, column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_LEFT
                    except ValueError as error:
                        pass
                    try:
                        line, column = table.get_new_position(line_of_empty_slot, column_of_empty_slot, constants.DIRECTION_LEFT)
                        if table.get_table_element(line, column) == constants.AI_SLOT:
                            return line*3+column,constants.DIRECTION_RIGHT
                    except ValueError as error:
                        pass
                    # print("blocking position"+str(blocking_position + 1))
        return super().move_pawn_on_board(pawns_positions)

    def remove_pawn(self,pawns_position,table=None):
        if table is not None:
            for index1, line in enumerate(table.table):
                player_slots_per_line = 0
                index_of_empty_slot = -1
                index_of_player_slot = -1
                for index2, slot in enumerate(line):
                    if slot == constants.PLAYER_SLOT:
                        index_of_player_slot = index2
                        player_slots_per_line += 1
                    elif slot == constants.EMPTY_SLOT:
                        index_of_empty_slot = index2
                if player_slots_per_line == 2 and index_of_empty_slot != -1:
                    position = index1 * 3 + index_of_player_slot
                    return position

            for column in constants.COLUMNS:
                player_slots_per_line = 0
                line_of_player_slot = -1
                column_of_player_slot = -1
                was_empty_slot = False
                for slot_position in column:
                    current_line = slot_position[0]
                    current_column = slot_position[1]
                    if table.table[current_line][current_column] == constants.EMPTY_SLOT:
                        was_empty_slot = True
                    elif table.table[current_line][current_column] == constants.PLAYER_SLOT:
                        player_slots_per_line += 1
                        line_of_player_slot = current_line
                        column_of_player_slot = current_column
                if player_slots_per_line == 2 and was_empty_slot:
                    position =  line_of_player_slot * 3 + column_of_player_slot
                    return position
        return super().remove_pawn(pawns_position)
