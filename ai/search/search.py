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
from util import PriorityQueue
from util import Queue
from util import Stack

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

def push(c, t):
    if isinstance(c, Stack) or isinstance(c, Queue):
        c.push(t)
    else:
        c.push(t, t[3] + t[4])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def generalizedSearch(problem, container, heuristic=nullHeuristic):
    startState = problem.getStartState()
    push(container, (startState, '', '', 0, 0))
    parents = {}
    done = set()
    while not container.isEmpty():
        state, parent, action, cost, _ = container.pop()
        if state in done:
            continue
        done.add(state)
        parents[state] = (parent, action)
        if (problem.isGoalState(state)):
            actions = []
            while parents[state][1] != '':
                actions.insert(0, parents[state][1])
                state = parents[state][0]
            return actions
        for successor in problem.getSuccessors(state):
            # successor -> (nextState, action, cost)
            push(container, (successor[0], state, successor[1], successor[2] + cost, heuristic(successor[0], problem)))

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.
    """
    return generalizedSearch(problem, Stack())

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    return generalizedSearch(problem, Queue())

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    return generalizedSearch(problem, PriorityQueue())

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    return generalizedSearch(problem, PriorityQueue(), heuristic)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
