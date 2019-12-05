# logicPlan.py
# ------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In logicPlan.py, you will implement logic planning methods which are called by
Pacman agents (in logicAgents.py).
"""

import util
import sys
import logic
import game

from logic import A, B, C, Expr
from itertools import combinations
import time

pacman_str = 'P'
ghost_pos_str = 'G'
ghost_east_str = 'GE'
pacman_alive_str = 'PA'


class PlanningProblem:
    """
    This class outlines the structure of a planning problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the planning problem.
        """
        util.raiseNotDefined ()

    def getGhostStartStates(self):
        """
        Returns a list containing the start state for each ghost.
        Only used in problems that use ghosts (FoodGhostPlanningProblem)
        """
        util.raiseNotDefined ()

    def getGoalState(self):
        """
        Returns goal state for problem. Note only defined for problems that have
        a unique goal state such as PositionPlanningProblem
        """
        util.raiseNotDefined ()


def tinyMazePlan(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def sentence1():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    A or B
    (not A) if and only if ((not B) or C)
    (not A) or (not B) or C
    """
    "*** YOUR CODE HERE ***"
    A = Expr ("A")
    B = Expr ("B")
    C = Expr ("C")
    ins_1 = A | B;
    ins_2 = ~A % ((~B) | C)
    ins_3 = logic.disjoin ((~A), (~B), C)
    return logic.conjoin (ins_1, ins_2, ins_3)

    util.raiseNotDefined ()


def sentence2():
    """Returns a logic.Expr instance that encodes that the following expressions are all true.

    C if and only if (B or D)
    A implies ((not B) and (not D))
    (not (B and (not C))) implies A
    (not D) implies C
    """
    "*** YOUR CODE HERE ***"
    A = Expr ("A")
    B = Expr ("B")
    C = Expr ("C")
    D = Expr ("D")
    ins_4 = C % (B | D)
    ins_5 = A >> (~B & ~D)
    ins_6 = (~(B & (~C))) >> A
    ins_7 = (~D) >> C
    return logic.conjoin (ins_4, ins_5, ins_6, ins_7)
    util.raiseNotDefined ()


def sentence3():
    """Using the symbols WumpusAlive[1], WumpusAlive[0], WumpusBorn[0], and WumpusKilled[0],
    created using the logic.PropSymbolExpr constructor, return a logic.PropSymbolExpr
    instance that encodes the following English sentences (in this order):

    The Wumpus is alive at time 1 if and only if the Wumpus was alive at time 0 and it was
    not killed at time 0 or it was not alive and time 0 and it was born at time 0.

    The Wumpus cannot both be alive at time 0 and be born at time 0.

    The Wumpus is born at time 0.
    """
    "*** YOUR CODE HERE ***"
    ins_8 = logic.PropSymbolExpr ('WumpusAlive', 1)
    ins_9 = logic.PropSymbolExpr ('WumpusAlive', 0)
    ins_10 = logic.PropSymbolExpr ('WumpusBorn', 0)
    ins_11 = logic.PropSymbolExpr ('WumpusKilled', 0)
    ins_12 = ins_8 % logic.disjoin ((ins_9 & ~ins_11), (~ins_9 & ins_10))
    ins_13 = ~(ins_9 & ins_10) & ins_10
    return logic.conjoin (ins_12, ins_13)
    # return logic.to_cnf(ins_12)
    util.raiseNotDefined ()


def findModel(sentence):
    """Given a propositional logic sentence (i.e. a logic.Expr instance), returns a satisfying
    model if one exists. Otherwise, returns False.
    """
    "*** YOUR CODE HERE ***"
    cnf_s = logic.to_cnf (sentence)
    sat_s = logic.pycoSAT (cnf_s)
    # print(sat_s)
    return sat_s
    util.raiseNotDefined ()


