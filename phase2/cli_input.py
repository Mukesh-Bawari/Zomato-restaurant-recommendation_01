def get_user_preferences():
    """
    Prompts the user for their location and budget.
    Returns:
        dict: A dictionary containing 'location' and 'budget'.
    """
    print("\n--- Zomato AI Restaurant Recommendation ---")
    
    location = input("Enter your location (e.g., Banashankari): ").strip()
    
    while True:
        budget_str = input("Enter your budget for one person (in Rupees): ").strip()
        try:
            budget = float(budget_str)
            if budget <= 0:
                print("Budget must be a positive number.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for budget.")
            
    return {
        "location": location,
        "budget": budget
    }

if __name__ == "__main__":
    prefs = get_user_preferences()
    print(f"\nYour preferences: {prefs}")
