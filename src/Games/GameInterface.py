# The base game class
# A game that extends Game
# must be located in the Games folder,
# must be called <game name>Class.py
# must have a class/object call <game name> that extends Game

import json


class GameError(Exception):
    def __init__(self, message):
        super().__init__(message); self.message = message


class Game():
    def __init__(self, players):
        '''
        List of player id's as a string object.
        Any addition args will be sent in as a string.
        '''
        pass
        

    def move(self, player):
        '''
        A players (string id) move.
        returns True if the move successful.
        returns False if the move is invalid.
        '''
        return False

    def winner(self):
        '''
        Returns the player whos won the game, if any.
        If no player has won yet, returns None
        '''
        return None

    def get_turn(self):
        '''
        Returns the ip of the player whos current turn it is.
        '''
        return None

    def set_turn(self, player):
        '''
        Sets the current turn of a player.
        '''
        pass

    def __str__(self):
        '''Display the board for the terminal screen'''
        return 'Not implemented'

    
        
