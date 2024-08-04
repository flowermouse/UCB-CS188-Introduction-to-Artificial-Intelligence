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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        currentFood = currentGameState.getFood()
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        newCapsules = successorGameState.getCapsules()


        currentGhostStates = currentGameState.getGhostStates()
        currentGhost = currentGhostStates[0].getPosition()
        currentPacman = currentGameState.getPacmanPosition()
        "*** YOUR CODE HERE ***"
        # print("score:", successorGameState.getScore())
        # current score
        score = successorGameState.getScore()
        # print(newScaredTimes)
        ghost_distance_score = 0
        if manhattanDistance(currentPacman, currentGhost) >= 15:
            for index in range(len(newGhostStates)):
                if newScaredTimes[index] > 0:
                    ghost_distance_score += - manhattanDistance(newPos, newGhostStates[index].getPosition()) * 0.5 + 100
                else:
                    ghost_distance_score += manhattanDistance(newPos, newGhostStates[index].getPosition()) * 0.5
        elif manhattanDistance(currentPacman, currentGhost) >= 10:
            for index in range(len(newGhostStates)):
                if newScaredTimes[index] > 0:
                    ghost_distance_score += - manhattanDistance(newPos, newGhostStates[index].getPosition()) * 1.2 + 100
                else:
                    ghost_distance_score += manhattanDistance(newPos, newGhostStates[index].getPosition()) * 1.2
        elif manhattanDistance(currentPacman, currentGhost) >= 6:
            for index in range(len(newGhostStates)):
                if newScaredTimes[index] > 0:
                    ghost_distance_score += - manhattanDistance(newPos, newGhostStates[index].getPosition()) * 3 + 100
                else:
                    ghost_distance_score += manhattanDistance(newPos, newGhostStates[index].getPosition()) * 3
        else:
            for index in range(len(newGhostStates)):
                if newScaredTimes[index] > 0:
                    ghost_distance_score += - manhattanDistance(newPos, newGhostStates[index].getPosition()) * 5 + 100
                else:
                    ghost_distance_score += manhattanDistance(newPos, newGhostStates[index].getPosition()) * 5

        if len(currentFood.asList()) >= 13:
            food_distance_score = 0
            for food in newFood.asList():
                food_distance_score += -manhattanDistance(newPos, food) * 0.1
        elif len(currentFood.asList()) >= 7:
            food_distance_score = 0
            for food in newFood.asList():
                food_distance_score += -manhattanDistance(newPos, food) * 0.9
        elif len(currentFood.asList()) >= 3:
            food_distance_score = 0
            for food in newFood.asList():
                food_distance_score += -manhattanDistance(newPos, food) * 1.1
        elif len(currentFood.asList()) > 1:
            food_distance_score = 0
            for food in newFood.asList():
                food_distance_score += -manhattanDistance(newPos, food) * 1.2
        else:
            food_distance_score = 0
            for food in newFood.asList():
                food_distance_score += -manhattanDistance(newPos, food) * 1.3

        capsule_distance_score = -100 * len(newCapsules)
        for capsule in newCapsules:
            capsule_distance_score += - manhattanDistance(newPos, capsule) * 1.6

        score += ghost_distance_score + food_distance_score + capsule_distance_score
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
    def value(self, gameState, depth):
        agent = depth % gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        elif agent == 0:
            return self.max_value(gameState, depth)
        else:
            return self.min_value(gameState, depth)
        
    def max_value(self, gameState, depth):
        v = float('-inf')
        for successor in gameState.getLegalActions(0):
            v = max(v, self.value(gameState.generateSuccessor(0, successor), depth + 1))
        return v
    
    def min_value(self, gameState, depth):
        v = float('inf')
        agent = depth % gameState.getNumAgents()
        for successor in gameState.getLegalActions(agent):
            v = min(v, self.value(gameState.generateSuccessor(agent, successor), depth + 1))
        return v

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
        child_nodes = [(action, gameState.generateSuccessor(0, action)) for action in gameState.getLegalActions(0)]
        action = max(child_nodes, key=lambda x: self.value(x[1], 1))[0]
        return action

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha, beta = float('-inf'), float('inf')
        best_action = None
        v = float('-inf')
        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            value_of_action = self.value(successor, 1, alpha, beta)
            if value_of_action > v:
                v = value_of_action
                best_action = action
            if v > beta:
                return best_action
            alpha = max(alpha, v)
        return best_action

    def value(self, gameState, depth, alpha, beta):
        agent = depth % gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        elif agent == 0:
            return self.max_value(gameState, depth, alpha, beta)
        else:
            return self.min_value(gameState, depth, alpha, beta)

    def max_value(self, gameState, depth, alpha, beta):
        v = float('-inf')
        for successor in gameState.getLegalActions(0):
            v = max(v, self.value(gameState.generateSuccessor(0, successor), depth + 1, alpha, beta))
            if v > beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, gameState, depth, alpha, beta):
        v = float('inf')
        agent = depth % gameState.getNumAgents()
        for successor in gameState.getLegalActions(agent):
            v = min(v, self.value(gameState.generateSuccessor(agent, successor), depth + 1, alpha, beta))
            if v < alpha:
                return v
            beta = min(beta, v)
        return v

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        child_nodes = [(action, gameState.generateSuccessor(0, action)) for action in gameState.getLegalActions(0)]
        action = max(child_nodes, key=lambda x: self.value(x[1], 1))[0]
        return action
    
    def value(self, gameState, depth):
        agent = depth % gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        elif agent == 0:
            return self.max_value(gameState, depth)
        else:
            return self.exp_value(gameState, depth)
        
    def max_value(self, gameState, depth):
        v = float('-inf')
        for successor in gameState.getLegalActions(0):
            v = max(v, self.value(gameState.generateSuccessor(0, successor), depth + 1))
        return v
    
    def exp_value(self, gameState, depth):
        v = 0
        agent = depth % gameState.getNumAgents()
        for successor in gameState.getLegalActions(agent):
            v += self.value(gameState.generateSuccessor(agent, successor), depth + 1)
        return v / len(gameState.getLegalActions(agent))

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pacman = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    ghost = currentGameState.getGhostStates()[0].getPosition()
    Capsules = currentGameState.getCapsules()

    exp_agent = ExpectimaxAgent()
    exp_depth = 4
    exp_value = exp_agent.value(currentGameState, exp_depth)

    ghost_distance_score = 0
    if manhattanDistance(pacman, ghost) >= 15:
        for index in range(len(GhostStates)):
            if ScaredTimes[index] > 0:
                ghost_distance_score += - manhattanDistance(pacman, GhostStates[index].getPosition()) * 0.5 + 100
            else:
                ghost_distance_score += manhattanDistance(pacman, GhostStates[index].getPosition()) * 0.5
    elif manhattanDistance(pacman, ghost) >= 10:
        for index in range(len(GhostStates)):
            if ScaredTimes[index] > 0:
                ghost_distance_score += - manhattanDistance(pacman, GhostStates[index].getPosition()) * 1.2 + 100
            else:
                ghost_distance_score += manhattanDistance(pacman, GhostStates[index].getPosition()) * 1.2
    elif manhattanDistance(pacman, ghost) >= 6:
        for index in range(len(GhostStates)):
            if ScaredTimes[index] > 0:
                ghost_distance_score += - manhattanDistance(pacman, GhostStates[index].getPosition()) * 3 + 100
            else:
                ghost_distance_score += manhattanDistance(pacman, GhostStates[index].getPosition()) * 3
    else:
        for index in range(len(GhostStates)):
            if ScaredTimes[index] > 0:
                ghost_distance_score += - manhattanDistance(pacman, GhostStates[index].getPosition()) * 5 + 100
            else:
                ghost_distance_score += manhattanDistance(pacman, GhostStates[index].getPosition()) * 5

    food_distance_score = 0
    if len(food.asList()) >= 13:
        for food in food.asList():
            food_distance_score += -manhattanDistance(pacman, food) * 0.1
    elif len(food.asList()) >= 7:
        for food in food.asList():
            food_distance_score += -manhattanDistance(pacman, food) * 0.9
    elif len(food.asList()) >= 3:
        for food in food.asList():
            food_distance_score += -manhattanDistance(pacman, food) * 1.1
    elif len(food.asList()) > 1:
        for food in food.asList():
            food_distance_score += -manhattanDistance(pacman, food) * 1.2
    else:
        for food in food.asList():
            food_distance_score += -manhattanDistance(pacman, food) * 1.3

    capsule_distance_score = -100 * len(Capsules)
    for capsule in Capsules:
        capsule_distance_score += - manhattanDistance(pacman, capsule) * 1.6

    score = exp_value * 4 + ghost_distance_score + food_distance_score + capsule_distance_score
    return score

# Abbreviation
better = betterEvaluationFunction
