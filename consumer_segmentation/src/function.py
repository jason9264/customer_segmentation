import pandas as pd

#Create score assigner for reading amount columns and converting to integer
def assign_score(value):
    if value == "VERY LOW":
        return 1
    elif value == "LOW":
        return 2
    elif value == "MID":
        return 3
    elif value == "HIGH":
        return 4
    elif value == "VERY HIGH":
        return 5
    else:
        return 0 

#Create value assigner for low, medium, high
def assign_value(score, total):
    if score != 0:
        ratio = score / total
        if ratio <= 0.33:
            return "low" # on average LOW or VERY LOW
        elif ratio <= 0.66: 
            return "medium" # on average LOW, MID, or HIGH
        elif ratio <= 1:
            return "high" # on average HIGH or VERY HIGH
        else:
            return ValueError 
    else:
        return "low"

#Assign status used for family status calculations
def assign_status(score, total):
    if score != 0:
        ratio = score / total
        if ratio > .4:
            return "family" # on average LOW, MID, HIGH, or VERY HIGH
        elif ratio <= .4:
            return "individual" # on average VERY LOW
    else:
        return "individual"

# Takes in a dictionary of a members attributes
def process_income_attributes(attributes):
    # Process Current Income Attributes (rules)
    income_score = assign_score(attributes.get("income~both~salary/regular income-cat", 0))
    active_income_score = assign_score(attributes.get("active_income~sum", 0))
    income_bank_salary_score = assign_score(attributes.get("income~bank~salary/regular income-cat", 0))
    income_bank_other_score = assign_score(attributes.get("income~bank~other income-cat", 0))

    # Exclude non read in values (they will be zero if they dont exist in data) and find the sum
    income_attributes = [income_score, active_income_score, income_bank_salary_score, income_bank_other_score]
    income_attributes = [score for score in income_attributes if score != 0]
    income = sum(income_attributes)
    
    # Calls assign_value function to process and give categorical rating
    return assign_value(income, len(income_attributes) * 5)

# Takes in a dictionary of a members attributes and processes the spending category rules
def process_spending_attributes(attributes):
    # Process Current Spending Attributes (rules)
    bargain_groceries_score = assign_score(attributes.get("bargain_groceries~sum", 0))
    discount_stores_score = assign_score(attributes.get("spend~both~discount stores@monthly~a", 0))
    personal_family_score = assign_score(attributes.get("bargain_personal/family~sum", 0))
    bargain_discount_stores_score = assign_score(attributes.get("spend~both~bargain_discount_and_wholesale_stores", 0))
    mass_market_pet_services_score = assign_score(attributes.get("spend~both~mass_market_pet_services", 0))
    premium_restaurants_score = assign_score(attributes.get("premium_restaurants~sum", 0))
    premium_electronics_score = assign_score(attributes.get("premium_electronics/general_merchandise~sum", 0))
    premium_department_stores_score = assign_score(attributes.get("spend~both~premium_department_stores", 0))
    premium_travel_score = assign_score(attributes.get("premium_travel~sum", 0))

    # Exclude non read in values (they will be zero if they dont exist in data) and find the sum
    spending_attributes = [bargain_groceries_score, discount_stores_score, personal_family_score,
                           bargain_discount_stores_score, mass_market_pet_services_score,
                           premium_restaurants_score, premium_electronics_score,
                           premium_department_stores_score, premium_travel_score]
    spending_attributes = [score for score in spending_attributes if score != 0]
    disc_spend = sum(spending_attributes)

    return assign_value(disc_spend, len(spending_attributes) * 5)

# Takes in a dictionary of a members attributes and processes the family attributes
def process_family_attributes(attributes):
    # Process Current family Attributes (rules)
    elementary_school_score = assign_score(attributes.get("elementary_middle_school~sum", 0))
    child_expenses_score = assign_score(attributes.get("spend~card~child/dependent expenses", 0))
    primary_secondary_schools_score = assign_score(attributes.get("spend~both~primary and secondary schools", 0))
    daycare_preschools_score = assign_score(attributes.get("spend~bank~day care and preschools", 0))
    income_bank_children_score = assign_score(attributes.get("income~bank~children", 0))
    income_bank_child_support_score = assign_score(attributes.get("income~bank~child support", 0))
    spend_child_score = assign_score(attributes.get("spend~both~children@monthly~a", 0))
    spend_teen_fashion_score = assign_score(attributes.get("spend~both~bargain_teen_and_young_adult_fashion", 0))
    spend_university_score = assign_score(attributes.get("spend~both~colleges_and_universities@monthly~a", 0))
    spend_bank_education_score = assign_score(attributes.get("spend~bank~education-cat", 0))
    spend_both_daycare_score = assign_score(attributes.get("spend~both~daycare/preschool", 0))
    spend_both_toys_score = assign_score(attributes.get("spend~both~toys/baby_stuff", 0))

    # Exclude non read in values (they will be zero if they dont exist in data) and find the sum
    family_attributes = [elementary_school_score, 
                         child_expenses_score,
                         primary_secondary_schools_score, 
                         daycare_preschools_score,
                         income_bank_children_score, 
                         income_bank_child_support_score,
                         spend_child_score,
                         spend_teen_fashion_score,
                         spend_university_score,
                         spend_bank_education_score,
                         spend_both_daycare_score,
                         spend_both_toys_score]
    family_attributes = [score for score in family_attributes if score != 0]
    family = sum(family_attributes)

    # Calls assign_status function to process and give categorical rating
    return assign_status(family, len(family_attributes) * 5)

# Processes data by calling processing functions for attributes based on rules defined in them.
def process_data(data):
    scores = {}

    for unique_mem_id, attributes in data.items():
        scores[unique_mem_id] = {
            "Discretionary": process_spending_attributes(attributes),
            "Income": process_income_attributes(attributes),
            "Family": process_family_attributes(attributes)
        }

    return scores

#Evaluates the dictionary and places each unique_mem_id in each category
def evaluator(dictionary, granularity):
    #Iterate and read each unique_mem_id nest key value pair
    #Grab first letters for each key to append to corresponding list

    persona_lists = {}

    for unique_mem_id, attributes in dictionary.items():
        if granularity == "group":
            list_name = persona_group(attributes['Income'], attributes['Family'])
        else:
            list_name = persona_name(attributes['Discretionary'], attributes['Income'], attributes['Family'])

        if list_name not in persona_lists:
            persona_lists[list_name] = []
        
        persona_lists[list_name].append(unique_mem_id)

    return persona_lists

def persona_group(income, family):
    persona_group_name = ""
    if income == "low":
        persona_group_name += "Striving "
    elif income == "medium":
        persona_group_name += "Mainstream "
    else:
        persona_group_name += "Affluent "
    if family == "family":
        persona_group_name += "Families"        
    else:
        persona_group_name += "Individuals"
    return persona_group_name    
        
def persona_name(discretionary, income, family):
    persona_name_name = ""
    if income == "low":
        persona_name_name += "Striving "
    elif income == "medium":
        persona_name_name += "Mainstream "
    else:
        persona_name_name += "Affluent "
    if discretionary == "low":
        persona_name_name += "Cautious "
    elif discretionary == "medium":
        persona_name_name += "Budgeting "
    else:
        persona_name_name += "Lavish "        
    if family == "family":
        persona_name_name += "Families"        
    else:
        persona_name_name += "Individuals"
    return persona_name_name