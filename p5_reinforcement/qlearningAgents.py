# qlearningAgents.py
# ------------------
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


from game import *
from learningAgents import ReinforcementAgent
from featureExtractors import *

import random,util,math

class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)

        "*** YOUR CODE HERE ***"
        self.Q_value=util.Counter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        "*** YOUR CODE HERE ***"
        return self.Q_value[(state,action)]
        util.raiseNotDefined()


    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        "*** YOUR CODE HERE ***"
        ##print("***      invoke compute_value     ***")
        final_value=0.0
        value_list=[]
        legal_list=self.getLegalActions(state)
        if(len(legal_list)!=0):
            for action in legal_list:
                value_list.append(self.getQValue(state,action))
            final_value=max(value_list)
        ##print (value_list,final_value,legal_list,state)
        ##print("-"*10)
        return final_value

        util.raiseNotDefined()

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        "*** YOUR CODE HERE ***"
        ##print("***      invoke compute_action     ***")
        final_action = None
        value_list = []
        action_list= []
        overlap_action_list=[]
        legal_list = self.getLegalActions(state)
        if (len(legal_list) != 0):
            for action in legal_list:
                value_list.append(self.getQValue(state, action))
                action_list.append(action)
            ###print("-" * 20)
            max_value=max(value_list)
            ###print(action_list)
            ###print(value_list)
            for i in range(len(value_list)):
                if(value_list[i]==max_value):
                    overlap_action_list.append(action_list[i])


            print_result=random.choice(overlap_action_list)
            ##print(overlap_action_list,##print_result,state)
            ##print("-" * 10)
            return print_result
        else:

            ##print(None,state)
            ##print("-" * 10)
            return None
        util.raiseNotDefined()

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: You might want to use util.flipCoin(prob)
          HINT: To pick randomly from a list, use random.choice(list)
        """
        # Pick Action
        legalActions = self.getLegalActions(state)
        action = None
        "*** YOUR CODE HERE ***"
        ###print("***      invoke get_Action     ***")
        if (len(legalActions) != 0):
            if(util.flipCoin(self.epsilon)):
                action=random.choice(legalActions)
            else:action=self.getPolicy(state)
        return action
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        "*** YOUR CODE HERE ***"
        ##print("*****************      invoke update     ********************")
        ##print(state,nextState,action)
        if(nextState):
            # pre_value=(1.0-self.alpha)*self.getQValue(state,action)
            # reward_value=self.alpha*reward
            # new_value=self.alpha*self.discount*self.getValue(nextState)
            #self.Q_value[(state,action)]=pre_value+reward_value+new_value
            self.Q_value[(state, action)]=(1.0-self.alpha)*self.getQValue(state,action)+self.alpha*(reward+self.discount*self.getValue(nextState))
            ##print (self.Q_value)
            ##print("*****************      end invoke update     ********************")
        #util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.05,gamma=0.8,alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0  # This is always Pacman
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, extractor='IdentityExtractor', **args):
        self.featExtractor = util.lookup(extractor, globals())()
        PacmanQAgent.__init__(self, **args)
        self.weights = util.Counter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        "*** YOUR CODE HERE ***"
        appro_Q_value=0.0
        #print(type(self.weights))
        #print(type(self.featExtractor))
        if not isinstance(state,str):
            feature_vector=self.featExtractor.getFeatures(state,action)
            weight=self.weights[(state,action)]
            print(type(feature_vector))
            print(type(weight))
            # if(not action):
            for feature_name,feature_value in feature_vector.items():
                appro_Q_value+=self.weights[feature_name]*feature_value
        return appro_Q_value
        util.raiseNotDefined()

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        "*** YOUR CODE HERE ***"
        feature_vector = self.featExtractor.getFeatures(state, action)
        # if (not action):
        difference_part=reward+self.discount*self.getQValue(nextState,self.getPolicy(nextState))-self.getQValue(state,action)
        for feature_name, feature_value in feature_vector.items():
            self.weights[feature_name]=self.weights[feature_name]+self.alpha*feature_value*difference_part
    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            # you might want to ##print your weights here for debugging
            "*** YOUR CODE HERE ***"
            pass
