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
  def __init__(self):
    self.lastPositions = []
    self.dc = None


  def getAction(self, gameState):
    """
    getAction chooses among the best options according to the evaluation function.

    getAction takes a GameState and returns some Directions.X for some X in the set {North, South, West, East, Stop}
    ------------------------------------------------------------------------------
    Description of GameState and helper functions:

    A GameState specifies the full game state, including the food, capsules,
    agent configurations and score changes. In this function, the |gameState| argument
    is an object of GameState class. Following are a few of the helper methods that you
    can use to query a GameState object to gather information about the present state
    of Pac-Man, the ghosts and the maze.

    gameState.getLegalActions():
        Returns the legal actions for the agent specified. Returns Pac-Man's legal moves by default.

    gameState.generateSuccessor(agentIndex, action):
        Returns the successor state after the specified agent takes the action.
        Pac-Man is always agent 0.

    gameState.getPacmanState():
        Returns an AgentState object for pacman (in game.py)
        state.configuration.pos gives the current position
        state.direction gives the travel vector

    gameState.getGhostStates():
        Returns list of AgentState objects for the ghosts

    gameState.getNumAgents():
        Returns the total number of agents in the game

    gameState.getScore():
        Returns the score corresponding to the current state of the game


    The GameState class is defined in pacman.py and you might want to look into that for
    other helper methods, though you don't need to.
    """
    # Collect legal moves and successor states
    legalMoves = gameState.getLegalActions()

    # Choose one of the best actions
    scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
    bestScore = max(scores)
    bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
    chosenIndex = random.choice(bestIndices) # Pick randomly among the best


    return legalMoves[chosenIndex]

  def evaluationFunction(self, currentGameState, action):
    """
    The evaluation function takes in the current and proposed successor
    GameStates (pacman.py) and returns a number, where higher numbers are better.

    The code below extracts some useful information from the state, like the
    remaining food (oldFood) and Pacman position after moving (newPos).
    newScaredTimes holds the number of moves that each ghost will remain
    scared because of Pacman having eaten a power pellet.
    """
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

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

  def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

######################################################################################
# Problem 1b: implementing minimax

class MinimaxAgent(MultiAgentSearchAgent):
  """
    Your minimax agent (problem 1)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction. Terminal states can be found by one of the following:
      pacman won, pacman lost or there are no legal moves.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game

      gameState.getScore():
        Returns the score corresponding to the current state of the game

      gameState.isWin():
        Returns True if it's a winning state

      gameState.isLose():
        Returns True if it's a losing state

      self.depth:
        The depth to which search should continue

    """

    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
    def recurse(state, agentIndex, depth):
      if state.isWin() or state.isLose():
        return (state.getScore(), "none")
      elif depth == 0:
        return (self.evaluationFunction(state), "hello")
      elif state.getLegalActions(0) == [] or state.getLegalActions(0) is None:
        return float('-inf'), Directions.STOP
      else:
        if agentIndex == 0:
          return max([(recurse(state.generateSuccessor(0, action), agentIndex+1, depth)[0], action) for action in state.getLegalActions(0)])
        else:
          if agentIndex + 1 == gameState.getNumAgents():
            return min([(recurse(state.generateSuccessor(agentIndex, action), 0, depth-1)[0], action) for action in state.getLegalActions(agentIndex)])
          else:
            return min([(recurse(state.generateSuccessor(agentIndex, action), agentIndex+1, depth)[0], action) for action in state.getLegalActions(agentIndex)])

    return recurse(gameState, 0, self.depth)[1]
    # END_YOUR_CODE

