# multiAgents.py
# --------------
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

from util import manhattanDistance
from game import Directions
import random
import util
from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [
            self.evaluationFunction(gameState, action) for action in legalMoves
        ]
        bestScore = max(scores)
        bestIndices = [
            index for index in range(len(scores)) if scores[index] == bestScore
        ]
        chosenIndex = random.choice(
            bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates
        ]
        # total_scores = successorGameState.getScore()
        # ghost_ds_set = []
        # for ghost in newGhostStates:
        #     ghost_ds_set += [manhattanDistance(newPos, ghost.getPosition)]
        # distances_Ghost = min(ghost_ds_set)
        # food_ds_set = []
        # for food in newFood.asList():
        #     food_ds_set += [manhattanDistance(newPos, food)]
        # distances_Food = min(food_ds_set)
        # inverse_food_ds = 0
        # inverse_food_ds = 1.0 / distances_Food
        # total_scores += (inverse_food_ds**2) * distances_Ghost
        # return total_scores
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """
    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)
        global INF_POS
        INF_POS = float("inf")
        global INF_NEG
        INF_NEG = float("-inf")
        # foodlist = []
        # for curr_food in newFood.asList():
        #     foodlist.append(curr_food)

    def isEnd(self, state, depth):
        if state.isWin() or state.isLose() or depth == self.depth:
            return True


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def maxValue(state, depth, agentIndex):
            if self.isEnd(state, depth):
                return self.evaluationFunction(state)
            if agentIndex == state.getNumAgents():
                return maxValue(state, depth + 1, 0)
            max_successor = []
            for curr_action in state.getLegalActions(0):
                max_successor += [
                    minValue(state.generateSuccessor(0, curr_action), depth, 1)
                ]
            return max(max_successor)

        def minValue(state, depth, agentIndex):
            if self.isEnd(state, depth):
                return self.evaluationFunction(state)
            nextmax_successor = []
            min_successor = []
            v1 = INF_POS
            v2 = INF_POS
            for curr_action in state.getLegalActions(agentIndex):
                if agentIndex + 1 == gameState.getNumAgents():
                    nextmax_successor += [
                        maxValue(
                            state.generateSuccessor(agentIndex, curr_action),
                            depth, agentIndex + 1)
                    ]
                    v1 = min(nextmax_successor)
                else:
                    min_successor += [
                        minValue(
                            state.generateSuccessor(agentIndex, curr_action),
                            depth, agentIndex + 1)
                    ]
                    v2 = min(min_successor)
            return min(v1, v2)

        pac_maxValue = INF_NEG
        pac_maxAction = Directions.STOP
        for pac_action in gameState.getLegalActions(0):
            # if (pac_action != Directions.STOP):
            next_sucessor = []
            next_sucessor += [
                minValue(gameState.generateSuccessor(0, pac_action), 0, 1)
            ]
            # if agentIndex != 0:
            #     next_value = self.minValue(gameState, 0, agentIndex)
            # else:
            #     next_value = self.maxValue(gameState, 0)
            next_value = max(next_sucessor)
            if next_value > pac_maxValue:
                pac_maxValue = next_value
                pac_maxAction = pac_action
        return pac_maxAction

    # util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # alpha = INF_NEG
        # beta = INF_POS

        def maxValue(state, depth, agentIndex, alpha, beta):
            if self.isEnd(state, depth):
                return self.evaluationFunction(state)
            if agentIndex == state.getNumAgents():
                return maxValue(state, depth + 1, 0, alpha, beta)
            # max_successor = []
            max_value = INF_NEG
            for curr_action in state.getLegalActions(0):
                # max_successor += [
                #     minValue(state.generateSuccessor(0, curr_action), depth, 1, alpha, beta)
                # ]
                # max_value = max(max_successor)
                max_value = max(
                    max_value,
                    minValue(state.generateSuccessor(0, curr_action), depth, 1,
                             alpha, beta))
                if max_value > beta:
                    return max_value
                alpha = max(alpha, max_value)
            return max_value

        def minValue(state, depth, agentIndex, alpha, beta):
            if self.isEnd(state, depth):
                return self.evaluationFunction(state)
            # nextmax_successor = []
            # min_successor = []
            v_min = INF_POS
            for curr_action in state.getLegalActions(agentIndex):
                if agentIndex + 1 == gameState.getNumAgents():
                    # nextmax_successor += [
                    #     maxValue(
                    #         state.generateSuccessor(agentIndex, curr_action),
                    #         depth, agentIndex + 1, alpha, beta)
                    # ]
                    v_min = min(
                        v_min,
                        maxValue(
                            state.generateSuccessor(agentIndex, curr_action),
                            depth, agentIndex + 1, alpha, beta))
                else:
                    # min_successor += [
                    #     minValue(
                    #         state.generateSuccessor(agentIndex, curr_action),
                    #         depth, agentIndex + 1, alpha, beta)
                    # ]
                    v_min = min(
                        v_min,
                        minValue(
                            state.generateSuccessor(agentIndex, curr_action),
                            depth, agentIndex + 1, alpha, beta))
                if v_min < alpha:
                    return v_min
                beta = min(beta, v_min)
            return v_min

        pac_maxValue = INF_NEG
        pac_maxAction = Directions.STOP
        next_value = INF_NEG
        for pac_action in gameState.getLegalActions(0):
            # if (pac_action != Directions.STOP):
            # next_sucessor = []
            # next_sucessor += [
            #     minValue(gameState.generateSuccessor(0, pac_action), 0, 1, INF_NEG, INF_POS)
            # ]
            # if agentIndex != 0:
            #     next_value = self.minValue(gameState, 0, agentIndex)
            # else:
            #     next_value = self.maxValue(gameState, 0)
            next_value = max(
                next_value,
                minValue(gameState.generateSuccessor(0, pac_action), 0, 1,
                         next_value, INF_POS))
            if next_value > pac_maxValue:
                pac_maxValue = next_value
                pac_maxAction = pac_action
        return pac_maxAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def maxValue(state, depth, agentIndex):
            if self.isEnd(state, depth):
                return self.evaluationFunction(state)
            if agentIndex == state.getNumAgents():
                return maxValue(state, depth + 1, 0)
            max_successor = []
            for curr_action in state.getLegalActions(0):
                max_successor += [
                    avgValue(state.generateSuccessor(0, curr_action), depth, 1)
                ]
            return max(max_successor)

        def avgValue(state, depth, agentIndex):
            if self.isEnd(state, depth):
                return self.evaluationFunction(state)
            avg_successor = []
            v = 0
            for curr_action in state.getLegalActions(agentIndex):
                if agentIndex + 1 == gameState.getNumAgents():
                    avg_successor += [
                        maxValue(
                            state.generateSuccessor(agentIndex, curr_action),
                            depth, agentIndex + 1)
                    ]
                else:
                    avg_successor += [
                        avgValue(
                            state.generateSuccessor(agentIndex, curr_action),
                            depth, agentIndex + 1)
                    ]
                v = sum(avg_successor) / len(avg_successor)
            return v

        pac_maxValue = INF_NEG
        pac_maxAction = Directions.STOP
        for pac_action in gameState.getLegalActions(0):
            # if (pac_action != Directions.STOP):
            next_sucessor = []
            next_sucessor += [
                avgValue(gameState.generateSuccessor(0, pac_action), 0, 1)
            ]
            # if agentIndex != 0:
            #     next_value = self.minValue(gameState, 0, agentIndex)
            # else:
            #     next_value = self.maxValue(gameState, 0)
            next_value = max(next_sucessor)
            if next_value > pac_maxValue:
                pac_maxValue = next_value
                pac_maxAction = pac_action
        return pac_maxAction

        # util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    score = scoreEvaluationFunction(currentGameState)
    newFood = currentGameState.getFood()
    newPos = currentGameState.getPacmanPosition()
    newcapsules = currentGameState.getCapsules()
    # total_scores = successorGameState.getScore()
    newGhostStates = currentGameState.getGhostStates()
    capsulesvalue = len(newcapsules)
 
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    for time in newScaredTimes:
        score += time
    ghost_ds_set = []
    for ghost in newGhostStates:
        ghost_ds_set += [manhattanDistance(newPos, ghost.getPosition())]
    distances_Ghost = sum(ghost_ds_set) / len(ghost_ds_set)
    food_ds_set = []
    for food in newFood.asList():
        food_ds_set += [manhattanDistance(newPos, food)]
   
    inverse_food_ds = 0
    if len(food_ds_set)>0 and min(food_ds_set)>0:
        distances_Food = min(food_ds_set)
        inverse_food_ds = 1.0 / distances_Food
    score += (inverse_food_ds**5) * distances_Ghost + min(ghost_ds_set)
    if newPos in food_ds_set:
        score *= 10
    foodvalue =len(food_ds_set)
    return score-2*currentGameState.getNumFood()+capsulesvalue*15-3*foodvalue
    # util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
