from collections import namedtuple
from typing import Optional, List, Tuple, Set, Text

from parl_annotations.annotated_tasks import PartialState

from downward_translate.pddl_parser import open as downward_open
from downward_translate.translate import pddl_to_sas
from pyperplan.planner import ground_problem
from pyperplan.task import Operator as PyperplanOperator


class StripsOption:
    """
    option created from a strips operator
    strips represent a planning state by a set of positive literals.

    init_set: precondition of the strips operator
    term_set: effect of the strips operator, as a consequence of applying an operator
              we add facts from add effect, and removed facts in del effects.
              we also need to add invariant facts, prevails to test termination w.r.t. strips representation

    In strips operator (no negative precondition),
        is there any operator that can delete fact that does not appear in precondition? No, if so modeling is wrong
        so only the facts in the precondition can be deleted

    the role of del_set is important because they must be deleted upon reaching termination of an option
    testing for inclusion is not enough! In RL, is that case really happening?
    If add/del facts are synced due to no-negative precondition, then not a problem.
    """
    def __init__(self,
                 name: Text,
                 init_set: PartialState,
                 term_set: PartialState,
                 context: Optional[PartialState] = None):
        self.name = name
        self.init_set = init_set
        self.term_set = term_set        # in STRIPS, only add effect is relevant since del effect evaluates False
        self.del_set = init_set - term_set   # however, if del_set cannot appear in the result
        self.context = context

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
        return self.name < other.name

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return "name={}, init_set={}, term_set={}".format(self.name, self.init_set, self.term_set)


def sas_literal_str_to_pddl_str(sas_literal: Text):
    assert sas_literal != "<none of those>"         # it is not possible to have this value in precondition
    atom_str, *fact_str = sas_literal.split()
    fact_str = " ".join(fact_str)
    fact_str = fact_str.replace("(", " ").replace(",", "").replace(")", "")
    fact_str = "(" + fact_str.strip() + ")"
    # fact_str = "(" + fact_str.replace("(", " ").replace(",", "")
    if sas_literal.startswith("NegatedAtom"):       # parsed string here?
        fact_str = "(not " + fact_str + ")"
    return fact_str


StripsOperator = namedtuple('StripsOperator', ['name', 'precondition', 'effect'])


def generate_strips_option_sas_goal(domain_file: Text, problem_file: Text):
    pddl_task = downward_open(domain_file, problem_file)
    sas_task = pddl_to_sas(pddl_task)
    goal_vars = [var for var, val in sas_task.goal.pairs]

    reachable_facts = set()
    for sas_var in sas_task.variables.value_names:
        for sas_literal in sas_var:
            reachable_facts.add(sas_literal_str_to_pddl_str(sas_literal))

    strips_ops: List[StripsOperator] = []
    check_duplicate_strips_ops = set()

    for sas_op in sas_task.operators:   # sorted by name
        precondition: List[Tuple[int, int]] = []
        effect: List[Tuple[int, int]] = []
        for var, pre, post, eff_cond in sas_op.pre_post:
            assert len(eff_cond) == 0, "conditional effects are not supported!"
            if var in goal_vars:
                if pre != -1:
                    precondition.append((var, pre))
                effect.append((var, post))
        for var, val in sas_op.prevail:
            if var in goal_vars:
                precondition.append((var, val))
                effect.append((var, val))
        # skip empty effect
        if not effect:
            continue

        precondition_tuple = tuple(sorted(precondition))
        effect_tuple = tuple(sorted(effect))
        if precondition_tuple == effect_tuple:
            continue

        # make precondition and effect expression
        if (precondition_tuple, effect_tuple) not in check_duplicate_strips_ops:
            check_duplicate_strips_ops.add((precondition_tuple, effect_tuple))
            # reconstruct pddl strings for precondition and effect expression
            pre_str = []
            for var, val in precondition:
                parsed_str = sas_task.variables.value_names[var][val]
                pddl_literal_str = sas_literal_str_to_pddl_str(parsed_str)
                if pddl_literal_str in reachable_facts:
                    pre_str.append(pddl_literal_str)
            pre_partial_state = frozenset(pre_str)

            eff_str = []
            for var, val in effect:
                parsed_str = sas_task.variables.value_names[var][val]
                pddl_literal_str = sas_literal_str_to_pddl_str(parsed_str)
                if pddl_literal_str in reachable_facts:
                    eff_str.append(pddl_literal_str)
            eff_partial_state = frozenset(eff_str)

            if pre_partial_state or eff_partial_state:
                strips_ops.append(StripsOperator(sas_op.name, pre_partial_state, eff_partial_state))

    strips_options: List[StripsOption] = []
    for strips_op in strips_ops:
        option = StripsOption(strips_op.name, strips_op.precondition, strips_op.effect, None)
        strips_options.append(option)
    return strips_options


def generate_strips_option_pddl(domain_file: Text, problem_file: Text):
    pyperplan_task = generate_pyperplan_task(domain_file, problem_file)
    strips_ops: List[StripsOption] = []

    pddl_op: PyperplanOperator
    for pddl_op in sorted(pyperplan_task.operators, key=lambda x: x.name):
        prevail = set()
        for literal in pddl_op.preconditions:
            if literal not in pddl_op.del_effects:
                prevail.add(literal)
        term_set = set(pddl_op.add_effects) | prevail
        term_set = frozenset(term_set)
        option = StripsOption(pddl_op.name, pddl_op.preconditions, term_set)
        strips_ops.append(option)
    return strips_ops


def generate_pyperplan_task(domain_file: Text, problem_file: Text, project_reachable=False):
    pddl_task = downward_open(domain_file, problem_file)
    reachable_facts = set()
    if project_reachable:
        sas_task = pddl_to_sas(pddl_task)
        for sas_var in sas_task.variables.value_names:
            for sas_literal in sas_var:
                reachable_facts.add(sas_literal_str_to_pddl_str(sas_literal))
    pyperplan_task = ground_problem(domain_file, problem_file, reachable_facts)
    return pyperplan_task


