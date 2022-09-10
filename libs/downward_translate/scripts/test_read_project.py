from collections import namedtuple

from downward_translate.pddl_parser import open as downward_open
from downward_translate.translate import pddl_to_sas


AbsOperator = namedtuple('AbsOperator', ['name', 'precondition', 'effect'])


def sas_literal_str_to_pddl_str(sas_literal_str):
    assert sas_literal_str != "<none of those>"         # it is not possible to have this value in precondition
    atom_str, *fact_str = sas_literal_str.split()
    fact_str = " ".join(fact_str)

    fact_str = "(" + fact_str.replace("(", " ").replace(",", "")
    if sas_literal_str.startswith("NegatedAtom"):       # parsed string here?
        fact_str = "(not " + fact_str + ")"
    return fact_str


def generate_strips_abstract_option_tasks(domain_file: str, problem_file: str):

    pddl_task = downward_open(domain_file, problem_file)
    sas_task = pddl_to_sas(pddl_task)
    num_sas_vars = len(sas_task.variables.ranges)
    num_sas_ops = len(sas_task.operators)
    goal_vars = [var for var, val in sas_task.goal.pairs]
    non_goal_vars = [var for var in range(num_sas_vars) if var not in goal_vars]

    abstract_ops = []
    check_duplicate_abstract_ops = set()

    projected_vars = goal_vars
    for sas_op in sas_task.operators:   # sorted(sas_task.operators, key=lambda x: x.name): sorted already
        precondition = []
        effect = []
        for var, pre, post, eff_cond in sas_op.pre_post:
            assert len(eff_cond) == 0, "conditional effects are not supported!"
            if var in projected_vars:
                if pre != -1:
                    precondition.append((var, pre))
                effect.append((var, post))
        for var, val in sas_op.prevail:
            if var in projected_vars:
                precondition.append((var, val))
                effect.append((var, val))
        if not effect:
            continue
        precondition = tuple(sorted(precondition))
        effect = tuple(sorted(effect))
        if precondition == effect:
            continue

        # make precondition and effect expression
        if (precondition, effect) not in check_duplicate_abstract_ops:
            check_duplicate_abstract_ops.add((precondition, effect))
            # reconstruct pddl strings for precondition and effect expression to use _parse_into_literal(string)
            pre_str = []
            for var, val in precondition:
                parsed_str = sas_task.variables.value_names[var][val]
                pddl_literal_str = sas_literal_str_to_pddl_str(parsed_str)
                pre_str.append(pddl_literal_str)
            pre_str = "(and " + " ".join(pre_str) + ")"     # only support conjunction of literals

            eff_str = []
            for var, val in effect:
                parsed_str = sas_task.variables.value_names[var][val]
                pddl_literal_str = sas_literal_str_to_pddl_str(parsed_str)
                eff_str.append(pddl_literal_str)
            eff_str = "(and " + " ".join(eff_str) + ")"

            abstract_ops.append(AbsOperator(name=sas_op.name, precondition=pre_str, effect=eff_str))

    for ind, abs_op in enumerate(abstract_ops):
        print(ind, abs_op)


if __name__ == "__main__":
    domain_file = "logistics.pddl"
    problem_file = "logistics-c2-p2_test-0.pddl"
    generate_strips_abstract_option_tasks(domain_file, problem_file)