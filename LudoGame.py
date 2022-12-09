# Author: Maggie Wu
# GitHub username: wumag
# Date: 08/09/2022
# Description: A simplified version of Ludo board game.

class Player:
    """
    Represents the player who plays the game at a certain position
    """

    def __init__(self, player_position):
        """
        The constructor for Player class.
        Initializes the required data members.
        All data members are private.
        """
        self._player_position = player_position
        self._token_p_step_count = -1
        self._token_q_step_count = -1
        self._start_space = (ord(player_position) - ord('A')) * 14 + 1
        self._end_space = (self._start_space + 49) % 56
        self._completed = False

    def get_player_position(self):
        return self._player_position

    def get_completed(self):
        return self._completed

    def set_completed(self, value):
        self._completed = value

    def get_token_p_step_count(self):
        return self._token_p_step_count

    def set_token_p_step_count(self, value):
        self._token_p_step_count = value

    def get_token_q_step_count(self):
        return self._token_q_step_count

    def set_token_q_step_count(self, value):
        self._token_q_step_count = value

    def get_token_space(self, step_count):
        """
        Takes one parameter:
        step_count - represents the number of steps taken
        Purpose: Checks current token's space on the board
        Returns:
            space - if space is valid
        """
        assert step_count > 0
        if step_count == 57:
            space = 0
        elif step_count > 50:
            space = (step_count - 50) + 56 + (ord(self._player_position) - ord('A')) * 6
        else:
            space = step_count + self._start_space - 1
            if space > 56:
                space -= 56
        return space


