"""
AP Pathfinder

A Python-based academic planning system that generates personalized
AP course recommendations and predicts academic outcomes based on
a student's academic profile.
"""

# ---------------------------
# 1. IMPORTS & LIBRARIES
# ---------------------------
import sys


# ---------------------------
# 2. PROCEDURES
# ---------------------------
def get_valid_boolean(question, true_value, false_value):
    """
    Prompts the user for a boolean input until they enter either the 'true_value' or 'false_value'.
    Returns the valid input as a string.
    """
    while True:
        user_input = input(question).lower().strip()
        if user_input == true_value or user_input == false_value:
            return user_input
        print(f"Invalid input. Please enter '{true_value}' or '{false_value}' only.\n")

def get_valid_number_in_range(question, min_value, max_value, fail_threshold):
    """
    Prompts the user for a numeric input within the given range (min_value to max_value).
    If the input is below the fail_threshold, the program exits.
    Returns the valid number.
    """
    while True:
        try:
            user_input = int(input(question).strip())
            if min_value <= user_input <= max_value:
                break
            print(f"Invalid range. Enter a value between {min_value} and {max_value}.\n")
        except ValueError:
            print("Invalid input. Please enter a numeric value using digits only (no decimals).\n")
    if user_input < fail_threshold:
        print(f"Based on the minimum requirement of {fail_threshold}, you are not currently eligible to proceed.")
        sys.exit()
    return user_input

def get_valid_string(question):
    """
    Prompts the user for a string input containing only letters and spaces.
    Repeats until valid input is received and returns the string.
    """
    while True:
        user_input = input(question).strip()
        if user_input.replace(" ", "").isalpha():
            return user_input
        print("Invalid input. Use letters only (no numbers or special characters).\n")

def get_valid_input_in_list(question, options_list):
    """
    Prompts the user for input that must match one of the provided options in a list.
    Returns the valid selection.
    """
    while True:
        user_input = input(question).lower().strip()
        for item in options_list:
            if user_input == item.lower():
                return item
        print(f"Invalid input. Please match the required format (e.g., {options_list[0]}).\n")
    
def remove_item_from_list(lst, item):
    """
    Safely removes an item from a list if it exists.
    If the item is not present, nothing happens.
    """
    try:
        lst.remove(item)
    except ValueError:
        pass
    
def input_ap_exam_marks(min_exams, max_exams, student_data, all_courses_key, taken_exam_key, exam_scores_key):
    """
    Prompts the user to enter AP exams they have taken and the scores for each.
    Updates the student_data dictionary with the taken exams and their corresponding scores.
    Returns the total number of exams taken.
    """
    if get_valid_boolean("Have you taken any AP exams yet? (Yes/No): ", "yes", "no") == "yes":
        total_exams_taken = get_valid_number_in_range(f"How many AP exams have you taken in total? ({min_exams}-{max_exams}): ", min_exams, max_exams, 0)
        print(f"\nGreat! Since you've taken {total_exams_taken} AP(s), please enter the name of each one below (e.g., AP Calculus AB).")
        for i in range(total_exams_taken):
            while True:
                exam_taken = get_valid_input_in_list(f"Enter the name for AP #{i + 1}: ", student_data[all_courses_key])
                if exam_taken not in student_data[taken_exam_key]:
                    student_data[taken_exam_key].append(exam_taken)
                    break
                print(f"   ↳ {exam_taken} is already recorded. Please provide a different exam for slot #{i + 1}.\n")
        print(f"\nImpressive! Taking: {', '.join(student_data[taken_exam_key])} shows great rigor.\n\n")
        for exam_taken in student_data[taken_exam_key]:
            student_data[exam_scores_key][exam_taken] = get_valid_number_in_range(f"What score did you get on the {exam_taken} exam? (1-5): ", 1, 5, 0)
        print(f"\n\nYou have taken {total_exams_taken} AP exam(s).")
    else:
        total_exams_taken = 0
        print("No problem! APs aren't the only way to demonstrate your academic strengths.\n")
    print()
    return total_exams_taken

