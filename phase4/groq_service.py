import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_ai_recommendations(filtered_restaurants, user_prefs):
    """
    Uses Groq LLM to generate a personalized recommendation message.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Error: GROQ_API_KEY not found in .env file."
    
    client = Groq(api_key=api_key)
    
    # Prepare data for the prompt
    restaurant_list = filtered_restaurants[['name', 'rate', 'cuisines', 'approx_cost(for two people)']].head(5).to_dict(orient='records')
    
    prompt = f"""
    You are a Zomato AI assistant. A user is looking for restaurant recommendations.
    
    User Preferences:
    - Location: {user_prefs['location']}
    - Budget (per person): {user_prefs['budget']} Rupees
    
    Filtered Restaurant Options:
    {restaurant_list}
    
    Based on the above list, please provide a friendly recommendation. 
    Explain why you chose these restaurants based on their ratings and cuisines.
    Keep it concise and helpful.
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.1-8b-instant",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        return f"Error connecting to Groq: {e}"

if __name__ == "__main__":
    import pandas as pd
    # Mock data for testing
    mock_df = pd.DataFrame({
        'name': ['Jalsa', 'Spice Elephant'],
        'rate': ['4.1/5', '4.1/5'],
        'cuisines': ['North Indian', 'Chinese'],
        'approx_cost(for two people)': [800, 800]
    })
    mock_prefs = {'location': 'Banashankari', 'budget': 500}
    
    # This will fail without API key, but good for structure verification
    print(get_ai_recommendations(mock_df, mock_prefs))
