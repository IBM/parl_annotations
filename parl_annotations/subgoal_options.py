"""
What is subgoal? How to obtain such subgoals?

From HDQN or similar, we assume that subgoals are collection of states; mostly it's a RL state.
Deriving useful subgoals in an abstract state space is a research topic.
We can consider two kinds of annotations.
1. declarative annotation like PDDL planning task that provides knoweldge about "what"
2. procedural annotation likt  HTN task that provides knowledge about "how"
We view subgoals belong to "how" kind since it is a incomplete plan or solution for solving problem.

How to collect states as subgoals and represent them?
* if a state is labelled or it has symbolic representation, we can manipulate such symbols
* if state is a feature vector, it is not obvious how to achieve this.
  * consider MZ domain, one probably want to store frames but it doesn't make sense.
  * One should introduce additional FE to indirectly obtain something corresponds to symbolic representation.

* Here, assume that env is a GoalEnv, so we have **goal test function using environment information**
  * otherwise, we use symbolic labels (planning state)
  * subgoal options don't have initation set since it can be initated anywhere in the state space

"""

from typing import Optional, List, Tuple, Set, Text, Callable


class SubgoalOption:
    """
    option class for Hierarchical DQN or similar that
    use the subgoals as termination set of options
    """
    def __init__(self, name: Text, subgoal, goal_test: Optional[Callable]=None):
        self.name = name
        self.subgoal = subgoal     # states can be labels, features, etc
        if isinstance(goal_test, Callable):
            self.goal_test = goal_test
        else:
            self.goal_test = lambda state: state == self.subgoal


    def is_terminated(self, state):
        return self.goal_test(state, self.subgoal)     # term_set can be subgoal expression

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "name={}, subgoal={}".format(self.name, self.subgoal)


