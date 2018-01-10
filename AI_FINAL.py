# -*- coding: utf-8 -*-
"""
Created on Fri Nov  10 11:09:33 2017

@author: Abdullah Mobeen
"""

import time
import math
import camelot_board
from camelot_board import decode,encode


def capture(board,player,possible_moves, pos, loc, i):
    """Function that gathers all the capturing moves possible for all the pieces on the board. 
        Capture is when you kill an enemy piece by jumping over it. The function takes in as arguments: 
            board ~ the camelot game board as a single array
            player ~ human (1) or computer (-1)
            possible_moves ~ an array containing all the possible moves for any piece on the board
        It returns a boolean value corresponding to whether there was a capture or not"""
              
    if player == 1 and encode(loc+i) in board.black:
        next_piece = encode(loc+i) 
        new_pos = int(loc + (i*2)) 
        if not((pos[0] == 'B') and ((next_piece)[0] == 'A')) and not((pos[0] == 'G') and ((next_piece)[0] == 'H')):
            new_enc = encode(new_pos)
            if new_pos in range(0,112) and (new_enc not in board.white) and (new_enc not in board.black) and (new_enc not in board.empty):
                possible_moves.append([pos,new_enc,next_piece])
                return True
                
    if player == -1 and encode(loc+i) in board.white:   
        next_piece = encode(loc+i) 
        new_pos = int(loc + (i*2))
        if not((pos[0] == 'B') and ((next_piece)[0] == 'A')) and not((pos[0] == 'G') and ((next_piece)[0] == 'H')):
            new_enc = encode(new_pos)
            if new_pos in range(0,112) and (new_enc not in board.white) and (new_enc not in board.black) and (new_enc not in board.empty):
                possible_moves.append([pos,new_enc,next_piece])
                return True
                
    return False

def canter(board,player,possible_moves, pos, loc, i):
    """Function that gathers all the cantering moves possible. Canter move is when a player jumps over
        its own piece and lands ahead. This function takes in as arguments:
            board ~ the camelot game board as a single array
            player ~ human (1) or computer (-1)
            possible_moves ~ an array containing all the possible moves for any piece on the board"""
    
    next_piece = encode(loc+i)    
    new_pos = loc + (i*2)
    
    if player == 1  and next_piece in board.white:
        if not((pos[0] == 'B') and ((next_piece)[0] == 'A')) and not((pos[0] == 'G') and ((next_piece)[0] == 'H')):
            new_enc = encode(new_pos)
            if new_pos in range(0,112) and (new_enc not in board.white) and (new_enc not in board.black) and (new_enc not in board.empty):
                possible_moves.append([pos,new_enc])
    if player == -1  and next_piece in board.black:
        if not((pos[0] == 'B') and ((next_piece)[0] == 'A')) and not((pos[0] == 'G') and ((next_piece)[0] == 'H')):
            new_enc = encode(new_pos)
            if new_pos in range(0,112) and (new_enc not in board.white) and (new_enc not in board.black) and (new_enc not in board.empty):
                possible_moves.append([pos,new_enc])
                
def plain(board,player,possible_moves, pos, loc, i):
    """Function that gathers all the plain moves possible for a piece. Plain move is a single move:
        horizontal, vertical, or diagonal in an empty box. This function takes in as arguments:
            board ~ the camelot game board as a single array
            player ~ human (1) or computer (-1)
            possible_moves ~ the possible moves for any piece on the board"""
    
    new_position = encode(loc+i)       
    if (encode(loc+i) not in board.black) and (encode(loc+i) not in board.white) and (encode(loc+i) not in board.empty) and ((loc+i) in range(0,112)):
        possible_moves.append([pos,new_position])

                
def legal_moves(board,player=None):
    """Function that implements the search for all the moves possible for all the pieces of a particular
        player. It takes in as arguments:
            board ~ the camelot game board as a single array
            player ~ human (1) or computer (-1)
        This function returns the array of all the possible moves at one state. It also ensures that
        if a capture move is possible, it must be taken by the player"""
        
    possible_moves = []
    moves = []
    if player == None:
        moves += board.white + board.black
    elif player == -1:
        moves += board.black
    elif player == 1:
        moves += board.white
    
    captured = False
    for pos in moves:
        if pos[0] == 'A':
            m = [-8,-7,1,8,9]
        elif pos[0] == 'H':
            m = [-9,-8,-1,7,8]
        else:
            m = [-9,-8,-7,-1,1,7,8,9]
        loc = decode(pos)
        for i in m:
            captured = capture(board, player, possible_moves, pos, loc, i)
            canter(board, player, possible_moves, pos, loc, i)
            plain(board, player, possible_moves, pos, loc, i)
    
    if captured:
        enemy_list = []
        for capturing_move in possible_moves:
            if len(capturing_move) == 3:
                enemy_list.append(capturing_move)
        possible_moves = list(enemy_list)

    return possible_moves
    
