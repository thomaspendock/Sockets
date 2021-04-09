from Games import GameInterface
from random import sample


from Frontend.TerminalGraphics.macColors import *
from Frontend.TerminalGraphics.grafix import border

# Private helper
def _get_player_tokens(players):
    possible = set('XO')
    player_to_token = dict()
    token = sample(possible, len(players))
    return dict(zip(players, token))

class TicTacToe(GameInterface.Game):
    def __init__(self, players, height, width, to_win):
        super().__init__(players)
        
        #height = int(args[0]); width = int(args[1]); to_win = int(args[2])
        height = int(height); width = int(width); to_win = int(to_win)
        
        self.blank   = ' '
        self.players = _get_player_tokens(players)
        self.height  = height
        self.width   = width
        self.board   = [[self.blank for j in range(width)] for i in range(height)]
        self.to_win  = to_win
        self.turn    = None
        
    #@Override
    def move(self, player, row, col):
        '''
        A players move.
        returns True if the move successful.
        returns False if the move is invalid.
        '''
        row = int(row)
        col = int(col)
        # Check valid player
        if player not in self.players:
            raise GameInterface.GameError('Unkown player.')

        # Check in bound
        if not (-1 < row < self.height) or not (-1 < col < self.width):
            raise GameInterface.GameError('Out of bounds.')

        # Position already taken
        if self.board[row][col] != self.blank:
            raise GameInterface.GameError('Position already taken.')

        # Not players turn
        if player != self.turn:
            raise GameInterface.GameError('Not your turn.')

        # Place the token on the board
        self.board[row][col] = self.players[player]

        # Set turn to other player
        for k in self.players:
            if k != player:
                self.turn = k
                break
        
        return True

    def _check_player_win_diag(self, player):
        rows = list(range(self.height - 1, -1, -1)) + [0]*(self.width - 1)
        cols = [0]*self.width + list(range(1, self.height))
        for mirror in [0, 1]:
            for start_row, start_col in zip(rows, cols):
                row, col = start_row, start_col
                running = 0
                while row < self.height and col < self.width:
                    
                    # Flip the board by reversing column
                    mirror_col = self.height - 1 - col if mirror else col

                    # Check match and udpate running streak of matched tokens
                    match = self.board[row][mirror_col] == self.players[player]
                    running = (running + match) * match
                    if running >= self.to_win:
                        return player
                    row += 1
                    col += 1

        
    def _check_player_win(self, player):
        '''Checks if player has won the game'''
        '''
        # Check to win
        search_start = (0, 0) # Start any search in the top left of the borad
        dirs = [((0, 1), (1, 0)), # Left to right horizontal, sweep down
                ((1, 0), (0, 1)), # Top to bot, sweep left to right
                ((1, 1), (0, 1)), # Diag top to bot
                ((1, 1), (1, 0))] # Diag left to right
        '''

        # Horz
        for row in range(self.height):
            running = 0
            for col in range(self.width):
                match = self.board[row][col] == self.players[player]
                running = (running + match) * match
                if running >= self.to_win:
                    return True

        # Ver
        for col in range(self.width):
            running = 0
            for row in range(self.height):
                # yoink
                match = self.board[row][col] == self.players[player]
                running = (running + match) * match
                if running >= self.to_win:
                    return True
                # yoink
    
        # diag
        if self._check_player_win_diag(player):
            return True
        
        # Check the sum filter for each player
        #horz = zip([0]*self.width, range(0, self.width))
        #vert = zip(range(0, self.height), [0]*self.height)
        #tmatch = lambda r, c: self.board[r][c] == self.players[player]
        #horz = any([sum( tmatch(r + dr, c + dc) for r,c in horz ) >= self.to_win for dr, dc in vert])
        #vert = any([sum( tmatch(r + dr, c + dc) for r,c in vert ) >= self.to_win for dr, dc in horz])
        #return horz or vert
        
        
    #@Override
    def winner(self):
        '''
        Returns the player whos won the game, if any.
        If no player has won yet, returns None
        '''

        for player in self.players:
            if self._check_player_win(player):
                return player
        
        return None

    def get_turn(self):
        '''
        Returns the ip of the player whos current turn it is.
        '''
        return self.turn

    def set_turn(self, player):
        '''
        Sets the current turn of a player.
        '''
        self.turn = player

    def __str__(self):
        sep = bg(' ', index=240)

        raw_col = ' ' * 2
        raw_row = ' ' * ((2 * len(raw_col) + 1) * self.width + 2)
        row_sep = bg(raw_row, index=240)
        
        col_sep = bg(raw_col, index=241)
        s = ''
        s += row_sep + '\n'
        s += ('\n' + row_sep + '\n').join([col_sep + ' ' + (' ' + col_sep + ' ').join(row) + ' ' + col_sep for row in self.board])
        s += '\n' + row_sep
        s, _ = border(s, 0, 0, len(raw_row), index=245)
        return s


        