def atLeastOne(literals):
    """
    Given a list of logic.Expr literals (i.e. in the form A or ~A), return a single
    logic.Expr instance in CNF (conjunctive normal form) that represents the logic
    that at least one of the literals in the list is true.
    >>> A = logic.PropSymbolExpr('A');
    >>> B = logic.PropSymbolExpr('B');
    >>> symbols = [A, B]
    >>> atleast1 = atLeastOne(symbols)
    >>> model1 = {A:False, B:False}
    >>> print logic.pl_true(atleast1,model1)
    False
    >>> model2 = {A:False, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    >>> model3 = {A:True, B:True}
    >>> print logic.pl_true(atleast1,model2)
    True
    """
    "*** YOUR CODE HERE ***"
    # symbols=list(combinations(literals,2))
    y = logic.disjoin (literals)
    # print(symbols)
    # for i in symbols:
    #     x=logic.conjoin(i)
    #     y=logic.disjoin(y,x)
    return y
    util.raiseNotDefined ()


def atMostOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form) that represents the logic that at most one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    # for i in literals:
    #     i=~i
    symbols = list (combinations (literals, 2))
    # y = logic.conjoin (literals)
    y_1 = Expr ("A")
    y_2 = ~y_1
    y = logic.disjoin (y_1, y_2)
    # print (symbols)
    for i in symbols:
        x = (logic.disjoin (~i[0], ~i[1]))
        y = logic.conjoin (y, x)
    # print(y)
    return y
    util.raiseNotDefined ()


def exactlyOne(literals):
    """
    Given a list of logic.Expr literals, return a single logic.Expr instance in
    CNF (conjunctive normal form)that represents the logic that exactly one of
    the expressions in the list is true.
    """
    "*** YOUR CODE HERE ***"
    symbols = list (combinations (literals, 2))
    # in_literals=[]
    # for i in literals:
    #     print(i)
    #     in_literals+=~i
    t = logic.disjoin (literals)
    y_1 = Expr ("A")
    y_2 = ~y_1
    y = logic.disjoin (y_1, y_2)
    # print (symbols)
    for i in symbols:
        x = (logic.disjoin (~i[0], ~i[1]))
        y = logic.conjoin (y, x)
    y = logic.conjoin (t, y)
    # print(y)
    return y
    util.raiseNotDefined ()


def extractActionSequence(model, actions):
    """
    Convert a model in to an ordered list of actions.
    model: Propositional logic model stored as a dictionary with keys being
    the symbol strings and values being Boolean: True or False
    Example:
    >>> model = {"North[3]":True, "P[3,4,1]":True, "P[3,3,1]":False, "West[1]":True, "GhostScary":True, "West[3]":False, "South[2]":True, "East[1]":False}
    >>> actions = ['North', 'South', 'East', 'West']
    >>> plan = extractActionSequence(model, actions)
    >>> print plan
    ['West', 'South', 'North']
    """
    "*** YOUR CODE HERE ***"
    nosort = []
    final_sorted = []
    for i in model.keys ():
        if (model[i]):
            if (len (i.parseExpr (i)[1]) != 3 and (i.parseExpr (i)[0] in actions)):
                # print(z[0])
                nosort.append (i)
    print (nosort)
    m = 0
    while (len (final_sorted) < len (nosort)):
        # x=nosort[m]
        # print(x.parseExpr(x))
        # x=nosort[j]
        for j in range (len (nosort)):
            if (eval (nosort[j].parseExpr (nosort[j])[1]) == m):
                final_sorted.append (nosort[j].parseExpr (nosort[j])[0])
        # print (nosort[j])
        # print(final_sorted)
        m += 1
    return final_sorted
    # print(nosort)
    util.raiseNotDefined ()