######################################################################################
# Problem 2a: implementing alpha-beta
class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (problem 2)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """

    # BEGIN_YOUR_CODE (our solution is 36 lines of code, but don't worry if you deviate from this)
    def minimax(state, depth, agentIndex, alpha, beta):
      if state.isWin() or state.isLose():
        return state.getScore()
      elif depth == 0:
        return self.evaluationFunction(state)
      if agentIndex == 0:
        maxEval = float("-inf"), Directions.STOP
        for action in state.getLegalActions(agentIndex):
          eval = minimax(state.generateSuccessor(0, action), depth, agentIndex+1, alpha, beta)
          if type(eval) == tuple:
            eval = eval[0]
          if eval > maxEval[0]:
            maxEval = eval, action
          alpha = max(alpha, maxEval[0])
          if beta <= alpha:
            break
        return maxEval
      elif agentIndex + 1 == gameState.getNumAgents():
        minEval = float("inf"), Directions.STOP
        for action in state.getLegalActions(agentIndex):
          eval = minimax(state.generateSuccessor(agentIndex, action), depth-1, 0, alpha, beta)
          if type(eval) == tuple:
            eval = eval[0]
          if eval < minEval[0]:
            minEval = eval, action
          beta = min(beta, minEval[0])
          if beta <= alpha:
            break
        return minEval
      else:
        minEval = float("inf"), Directions.STOP
        for action in state.getLegalActions(agentIndex):
          eval = minimax(state.generateSuccessor(agentIndex, action), depth, agentIndex+1, alpha, beta)
          if type(eval) == tuple:
            eval = eval[0]
          if eval < minEval[0]:
            minEval = eval, action
          beta = min(beta, minEval[0])
          if beta <= alpha:
            break
        return minEval
    return minimax(gameState, self.depth, 0, float("-inf"), float("inf"))[1]
    # END_YOUR_CODE

######################################################################################
# Problem 3b: implementing expectimax

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (problem 3)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """

    # BEGIN_YOUR_CODE (our solution is 20 lines of code, but don't worry if you deviate from this)
    def minimax(state, depth, agentIndex):
      if state.isWin() or state.isLose():
        return state.getScore()
      elif depth == 0:
        return self.evaluationFunction(state)
      if agentIndex == 0:
        maxEval = float("-inf"), Directions.STOP
        for action in state.getLegalActions(agentIndex):
          eval = minimax(state.generateSuccessor(0, action), depth, agentIndex + 1)
          if type(eval) == tuple:
            eval = eval[0]
          if eval > maxEval[0]:
            maxEval = eval, action
        return maxEval
      elif agentIndex + 1 == gameState.getNumAgents():
        choices = [minimax(state.generateSuccessor(agentIndex, action), depth-1, 0) for action in state.getLegalActions(agentIndex)]
        choices = [i[0] if type(i) == tuple else i for i in choices]
        return sum(choices) / len(choices)
      else:
        choices = [minimax(state.generateSuccessor(agentIndex, action), depth, agentIndex+1) for action in
                   state.getLegalActions(agentIndex)]
        choices = [i[0] if type(i) == tuple else i for i in choices]
        return sum(choices) / len(choices)
    return minimax(gameState, self.depth, 0)[1]
    # END_YOUR_CODE

######################################################################################
# Problem 4a (extra credit): creating a better evaluation function

def betterEvaluationFunction(currentGameState):
  """
    Your extreme, unstoppable evaluation function (problem 4).

    DESCRIPTION: <write something here so we know what you did>
  """

  # BEGIN_YOUR_CODE (our solution is 13 lines of code, but don't worry if you deviate from this)
  score = currentGameState.getScore()
  ghosts = currentGameState.getGhostPositions()
  ghostStates = currentGameState.getGhostStates()
  pacman = currentGameState.getPacmanPosition()
  ghost_distances = [manhattanDistance(pacman, ghost) for ghost in ghosts]
  currentFood = currentGameState.getFood()
  capsules = currentGameState.getCapsules()
  SCARED_GHOST_VALUE = 180
  FOOD_VALUE = 10
  # SCARED_GHOST_VALUE = 180 WINS 16/20 OF THE GAMES WITH WINNING VALUE = 1703
  # SCARED_GHOST_VALUE = 100 WINS 20/20 OF THE GAMES WITH WINNING VALUE = 1626
  minFoodDistance = min(
    [manhattanDistance(pacman, (x, y)) for x in range(19) for y in range(6) if currentFood[x][y]])
  if len(capsules) > 0:
    minCapsuleDistance = min([manhattanDistance(pacman, (x, y)) for x, y in capsules])
    minFoodDistance = min(minFoodDistance, minCapsuleDistance)
  n_scared_ghosts = 0
  minScaredDistance = 30
  for i, ghost in enumerate(ghostStates):
    distance = ghost_distances[i]
    if ghost.scaredTimer > 0:
      ghost_distances[i] = float("inf")
      n_scared_ghosts += 1
      score += SCARED_GHOST_VALUE / distance
      if distance < minScaredDistance:
        minScaredDistance = distance
  score += FOOD_VALUE / minFoodDistance
  return score
  # END_YOUR_CODE

# Abbreviation
better = betterEvaluationFunction