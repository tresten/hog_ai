"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    total, oneFound = 0, False
    for i in range(num_rolls):
        number=dice()
        if number==1 or oneFound:
            total=1
            oneFound, total=True ,1
        else:
            total+=number
    return total
    # END PROBLEM 1


def free_bacon(score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    assert score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2
    first_num=score%10
    return max(first_num, score//10)+1
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls==0:
        return free_bacon(opponent_score)
    else:
        return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def is_swap(score0, score1):
    """Return whether one of the scores is an integer multiple of the other."""
    # BEGIN PROBLEM 4
    bool=False
    if score0>1 and score1>1:
        if (score0%score1==0 or score1%score0==0):
            bool=True
        else:
            bool= False
    return bool
    # END PROBLEM 4


def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence

def always0(s1,s2):
    return 0
def always3(s1,s2):
    return 3

def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    def less_than_goal():
        return (score0<goal and score1<goal)

    def swap_if_needed():
        if is_swap(score0,score1):
                return score1,score0
        else:
            return score0,score1

    new_say=announce_lead_changes()
    turn=0
    double_turns=False
    while less_than_goal():
        dice_rolled=strategy0(score0,score1)
        score0+=take_turn(dice_rolled,score1, dice)
        score0,score1=swap_if_needed()
        say=say(score0,score1)
        turn+=1 
        if dice_rolled!=turn-1 or double_turns:
            double_turns=False
            while less_than_goal():
                dice_rolled=strategy1(score1,score0)
                score1+=take_turn(dice_rolled,score0, dice)
                score0,score1=swap_if_needed()
                say=say(score0,score1)
                turn+=1
                if dice_rolled != turn-1 or double_turns:
                    break
                else:
                    double_turns=True
            double_turns=False
        else:
            double_turns=True

    # END PROBLEM 5
    return score0, score1


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(previous_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != previous_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 6)
    Player 0 now has 10 and Player 1 now has 6
    >>> h3 = h2(6, 18) # Player 0 gets 8 points, then Swine Swap applies
    Player 0 now has 6 and Player 1 now has 18
    Player 1 takes the lead by 12
    """
    # BEGIN PROBLEM 6
    def new_func(sc0, sc1):
        call_f=f(sc0,sc1)
        call_g=g(sc0,sc1)
        return both(call_f, call_g)
    return new_func
    # END PROBLEM 6


def announce_highest(who, previous_high=0, previous_score=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(11, 0)
    >>> f2 = f1(11, 1)
    1 point! That's the biggest gain yet for Player 1
    >>> f3 = f2(20, 1)
    >>> f4 = f3(5, 20) # Player 1 gets 4 points, then Swine Swap applies
    19 points! That's the biggest gain yet for Player 1
    >>> f5 = f4(20, 40) # Player 0 gets 35 points, then Swine Swap applies
    20 points! That's the biggest gain yet for Player 1
    >>> f6 = f5(20, 55) # Player 1 gets 15 points; not enough for a new high
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def player_inpendent_process(score):
        new_high=previous_high
        difference=score-previous_score
        if previous_high<difference:
            new_high=difference
            print(("1 point!" if difference==1 else str(difference) +" points!") +" That's the biggest gain yet for Player "+str(who))
        return new_high

    def comentary_function(current_score0, current_score1):
        if who==0:
            new_high=player_inpendent_process(current_score0)
            return announce_highest(who,new_high, current_score0)
        else:
            new_high=player_inpendent_process(current_score1)
            return announce_highest(who,new_high, current_score1)
    return comentary_function
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(fn, num_samples=100):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.0
    """
    # BEGIN PROBLEM 8
    def averaging_function(*args):
        sum=0
        for i in range(num_samples):
            sum+=fn(*args)
        return sum/num_samples
    return averaging_function
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    averaged_roll=make_averaged(roll_dice,num_samples)
    bestNumberofDice=0
    bestAverage=0
    for num_dice in range(10):
        average=averaged_roll(num_dice+1, dice)
        if average>bestAverage:
            bestAverage=average
            bestNumberofDice=num_dice+1
    return bestNumberofDice

    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1





def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)

    if True:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if False:  # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"


def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    if free_bacon(opponent_score)>=margin:
        return 0
    else:
        return num_rolls
    return 4  # Replace this statement
    # END PROBLEM 10


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    if free_bacon(opponent_score)>=margin or (opponent_score>score and is_swap(free_bacon(opponent_score)+score, opponent_score)):
        return 0
    else:
        return num_rolls
    # END PROBLEM 11





def ave():
    average = [1]*11
    i = 1
    while i <= 10:
        count,total = 1,0,
        while count <= 1000: 
            the_roll = roll_dice(i)
            total += the_roll
            count += 1
        average[i] = total//100
        i += 1
    return average

AVERAGE = ave()

def save_primes():
    index = 0
    num = 3
    prime_nums = [0]*GOAL_SCORE
    prime_nums[index] = 2
    prime = True
    while num < GOAL_SCORE:
        for i in range(1,index):
            if not num % prime_nums[i]:
                prime = False
        if prime:
            index += 1
            prime_nums[index] = num
        num += 2
    return prime_nums

PRIMES = save_primes()


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    If I am in the lead, then I want to check to see if there is a way to make my score a prime number or if I can reach my goal. If not, then I want to see if it is a good idea to use the bacon method. Otherwise, my default is to roll 4 dice.
    If I am not in the lead, then I want to check to see if there is a way to make my score a factor of my opponent's score. If not, then go for highest score.
    """ 
    def is_prime(num):
        for i in PRIMES:
            if i > num:
                return i - num
        return 0

    def prob_score(goal):
        count = 1
        while count <= 10:
            if goal == AVERAGE[count]:
                return count
            count += 1
        return 0
        
    def next_factor(s,opp):
        g = 1
        while not opp%(g+s):
            g += 1
        return g

    # BEGIN PROBLEM 12
    bacon = free_bacon(opponent_score)
    need = GOAL_SCORE - score
    r = 0
    if GOAL_SCORE - opponent_score <= 10:
        if need > bacon:
            if need < 10:
                return 2
            elif need < 15:
                return 4
            elif need < 20:
                return 6
            elif need < 25:
                return 7
            elif need < 30:
                return 8
            else:
                return 10

    if need <= 10:
        if bacon >= need:
            return 0
        else:
            return 2
    else:
        if score >= opponent_score:
            need = is_prime(score)
            if bacon == need:
                return 0
            if opponent_score != 0:
                if (score+bacon)%opponent_score:
                    no_need = next_factor(opponent_score, score)
                    if no_need < 10 and no_need < bacon or no_need > (bacon+1):
                        return 0
                    if no_need == 1:
                        return 1
        elif score < opponent_score:
            need = next_factor(score, opponent_score)
            if opponent_score%(bacon+score) == 0:
                return 0
    
    r = prob_score(need)
    if r:
        return r
    return 5 

    # END PROBLEM 12


def average_win_rate(strategy, baseline=final_strategy):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()