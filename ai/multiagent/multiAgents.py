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
import random, util

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
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        score = successorGameState.getScore()
        minFoodDistance = min([util.manhattanDistance(newPos, foodPos) for foodPos in newFood.asList()] or [0])
        score -= minFoodDistance
        if currentGameState.getFood()[newPos[0]][newPos[1]]:
            score += 500
        minGohstDistance = min([util.manhattanDistance(newPos, ghostState.getPosition()) for ghostState in newGhostStates])
        if minGohstDistance < 2:
            score -= 1000
        return score

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def max(self, state, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), ''
        return max([(self.min(state.generateSuccessor(0, a), depth, 1)[0], a) for a in state.getLegalActions(0)])

    def min(self, state, depth, agent):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), ''
        if agent == state.getNumAgents() - 1:
            return min([(self.max(state.generateSuccessor(agent, a), depth - 1)[0], a) for a in state.getLegalActions(agent)])
        return min([(self.min(state.generateSuccessor(agent, a), depth, agent + 1)[0], a) for a in state.getLegalActions(agent)])

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
        """
        return self.max(gameState, self.depth)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def max(self, state, depth, alpha, beta):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), ''
        v = (float("-inf"), '')
        for a in state.getLegalActions(0):
            v = max(v, (self.min(state.generateSuccessor(0, a), depth, 1, alpha, beta)[0], a))
            alpha = max(alpha, v[0])
            if v[0] > beta:
                return v
        return v

    def min(self, state, depth, agent, alpha, beta):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), ''
        v = (float("inf"), '')
        if agent == state.getNumAgents() - 1:
            for a in state.getLegalActions(agent):
                v = min(v, (self.max(state.generateSuccessor(agent, a), depth - 1, alpha, beta)[0], a))
                beta = min(beta, v[0])
                if v[0] < alpha:
                    return v
            return v
        for a in state.getLegalActions(agent):
            v = min(v, (self.min(state.generateSuccessor(agent, a), depth, agent + 1, alpha, beta)[0], a))
            beta = min(beta, v[0])
            if v[0] < alpha:
                return v
        return v

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        return self.max(gameState, self.depth, float("-inf"), float("inf"))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def max(self, state, depth):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), ''
        return max([(self.min(state.generateSuccessor(0, a), depth, 1)[0], a) for a in state.getLegalActions(0)])

    def min(self, state, depth, agent):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state), ''
        l = []
        if agent == state.getNumAgents() - 1:
            l = [(self.max(state.generateSuccessor(agent, a), depth - 1)[0], a) for a in state.getLegalActions(agent)]
        else:
            l = [(self.min(state.generateSuccessor(agent, a), depth, agent + 1)[0], a) for a in state.getLegalActions(agent)]
        return sum(l[x][0] for x in range(len(l))) / len(l), l[0][1]

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        return self.max(gameState, self.depth)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).
      1. Used standard score.
      2. Penalty if far from closest food. (no weight)
      3. Penalty if close to ghost. (no weight)
    """
    pos = currentGameState.getPacmanPosition()

    score = currentGameState.getScore()
    score -= min([util.manhattanDistance(pos, foodPos) for foodPos in currentGameState.getFood().asList()] or [0])
    if 2 > min([util.manhattanDistance(pos, ghost.getPosition()) for ghost in currentGameState.getGhostStates()]):
        score -= 1000
    return score

# Abbreviation
better = betterEvaluationFunction

