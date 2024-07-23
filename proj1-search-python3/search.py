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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

class Node():
    def __init__(self, state, action, cost, parent):
        self.state = state
        self.action = action
        self.cost = cost
        self.parent = parent

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # print("Start:", problem.getStartState())   
    # >>> (5, 5)
    # print("Is the start a goal?", problem.isGoalState(problem.getStartState())) 
    # >>> False
    # print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    # >>> [((5, 4), 'South', 1), ((4, 5), 'West', 1)]

    reached = set()
    path = []
    frontier = util.Stack()
    frontier.push(Node(problem.getStartState(), None, 0, None))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return path
        if node.state not in reached:
            reached.add(node.state)
            for state, action, cost in problem.getSuccessors(node.state):
                frontier.push(Node(state, action, cost, node))
    return None


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    reached = set()
    path = []
    frontier = util.Queue()
    frontier.push(Node(problem.getStartState(), None, 0, None))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return path
        if node.state not in reached:
            reached.add(node.state)
            for state, action, cost in problem.getSuccessors(node.state):
                frontier.push(Node(state, action, cost, node))
    return None

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    reached = set()
    path = []
    frontier = util.PriorityQueue()
    frontier.push(Node(problem.getStartState(), None, 0, None), 0)
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return path
        if node.state not in reached:
            reached.add(node.state)
            for state, action, cost in problem.getSuccessors(node.state):
                frontier.push(Node(state, action, node.cost + cost, node), node.cost + cost)
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    def f(node):
        return heuristic(node.state, problem) + node.cost
    
    reached = set()
    path = []
    frontier = util.PriorityQueueWithFunction(f)
    frontier.push(Node(problem.getStartState(), None, 0, None))
    while not frontier.isEmpty():
        node = frontier.pop()
        if problem.isGoalState(node.state):
            while node.parent is not None:
                path.append(node.action)
                node = node.parent
            path.reverse()
            return path
        if node.state not in reached:
            reached.add(node.state)
            for state, action, cost in problem.getSuccessors(node.state):
                frontier.push(Node(state, action, node.cost + cost, node))
    return None


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