class LudoGame:
    """
    Represents the game as played.
    """

    def __init__(self):
        """
        The constructor for LudoGame class. Takes no parameters.
        Initializes the required data members. All data members are private.
        """
        self._board = []
        self._players = []

    def create_board(self):
        """
        Takes no parameters.
        Purpose: Creates a board
        Returns: N/A
        """
        for space in range(81):
            self._board.append([])

    def create_players(self, players):
        """
        Takes one parameter:
        players - represents the players that are participating in the game
        Purpose: Creates a player
        Returns: N/A
        """
        for player_obj in players:
            self._players.append(Player(player_obj))

    def get_player_by_position(self, player_position):
        """
        Takes one parameter:
        player_position - represents the player’s position as a string
        Purpose: Checks player’s position on the board
        Returns:
            Player object - if string parameter is valid
            “Player not found!” - if string parameter is invalid
            the player object. For an invalid string parameter, it will return Player not found!
        """
        for player in self._players:
            if player_position == player.get_player_position():
                return player
        return "Player not found!"

    def print_board(self):
        """
        Takes no parameter.
        Purpose: Prints board game
        Returns: N/A
        """
        self.print_space(0)
        print()
        for space in range(1, 81):
            if self._board[space]:
                self.print_space(space)
            else:
                print(space, end='\t')
            if space in [14, 28, 42, 56, 62, 68, 74, 80]:
                print()
        print()

    def print_space(self, space):
        """
        Takes one parameter:
        space - represents a space on board
        Purpose: Prints a space
        Returns: N/A
        """
        print("[", end='')
        for i in range(len(self._board[space])):
            if i != (len(self._board[space]) - 1):
                print(self._board[space][i][0] + self._board[space][i][1], end='/')
            else:
                print(self._board[space][i][0] + self._board[space][i][1], end='')
        print("]", end='\t')

    def move_token(self, player, token_name, token_steps):
        """
        Takes three parameters:
        player - represents the player object
        token_name - represents token ‘p’ or ‘q’
        steps - represents the steps (integer) the token will move on the board
        Purpose: Directs one token moving on the board, update the token’s total steps, and addresses kicking out other opponent tokens as needed.
        Updates the token’s total steps.
        """
        if token_name == 'p':
            prev_step_count = player.get_token_p_step_count()
            if prev_step_count != 0:
                del self._board[player.get_token_space(prev_step_count)][0]
            if prev_step_count <= 50:
                new_step_count = prev_step_count + token_steps
                player.set_token_p_step_count(new_step_count)
                self.clear_space(player.get_player_position(), player.get_token_space(new_step_count))
                self._board[player.get_token_space(new_step_count)][0:0] = [(player.get_player_position(), 'p')]
            else:
                new_step_count = prev_step_count + token_steps
                if new_step_count > 57:
                    new_step_count = 57 - (new_step_count - 57)
                player.set_token_p_step_count(new_step_count)
                if new_step_count == 57:
                    self._board[0].append((player.get_player_position(), 'p'))
                else:
                    self._board[player.get_token_space(new_step_count)][0:0] = [(player.get_position(), 'p')]
        else:
            prev_step_count = player.get_token_q_step_count()
            if prev_step_count != 0:
                del self._board[player.get_token_space(prev_step_count)][-1]
            if prev_step_count <= 50:
                new_step_count = prev_step_count + token_steps
                player.set_token_q_step_count(new_step_count)
                self.clear_space(player.get_player_position(), player.get_token_space(new_step_count))
                self._board[player.get_token_space(new_step_count)].append((player.get_player_position(), 'q'))
            else:
                new_step_count = prev_step_count + token_steps
                if new_step_count > 57:
                    new_step_count = 57 - (new_step_count - 57)
                player.set_token_q_step_count(new_step_count)
                if new_step_count == 57:
                    self._board[0].append((player.get_player_position(), 'q'))
                else:
                    self._board[player.get_token_space(new_step_count)].append((player.get_player_position(), 'q'))

    def clear_space(self, position, space):
        """
        Takes two parameters:
        position - represents the player position on the board
        space - a space on the board
        Purpose: Clears the space
        Returns: N/A
        """
        if self._board[space]:
            for (player_obj, token) in self._board[space]:
                if player_obj == position:
                    return
                else:
                    self.restart_token(player_obj, token)
            self._board[space].clear()

    def restart_token(self, position, token_name):
        """
        Takes two parameters:
        position - represents the player position on the board
        token_name - a token (p/q) on the board
        Purpose: Resets token to home base
        Returns: N/A
        """
        player = self.get_player_by_position(position)
        if token_name == 'p':
            player.set_token_p_step_count(-1)
        else:
            player.set_token_q_step_count(-1)

    def opponent_occupied(self, player, space):
        """
        Takes two parameters:
        player - represents the player object
        space - a space on the board
        Purpose: Checks space for opponent token
        Returns:
            True - An opponent is present
            False - There is no opponent present
        """
        if self._board[space]:
            for (player_obj, token) in self._board[space]:
                if player_obj != player.get_player_position():
                    return True
            return False

    def play_game(self, players, turns):
        """
        Takes two parameters:
        players - represents the list of positions players choose
        turns - represents a list of tuples with each type a roll for one player
        Purpose: Creates the player list first using the players list pass in, and then move the tokens according to the turns list following the priority rule and update the tokens position and the player’s game state (whether finished the game or not).
        Returns:
            current_spaces_of_all_tokens - represents the space of tokens for each player with a list of strings of:
            H - if token is in home yard position
            R - if token is in ready to go position
            E - if token is in finished position
        """
        self.create_board()
        self.create_players(players)
        for (player_position, token_steps) in turns:
            self.print_board()
            print(player_position, token_steps)
            player = self.get_player_by_position(player_position)
            if player.get_completed():
                continue
            if player.get_token_p_step_count() == -1 and player.get_token_q_step_count() == -1:
                if token_steps == 6:
                    player.set_token_p_step_count(0)
                continue
            elif player.get_token_p_step_count() == -1:
                if token_steps == 6:
                    player.set_token_p_step_count(0)
                else:
                    self.move_token(player, 'q', token_steps)
                continue
            elif player.get_token_q_step_count() == -1:
                if token_steps == 6:
                    player.set_token_q_step_count(0)
                else:
                    self.move_token(player, 'p', token_steps)
                continue
            elif player.get_token_p_step_count() == 0 and player.get_token_q_step_count() == 0:
                self.move_token(player, 'p', token_steps)
                continue
            elif player.get_token_p_step_count() == player.get_token_q_step_count() and player.get_token_p_step_count() != 57:
                self.move_token(player, 'p', token_steps)
                self.move_token(player, 'q', token_steps)
                if player.get_token_p_step_count() == 57:
                    player.set_completed(True)
                    print(player_position + " has finished the game!")
                continue
            elif player.get_token_p_step_count() == player.get_token_q_step_count() and player.get_token_p_step_count() == 57:
                player.set_completed(True)
                print(player_position + " has finished the game!")
                continue
            elif player.get_token_p_step_count() == 57:
                self.move_token(player, 'q', token_steps)
                if player.get_token_q_step_count() == 57:
                    player.set_completed(True)
                    print(player_position + " has finished the game!")
                continue
            elif player.get_token_q_step_count() == 57:
                self.move_token(player, 'p', token_steps)
                if player.get_token_p_step_count() == 57:
                    player.set_completed(True)
                    print(player_position + " has finished the game!")
                continue
            else:
                new_p_steps = player.get_token_p_step_count() + token_steps
                new_q_steps = player.get_token_q_step_count() + token_steps
                if new_p_steps == 57:
                    self.move_token(player, 'p', token_steps)
                elif new_q_steps == 57:
                    self.move_token(player, 'q', token_steps)
                elif new_p_steps <= 50 and self.opponent_occupied(player, player.get_token_space(new_p_steps)):
                    self.move_token(player, 'p', token_steps)
                elif new_q_steps <= 50 and self.opponent_occupied(player, player.get_token_space(new_q_steps)):
                    self.move_token(player, 'q', token_steps)
                elif new_p_steps <= new_q_steps:
                    self.move_token(player, 'p', token_steps)
                else:
                    self.move_token(player, 'q', token_steps)
                continue
        self.print_board()


# def main():
#     players = ['A', 'B']
#     turns = [('A', 6), ('A', 4), ('A', 5), ('A', 4), ('B', 6), ('B', 4), ('B', 1), ('B', 2), ('A', 6), ('A', 4),
#              ('A', 6), ('A', 3), ('A', 5), ('A', 1), ('A', 5), ('A', 4)]
#     game = LudoGame()
#     current_tokens_space = game.play_game(players, turns)
#     player_A = game.get_player_by_position('A')
#     player_B = game.get_player_by_position('B')
#
#
# if __name__ == "__main__":
#     main()
