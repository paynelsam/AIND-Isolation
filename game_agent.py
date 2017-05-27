"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""
import random
import sys

class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass

#####################################################################
# Helper functions for board symmetry
#####################################################################

def flip_game(game, orientation) :
    """ flips the board state of the game """
    new_game = game.copy()

    # flip around diagnal center
    if orientation == 'diagonal':
        # reverse columns
        new_game.__board_state__ = new_game.__board_state__[::-1]
        # reverse rows
        i = 0
        for row in new_game.__board_state__:
            new_row = row[::-1]
            new_game.__board_state__[i] = new_row
            i = i + 1
        # reverse player positions
        for p in new_game.__last_player_move__:
            pos = new_game.__last_player_move__[p]
            new_y = new_game.height - 1 - pos[0]
            new_x = new_game.width - 1 - pos[1]
            new_game.__last_player_move__[p] = (new_y, new_x)
        return new_game
    # flip around horizontal center
    elif (orientation == 'horizontal'):
        # reverse columns
        new_game.__board_state__ = new_game.__board_state__[::-1]
        # reverse player positions
        for p in new_game.__last_player_move__:
            pos = new_game.__last_player_move__[p]
            new_y = new_game.height - 1 - pos[0]
            new_game.__last_player_move__[p] = (new_y, pos[1])
        return new_game
    # flip around vertical center
    elif (orientation == 'vertical'):
        # reverse rows
        i = 0
        for row in new_game.__board_state__:
            new_row = row[::-1]
            new_game.__board_state__[i] = new_row
            i = i + 1
        # reverse player positions
        for p in new_game.__last_player_move__:
            pos = new_game.__last_player_move__[p]
            new_x = new_game.width - 1 - pos[1]
            new_game.__last_player_move__[p] = (pos[0], new_x)
        return new_game
    else:
        print("flip_game: WARNING: UNRECOGNIZED SYMBOL:", orientation)
        return game

def check_h_symmetry(game):
    """ returns True if the board is symetric horizontally"""
    symmetry = True
    # create flipped game
    flipped_game = flip_game(game, 'horizontal')
    if game.height % 2 == 1:
        half_height = int(game.height/2 + 1)
    else:
        half_height = int(game.height/2)

    # compare blocked out spaces
    for i in range(half_height):
        for j in range(game.width):
            if not game.__board_state__[i][j] and not flipped_game.__board_state__[i][j]:
                pass
            elif game.__board_state__[i][j] and flipped_game.__board_state__[i][j]:
                pass
            else:
                symmetry = False

    # compare player locations for symmetry
    if (flipped_game.get_player_location(flipped_game.active_player) != game.get_player_location(game.inactive_player)):
        symmetry = False
    return symmetry


def check_v_symmetry(game):
    """ returns True if the board is symetric vertically"""
    symmetry = True
    # create flipped game
    flipped_game = flip_game(game, 'vertical')
    if game.height % 2 == 1:
        half_width = int(game.height/2 + 1)
    else:
        half_width = int(game.height/2)

    # compare blocked out spaces
    for i in range(game.height):
        for j in range(half_width):
            if not game.__board_state__[i][j] and not flipped_game.__board_state__[i][j]:
                pass
            elif game.__board_state__[i][j] and flipped_game.__board_state__[i][j]:
                pass
            else:
                symmetry = False

    # compare player locations for symmetry
    if (flipped_game.get_player_location(flipped_game.active_player) != game.get_player_location(game.inactive_player)):
        symmetry = False
    return symmetry

def check_d_symmetry(game):
    """ returns True if the board is symetric diagonally"""
    symmetry = True
    # create flipped game
    flipped_game = flip_game(game, 'diagonal')
    if game.height % 2 == 1:
        half_width = int(game.height/2 + 1)
    else:
        half_width = int(game.height/2)

    # compare blocked out spaces
    for i in range(game.height):
        for j in range(half_width):
            if not game.__board_state__[i][j] and not flipped_game.__board_state__[i][j]:
                pass
            elif game.__board_state__[i][j] and flipped_game.__board_state__[i][j]:
                pass
            else:
                symmetry = False

    # compare player locations for symmetry
    if (flipped_game.get_player_location(flipped_game.active_player) != game.get_player_location(game.inactive_player)):
        symmetry = False
    return symmetry

def is_symmetric(game) :

    return check_h_symmetry(game) or check_v_symmetry(game) or check_d_symmetry(game)

#####################################################################
# Assignment Code: custom scores
#####################################################################

