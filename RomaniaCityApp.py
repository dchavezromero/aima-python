"""
RomaniaCityApp.py

A console application that uses the SimpleProblemSolvingAgent to find
the best path between any two Romania cities using Greedy Best-First Search,
A* Search, Hill Climbing, and Simulated Annealing.

Author: Dennis Chavez Romero
Course: CS 534 - Artificial Intelligence
Date: 03/08/2026
"""

from search import romania_map
from SimpleProblemSolvingAgent import SimpleProblemSolvingAgent


def main():
    """Main function that runs the Romania City path-finding application."""
    sorted_cities = sorted(romania_map.locations.keys())
    print()
    print("Here are all the possible Romania cities that can be traveled:\n")
    print(sorted_cities)

    while True:
        print()

        # Prompt user for origin and destination until valid pair is entered
        while True:
            origin = get_valid_city(sorted_cities, True)
            print()
            destination = get_valid_city(sorted_cities)

            if destination == origin:
                print("\nThe same city can't be both origin and destination. Please try again.\n")
            else:
                break

        # Create agent and run all four search algorithms
        agent = SimpleProblemSolvingAgent(romania_map, romania_map.locations,
                                         origin, destination)

        print()
        run_and_display(agent, 'greedy',              'Greedy Best-First Search')
        run_and_display(agent, 'astar',               'A* Search')
        run_and_display(agent, 'hill_climbing',        'Hill Climbing Search')
        run_and_display(agent, 'simulated_annealing',  'Simulated Annealing Search')

        # Ask user if they want to search again
        again = input("Would you like to find the best path between the other two cities? ")
        if again.strip().lower() != 'yes':
            print("\nThank You for Using Our App")
            break


def get_valid_city(city_list, is_origin=False):
    """
    Prompt the user to enter a valid city name from the Romania map.

    Args:
        city_list: A sorted list of valid city names.
        is_origin: If True, prompt for origin city; otherwise destination.

    Returns:
        A valid city name string.
    """
    if is_origin:
        prompt = "Please enter the origin city: "
    else:
        prompt = "Please enter the destination city: "

    city = input(prompt).strip()
    while city not in city_list:
        city = input(f"\nCould not find {city}, please try again: ").strip()
    return city

def run_and_display(agent, algorithm_key, display_name):
    """
    Run a search algorithm and display the results.

    Args:
        agent: A SimpleProblemSolvingAgent instance.
        algorithm_key: The algorithm identifier string.
        display_name: The display name for the algorithm in output.
    """
    result = agent.solve(algorithm_key)
    path_str = " → ".join(result['path'])
    cost = result['total_cost']

    print(display_name)
    print(path_str)
    print(f"Total Cost: {cost}")
    if not result['reached_goal']:
        print("(Goal not reached)")
    print()


if __name__ == "__main__":
    main()