from pyperplan.planner import (
    HEURISTICS,
    SEARCHES
)


class PyperplanPlanner:
    def __init__(self, search_alg="gbf2"):
        if search_alg == "gbf2":
            self.search = SEARCHES["gbf2"]
        else:
            self.search = SEARCHES["astar2"]
        self.heuristic_class = HEURISTICS["hff"]

    def solve(self, task):
        policy = self.search(task, self.heuristic_class(task))
        return policy
