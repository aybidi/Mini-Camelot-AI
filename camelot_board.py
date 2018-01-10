# -*- coding: utf-8 -*-
"""
Created on Fri Nov 3 16:00:20 2017

@author: Abdullah Mobeen
"""

class Camelot:
    """Camelot board game. The data structure of the board is inspired by a famous implementation
    of board games using the alphanumeric encoding for rows and columns. I did search over the
    internet to find effective board encoding and found this one to be heavily used."""
    
    def __init__(self, white = None, black = None):
        self.board = ['-' for i in range(0,112)]
        if white == None:
            self.white = ['C5','D5','E5','F5','D6','E6']
        else:
            self.white = white
        if black == None:
            self.black = ['C10','D10','E10','F10','D9','E9']
        else:
            self.black = black
        self.empty = ['A1','B1','C1','F1','G1','H1','A2','B2','G2','H2',
                      'A3','H3','A12','H12','A13','B13','G13','H13','A14',
                      'B14','C14','F14','G14','H14']
                      
    def board_print(self):
        for i in range(0,len(self.board)-1):
            self.board[i] = '-'
        for i in self.white:
            ind = decode(i)
            self.board[ind] = 'W'
        for i in self.black:
            ind = decode(i)
            self.board[ind] = 'B'
        for i in self.empty:
            ind = decode(i)
            self.board[ind] = ' '
        print()
        print("2D plane with (x,y) coordinates corresponding to the position of a piece\n\n")
        print("\tA\tB\tC\tD\tE\tF\tG\tH")
        row = 1
        string_board = ""
        for i in range(0,len(self.board)):
            if i%8 == 0:
                if i != 0:
                    string_board += '\t' + str(row) +'\n\n'
                    row += 1
                string_board += str(row)
            string_board += '\t' + self.board[i]            
        print(string_board + '\t' + str(row))
        print("\tA\tB\tC\tD\tE\tF\tG\tH")
            
def decode(coord):
    mapping = {'A':0,'B':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7}
    x,y = coord[0], coord[1:]
    num = mapping[x]
    ind = (int(y)-1)*8 + num
    return ind
    
def encode(coord):
    mapping = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H'}
    c = coord%8
    alph = mapping[c]
    num = int(coord//8) + 1
    alphanum = alph + str(num)
    return alphanum