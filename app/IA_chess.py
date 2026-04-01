import chess

def calcular_material(board):
    valores = {
        chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30,
        chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 900
    }
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            valor = valores[piece.piece_type]
            
            rank = chess.square_rank(square)
            if piece.color == chess.WHITE:
                score += (valor + rank)
            else:
                score -= (valor + (7 - rank))
    return score

def minimax(board, profundidade, alpha, beta, maximizando):
    if profundidade == 0 or board.is_game_over():
        return calcular_material(board)

    if maximizando: 
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, profundidade - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha: break 
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, profundidade - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha: break 
        return min_eval

def IaChess(board, profundidade=4):
    melhor_move = None
    melhor_valor = float('inf') 
    
    for move in board.legal_moves:
        board.push(move)
        valor_jogada = minimax(board, profundidade - 1, -float('inf'), float('inf'), True)
        board.pop()
        
        if valor_jogada < melhor_valor:
            melhor_valor = valor_jogada
            melhor_move = move
            
    return melhor_move