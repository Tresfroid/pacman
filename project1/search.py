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
# -*- coding: utf-8 -*-


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
    from util import Stack
    stack = Stack() # store the node
    stack2 = Stack() #store each action
    visited = [] # label the extended state
    path = {} # current_state:parent_state, actions
    result = [] # store the action list

    start_state = problem.getStartState()
    stack.push(start_state)

    while stack.isEmpty() == False:
        current_state = stack.pop()

        if problem.isGoalState(current_state) == True:
            while current_state != start_state:
                stack2.push(path[current_state][1])
                current_state = path[current_state][0]
            while stack2.isEmpty() == False:
                result.append(stack2.pop())
            return result

        if current_state in visited:
            continue

        successors = problem.getSuccessors(current_state)
        for successor in successors:
            if successor[0] not in visited:
                stack.push(successor[0])
                path[successor[0]] = (current_state, successor[1])

        visited.append(current_state)

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    queue = util.Queue()
    start_state = problem.getStartState()
    # print "Start:", problem.getStartState()

    visited = []
    visited.append(start_state)

    dict = {}
    stack = util.Stack()
    move_list = []
    dict[start_state] = ((0, 0), '')

    queue.push((start_state, []))

    while not queue.isEmpty():
        current_state = queue.pop()
        now_state = current_state[0]
        now_action = current_state[1]
        if problem.isGoalState(now_state):
            while dict[now_state][0] != (0, 0):
                stack.push(dict[now_state][1])
                now_state = dict[now_state][0]
            while not stack.isEmpty():
                move_list.append(stack.pop())
            return move_list
        for i in problem.getSuccessors(now_state):
            if i[0] not in visited:
                visited.append(i[0])
                queue.push((i[0], i[1]))
                dict[i[0]] = (now_state, i[1])

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    from util import Stack

    queue = PriorityQueue()  #store ((state , path ), cost)
    path = {} #current_state: parent_state, actions
    result = [] #store the action list
    visited = [] #store the extended state
    stack = Stack() #store each action

    start_state = problem.getStartState()
    path[start_state] = (0, "")
    visited.append(start_state)
    queue.push((start_state, 0), 0)

    while queue.isEmpty() == False:
        current_state, current_cost = queue.pop()

        if problem.isGoalState(current_state):
            while current_state !=start_state:
                stack.push(path[current_state][1])
                current_state = path[current_state][0]
            while stack.isEmpty() == False:
                result.append(stack.pop())
            return result

        successors = problem.getSuccessors(current_state)
        for successor, action, cost in successors:
            if successor not in visited:
                total_cost = current_cost + cost
                queue.push((successor, total_cost), total_cost)
                path[successor] = (current_state, action)
                visited.append(successor)
            else:
                if problem.isGoalState(successor):
                    total_cost = current_cost + cost
                    queue.push((successor, total_cost), total_cost)
                    path[successor] = (current_state, action)


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
    open_list = util.PriorityQueue()  # store the state,priority,cost , 2 tuple
    closed_list = set()  # store the visited nodes
    start_state = problem.getStartState()
    g_score = 0
    h_score = heuristic(start_state, problem)
    f_score = g_score + h_score
    open_list.push((start_state, [], f_score), f_score)

    while not open_list.isEmpty():
        current = open_list.pop()
        current_state = current[0]
        current_move = current[1]
        current_cost = current[2]
        if current_state in closed_list:
            continue
        closed_list.add(current_state)
        if problem.isGoalState(current_state):
            return current_move
        for state, move, cost in problem.getSuccessors(current_state):
            open_list.push((state, current_move + [move], cost + current_cost),
                           cost + current_cost + heuristic(state, problem))
    return []

    util.raiseNotDefined()

def greedySearch(problem,heuristic=nullHeuristic):

    from util import PriorityQueue

    queue = PriorityQueue() #store state, cost
    visited = []
    result = {} #store state:action from start to this state

    start_state = problem.getStartState()
    result[start_state] = []
    visited.append(start_state)
    queue.push(start_state, 0)

    while queue.isEmpty() == False:
        current_state = queue.pop()

        if problem.isGoalState(current_state):
            return result[current_state]

        successors = problem.getSuccessors(current_state)
        for successor in successors:
            if successor[0] not in visited:
                path = result[current_state][:]
                path.append(successor[1])
                result[successor[0]] = path
                queue.push(successor[0], heuristic(successor[0]))
                visited.append(successor[0])
        #visited.append(current_state)



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch