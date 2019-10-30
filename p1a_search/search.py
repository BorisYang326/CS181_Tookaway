Skip to content

Pull requests
Issues
Marketplace
Explore
 
 
Learn Git and GitHub without any code!
Using the Hello World guide, you’ll start a branch, write comments, and open a pull request.

Read the guide

 Unwatch 1
 Star0 Fork0BorisYang326/CS188
 Code Issues 0 Pull requests 0 Projects 0 Wiki Security Insights Settings
Branch: master 
CS188/Desktop/CS181/Project1_Part_A_search/search.py
Find fileCopy path
 BorisYang326 first commit ai
07ac9ec 11 hours ago
1 contributor
Executable File  120 lines (95 sloc)  3.74 KB
RawBlameHistory
  
# search.py
# ---------
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
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class Search_Unit:
    def __init__(self,state,path,cost):
        self.state = state
        self.cost = cost
        self.path = path
def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    stack=util.Stack()
    closed=[]
    new_path=[]
    initial_state=(Search_Unit(problem.getStartState(),[],0))
    stack.push(initial_state)
    while not stack.isEmpty():
        node=stack.pop()
        #print(node.path)
        #print(1)
        if problem.isGoalState(node.state):
            return node.path
        if node.state not in closed:
            closed.append(node.state)
            #print(closed)
            for curr_seccessor in problem.getSuccessors(node.state):
                new_state = curr_seccessor[0]
                new_path=node.path+[curr_seccessor[1]]
                new_cost=curr_seccessor[2]+node.cost
                stack.push(Search_Unit(new_state,new_path,new_cost))
        else:continue
        #print(node.path)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue=util.Queue()
    closed=[]
    new_path=[]
    initial_state=(Search_Unit(problem.getStartState(),[],0))
    queue.push(initial_state)
    while not queue.isEmpty():
        node=queue.pop()
        #print(node.path)
        #print(1)
        if problem.isGoalState(node.state):
            return node.path
        if node.state not in closed:
            closed.append(node.state)
            #print(closed)
            for curr_seccessor in problem.getSuccessors(node.state):
                new_state = curr_seccessor[0]
                new_path=node.path+[curr_seccessor[1]]
                new_cost=curr_seccessor[2]+node.cost
                queue.push(Search_Unit(new_state,new_path,new_cost))
        else:continue
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    priorityqueue=util.PriorityQueue()
    closed=[]
    new_path=[]
    initial_state=(Search_Unit(problem.getStartState(),[],0))
    priorityqueue.push(initial_state,0)
    while not priorityqueue.isEmpty():
        node=priorityqueue.pop()
        #print(node.path)
        #print(1)
        if problem.isGoalState(node.state):
            return node.path
        if node.state not in closed:
            closed.append(node.state)
            #print(closed)
            for curr_seccessor in problem.getSuccessors(node.state):
                new_state = curr_seccessor[0]
                new_path=node.path+[curr_seccessor[1]]
                new_cost=curr_seccessor[2]+node.cost
                priorityqueue.push(Search_Unit(new_state,new_path,new_cost),new_cost)
        else:continue
    util.raiseNotDefined()
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    priorityqueue=util.PriorityQueue()
    closed=[]
    new_path=[]
    initial_state=(Search_Unit(problem.getStartState(),[],0))
    priorityqueue.push(initial_state,0+heuristic(initial_state.state,problem))
    while not priorityqueue.isEmpty():
        node=priorityqueue.pop()
        #print(node.path)
        #print(1)
        if problem.isGoalState(node.state):
            return node.path
        if node.state not in closed:
            closed.append(node.state)
            #print(closed)
            for curr_seccessor in problem.getSuccessors(node.state):
                new_state = curr_seccessor[0]
                new_path=node.path+[curr_seccessor[1]]
                new_cost=curr_seccessor[2]+node.cost+heuristic(node.state,problem)
                priorityqueue.push(Search_Unit(new_state,new_path,new_cost),new_cost)
        else:continue
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
