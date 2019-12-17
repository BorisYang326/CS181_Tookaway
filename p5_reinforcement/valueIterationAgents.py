# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        # Write value iteration code here
        "*** YOUR CODE HERE ***"

        states = self.mdp.getStates()
        iter = 0
        while (iter < self.iterations):
            temp_dic = util.Counter()
            #print("=" * 30)
            for state in states:
                value_list = []
                if (not self.mdp.isTerminal(state)):
                    i = 0
                    actions = self.mdp.getPossibleActions(state)
                    #print(actions)
                    for action in actions:
                        i += 1
                        value_list.append(self.computeQValueFromValues(state, action))
                    #print("-" * 20)
                    #print(state, value_list)
                    #print(i)
                    temp_dic[state] = max(value_list)
                    #print(temp_dic)
                    #print("-" * 20)
            self.values = temp_dic
            iter += 1

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """

        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        # #print("** invoke **")
        action_value = 0
        trans = self.mdp.getTransitionStatesAndProbs(state, action)
        for tran in trans:
            action_value += tran[1] * (
                        self.mdp.getReward(state, action, tran[0]) + self.discount * self.values[tran[0]])
        # #print(action_value,action)
        return action_value
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        value_list = []
        action_list = []
        final_action = None
        if (not self.mdp.isTerminal(state)):
            actions = self.mdp.getPossibleActions(state)
            for action in actions:
                value_list.append(self.computeQValueFromValues(state, action))
                action_list.append(action)
            final_action = action_list[value_list.index(max(value_list))]
        else:
            pass
        return final_action

        # util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)


class AsynchronousValueIterationAgent(ValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        An AsynchronousValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs cyclic value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=1000):
        """
          Your cyclic value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy. Each iteration
          updates the value of only one state, which cycles through
          the states list. If the chosen state is terminal, nothing
          happens in that iteration.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state)
              mdp.isTerminal(state)
        """
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        for iter in range(self.iterations):
            # temp_dic = util.Counter()
            #print("=" * 30)
            state = states[iter % len(states)]
            value_list = []
            if (not self.mdp.isTerminal(state)):
                i = 0
                actions = self.mdp.getPossibleActions(state)
                #print(actions)
                for action in actions:
                    i += 1
                    value_list.append(self.computeQValueFromValues(state, action))
                #print("-" * 20)
                #print(state, value_list)
                #print(i)
                # temp_dic[state] = max(value_list)
                # #print(temp_dic)
                #print("-" * 20)
                self.values[state] = max(value_list)


class PrioritizedSweepingValueIterationAgent(AsynchronousValueIterationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A PrioritizedSweepingValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs prioritized sweeping value iteration
        for a given number of iterations using the supplied parameters.
    """

    def __init__(self, mdp, discount=0.9, iterations=100, theta=1e-5):
        """
          Your prioritized sweeping value iteration agent should take an mdp on
          construction, run the indicated number of iterations,
          and then act according to the resulting policy.
        """
        self.theta = theta
        ValueIterationAgent.__init__(self, mdp, discount, iterations)

    def runValueIteration(self):
        "*** YOUR CODE HERE ***"
        states = self.mdp.getStates()
        iter = 0
        set_dic = {}
        ##print("**   invoke   **")
        for state in states:
            set_dic[state] = set()
        for state in states:
            value_list = []
            if (not self.mdp.isTerminal(state)):
                actions = self.mdp.getPossibleActions(state)
                # #print(actions)
                for action in actions:
                    value_list.append(self.computeQValueFromValues(state, action))
                    trans = self.mdp.getTransitionStatesAndProbs(state, action)
                    #print(trans)
                    for tran in trans:
                        set_dic[tran[0]].add(state)
        ##print(set_dic)
        error_heap = util.PriorityQueue()
        for state in states:
            value_list = []
            if (not self.mdp.isTerminal(state)):
                actions = self.mdp.getPossibleActions(state)
                for action in actions:
                    value_list.append(self.computeQValueFromValues(state, action))
                diff = abs(max(value_list)-self.values[state])
        #         #print(diff)
        #         #print('-'*10)
        #         #print(self.values[state])
        #         #print("*"*10)
        # #print(diff)
            ##print(-1 * diff)
            ##print(type(-1*diff))
                ##print(type(state),type(-diff))
                error_heap.update(state,-diff)

        while (iter < self.iterations):
            if (error_heap.isEmpty()):
                break
            cur_state = error_heap.pop()
            value_list_cur = []
            if (not self.mdp.isTerminal(cur_state)):
                actions = self.mdp.getPossibleActions(cur_state)
                for action in actions:
                    value_list_cur.append(self.computeQValueFromValues(cur_state, action))
                self.values[cur_state] = max(value_list_cur)
            for pre_state in set_dic[cur_state]:
                value_list_next = []
                if (not self.mdp.isTerminal(pre_state)):
                    actions = self.mdp.getPossibleActions(pre_state)
                    for action in actions:
                        ##print("-"*20)
                        value_list_next.append(self.computeQValueFromValues(pre_state, action))
                        ##print(value_list)
                    diff_next = abs(max(value_list_next)-self.values[pre_state])
                    if (diff_next > self.theta):
                        error_heap.update(pre_state,-diff_next)
            iter += 1
