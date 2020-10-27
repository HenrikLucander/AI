#!/usr/bin/python3

# Both the Minimax and the Alpha-beta algorithm represent the players
# as integers 0 and 1. The moves by the two players alternate 0, 1, 0, 1, ...,
# so in the recursive calls you can compute the next player as the subtraction
# 1-player.
# The number of recursive calls to the algorithms is kept track with
# the variable 'calls'. Let your implementation increase this variable
# by one in the beginning of each recursive call. This variable is
# also used as part of the evaluation of the implementations.

calls = 0

def minimax(player,state,depthLeft):
  global calls
  calls += 1
  if depthLeft == 0 or state.applicableActions(player) == []:
    return state.value()
### INSERT YOUR IMPLEMENTATION OF MINIMAX HERE
### It should be recursively calling 'minimax'.
  player2 = 1-player
  if player == 0:
    bestVal = 1000
  else:
    bestVal = -1000

  for cell in state.applicableActions(player):
    #tähän merkin LAITTO, koska value riviä edemmäs ei enää mennä kun depthLeft => 0
    state2 = state.successor(player,cell)
    value = minimax(player2,state2,depthLeft-1)
    #state.show()
    #print(value)
    #tähän merkin POISTO, koska value riviä edemmäs ei enää mennä kun depthLeft => 0
    #state.cells[cell] = -1
    #state.successor(-1,cell)

    if player == 0:
      if value < bestVal:
        bestVal = value
    else:
      if value > bestVal:
        bestVal = value
 
  return bestVal


  #else:
    #best = [-1, -1, float("inf")]
    #bestVal = float("inf")
    #bestVal = 99999
   #for cell in state.applicableActions(player):
     # state.cells[cell]=player
      #state.successor(player,cell)
     # value = minimax(player,state,depthLeft-1)
      #bestVal = min(bestVal,value)
     # print(bestVal)
      #state.cells[cell]=-1
    #return bestVal    

  #for cell in state.applicableActions(player):
    #state[cell] = player
    #print(state.successor(player,player))
    #print(state.value())
    
    #score = minimax(player,state,depthLeft-1)
    #print(state.applicableActions(player))
    #print(state.value())
    #state[cell] = -1
    #score[0], score[1] = x,y
    #score = cell

    #if player == 1:
      #if score > best:
        #best = score
        #best[2] = score
    #else:
      #if score < score:
        #best = score
   
  #return best

      #if score < best[2]:
        #best[2] = score
  #print(best[2])
    #if player == 0 and score == -1:
      #return state.value()
  #return best[2]
    
  

def alphabeta(player,state,depthLeft,alpha,beta):
  global calls
  calls += 1
  if depthLeft == 0 or state.applicableActions(player)==[]:
    return state.value()
### INSERT YOUR IMPLEMENTATION OF ALPHABETA HERE
### It should be recursively calling 'alphabeta'.

  player2 = 1-player  
  if player == 0:
    bestVal = 1000
    for cell in state.applicableActions(player):
      state2 = state.successor(player,cell)
      value = alphabeta(player2,state2,depthLeft-1,alpha,beta)
      bestVal = min(bestVal, value)
      beta = min(beta, bestVal)
      if beta <= alpha:
        break
    return bestVal

  else:
    bestVal = -1000
    for cell in state.applicableActions(player):
      state2 = state.successor(player,cell)
      value = alphabeta(player2,state2,depthLeft-1,alpha,beta)
      bestVal = max(bestVal, value)
      alpha = max(alpha, bestVal)
      if beta <= alpha:
        break
    return bestVal 

def gamevalue(startingstate,depth):
  global calls
  calls = 0
  v = minimax(0,startingstate,depth)
  print(str(v) + " value with " + str(calls) + " calls with minimax to depth " + str(depth))
  calls = 0
  v = alphabeta(0,startingstate,depth,0-float("inf"),float("inf"))
  print(str(v) + " value with " + str(calls) + " calls with alphabeta to depth " + str(depth))
  calls = 0
