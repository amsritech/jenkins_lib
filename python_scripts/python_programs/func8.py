def choose_states(budget, costs):
    total_cost = 0
    chosen_states = []
    for state, cost in costs.items():
        if total_cost + cost > budget:
            break
        total_cost += cost
        chosen_states.append(state)
    return chosen_states


def calculate_cost(states, costs):
    total = 0
    for state in states:
        total += costs[state]
    return total


travel_budget = 3000
state_costs = {
    'California': 800,
    'Nevada': 600,
    'Arizona': 500,
    'Utah': 700,
    'Colorado': 900
}

chosen_states = choose_states(travel_budget, state_costs)
trip_cost = calculate_cost(chosen_states, state_costs)

print(f"The states included in the road trip are: {chosen_states}")
print(f"The total cost of the road trip is: ${trip_cost}")