def execution(move,legal,board,player):
    """This function executes the move input by human player (capture, canter, or plain).
        It takes in as argument:
        move ~ the move specified by the human player
        legal ~ the list of all legal moves
        board ~ game board
        player ~ number assigned to human player - 1 or -1"""
        
    if player == 1:
        if move in legal:
            for i in range(0,len(board.white)):
                if board.white[i] == move[0]:
                    board.white[i] = move[1]
            if len(move) == 3:
                board.black.remove(move[-1])

        else:
            print("Illegal move, please input a legal move")
            human_move(board,player)
    else:
        if move in legal:
            if len(move) == 3:
                board.white.remove(move[-1])
            for i in range(0,len(board.black)):
                if board.black[i] == move[0]:
                    board.black[i] = move[1]
        else:
            print("Illegal move, please input a legal move")
            human_move(board,player)
            
def com_execution(board,move,player):
    """This fuction executes the move of the computer. It takes in as arguments:
        board ~ the game board
        move ~ the move decided by the minimax algorithm with alpha-beta pruning
        player ~ the number assigned to computer -> 1 or -1"""
        
    if player == -1:
        if move in legal_moves(board,player):
            for i in range(0,len(board.black)):
                if board.black[i] == move[0]:
                    board.black[i] = move[1]
            if len(move) == 3:           
                board.white.remove(move[2])
    else:
        if move in legal_moves(board,player):
            for i in range(0,len(board.white)):
                if board.white[i] == move[0]:
                    board.white[i] = move[1]
            if len(move) == 3:           
                board.black.remove(move[2])        
        
def human_move(board,player):
    """Function that allows the user to specify the move by taking the input from the user.
        It then makes a list of the positions in the command by splitting it over  the dash 
        sign. It then calls the above function, execution() to implement the lmove specified by
        the user, if legal"""
        
    s = input("Please input a legal move in a format of  \"current_position-landing_position\", if the move is cantering or plain. In case of a capturing move, follow \"current_position-landing_position-enemy piece\": ")
    move = s.split('-')
    legal = legal_moves(board,player)
    execution(move,legal,board,player)
    

def computer_move(board,move,player):
    """This function implements the move specified by the computer"""
    com_execution(board, move, player)
  
def result(board, legal_moves, max_util, min_util, depth,flag,player,transition_model):
    """This function is the RESULT function in Artificial Intelligence textbook. 
        It creates the Transition Model of a current state by assigning a cost
        to each move. It takes in as arguments:
            board ~ the game board
            legal_moves ~ the list of all the legal moves at a given state
            max_util ~ the lower bound for the Max player
            min_util ~ the upper bound for the Min player
            depth ~ the depth of the game search"""
            
    global max_depth
    global nodes_generated
    global min_prunes
    global max_prunes
    global depth_limit
    global start_time
    
    flag = None
    if player == -1:
        for j in range(0,len(legal_moves)):
            move = legal_moves[j]
            new_board = camelot_board.Camelot(list(board.white), list(board.black))
            for i in range(0,len(new_board.black)):
                if new_board.black[i] == move[0]:
                    new_board.black[i] = move[1]
            if len(move) == 3:
                flag = move      
                new_board.white.remove(move[2])
            v = max_value(new_board,max_util,min_util,depth+1)
            transition_model[j] = v
    else:
        for j in range(0,len(legal_moves)):
            move = legal_moves[j]
            new_board = camelot_board.Camelot(list(board.white), list(board.black))
            for i in range(0,len(new_board.white)):
                if new_board.white[i] == move[0]:
                    new_board.white[i] = move[1]
            if len(move) == 3:
                flag = move         
                new_board.black.remove(move[2])
            v = min_value(new_board,max_util,min_util,depth+1)
            transition_model[j] = v       

    return flag
    