def tier_skips(student_data, chosen_branch, tier_skips_key, removed_exams_key, gpa, english_score, math_score):
    """
    Applies course skips based on GPA and standardized test performance.
    Updates removed_exams_key with eligible skipped courses and adjusts course path for advanced placement.
    """
    if math_score >= 700 or gpa >= 94:
        student_data[removed_exams_key].extend(student_data[tier_skips_key]["stem"])  
        print("💡 General STEM Excellence: Removing introductory electives.")                 
    if english_score >= 720 or gpa >= 95:
        student_data[removed_exams_key].extend(student_data[tier_skips_key]["humanities"])
        print("✍️ Humanities Excellence: Skipping introductory English Language.")
    if math_score >= 750 or gpa >= 96:
        student_data[removed_exams_key].extend(student_data[tier_skips_key]["math"])
        print("📐 Math Excellence: Fast-tracking past Precalculus.")
    if math_score >= 770 or gpa >= 97:
        student_data[removed_exams_key].extend(student_data[tier_skips_key]["physics"])
        print("🚀 Physics Excellence: Skipping Algebra-Physics for Physics C.")
        student_data[f"{chosen_branch}_list"].insert(student_data[f"{chosen_branch}_list"].index("AP Calculus AB"), "AP Calculus BC")
        student_data[f"{chosen_branch}_list"].remove("AP Calculus AB")
        student_data[f"{chosen_branch}_list"].pop(student_data[f"{chosen_branch}_list"].index("AP Calculus BC",(student_data[f"{chosen_branch}_list"].index("AP Calculus BC"))+1))
        

def process_exam_credits(student_data, total_exams_taken, exam_scores_key, course_hierarchies_key, removed_exams_key):
    """
    Processes AP exam scores and applies credit-based course removals and sequence skipping.
    Updates removed_exams_key based on passing scores and course hierarchies.
    """    
    if total_exams_taken > 0:
        for exam_taken in student_data[exam_scores_key]:
            if student_data[exam_scores_key][exam_taken] >= 3:
                if exam_taken not in student_data[removed_exams_key]:
                    student_data[removed_exams_key].append(exam_taken)
                for exam_sequence in student_data[course_hierarchies_key].values():
                    if exam_taken in exam_sequence:
                        index = exam_sequence.index(exam_taken)
                        remaining_sequence = exam_sequence[index+1:]
                        for exams_to_skip in remaining_sequence:
                            if exams_to_skip not in student_data[removed_exams_key]:
                                student_data[removed_exams_key].append(exams_to_skip)
            else:
                if exam_taken in student_data[removed_exams_key]:
                        remove_item_from_list(student_data[removed_exams_key], exam_taken)    
                        
def remove_courses(student_data, chosen_branch, removed_exams_key):
    """
    Removes courses from the recommended branch list based on previously determined exclusions.
    Returns the total number of removed courses.
    """    
    removed_exams_count = 0
    for removed_exam in student_data[removed_exams_key]:
            remove_item_from_list(student_data[f"{chosen_branch}_list"], removed_exam)
            removed_exams_count += 1
    if removed_exams_count !=0:
        print(f"\n{removed_exams_count} course(s) removed from your recommended sequence based on prior APs and excellence.\n\n")
    return removed_exams_count
       
def recommend_ap_sequence(chosen_branch, student_data, recommendation_key, num_exams_to_take):
    """
    Prints a recommended sequence of AP exams for the user's chosen branch.
    Updates the recommendation list in the student_data dictionary.
    """
    print("\nTo build a competitive college application while maintaining a balanced schedule, I recommend following this sequence:\n")
    for i in range(num_exams_to_take):
        print(f"{i + 1}. {student_data[f'{chosen_branch}_list'][i]}")
        student_data[recommendation_key].append(student_data[f"{chosen_branch}_list"][i])
    print("\n")
    
