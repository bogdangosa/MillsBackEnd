import Constants.constants
from Constants import constants
from Services.Services import Services


class ConsoleUi:

    def __init__(self):
        self.services = Services(constants.PLAYER_VS_AI)
        self.start_menu()

    def print_options(self):
        game_state = self.services.get_game_state()
        if game_state == constants.GAME_HASNT_STARTED:
            print("1.Play against easy ai")
            print("2.Play against medium ai")
            print("3.Play against hard ai(minimax)")
            print("0.Exit")
        else:
            print(self.services.get_table())
            if game_state == constants.FILL_THE_TABLE:
                print("Add pawn to the table")
            elif game_state == constants.MOVE_PIECES:
                print("Move piece")
            elif game_state == constants.REMOVE_PIECES:
                print("Remove piece")
            elif game_state == constants.GAME_ENDED:
                print("The game has ended!")
                print("Press 1 to play again!")

    def put_pawn_on_the_board(self):
        print("Please select a position where you want to place your pawn:")
        print("Select the position:", end='')
        try:
            position = int(input()) - 1
            self.services.add_pawn_to_board(position)
        except ValueError as error:
            print(error)

    def remove_pawn_from_the_board(self):
        print("Please select a pawn that you want to remove:")
        print("Select the position:", end='')
        try:
            position = int(input()) - 1
            self.services.remove_pawn_from_board(position)
        except ValueError as error:
            print(error)

    def move_pawn(self):
        print("Please select a pawn that you want to move:")
        position = int(input()) - 1
        print("Please select the direction(r-right,l-left,b-bottom,t-top")
        direction = input()
        try:
            self.services.move_pawn(position,direction)
        except ValueError as error:
            print(error)

    def handle_command(self,command):
        game_state = self.services.get_game_state()
        if game_state == constants.GAME_HASNT_STARTED:
            if command == constants.COMMAND_END_PROGRAM:
                print("Bye!")
                return False
            elif command == 1:
                self.services.start_game(constants.RANDOM_AI)
            elif command == 2:
                self.services.start_game(constants.DUMB_AI)
            elif command == 3:
                self.services.start_game(constants.SMART_AI)
        if game_state == constants.FILL_THE_TABLE:
            self.put_pawn_on_the_board()
        if game_state == constants.REMOVE_PIECES:
            self.remove_pawn_from_the_board()
        if game_state == constants.MOVE_PIECES:
            self.move_pawn()

        if game_state == constants.GAME_ENDED:
            start_game = input()
        return True

    def start_menu(self):
        self.print_options()
        command = int(input())
        while self.handle_command(command):
            self.print_options()


if __name__ == "__main__":
    UI = ConsoleUi()