def alpha_beta_prune(board,player,depth):
    """Alpha-Beta pruning on MiniMax Algorithm. Recursively implements the pruning during 
    the max_value function and min_value function. Once the depth limit has been reached under time,
    it implements depth-limited search with the depth limit incremented by 1"""
    
    global max_depth
    global depth_limit
    global nodes_generated
    global max_prune
    global min_prune
    global start_time
    
    moves_and_val = {}
    start_time = float(time.time())
    
    nodes_generated += 1
    
    flag = None        
    max_util = -1000
    min_util = 1000
    
    all_moves = legal_moves(board,player)
    flag = result(board, all_moves, max_util, min_util, depth,flag,player,moves_and_val)
    
    if player == -1:
        optimal = min(moves_and_val)
    if player == 1:
        optimal = max(moves_and_val)
        
    finish_time = float(time.time())
    if (finish_time - start_time) < 5 and max_depth == depth_limit:
        depth_limit += 1
        print("Now performing Depth-Limited Search with incremented depth_limit")
        return alpha_beta_prune(board,player,0)
    else:
        if flag == None:
            return all_moves[optimal]
        else:
            return flag

def action(new_board, move, player):
    """Implements the ACTION function in Artificial Intelligence textbook. This function
    expands the game search by creating a copy of the game board for each legal move in
    a player's domain. The board it creates are passed into the minimax algorithm to determine
    the utility of legal moves"""
    
    global nodes_generated 
    global min_prune
    global max_prune
    global max_depth
    
    if player == 1:
        for i in range(0,len(new_board.white)):
            if new_board.white[i] == move[0]:
                new_board.white[i] = move[1]
        if len(move) == 3:
            new_board.black.remove(move[2])
    elif player == -1:
        for i in range(0,len(new_board.black)):
            if new_board.black[i] == move[0]:
                new_board.black[i] = move[1]
        if len(move) == 3:
            new_board.white.remove(move[2])
    return new_board

def max_value(board, max_util, min_util, depth):
    """Maxvalue function of the minmax algorithm. Determines the best move for the MAX
    player and reassigns the value of alpha (lower bound) to a greater value. Implements
    pruning once the alpha (max_util) becomes greater than beta (min_util). 
    Takes in as arguments:
        board ~ the game board
        max_util ~ the lower bound or alpha
        min_util ~ the upper bound or beta
        depth ~ depth of the game tree explored
    Returns the value v picked by the MAX player"""
    
    global nodes_generated 
    global min_prune
    global max_prune
    global max_depth
    
    nodes_generated += 1
    max_depth = max(max_depth,depth)
    
    if cutoff_search(board, depth):
        return evaluation(board)
    v = -1000
    moves = legal_moves(board,1)
    for move in moves:
        temp_board = camelot_board.Camelot(list(board.white),list(board.black))
        state = action(temp_board, move, 1)
        v = max(v, min_value(state, max_util, min_util, depth + 1))
        if v >= min_util:
            max_prune += 1
            return v
        max_util = max(max_util, v)
    return v

def min_value(board, max_util, min_util,depth):
    """Minvalue function of the minmax algorithm. Determines the best move for the MIN
    player and reassigns the value of beta (upper bound) to a lower value. Implements
    pruning once the beta (min_util) becomes less than alpha (max_util). 
    Takes in as arguments:
        board ~ the game board
        max_util ~ the lower bound or alpha
        min_util ~ the upper bound or beta
        depth ~ depth of the game tree explored
    Returns the value v picked by the MIN player"""
    
    global nodes_generated 
    global min_prune
    global max_prune
    global max_depth
    
    nodes_generated += 1
    max_depth = max(max_depth,depth)
    
    if cutoff_search(board, depth):
        return evaluation(board)
    v = 1000
    moves = legal_moves(board,-1)
    for move in moves:
        temp_board = camelot_board.Camelot(list(board.white),list(board.black))
        state = action(temp_board, move, -1)
        v = min(v, max_value(state, max_util, min_util, depth + 1))
        if v <= max_util:
            min_prune += 1
            return v
        min_util = min(min_util, v)
    return v
    

def cutoff_search(board, depth):
    """The function replacing the terminal-test. 
    Implemets the cutoff on game search once:
        1) the time exceeds 10 seconds during the search
        2) the white player has 2 pieces in black player's castle
        3) the black player has 2 pieces in white player's castle
        4) either of the player has all the pieces eliminated
        5) once the depth exceeds the depth limit for the Depth Limited Search in IDS"""
        
    global start_time
    global depth_limit
    global winner_white
    global winner_black
    
    test = False
    current_time = float(time.time())
    if depth != 0 and (current_time - start_time) >= 10.0:
        test = True
     
    b_castle = 0
    w_castle = 0
    
    for i in winner_white:
        if i in board.white:
            w_castle += 1
            if w_castle == 2:
                test = True
    for i in winner_black:
        if i in board.black:
            b_castle += 1
            if b_castle == 2:
                test = True
    if (len(board.white) == 0) or (len(board.black) == 0):
        test = True
    
    if depth >= depth_limit:
        test = True
        
    return test
    