def predict_ap_scores(question, student_data, recommendation_key, standardized_score, max_score):
    """
    Predicts future AP scores based on the user's profile and math score.
    Prints the predicted score for each course in the prediction_list.
    Returns the user's yes/no response as a string.
    """
    item_number = 0
    prediction_dictionary = {}
    user_response = get_valid_boolean(question, "yes", "no")
    if user_response == "yes":
        print("💡 Keep in mind: These predicted scores are achievable if you maintain consistent effort and dedication!\n")
        for exam_name in student_data[recommendation_key]:
            if standardized_score >= max_score * 0.95:
                    prediction_dictionary[exam_name] = 5
            elif standardized_score >= max_score * 0.9:
                    prediction_dictionary[exam_name] = 4
            else:
                prediction_dictionary[exam_name] = 3
        for exam_name, predicted_score in prediction_dictionary.items():
            item_number += 1
            print(f"{item_number}. {exam_name:<66} Predicted AP Score: {predicted_score:>2}")
    return user_response


# --------------------------------------------------------------------
# STUDENT DATA & BRANCH-SPECIFIC AP SEQUENCES (Collections)
# --------------------------------------------------------------------
"""
# The following lists were curated based on real-world engineering prerequisites:
# 1. Dependency Logic: Calculus-based Physics (Physics C) is placed only after 
#    Calculus AB/BC to ensure mathematical readiness.
# 2. Major Specifics:
#    - Computer: Prioritizes early Logic/CS Principles.
#    - Electrical/Mechanical: Prioritizes Physics 2 (Fluids/Thermodynamics) and Chemistry.
#    - Civil: Prioritizes Environmental Science and Statistics for urban planning.
# 3. Efficiency: Hard sciences are front-loaded to clear university 'weed-out' 
#    requirements, while Humanities/Arts are placed later as degree-completion utility.
"""
student_data = {
    "engineering_branches": (
        "mechanical", 
        "computer", 
        "civil", 
        "electrical"
    ),
    "all_ap_courses": (
        "AP Calculus AB", "AP Calculus BC", "AP Statistics", "AP Precalculus", 
        "AP Biology", "AP Chemistry", "AP Environmental Science", "AP Physics 1", 
        "AP Physics 2", "AP Physics C: Mechanics", "AP Physics C: Electricity and Magnetism", 
        "AP Computer Science A", "AP Computer Science Principles", 
        "AP English Language and Composition", "AP English Literature and Composition", 
        "AP United States History", "AP World History", "AP European History", 
        "AP Human Geography", "AP Government and Politics: US", 
        "AP Government and Politics: Comparative", "AP Art History", "AP Music Theory", 
        "AP 2-D Art and Design", "AP 3-D Art and Design", "AP Drawing", 
        "AP Spanish Language", "AP French Language", "AP Chinese Language", 
        "AP Latin", "AP Seminar", "AP Research", "AP Psychology", 
        "AP Microeconomics", "AP Macroeconomics", "AP African American Studies", 
        "AP Japanese Language and Culture", "AP German Language and Culture", 
        "AP Italian Language and Culture", "AP Spanish Literature and Culture"
    ),
    "computer_list": [
        "AP Precalculus", "AP Physics 1", "AP Computer Science Principles", 
        "AP English Language and Composition", "AP Chemistry", "AP Physics 2", 
        "AP Calculus AB", "AP Physics C: Mechanics", "AP Computer Science A", 
        "AP Calculus BC", "AP Physics C: Electricity and Magnetism", "AP Statistics", 
        "AP Microeconomics", "AP Macroeconomics", "AP Psychology", "AP Seminar", 
        "AP Research", "AP Government and Politics: US", "AP United States History", 
        "AP World History", "AP Human Geography", "AP Environmental Science", 
        "AP Biology", "AP Art History", "AP Music Theory", "AP Drawing", 
        "AP 2-D Art and Design", "AP 3-D Art and Design", "AP English Literature and Composition", 
        "AP Spanish Language", "AP French Language", "AP Chinese Language", 
        "AP Latin", "AP Japanese Language and Culture", "AP German Language and Culture", 
        "AP Italian Language and Culture", "AP Spanish Literature and Culture", 
        "AP African American Studies", "AP European History", "AP Government and Politics: Comparative"
    ],
    "electrical_list": [
        "AP Precalculus", "AP Physics 1", "AP Chemistry", "AP English Language and Composition", 
        "AP Physics 2", "AP Calculus AB", "AP Physics C: Mechanics", "AP Calculus BC", 
        "AP Physics C: Electricity and Magnetism", "AP Computer Science Principles", 
        "AP Computer Science A", "AP Statistics", "AP Microeconomics", "AP Macroeconomics", 
        "AP Psychology", "AP Seminar", "AP Research", "AP Government and Politics: US", 
        "AP United States History", "AP World History", "AP Human Geography", 
        "AP Environmental Science", "AP Biology", "AP Art History", "AP Music Theory", 
        "AP Drawing", "AP 2-D Art and Design", "AP 3-D Art and Design", 
        "AP English Literature and Composition", "AP Spanish Language", "AP French Language", 
        "AP Chinese Language", "AP Latin", "AP Japanese Language and Culture", 
        "AP German Language and Culture", "AP Italian Language and Culture", 
        "AP Spanish Literature and Culture", "AP African American Studies", 
        "AP European History", "AP Government and Politics: Comparative"
    ],
    "mechanical_list": [
        "AP Precalculus", "AP Physics 1", "AP Chemistry", "AP English Language and Composition", 
        "AP Physics 2", "AP Calculus AB", "AP Physics C: Mechanics", "AP Calculus BC", 
        "AP Physics C: Electricity and Magnetism", "AP Statistics", "AP Computer Science Principles", 
        "AP Computer Science A", "AP Microeconomics", "AP Macroeconomics", "AP Psychology", 
        "AP Seminar", "AP Research", "AP Government and Politics: US", "AP United States History", 
        "AP World History", "AP Human Geography", "AP Environmental Science", "AP Biology", 
        "AP Art History", "AP Music Theory", "AP Drawing", "AP 2-D Art and Design", 
        "AP 3-D Art and Design", "AP English Literature and Composition", "AP Spanish Language", 
        "AP French Language", "AP Chinese Language", "AP Latin", "AP Japanese Language and Culture", 
        "AP German Language and Culture", "AP Italian Language and Culture", 
        "AP Spanish Literature and Culture", "AP African American Studies", 
        "AP European History", "AP Government and Politics: Comparative"
    ],
    "civil_list": [
        "AP Precalculus", "AP Physics 1", "AP Chemistry", "AP Environmental Science", 
        "AP English Language and Composition", "AP Statistics", "AP Calculus AB", 
        "AP Physics C: Mechanics", "AP Human Geography", "AP Physics 2", 
        "AP Physics C: Electricity and Magnetism", "AP Calculus BC", "AP Microeconomics", 
        "AP Macroeconomics", "AP Computer Science Principles", "AP Computer Science A", 
        "AP Seminar", "AP Research", "AP Biology", "AP Psychology", "AP Government and Politics: US", 
        "AP United States History", "AP World History", "AP European History", "AP Art History", 
        "AP Music Theory", "AP Drawing", "AP 2-D Art and Design", "AP 3-D Art and Design", 
        "AP English Literature and Composition", "AP Spanish Language", "AP French Language", 
        "AP Chinese Language", "AP Latin", "AP Japanese Language and Culture", 
        "AP German Language and Culture", "AP Italian Language and Culture", 
        "AP Spanish Literature and Culture", "AP African American Studies", 
        "AP Government and Politics: Comparative"
    ],
    "taken_ap": [],
    "ap_scores": {},
    "tier_skips": {
        "stem": ["AP Computer Science Principles", "AP Government and Politics: US"],
        "humanities": ["AP English Language and Composition"],
        "math": ["AP Precalculus"],
        "physics": ["AP Physics 1", "AP Physics 2", "AP Calculus AB"]
    },
    "course_hierarchies": {
        "math": ["AP Calculus BC", "AP Calculus AB", "AP Precalculus"],
        "physicsmechanics": ["AP Physics C: Mechanics", "AP Physics 1"],
        "physicse&m": ["AP Physics C: Electricity and Magnetism", "AP Physics 2"],
        "cs": ["AP Computer Science A", "AP Computer Science Principles"],
        "econ": ["AP Macroeconomics", "AP Microeconomics"],
        "english": ["AP English Literature and Composition", "AP English Language and Composition"],
        "history": ["AP United States History", "AP World History", "AP Human Geography"]
    },
    "removed_exams": [],
    "Recommendation": []
}


