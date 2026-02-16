# Partial function to add another country to your trip plan if it fits the budget.
def add_country_if_fits_budget(budget, current_cost, new_country_cost):
    # TODO: Add the missing code to check if you can add the new country without exceeding the budget
    if current_cost + new_country_cost <= budget:
        return True
    else:
        return False

# Assuming sample values for demonstration
current_budget = 5000
current_cost = 3000
new_country_cost = 1200

# Check if adding the new country fits the budget
can_add_country = add_country_if_fits_budget(current_budget, current_cost, new_country_cost)
print(f"Can add new country within budget? {can_add_country}")