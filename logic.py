def executeMove(move, gameState, player):
    
    if move in legalMoves:
        
        gameState.hands[player].discard(move.type)
        if move.type == 'Guard':
            if gameState.hands[move.target][0] == move.guess:
                gameState.playerStatus[move.target] = 'out'
                gameState.hands[move.target].discard()
        elif move.type == 'Priest':
            
        elif move.type == 'Baron':
            if gameState.hands[player][0] > gameState.hands[move.target][0]:
                gameState.playerStatus[move.target] = 'out'
                gameState.hands[move.target].discard()
            elif gameState.hands[player][0] < gameState.hands[move.target][0]:
                gameState.playerStatus[player] = 'out'
                gameState.hands[player].discard()
            else:
                pass
        elif move.type == 'Handmaiden':
            gameState.playerStatus.current = 'protected'
        elif move.type == 'Prince':
            if gameState.hands[move.target][0] == 'Princess'
                gameState.hands[move.target].discard()
                gameState.playerStatus[move.target] = 'out'
            else:
                gameState.hands[move.target].discard()
                gameState.hands[player].drawCard()
        elif move.type == 'King':
            temp = gameState.hands[player][0]
            gameState.hands[player][0] = gameState.hands[move.target][0]
            gameState.hands[move.target][0] = temp
        elif move.type == 'Countess':
            pass
        elif move.type == 'Princess':
            gameState.playerStatus.current = 'out'

