
from markov import *

# Small test grid with teleports

testgrid1 = GridMDP(4,3,[0, 0, 0, 1,
                         0,99, 0,-1,
                         0, 0, 0, 0],
                    True)
testgrid1.show()

testgrid2 = GridMDP(7,5,[0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,
                         0,  0, -1,  2, -9,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0],
                    False)

testgrid2.show()

testgrid3 = GridMDP(8,6,[0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0, -9,  1,  1, -9,  0,  0,
                         0,  0, -9,  1,  1, -9,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0,
                         0,  0,  0,  0,  0,  0,  0,  0],
                    False)

testgrid3.show()

#### THE FOLLOWING IS TEST MATERIAL YOU CAN EXPERIMENT ####
#### THE FOLLOWING IS TEST MATERIAL YOU CAN EXPERIMENT ####
#### THE FOLLOWING IS TEST MATERIAL YOU CAN EXPERIMENT ####
#### THE FOLLOWING IS TEST MATERIAL YOU CAN EXPERIMENT ####
#### THE FOLLOWING IS TEST MATERIAL YOU CAN EXPERIMENT ####

# Testing the Value Iteration implementation

grid1V = valueIter(0.95,testgrid1)
for state,value in grid1V.items():
    print(str(state) + "  " + str(value))
grid1policy = makePolicy(grid1V,testgrid1,0.95)
testgrid1.showPolicy(grid1policy)

# testgrid1 optimal policy value function:
# 0  2.664027966635769
# 1  2.8598487357882525
# 2  3.0479966789322166
# 3  2.232202947492367
# 4  2.499581795855783
# 5  0
# 6  2.7575026772574414
# 7  2.9374994413631557
# 8  2.34968731314986
# 9  2.3872089847392477
# 10  2.5442622074194614
# 11  2.334477043721868
#
# testgrid1 optimal policy actions:
# EEEN
# N#NN
# NENW

grid2V = valueIter(0.5,testgrid2)
for state,value in grid2V.items():
  print(str(state) + "  " + str(value))
grid2policy = makePolicy(grid2V,testgrid2,0.5)
testgrid2.showPolicy(grid2policy)

grid2VB = valueIter(0.95,testgrid2)
for state,value in grid2VB.items():
  print(str(state) + "  " + str(value))
grid2policyB = makePolicy(grid2VB,testgrid2,0.95)
testgrid2.showPolicy(grid2policyB)

grid3V = valueIter(0.5,testgrid3)
for state,value in grid3V.items():
  print(str(state) + "  " + str(value))
grid3policy = makePolicy(grid3V,testgrid3,0.5)
testgrid3.showPolicy(grid3policy)

grid3VB = valueIter(0.95,testgrid3)
for state,value in grid3VB.items():
  print(str(state) + "  " + str(value))
grid3policyB = makePolicy(grid3VB,testgrid3,0.95)
testgrid3.showPolicy(grid3policyB)