def pacmanSuccessorStateAxioms(x, y, t, walls_grid):
    """
    Successor state axiom for state (x,y,t) (from t-1), given the board (as a
    grid representing the wall locations).
    Current <==> (previous position at time t-1) & (took action to move to x, y)
    """
    "*** YOUR CODE HERE ***"
    walls = walls_grid.asList ()
    r = logic.PropSymbolExpr (pacman_str, x, y, t)
    pre_loc = [0, 0, 0, 0]
    # true_1 = Expr ("A")
    # true_2 = ~true_1
    # true = logic.disjoin (true_1, true_2)
    # print(walls)
    for i in range (4):
        if (i == 0):
            pre_loc[0] = logic.conjoin (logic.PropSymbolExpr (pacman_str, x, y - 1, t - 1),
                                        logic.PropSymbolExpr ("North", t - 1))
            # print(pre_loc[0].parseExpr(pre_loc[0])[1][2])
            if (x, y - 1) in walls:
                pre_loc[0] = logic.conjoin (pre_loc[0], ~pre_loc[0])
        elif (i == 1):
            pre_loc[1] = logic.conjoin (logic.PropSymbolExpr (pacman_str, x, y + 1, t - 1),
                                        logic.PropSymbolExpr ("South", t - 1))
            if (x, y + 1) in walls:
                pre_loc[1] = logic.conjoin (pre_loc[1], ~pre_loc[1])
        elif (i == 2):
            pre_loc[2] = logic.conjoin (logic.PropSymbolExpr (pacman_str, x + 1, y, t - 1),
                                        logic.PropSymbolExpr ("West", t - 1))
            if (x + 1, y) in walls:
                pre_loc[2] = logic.conjoin (pre_loc[2], ~pre_loc[2])
        else:
            pre_loc[3] = logic.conjoin (logic.PropSymbolExpr (pacman_str, x - 1, y, t - 1),
                                        logic.PropSymbolExpr ("East", t - 1))
            if (x - 1, y) in walls:
                pre_loc[3] = logic.conjoin (pre_loc[3], ~pre_loc[3])
    # for i in pre_loc:
    #     #print(i)
    t = logic.disjoin (pre_loc)
    # print(r)
    # print(true)
    # print(r%true)
    return r % t  # Replace this with your expression


# (A | ~A | (P[1,1,0] & North[0]) | (P[1,3,0] & South[0]) | (P[2,2,0] & West[0] & ~(P[2,2,0] & West[0])) | (P[0,2,0] & East[0] & ~(P[0,2,0] & East[0])))
# (P[1,2,1] <=> (A | ~A | (P[1,1,0] & North[0]) | (P[1,3,0] & South[0]) | (P[2,2,0] & West[0] & ~(P[2,2,0] & West[0])) | (P[0,2,0] & East[0] & ~(P[0,2,0] & East[0]))))


