import json
import os


from .bot_pipe import BotPipe
from .serializer import Serializer
from ..game_logic.game import Game
from ..game_logic.actions import *

valid_moves = ['S', 'T', 'W', 's', 'w', 't']

class Log:
    def __init__(self, folder='logs') -> None:
        self.log_file_name = 'game_log.txt'
        self.log_folder = os.path.join(os.getcwd(), folder)

        # Create the folder if it doesn't exist
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        # Check if the file already exists and rename if needed
        log_path = os.path.join(self.log_folder, self.log_file_name)
        if os.path.exists(log_path):
            base_name, ext = os.path.splitext(self.log_file_name)
            i = 1
            while os.path.exists(log_path):
                self.log_file_name = f"{base_name}_{i}{ext}"
                log_path = os.path.join(self.log_folder, self.log_file_name)
                i += 1

        self.log_file = None

    def open(self) -> None:
        log_path = os.path.join(self.log_folder, self.log_file_name)
        self.log_file = open(log_path, 'a')

    def close(self) -> None:
        if self.log_file is not None:
            self.log_file.close()
            self.log_file = None

    def update(self, message: str) -> None:
        try:
            if self.log_file is not None:
                self.log_file.write(message + '\n')
                self.log_file.flush()
            else:
                raise ValueError('Log is not open. Please open the log before updating.')
        except ValueError as e:
            print(e)
class GameController:

    def __init__(self, bot_left: str, bot_right: str) -> None:
        self.bot_left = BotPipe(bot_left)
        self.bot_right = BotPipe(bot_right)

        self.game = Game()
        self.log = Log()

    def run(self) -> None:
        game_over = False
        self.log.open()

        while not game_over:
            game_dataJson = json.dumps(Serializer.get(self.game))
            response_left = self.bot_left.request(method='POST', data= game_dataJson)
            response_right = self.bot_right.request(method='POST',data= game_dataJson)

            self.log.update(response_left + ' | ' + response_right)

            left_action = self.command_to_action(response_left,'left')
            right_action = self.command_to_action(response_right, 'right')

            game_status = self.game.update(left_action, right_action)
            game_over = self.is_game_over(game_status)

        self.log.close()

    def is_game_over(self, game_status: tuple[str, str]) -> bool:
        if game_status[0] in ['Left win', 'Right win', 'Tie']:
            return True
        else:
            return False

    def command_to_action(self, move: str, side: str):
        if side not in ['left', 'right']:
            raise ValueError("Invalid side, please use 'left' or 'right'.")

        move = move.upper()

        if move == 'W':
            return Wait(side)
        elif move[0] == 'S':
            move = move.split(' ')
            soldier_type = 'swordsman'
            return SpawnSoldier(side, soldier_type)
        elif move[0] == 'T':
            move = move.split(' ')
            x = int(move[1])
            y = int(move[2])
            return BuildTurret(side, x, y)
        else:
            print("Wrong command")
            return Wait(side)


# Dev test
if __name__ == '__main__':
    game = GameController('./bots/random_bot.py','./bots/spawn_only_bot.py')
    game.run()


