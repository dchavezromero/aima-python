"""
SimpleProblemSolvingAgent.py

This module implements a Simple Problem-Solving Agent (SPSA) that finds
the best path between any two cities in the Romania map using four
search algorithms: Greedy Best-First Search, A* Search, Hill Climbing,
and Simulated Annealing.

Author: Dennis Chavez Romero
Course: CS 534 - Artificial Intelligence
Date: 03/08/2026
"""

from search import *
import numpy as np


class RomaniaRouteProblem(Problem):
    """
    A subclass of Problem that represents the Romania route-finding problem.
    Uses the Romania map graph and city coordinates to find paths between cities.
    """

    def __init__(self, initial, goal, graph, locations):
        """
        Initialize the Romania route problem.

        Args:
            initial: The starting city name.
            goal: The destination city name.
            graph: An UndirectedGraph representing the Romania map.
            locations: A dictionary mapping city names to (x, y) coordinates.
        """
        super().__init__(initial, goal)
        self.graph = graph
        self.locations = locations

    def actions(self, state):
        """Return a list of neighboring cities reachable from the given state."""
        return list(self.graph.get(state).keys())

    def result(self, state, action):
        """Return the city reached by taking the given action (moving to a neighbor)."""
        return action

    def path_cost(self, cost_so_far, A, action, B):
        """
        Return the total cost of the path arriving at city B from city A,
        given the cost so far to reach A.
        """
        edge_cost = self.graph.get(A, B)
        if edge_cost is None:
            return cost_so_far + float('inf')
        return cost_so_far + edge_cost

    def goal_test(self, state):
        """Return True if the given state matches the goal city."""
        return state == self.goal

    def h(self, node):
        """
        Heuristic function: returns the straight-line distance
        from the node's state to the goal city.
        """
        if self.locations and node.state in self.locations and self.goal in self.locations:
            return int(distance(self.locations[node.state], self.locations[self.goal]))
        return float('inf')

    def value(self, state):
        """
        Value function for local search algorithms.
        Returns the negative straight-line distance to the goal,
        so that states closer to the goal have higher values.
        """
        if self.locations and state in self.locations and self.goal in self.locations:
            return -distance(self.locations[state], self.locations[self.goal])
        return -float('inf')


