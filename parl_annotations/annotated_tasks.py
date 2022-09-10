from abc import ABC, abstractmethod
from typing import FrozenSet, Text, Optional

Literal = Text
PartialState = FrozenSet[Literal]


class AnnotatedTask(ABC):
    def __init__(self):
        self.env = None
        self.domain_file = None
        self.problem_file = None
        self.planning_task = None
        self.planning_facts = None
        self.strips_options = None

    @abstractmethod
    def rl_obs_to_pl_state(self, obs, *args, **kwargs) -> PartialState:
        """state mapping from rl observation to planning state"""

    @abstractmethod
    def set_pl_initial_state_from_obs(self, obs):
        """set planning init state"""

    @abstractmethod
    def set_pl_goal_from_obs(self, obs):
        """set planning goal state"""

    @abstractmethod
    def get_pl_initial_state(self):
        """get planning init state"""

    @abstractmethod
    def get_pl_goal(self):
        """get planning goal state"""

    @abstractmethod
    def dist_states(self, state1: PartialState, state2: PartialState, ignored: Optional[PartialState]):
        """distance between two planning states without ignored facts"""


class SubgoalTask(ABC):
    def __init__(self):
        self.env = None
        self.subgoal_options = None
        self.num_subgoals = None        # number of actions for the highlevel agent

    @abstractmethod
    def generate_subgoal_options(self):
        """ create subgoal options; term set is 1 rl state """

    @abstractmethod
    def subgoal_test(self, subgoal_index, state):
        """ test if state is subgoal index """