# --------------------------------------------
# 4. MAIN PROGRAM EXECUTION (Entry Point)
# --------------------------------------------

# -----------------------------
# User Introduction
# -----------------------------:
print("Welcome! Before we dive into your future...")
student_name = get_valid_string("What should we call you? ")
print(f"Nice to have you here, {student_name}!\n\n")

# -----------------------------
# Academic Interest Selection
# -----------------------------
print("First, tell me a little about your academic interests.")
chosen_branch = get_valid_input_in_list("Which Engineering branch are you most interested in: Mechanical, Computer, Civil, Electrical? ", student_data["engineering_branches"])
print(f"Excellent! {chosen_branch.title()} Engineering is a competitive major. I'll help you plan your schedule accordingly.\n\n")

# -----------------------------
# Student Academic Status
# -----------------------------
sat_taken = get_valid_boolean("Have you taken the SAT exam yet? (Yes/No): ", "yes", "no")
if sat_taken == "yes":
    print()
    math_score = get_valid_number_in_range("What was your Math score? (200-800): ", 200, 800, 650)
    english_score = get_valid_number_in_range("What was your English score? (200-800): ", 200, 800, 480)
    print(f"Got it! Your total SAT score is: {math_score + english_score}\n")
    gpa = 0
else:
    gpa = get_valid_number_in_range("\nWhat is your current school unweighted GPA percentage? (60-100): ", 60, 100, 75)
    math_score = 0
    english_score = 0
    print(f"Thanks! We'll use your GPA of {gpa}% to guide recommendations.\n")

