
import random

from qlearnexamples import *

# The Q-Learning Algorithm

# EXERCISE ASSIGNMENT:
# Implement the Q-learning algorithm for MDPs.
#   The Q-values are represented as a Python dictionary Q[s,a],
# which is a mapping from the state indices s=0..stateMax to
# and actions a to the Q-values.
#
# Choice of actions can be completely random, or, if you are interested,
# you could implement some scheme that prefers better actions, e.g.
# based on Multi-arm Bandit problems (find more about these in the literature:
# this is an optional addition to the programming assignment.)

# OPTIONAL FUNCTIONS:
# You can implement and use the auxiliary functions bestActionFor and execute
# if you want, as auxiliary functions for Qlearning and makePolicy and makeValues.

# bestActionFor chooses the best action for 'state', given Q values

def bestActionFor(mdp,state,Q):
  Qbest=0
  bestAction=0
  for a in mdp.applicableActions(state):
    if Q[state,a]>Qbest:
      bestAction=a
      Qbest=Q[state,a]
  return bestAction

# valueOfBestAction gives the value of best action for 'state'
def valueOfBestAction(mdp,state,Q):
  Qbest=0
  for a in mdp.applicableActions(state):
    if Q[state,a]>Qbest:
      Qbest=Q[state,a]
  return Qbest

# 'execute' randomly chooses a successor state for state s w.r.t. action a.
# The probability with which is given successor is chosen must respect
# to the probability given by mdp.successors(s,a).
# It returns a tuple (s2,r), where s2 is the successor state and r is
# the reward that was obtained.
#def execute(mdp,s,a):

# OBLIGATORY FUNCTION:
# Qlearning returns the Q-value function after performing the given
#   number of iterations i.e. Q-value updates.
def weighted_choice(options,weights):
  total = sum(weights)
  treshold = random.uniform(0,total)
  for k, weight in enumerate(weights):
    total -= weight
    if total < treshold:
      return options[k]

def Qlearning(mdp,gamma,lambd,iterations):
  # The Q-values are a real-valued dictionary Q[s,a] where s is a state and a is an action.
  Q = dict()
  s = 0
  successor = dict()
  i=0
  j=0
  while i < iterations:
    i=i+1
    a = random.choice(mdp.applicableActions(s))

    successor=mdp.successors(s,a)
    probability=[successor[x][1] for x in range(0,len(successor))]

    bestMove=weighted_choice(mdp.successors(s,a),probability)
    s2=bestMove[0]
    
    actions=mdp.applicableActions(bestMove[0])
    bestAction=-9999
    for j in actions:
      if not (s2,j) in Q:
        Q[s2,j]=0
      if Q[s2,j]>bestAction:
        bestAction=Q[s2,j]
        a2=j

    if not (s,a) in Q:
      Q[s,a] = 0
    if not (s2,a2) in Q:
      Q[s2,a2] = 0
     
    Q[s,a] = (1-lambd)*Q[s,a]+lambd*(bestMove[2]+gamma*Q[s2,a2])   #MAX???
    s = s2
    
  return Q

# OBLIGATORY FUNCTION:
# makePolicy constructs a policy, i.e. a mapping from state to actions,
#   given a Q-value function as produced by Qlearning.
def makePolicy(mdp,Q):
  # A policy is an action-valued dictionary P[s] where s is a state
  P = dict()
  state = [ i for i in range(0,mdp.stateMax+1)]
  for s in state:
    P[s] = bestActionFor(mdp,s,Q)
  return P


# OBLIGATORY FUNCTION:
# makeValues constructs the value function, i.e. a mapping from states to values,
#   given a Q-value function as produced by Qlearning.
def makeValues(mdp,Q):
  # A value function is a real-valued dictionary V[s] where s is a state
  V = dict()
  state = [ i for i in range(0,mdp.stateMax+1)]
  for s in state:
    V[s] = valueOfBestAction(mdp,s,Q)
  return V
