# Define a function to calculate the trip cost.
def calculate_trip_cost(countries, country_costs):
    total_cost = 0
    for country in countries:
        total_cost += country_costs[country]
    return total_cost

# Presuming the chosen_countries and their costs
chosen_countries = ['France', 'Italy', 'Spain']
country_costs = {'France': 1200, 'Italy': 950, 'Spain': 800}

# Call the function
trip_cost = calculate_trip_cost(chosen_countries, country_costs)
print(f"The total cost of the trip is: ${trip_cost}")