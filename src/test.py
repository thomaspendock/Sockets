from Games import TicTacToeClass


        
if __name__ == '__main__':
    game = TicTacToeClass.TicTacToe(['p1', 'p2'], 5, 5, 4)
    game.turn = 'p1'

    p1_moves = [(0, 0), (1, 1), (2, 2), (3, 3)]
    p2_moves = [(0, 1), (1, 2), (2, 1), (3, 1)]

    for m1, m2 in zip(p1_moves, p2_moves):
        
        game.move('p1', *m1)
        print(game)
        if game.winner() == 'p1':
            print('p1 winner')
            break
        game.move('p2', *m2)
        print(game)
        if game.winner() == 'p2':
            print('p2 winner')
            break
