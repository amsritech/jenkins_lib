# Define multiple functions and use them together to solve a problem.
def choose_countries(budget, costs):
    total_cost = 0
    chosen_countries = []
    for country, cost in costs.items():
        if total_cost + cost > budget:
            break
        total_cost += cost
        chosen_countries.append(country)
    return chosen_countries

def calculate_cost(countries, costs):
    total_cost = 0
    for country in countries:
        total_cost += costs[country]
    return total_cost

# Assuming sample data for budget and costs for demonstration
travel_budget = 5000
country_costs = {'France': 1200, 'Italy': 1500, 'Spain': 800, 'Germany': 900, 'Greece': 1100}

chosen_countries = choose_countries(travel_budget, country_costs)
trip_cost = calculate_cost(chosen_countries, country_costs)

print(f"The countries included in the trip are: {chosen_countries}")
print(f"The total cost of the trip is: ${trip_cost}")