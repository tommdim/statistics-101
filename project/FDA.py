import numpy as np
import matplotlib.pyplot as plt
from FDApy.representation.simulation import Brownian
from FDApy.visualization.plot import plot
import chess
import chess.pgn
import pandas as pd
import chess.engine
from stockfish import stockfish
from scipy.interpolate import make_interp_spline

#this method takes as input the board and the last move so to update the board and compute the evaluation
def get_evaluation(board,move):

    stockfish = Stockfish()     #if no parameter passed, takes as input the executable file called stockfish from the same directory, if found
    board.push_san(move)        #insert the move in the board
    stockfish.set_fen_position(board.fen())  #bpard.fen() applies a PGN to FEN conversion
    engine = chess.engine.SimpleEngine.popen_uci("stockfish")
    info = engine.analyse(board, chess.engine.Limit(time=0.1))     #gets the infos of the game
    
    #if the position on the board is not a mate the score is in centipawns, then it's divided by 100 to get the actual score
    #Gets the score from White’s point of view
    if chess.engine.PovScore.is_mate(info['score']):
        eval = chess.engine.PovScore.white(info['score'])
    else:
        eval = int(str(chess.engine.PovScore.white(info['score'])))/100

    return board, eval      #returns the board updated and the evaluation of the position

#create_dataFrame takes as input the name of the file pgn containing the game and returns a dataframe
def create_dataFrame(game_name): 

    #opens and reads the pgn file
    pgn = open(game_name) 
    game = chess.pgn.read_game(pgn)
    
                                   
    array = []      #initialize the array that will contain the data
    index_values = [] 
    i=0
    time_white = 0      #to keep track of the time for each player
    time_black = 0      #to keep track of the time for each player
    board = chess.Board()       #initialize the chessboard

    #iterate through the moves
    for node in game.mainline():        
        
        move = str(node.move)       #represents the last move
        board,evaluation = get_evaluation(board,move)       #the get_evaluation method returns the updated board and the evaluation of the current position

        if i%2 == 0:        #if the white is moving we update his time
            index_values.append("white")
            time_white = 600-node.clock()

        else:           #if the black is moving we update his time
            index_values.append("black") 
            time_black = 600-node.clock()

        #evaluation = get_evaluation(board,move)
        #we append an element in the array (a row in the dataframe) with move, time the player used, total time since the game started and evaluation of the position
        # if str(evaluation)[:2] == "#+":
        #     evaluation = 15
        # elif str(evaluation)[:2] == "#-":
        #     evaluation = -15
        array.append([str(node.move),round(600-node.clock(),4),round(time_white+time_black,4),evaluation])   
        i+=1
    
    column_values = ['move','time','real time','evaluation'] #create the columns names
    array = np.array(array)      #convert our array to a numpy array
    #create a dataframe
    df = pd.DataFrame(data = array, index = index_values, columns = column_values) 
    return df,board


df,board = create_dataFrame("games/08:14/partita1/valesepicacchi_vs_Sanjatosti_2022.08.14.pgn")   

eval = []
for x in range(len(df['evaluation'])):
    if type(df['evaluation'][x]) == float:
        eval.append(df['evaluation'][x])
    elif str(df['evaluation'][x])[1] =='+':
        # pick a good checkmate value
        eval.append(15.0)
    else:
        eval.append(-15.0)

t = np.array([x for x in range(len(df))])
# X_Y_Spline = make_interp_spline(df['real time'], eval)
# X_ = np.linspace(df['real time'].min(), df['real time'].max(), 5000)
# Y_ = X_Y_Spline(X_)
# plt.plot(X_, Y_)
plt.rcParams["figure.figsize"] = (13,6)
plt.grid()
plt.plot(df['real time'], eval)
#plt.plot(t, [0]*len(t), 'black')

plt.xlabel("Time (s)")
plt.ylabel("Position Evaluation")
plt.show()
df[["real time", "evaluation", "move"]].to_csv('file_name.csv')
# Smooth the data
data_smooth = df.noisy_data.smooth(points=0.5, neighborhood=14)

# Plot of the smoothing data
_ = plot(data_smooth)

# Plot individual curves
idx = 5
fig, ax = plt.subplots(1, 1)
ax.scatter(df.noisy_data.argvals['input_dim_0'],
           df.noisy_data.values[idx, :],
           alpha=0.5, label='Noisy')
ax.plot(df.data.argvals['input_dim_0'],
        df.data.values[idx, :],
        color='red', label='True')
ax.plot(data_smooth.argvals['input_dim_0'],
        data_smooth.values[idx, :],
        color='green', label='Smooth')
ax.set_xlabel('Sampling points')
ax.legend()