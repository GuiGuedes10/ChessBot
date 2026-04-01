import chess
import chess.svg
from flask import Flask, render_template, request, redirect, url_for
from IA_chess import IaChess

app = Flask(__name__)

board = chess.Board()

@app.route("/")
def index():
    last_move = board.peek() if board.move_stack else None
    tabuleiro_svg = chess.svg.board(
        board, 
        size=450, 
        lastmove=last_move,
        check=board.king(board.turn) if board.is_check() else None
    )
    
    return render_template(
        "index.html", 
        board_svg=tabuleiro_svg, 
        turn="Sua vez (Brancas)" if board.turn == chess.WHITE else "Inteligência Artificial (Pretas)",
        is_over=board.is_game_over(),
        result=board.result() if board.is_game_over() else ""
    )

@app.route("/jogar", methods=["POST"])
def jogar():
    move_uci = request.form.get("move").strip().lower()
    
    try:
        move = chess.Move.from_uci(move_uci)
        
        if move in board.legal_moves:
            board.push(move)

            if board.turn == chess.BLACK:
                computer_move = IaChess(board)
                board.push(computer_move)
        else:
            print("Movimento ilegal para esta posição.")
    except Exception:
        print("Formato de movimento inválido (use e2e4).")
        
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
    board.reset()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8080)