# -----------------------------
# AP Exams Already Taken
# -----------------------------
total_exams_taken = input_ap_exam_marks(1, 40, student_data, "all_ap_courses", "taken_ap", "ap_scores")

#------------------------------
# Apply Tier-Based Course Skips
#------------------------------
tier_skips(student_data, chosen_branch, "tier_skips", "removed_exams", gpa, english_score, math_score)

#------------------------------
# Process AP Credits
#------------------------------
process_exam_credits(student_data, total_exams_taken, "ap_scores", "course_hierarchies", "removed_exams")

# -----------------------------
# Apply Course Removals
# -----------------------------
removed_courses_count = remove_courses(student_data, chosen_branch, "removed_exams")

# -----------------------------
# Planning Future AP Exams
# -----------------------------
num_exams_to_take = get_valid_number_in_range(f"How many AP exams are you planning to take? (1-{40-removed_courses_count}): ", 1, 40-removed_courses_count, 0)

# -----------------------------
# Display Recommended AP Sequence
# -----------------------------
recommend_ap_sequence(chosen_branch, student_data, "Recommendation", num_exams_to_take)

# -----------------------------
# AP Score Predictions
# -----------------------------
if sat_taken == "yes":
    predict_ap_scores("Would you like me to predict your future AP scores based on your profile? (Yes/No): ", student_data, "Recommendation", math_score, 800)
else:
    want_prediction = predict_ap_scores("Would you like me to predict your future AP scores and estimated SAT based on your profile? (Yes/No): ", student_data, "Recommendation", gpa, 100)
    if want_prediction == "yes":
        if gpa >= 98:
            print("\nEstimated SAT: 1550-1600")
        elif gpa >= 95:
            print("\nEstimated SAT: 1450-1540")
        else:
            print("\nEstimated SAT: 1300-1440")

# -----------------------------
# Final Message
# -----------------------------
print(f"\nGood luck with your {chosen_branch.title()} Engineering journey, {student_name}!")