def positionLogicPlan(problem):
    """
    Given an instance of a PositionPlanningProblem, return a list of actions that lead to the goal.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    actions = ['North', 'South', 'East', 'West']
    walls = problem.walls
    width, height = problem.getWidth (), problem.getHeight ()
    loc_list = []
    list_walls = walls.asList ()
    for w in range (width + 1):
        for h in range (height + 1):
            if (w, h) not in list_walls:
                loc_list.append ((w, h))
                # loc_list=[(w,h) for h in range(height+1) if ((w, h) not in list_walls)]
            else:
                pass
    # loc_list=[(w,h) for w in range(width+1) for h in range(height+1) if ((w, h) not in list_walls)]
    final_list = []
    final_cnf = []
    for i in range (50):
        ac_list = [logic.PropSymbolExpr (actions[k], i) for k in range (len (actions))]
        final_list.append (exactlyOne (ac_list))
        pac_pos_list = [logic.PropSymbolExpr (pacman_str, j[0], j[1], i) for j in loc_list]
        final_list.append (exactlyOne (pac_pos_list))
        if (i != 0):
            for k in loc_list:
                final_list.append (pacmanSuccessorStateAxioms (k[0], k[1], i, walls))
                # tem_axiom=[pacmanSuccessorStateAxioms (k[0], k[1], i, walls) for k in loc_list]
                # final_list.extend(tem_axiom)
        else:
            pass
        # print(final_list)
        # x=findModel(logic.conjoin(final_list))
        final_list.append (logic.PropSymbolExpr (pacman_str, problem.getStartState ()[0], problem.getStartState ()[1], 0))
        cnf_s = logic.to_cnf (logic.conjoin (final_list))
        final_cnf.append (cnf_s)
        End_pos_con=logic.PropSymbolExpr (pacman_str, problem.getGoalState ()[0], problem.getGoalState ()[1], i)
        # print(cnf_s)
        # sat_s = logic.pycoSAT (cnf_s)
        #print (logic.pycoSAT (logic.conjoin (final_cnf)))
        #print(findModel(logic.conjoin (final_cnf)))
        if (logic.pycoSAT ((logic.conjoin (final_cnf))&End_pos_con) == False):
            # print("pass")
            print (i)
            final_list = []
        else:
            # print("break")
            break
    return extractActionSequence (logic.pycoSAT(logic.conjoin (final_cnf)&End_pos_con), actions)
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined ()


def foodLogicPlan(problem):
    """
    Given an instance of a FoodPlanningProblem, return a list of actions that help Pacman
    eat all of the food.
    Available actions are game.Directions.{NORTH,SOUTH,EAST,WEST}
    Note that STOP is not an available action.
    """
    walls = problem.walls
    width, height = problem.getWidth (), problem.getHeight ()
    food_list = problem.getStartState ()[1].asList ()
    # print(food_list)
    actions = ['North', 'South', 'East', 'West']
    final_cnf=[]
    loc_list = []
    list_walls = walls.asList ()
    for w in range (width + 1):
        for h in range (height + 1):
            if ((w, h) not in list_walls):
                loc_list.append ((w, h))
            else:
                pass
    final_list = []
    food_con = [[] for n in range (len (food_list))]
    # print(food_con)
    final_list.append (logic.PropSymbolExpr (pacman_str, problem.getStartState ()[0][0], problem.getStartState ()[0][1], 0))
    for i in range (50):
        for index, x in enumerate (food_list):
            food_con[index].append (logic.PropSymbolExpr (pacman_str, x[0], x[1], i))

        ac_list = [logic.PropSymbolExpr (actions[0], i), logic.PropSymbolExpr (actions[1], i),
                   logic.PropSymbolExpr (actions[2], i), logic.PropSymbolExpr (actions[3], i)]
        final_list.append (exactlyOne (ac_list))
        pac_pos_list = [logic.PropSymbolExpr (pacman_str, j[0], j[1], i) for j in loc_list]
        final_list.append (exactlyOne (pac_pos_list))
        food_disjoint = []
        if (i != 0):
            for k in loc_list:
                final_list.append (pacmanSuccessorStateAxioms (k[0], k[1], i, walls))
        else:
            pass
        for a in range (len (food_con)):
            food_disjoint.append (atLeastOne (food_con[a]))
            # print(food_disjoint)
        End_food_con=(logic.conjoin (food_disjoint))
        cnf_s = logic.to_cnf (logic.conjoin (final_list))
        final_cnf.append (cnf_s)
        if (logic.pycoSAT ((logic.conjoin (final_cnf)&End_food_con))== False):
            # if(i<3):print(logic.conjoin(final_list))
            # print("pass")
            final_list = []
            print(i)
        else:
            break
        # print("break")
    # print(food_con)

    # print(final_model)
    # print(final_express)
    # print(food_con)
    return extractActionSequence (logic.pycoSAT (logic.conjoin(final_cnf)&End_food_con), actions)
    # return extractActionSequence (final_model, actions)
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined ()


# Abbreviations
plp = positionLogicPlan
flp = foodLogicPlan

# Some for the logic module uses pretty deep recursion on long expressions
sys.setrecursionlimit (100000)