def white_win(board):
    """Function that checks if team white has won"""
    
    global w_castle
    global winner_white
    
    for i in winner_white:
        if i in board.white:
            w_castle += 1
            board.white.remove(i)
            if w_castle == 2:
                board.board_print()
                print("Game Over - White has won!")
                return True
    if len(board.black) == 0:
        print("Game Over - White has won!")
        return True
    return False

def black_win(board):
    """Function that checks if team black has won"""
    
    global b_castle
    global winner_black
    
    for i in winner_black:
        if i in board.black:
            b_castle += 1
            board.black.remove(i)
            if b_castle == 2:
                board.board_print()
                print("Game Over - Black has won!")
                return True
    if len(board.white) == 0:
        print("Game Over - Black has won!")
        return True
    return False        

def evaluation(board):
    """This is the evaluation function that gets applied once the game search is 
        cutoff. The evaluation function that I have designd is based on the non_linear
        sigmoid function, which assigns weights to the features. It gives more side losing to make things more interesting."""
        
    global winner_white
    global winner_black
    
    white_distance = 13
    black_distance = 13

    for position in board.white:
        row_num = int(decode(position)/8)
        if position in winner_white:
            return 1000
        white_distance = min(white_distance, 13 - row_num)

    for position in board.black:
        row_num = int(decode(position)/8)
        if position in winner_black:
            return -1000
        black_distance = min(black_distance,row_num)
        
    w_pieces = len(board.white)
    b_pieces = len(board.black)
    w_odd = math.exp(w_pieces - b_pieces)
    b_odd = math.exp(b_pieces - w_pieces)
    w_dodd = math.exp(white_distance - black_distance)
    b_dodd = math.exp(black_distance - white_distance)
    
    eval = 1000 * (((b_odd/(1+b_odd))* (w_pieces - b_pieces)/5)
            + ((w_odd/(1+w_odd)) * (b_pieces - w_pieces)/5)
            + ((b_dodd)/(1+b_dodd) * (1/white_distance))
            + ((w_dodd)/(1+w_dodd) * (-1/black_distance))) 


    return eval
    

if __name__ == "__main__":
    c = camelot_board.Camelot()
    c.board_print()
    diff = {"easy":4, "medium":6, "hard":8}
    
    difficulty = str(input("Please select the difficulty level: easy, medium, hard: "))
    
    if difficulty == "easy":
        print("Your selection is: ", difficulty)
        depth_l = diff["easy"]
        
    elif difficulty == "medium":
        print("Your selection is: ", difficulty)
        depth_l = diff["medium"]
        
    elif difficulty == "hard":
        print("Your selection is: ", difficulty)        
        depth_l = diff["hard"]
    
    else:
        print("Invalid option. Default difficulty medium has been set ")
        depth_l = diff["medium"]
    
    
    player = input("Would you like to to be White (W) or Black (B)?\n==> ")
    if player == 'W':
        player_num = 1
    elif player == 'B':
        player_num = -1
    else:
        print("Thats not a valid selection. Let the computer go first as White ")
        player_num = -1
        
    
    winner_white = ['D14','E14']
    winner_black = ['D1','E1']
    
    b_castle = 0
    w_castle = 0
    
    while True:
        max_depth = 0
        nodes_generated = 0
        max_prune = 0
        min_prune = 0
        start_time = 0
        depth_limit = depth_l
    
        
        if player_num == 1:
            human_move(c,player_num)
            c.board_print()
            if (black_win(c) or white_win(c)) != False:
                break
            computer_move(c,alpha_beta_prune(c,-player_num,0),-player_num)
            print("Maximum Depth Reached ~ ", max_depth)
            print("Total Nodes Generated ~ ", nodes_generated)
            print("Prunes in Max Value ~ ", max_prune)
            print("Prunes in Min Value ~ ", min_prune)
            print("No. of black pieces in white's castle: ", b_castle)
            print("No. of white pieces in black's castle: ", w_castle)
            c.board_print()
            if (black_win(c) or white_win(c)) != False: 
                break
        else:
            computer_move(c,alpha_beta_prune(c,-player_num,0),-player_num)
            print("Maximum Depth Reached ~ ", max_depth)
            print("Total Nodes Generated ~ ", nodes_generated)
            print("Prunes in Max Value ~ ", max_prune)
            print("Prunes in Min Value ~ ", min_prune)
            print("No. of black pieces in white's castle: ", b_castle)
            print("No. of white pieces in black's castle: ", w_castle)
            c.board_print()
            if (black_win(c) or white_win(c)) != False:
                break
            human_move(c,player_num)
            c.board_print()
            if (black_win(c) or white_win(c)) != False:
                break
    