class SimpleProblemSolvingAgent:
    """
    A Simple Problem-Solving Agent that searches for the best path
    between two cities using four different search algorithms:
    Greedy Best-First Search, A* Search, Hill Climbing, and Simulated Annealing.

    Based on Section 3.1 and 3.2 of the AIMA textbook.
    """

    ALGORITHMS = ['greedy', 'astar', 'hill_climbing', 'simulated_annealing']

    def __init__(self, graph, locations, initial, goal):
        """
        Initialize the agent with a graph, locations, and start/goal cities.

        Args:
            graph: An UndirectedGraph representing the Romania map.
            locations: A dictionary mapping city names to (x, y) coordinates.
            initial: The starting city name.
            goal: The destination city name.
        """
        self.graph = graph
        self.locations = locations
        self.initial = initial
        self.goal = goal

    def formulate_goal(self):
        """Return the goal city."""
        return self.goal

    def formulate_problem(self):
        """Create and return a RomaniaRouteProblem instance."""
        return RomaniaRouteProblem(self.initial, self.goal,
                                   self.graph, self.locations)

    def search(self, problem, algorithm_key='astar'):
        """
        Dispatch to the appropriate search algorithm based on the key.

        Args:
            problem: A RomaniaRouteProblem instance.
            algorithm_key: One of 'greedy', 'astar', 'hill_climbing',
                           or 'simulated_annealing'.

        Returns:
            A Node representing the end of the found path.
        """
        dispatch = {
            'greedy':              self.greedy_best_first_search,
            'astar':               self.a_star_search,
            'hill_climbing':       self.hill_climbing,
            'simulated_annealing': self.simulated_annealing,
        }
        if algorithm_key not in dispatch:
            raise ValueError(
                f"Unknown algorithm '{algorithm_key}'. "
                f"Choose from: {self.ALGORITHMS}"
            )
        return dispatch[algorithm_key](problem)

    def solve(self, algorithm_key='astar'):
        """
        Formulate the problem and solve it using the specified algorithm.

        Args:
            algorithm_key: The search algorithm to use.

        Returns:
            A dictionary containing the path, actions, total cost,
            and whether the goal was reached.
        """
        problem = self.formulate_problem()
        node = self.search(problem, algorithm_key)
        return self._extract_path_info(node, problem)

    def greedy_best_first_search(self, problem, display=False):
        """
        Greedy Best-First Search (Section 3.5.1).
        Expands the node closest to the goal based on the heuristic h(n).
        Uses best_first_graph_search with f(n) = h(n).
        """
        h = memoize(problem.h, 'h')
        return self._best_first_graph_search(problem, lambda n: h(n), display)

    def a_star_search(self, problem, display=False):
        """
        A* Search (Section 3.5.2).
        Expands the node with the lowest f(n) = g(n) + h(n),
        combining actual path cost and heuristic estimate.
        """
        h = memoize(problem.h, 'h')
        return self._best_first_graph_search(problem, lambda n: n.path_cost + h(n), display)

    def _best_first_graph_search(self, problem, f, display=False):
        """
        Best-First Graph Search (Figure 3.7).
        Searches by expanding the node with the lowest f value.
        Used as the foundation for both Greedy and A* search.

        Args:
            problem: The search problem.
            f: The evaluation function to minimize.
            display: If True, print search statistics.

        Returns:
            A Node representing the goal, or None if no solution is found.
        """
        f = memoize(f, 'f')
        node = Node(problem.initial)
        frontier = PriorityQueue('min', f)
        frontier.append(node)
        explored = set()

        while frontier:
            node = frontier.pop()

            if problem.goal_test(node.state):
                if display:
                    print(len(explored), "paths have been expanded and",
                          len(frontier), "paths remain in the frontier")
                return node

            explored.add(node.state)

            for child in node.expand(problem):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)
                elif child in frontier:
                    if f(child) < frontier[child]:
                        del frontier[child]
                        frontier.append(child)

        return None

    def hill_climbing(self, problem):
        """
        Hill Climbing Search (Figure 4.2).
        A local search algorithm that keeps moving to the highest-valued
        neighbor until no better neighbor exists. May get stuck at
        local maxima and not always reach the goal.
        """
        current = Node(problem.initial)
        visited = {problem.initial}

        while True:
            if problem.goal_test(current.state):
                return current

            neighbors = current.expand(problem)
            # Filter visited cities to ensure unique cities in path
            unvisited = [n for n in neighbors if n.state not in visited]
            if not unvisited:
                break

            neighbor = argmax_random_tie(unvisited,
                                         key=lambda node: problem.value(node.state))

            if problem.value(neighbor.state) <= problem.value(current.state):
                break

            visited.add(neighbor.state)
            current = neighbor

        return current

    def simulated_annealing(self, problem, schedule=exp_schedule(k=20, lam=0.005, limit=1000)):
        """
        Simulated Annealing Search (Figure 4.5).
        A local search algorithm that allows downhill moves with decreasing
        probability controlled by a temperature schedule. This enables
        escaping local maxima, though the result is not guaranteed to be optimal.
        """
        current = Node(problem.initial)
        visited = {problem.initial}

        for t in range(sys.maxsize):
            T = schedule(t)

            if T == 0:
                return current

            if problem.goal_test(current.state):
                return current

            neighbors = current.expand(problem)
            # Filter visited cities to ensure unique cities in path
            unvisited = [n for n in neighbors if n.state not in visited]
            if not unvisited:
                return current

            next_choice = random.choice(unvisited)
            delta_e = problem.value(next_choice.state) - problem.value(current.state)

            if delta_e > 0 or probability(np.exp(delta_e / T)):
                visited.add(next_choice.state)
                current = next_choice
            elif probability(np.exp(-delta_e / T)):
                visited.add(next_choice.state)
                current = next_choice

        return current

    @staticmethod
    def _extract_path_info(node, problem):
        """
        Extract path information from a search result node.

        Args:
            node: The final Node returned by a search algorithm.
            problem: The problem that was solved.

        Returns:
            A dictionary with keys:
                - path: List of city names from start to end.
                - actions: List of actions taken.
                - total_cost: Total path cost.
                - reached_goal: Whether the goal was reached.
        """
        if node is None:
            return {
                'path': [], 'actions': [],
                'total_cost': float('inf'), 'reached_goal': False
            }
        path_nodes = node.path()
        return {
            'path':         [n.state for n in path_nodes],
            'actions':      node.solution(),
            'total_cost':   node.path_cost,
            'reached_goal': problem.goal_test(node.state)
        }