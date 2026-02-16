# Define data
travel_budget = 5000
country_costs = {
    "France": 1000,
    "Italy": 800,
    "Spain": 700,
    "Germany": 500,
    "Japan": 1200
}

def choose_countries(travel_budget, country_costs):
    total_cost = 0
    chosen_countries = []

    for country, cost in country_costs.items():
        if total_cost + cost > travel_budget:
            break
        total_cost += cost
        chosen_countries.append(country)

    return chosen_countries




# Call function
chosen_countries = choose_countries(travel_budget, country_costs)
print(chosen_countries)
