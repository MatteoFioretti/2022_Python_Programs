#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Othello, or Reversi (https://en.wikipedia.org/wiki/Reversi), is a board game
played by two players, playing "disks" of different colors an 8x8 board.
Despite having relatively simple rules, Othello is a game of high strategic depth.
In this homework you will need to simulate a simplified version of othello,
called Dumbothello, in which '''# each player can capture the opponent's disks
# by playing a new disk on an adjacent empty cell.
'''The rules of Dumbothello are:

- each player has an associated color: white, black;

- the player with black is always the first to play;

- in turn, each player must place a disk of their color in such a way
  to capture one or more opponent's disks;

- capturing one or more opponent's disks means that the disk played by the
  player changes into the player's color all the directly adjacent opponent's disks,
  in any horizontal, vertical or diagonal direction;

- after playing one's own disk, the captured opponent's disks change
  their color, and become the same color as the player who just played;

- '''
  # if the player who has the turn cannot add any disk on the board,
  # the game ends. The player who has the higher number of disks on the board wins
  # or a tie occurs if the number of disks of the two players is equal;

#- the player who has the turn cannot add any disk if there is
 # no way to capture any opponent's disks with any move, or if there are no
  # more free cells on the board.

'''
Write a function dumbothello(filename) that reads the configuration of the
board from the text file indicated by the string "filename" and,
following the rules of Dumbothello, recursively generates the complete game tree
of the possible evolutions of the game, such that each leaf of the tree
is a configuration from which no more moves can be made.

The initial configuration of the chessboard in the file is stored line by
line in the file: letter "B" identifies a black disk, a "W" a white disk,
and the character "." an empty cell. The letters are separated by one or
more spacing characters.

'''
# The dumbothello function will return a triple (a, b, c), where:
# - a is the total number of evolutions ending in a black victory;
# - b is the total number of evolutions ending in a white victory;
# - c is the total number of evolutions ending in a tie.

'''
For example, given as input a text file containing the board:
. . W W
. . B B
W W B B
W B B W

The function will return the triple:
(2, 16, 0)

NOTICE: the dumbotello function or some other function used by it must be recursive.

'''



class Tree:
    def __init__(self, v):
        self.children = []
        self.value = v

    
    def AddChild(self, tree):
        self.children.append(tree)
        
    def isLeaf(self):
        if len(self.children) == 0:
            return True
        else:
            return False
    
    def __repr__(self, prefix=""):
        result = str(self.value) + "\n"
        prefix += "=|"
        for c in self.children:
            result += prefix + c.__repr__(prefix)
        return result
    
def mtx_to_ary(M):
    '''Given a 2D list it returns a 
       list containg the elements of the inner lists'''
    L = []
    for row in M:
        L.extend(row)
    return L
    

def win(matrix):
    '''Given a matrix containin n white disks 
        and n black disks, it returns the winner or tie'''
    counts = {"W": 0, "B": 0, ".": 0}
    for disk in [*matrix]:
        counts[disk] += 1

    if counts["W"] == counts["B"]:
        return "tie"
    
    return "white" if counts["W"] > counts["B"] else "black"

def mtx_gen(file):
    '''Given a file as an argument, it returns 
       a matrix containg the line of the file'''
    
    with open(file, "r", encoding = "utf8") as F:
        lines = F.readlines()
    return [line.split() for line in lines]

def chk_adj(M, row, column):
    L = []
    offsets = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))

    for r_offset, c_offset in offsets:
        new_row,new_column = row + r_offset, column+c_offset
        if (0 <= new_row < len(M)) and (0 <= new_column < len(M[0])):
            L.append((new_row, new_column))

    return L
   
def adj_dsk(M, L, disk):
    dsk_crd = set()
    for x,y in L[:]:
        if M[x][y] == disk:
            dsk_crd.add((x,y))
    return dsk_crd

def chk_dsk_pos(M, color):
    '''Given a table and a color as inputs, 
       it returns all the position of 
        the disks' of that given color'''
    return {(i, j) for i, row in enumerate(M) for j, val in enumerate(row) if val == color}
    

def possible_spot(M,L):
    
    valid_pos = {(x,y) for x,y in L[:] if M[x][y] == "."}
    return valid_pos
    
def valid__pos(table,color_B):
    d_pos = chk_dsk_pos(table, color_B)
    L = []
    for x,y in d_pos:
        L.extend(chk_adj(table,x,y))
    spots = possible_spot(table,L)
    return spots

def play(table, color_A, color_B):
    root = Tree(table)
    spots = valid__pos(table,color_B)
    if spots:
        for spot in spots:
            new_table = [el[:] for el in table]
            new_table[spot[0]][spot[1]] = color_A
            disks_to_color = adj_dsk(table, chk_adj(table, spot[0], spot[1]), color_B)
            for dx,dy in disks_to_color:
                new_table[dx][dy] = color_A
            new_node = play(new_table, color_B, color_A)
            root.AddChild(new_node)
    return root

def leaves(tree):
    if not tree.children:
        return [tree.value]
    else:
        leaves_list = []
        for child in tree.children:
            leaves_list.extend(leaves(child))
        return leaves_list

def dumbothello(filename : str) -> tuple[int,int,int]:
    table = mtx_gen(filename)
    table_tree = play(table,"B","W")
    leaves_1 = leaves(table_tree)
    t = [0,0,0]
    for leaf in leaves_1:
        point = win(mtx_to_ary(leaf))
        if point == "white":
                t[1] += 1
        if point == "black":
                t[0]+= 1
        if point == "tie":
                t[2] += 1
    return tuple(t)
    
    


    

         
if __name__ == "__main__":


    pass
      
