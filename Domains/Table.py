import numpy

from Constants import constants

class Table:

    def __init__(self):
        self.__table = []
        self.initialise_table()

    def initialise_table(self):
        self.__table = numpy.zeros((8,3))

    @property
    def table(self):
        return self.__table

    @table.setter
    def table(self,new_table):
        self.__table = new_table

    @staticmethod
    def convert_code_to_icon(code):
        if code == constants.EMPTY_SLOT:
            return constants.EMPTY_SLOT_ICON
        elif code == constants.PLAYER_SLOT:
            return constants.PLAYER_SLOT_ICON
        elif code == constants.AI_SLOT:
            return constants.AI_SLOT_ICON

    def convert_table_to_icons(self):
        icons_table = []
        for index,line in enumerate(self.table):
            icons_table.append([])
            for item in line:
                icons_table[index].append(Table.convert_code_to_icon(item))
        return icons_table

    def make_slot_empty(self,line,column):
        self.__table[line][column] = constants.EMPTY_SLOT

    def change_table_element(self,line,column,new_element):
        self.__table[line][column] = new_element

    def is_slot_empty(self,line,column):
        return self.__table[line][column] == constants.EMPTY_SLOT

    def get_table_element(self,line,column):
        return self.__table[line][column]

    def is_direction_available(self,line,column,direction):
        if direction == constants.DIRECTION_RIGHT:
            column += 1
        if direction == constants.DIRECTION_LEFT:
            column -= 1
        if direction == constants.DIRECTION_BOTTOM:
            for column_list in constants.COLUMNS:
                for index,position in enumerate(column_list[0:-1]):
                    if position == (line,column):
                        return True
            return False
        if direction == constants.DIRECTION_TOP:
            for column_list in constants.COLUMNS:
                for index, position in enumerate(column_list[1:]):
                    if position == (line, column):
                        return True
            return False
        if column < 0 or column > 3:
            return False
        if not self.is_slot_empty(line,column):
            return False
        return True

    def get_new_available_position(self,line,column,direction):
        line,column = self.get_new_position(line,column,direction)
        if not self.is_slot_empty(line,column):
            raise ValueError("Not an available position")
        return line,column

    @staticmethod
    def get_new_position(line,column,direction):
        """

        :param line:
        :param column:
        :param direction:
        :return: the line and column of the element if you go in that direction from the line and column passed to the method
        """
        if direction == constants.DIRECTION_RIGHT:
            column += 1
        if direction == constants.DIRECTION_LEFT:
            column -= 1
        if direction == constants.DIRECTION_BOTTOM:
            position_found = False
            for column_list in constants.COLUMNS:
                for index,position in enumerate(column_list[0:-1]):
                    if position == (line,column):
                        line = column_list[index+1][0]
                        column = column_list[index+1][1]
                        position_found = True
                        break
                if position_found:
                    break
            if not position_found:
                raise ValueError("Not a valid direction")
        if direction == constants.DIRECTION_TOP:
            position_found = False
            for column_list in constants.COLUMNS:
                for index, position in enumerate(column_list[1:]):
                    if position == (line, column):
                        line = column_list[index][0]
                        column = column_list[index][1]
                        position_found = True
                        break
                if position_found:
                    break
            if not position_found:
                raise ValueError("Not a valid direction")
        if column < 0 or column > 2:
            raise ValueError("Not a valid direction")
        return line,column

    def get_all_positions_of_slot(self,player_slot):
        positions_array = []
        counter = 0
        for line in self.__table:
            for slot in line:
                if slot == player_slot:
                    positions_array.append(counter)
                counter += 1
        return positions_array

    def to_dict(self):
        dict_table = []
        for index1,line in enumerate(self.__table):
            for index2,element in enumerate(line):
                position = index1*3+index2
                dict_table[str(position)] = element
        return dict_table

    def to_list(self):
        list_table = []
        for index1,line in enumerate(self.__table):
            for index2,element in enumerate(line):
                position = index1*3+index2
                list_table.append(element)
        return list_table

    def __str__(self):
        icons_table = self.convert_table_to_icons()
        return f"""
        {icons_table[0][0]}---------{icons_table[0][1]}---------{icons_table[0][2]}
        |   {icons_table[1][0]}-----{icons_table[1][1]}-----{icons_table[1][2]}   |
        |   |     |     |   |
        |   |  {icons_table[2][0]}--{icons_table[2][1]}--{icons_table[2][2]}  |   |
        |   |  |     |  |   |
        {icons_table[3][0]}---{icons_table[3][1]}--{icons_table[3][2]}     {icons_table[4][0]}--{icons_table[4][1]}---{icons_table[4][2]}
        |   |  |     |  |   |
        |   |  {icons_table[5][0]}--{icons_table[5][1]}--{icons_table[5][2]}  |   |
        |   |     |     |   |
        |   {icons_table[6][0]}-----{icons_table[6][1]}-----{icons_table[6][2]}   |
        {icons_table[7][0]}---------{icons_table[7][1]}---------{icons_table[7][2]}
        """