#custom_score_weighted
def custom_score_weighted(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(9.0 * own_moves - 1.0 * opp_moves)

def custom_score_opponent(game, player):
    """ same function as as custom_player(), but only the opponent's move count
    is taken into consideration """
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return float(-1 * opp_moves)
def custom_score_distance(game, player):
    """
    same function as custom_(), but also considers the player's
    euclidean distance from the other player
    """
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    own_pos = game.get_player_location(player)
    opp_pos = game.get_player_location(game.get_opponent(player))
    dist = (own_pos[0] - opp_pos[0])^2 + (own_pos[1] - opp_pos[1])^2

    return own_moves - opp_moves + .01 * dist

def custom_score_symmetry(game, player):
    """
    same function as custom_score() but also favors symmetric moves when
    playing second on a symmetric board. Falls back on custom_score() otherwise
    """
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")

    # for odd moves, examine if symmetry could be broken
    if (game.move_count % 2 == 1 and       # second player's turn
        game.__active_player__ == player): # we're up - we went second
        # for future moves, consider if we can copy
        for move in game.get_legal_moves(game.__active_player__):
            if is_symmetric(game.forecast_move(move)):
                # symmetry can be maintained, this is a good state for 2nd player
                return 100

    # return 100 if we're second and can copy the opponent's move
    if (game.move_count % 2 == 0 and         # our move followed our opponent
        game.__active_player__ != player and # it's the opponent's move
        is_symmetric(game)):                 # we made the board symmetric
            return 100

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    own_pos = game.get_player_location(player)
    opp_pos = game.get_player_location(game.get_opponent(player))

    return float(own_moves - opp_moves)

def custom_score(game, player):
    """
    same function as custom_score() but also favors symmetric moves when
    playing second on an even sized symmetric board. Falls back on custom_score() otherwise
    """
    if game.is_winner(player):
        return float("inf")

    if game.is_loser(player):
        return float("-inf")
    if (not game.height % 2 or not game.width %2) :
        # for odd moves, examine if symmetry could be broken
        if (game.move_count % 2 == 1 and       # second player's turn
            game.__active_player__ == player): # we're up - we went second
            # for future moves, consider if we can copy
            for move in game.get_legal_moves(game.__active_player__):
                if is_symmetric(game.forecast_move(move)):
                    # symmetry can be maintained, this is a good state for 2nd player
                    return 100

        # return 100 if we're second and can copy the opponent's move
        if (game.move_count % 2 == 0 and         # our move followed our opponent
            game.__active_player__ != player and # it's the opponent's move
            is_symmetric(game)):                 # we made the board symmetric
                return 100

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))

    own_pos = game.get_player_location(player)
    opp_pos = game.get_player_location(game.get_opponent(player))
    dist = (own_pos[0] - opp_pos[0])^2 + (own_pos[1] - opp_pos[1])^2

    return float(0.1 * own_moves - 0.9 * opp_moves - .01 * dist)

#####################################################################
# Assignment Code: CustomPlayer Class
#####################################################################

class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        if self.search_depth < 0 :
            self.search_depth = sys.maxsize

        self.time_left = time_left

        # TODO: finish this function!

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves

        score = float("-inf")
        i = 0
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            best_move = [-1, -1]
            if(self.iterative == False) :
                if self.method == 'minimax' :
                   _, best_move = self.minimax(game, self.search_depth + 1, True)
                if self.method == 'alphabeta' :
                   _, best_move = self.alphabeta(game, self.search_depth + 1, True)

            else :
                for i in range(0, game.width * game.height): #self.search_depth + 1):
                    if self.method == 'minimax' :
                        score, best_move = self.minimax(game, i + 1, True)
                    if self.method == 'alphabeta' :
                        score, best_move = self.alphabeta(game, i + 1, float("-inf"), float("inf"), True)
                        if score == float("inf") :
                            break;
        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return best_move


    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_move = [-1, -1]

        #if this is the last iteration, return
        if depth == 0:
            score = self.score(game, self)
            return score, best_move

        # find our possible moves from board state
        moves = game.get_legal_moves(game.active_player)
        # if no legal moves, we have lost
        #if moves == [] :
        #    return self.score(game, self), [-1, -1]

        # initialize minmax depending on active player
        if maximizing_player == True:
            minmax_score = float("-inf")
        else:
            minmax_score = float("inf")

        # for each legal move, consider new board state
        for move in moves:
            next_game = game.forecast_move(move)

            score, _ = self.minimax(next_game, depth-1, not maximizing_player)
            if maximizing_player and score >= minmax_score:
                minmax_score = score
                best_move = move
            elif not maximizing_player and score <= minmax_score:
                minmax_score = score
                best_move = move

        return minmax_score, best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        best_move = [-1, -1]

        #if this is the last iteration, return
        if depth == 0:
            return self.score(game, self), [-1, -1]

        # find our possible moves from board state
        moves = game.get_legal_moves(game.active_player)

        # initialize minmax depending on active player
        if maximizing_player == True:
            minmax_score = float("-inf")
            new_alpha = alpha
        else:
            minmax_score = float("inf")
            new_beta = beta

        # for each legal move, consider new board state
        for move in moves:
            next_game = game.forecast_move(move)

            if maximizing_player:
                score, _ = self.alphabeta(next_game, depth-1, new_alpha, beta, not maximizing_player)
                if score >= minmax_score:
                    minmax_score = score
                    new_alpha = minmax_score
                    best_move = move
                # the parent node (a minimizing node) will
                # not pick this node or any of its children
                if minmax_score >= beta:
                    return minmax_score, best_move

            if not maximizing_player:
                score, _ = self.alphabeta(next_game, depth-1, alpha, new_beta, not maximizing_player)
                if score <= minmax_score:
                    minmax_score = score
                    new_beta = minmax_score
                    best_move = move
                # the parent node (a maximizing node) will
                # not pick this node or any of its children
                if minmax_score <= alpha:
                    return minmax_score, best_move

        return minmax_score, best_move
