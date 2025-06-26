from pulp import *

def minimize(required_items, combos):

    '''
    Format

    required_items = {
    "burger": 2,
    "fries": 3
    }
    
    combos = [
        {"name": "Combo1", "items": {"burger": 1}, "price": 5},
        {"name": "Combo2", "items": {"burger": 1, "fries": 1}, "price": 7},
        {"name": "Combo3", "items": {"fries": 1}, "price": 3}
    ]
    '''
    prob = LpProblem("MealComboCost", LpMinimize)

    combo_vars = {
        combo["name"]: LpVariable(combo["name"], 0, cat="Integer")
        for combo in combos
    }

    prob += lpSum(combo_vars[combo["name"]] * combo["price"] for combo in combos)

    for item in required_items:
        prob += lpSum(
            combo_vars[combo["name"]] * combo["items"].get(item, 0)
            for combo in combos
        ) == required_items[item], f"Requirement_{item}"

    prob.solve()

    print(f"Status: {LpStatus[prob.status]}")
    print(f"Total Cost: {value(prob.objective)}")

    for combo in combos:
        count = combo_vars[combo["name"]].varValue
        if count > 0:
            print(f"Use {int(count)} of {combo['name']}")
