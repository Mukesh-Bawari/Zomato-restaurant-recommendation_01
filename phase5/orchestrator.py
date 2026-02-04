from phase1.data_loader import load_zomato_dataset
from phase2.cli_input import get_user_preferences
from phase3.logic import filter_restaurants
from phase4.groq_service import get_ai_recommendations
import sys

def run_feature():
    print("\n--- Zomato AI Restaurant Recommendation MVP ---")
    
    # Phase 1: Load Dataset (Data Layer)
    df = load_zomato_dataset()
    if df is None or df.empty:
        print("Error: Could not load Zomato dataset. Please check your connection.")
        sys.exit(1)
    
    # Phase 2: User Input (Interface Layer)
    user_prefs = get_user_preferences()
    
    # Phase 3: Processing & Filtering (Logic Layer)
    print(f"\n[Phase 3] Filtering {len(df)} records for {user_prefs['location']} under ₹{user_prefs['budget']}...")
    filtered_df = filter_restaurants(df, user_prefs['location'], user_prefs['budget'])
    
    if filtered_df.empty:
        print("\n[Phase 5] No restaurants found matching your criteria.")
        print("Suggestion: Try a broader location or increase your budget.")
        return

    # Phase 4 & 5: AI Recommendation & Final Display (AI & Output Layer)
    print(f"\n[Phase 4] Found {len(filtered_df)} matches. Consulting Zomato AI...")
    recommendation = get_ai_recommendations(filtered_df, user_prefs)
    
    display_final_output(recommendation)

def display_final_output(recommendation):
    """
    Phase 5: Final output display to the user
    """
    print("\n" + "="*50)
    print("PHASE 5: FINAL RECOMMENDATIONS")
    print("="*50)
    print(recommendation)
    print("="*50)
    print("\nThank you for using Zomato AI!")

if __name__ == "__main__":
    run_feature()
