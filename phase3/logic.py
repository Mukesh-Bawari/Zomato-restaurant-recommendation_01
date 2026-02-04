def filter_restaurants(df, location, budget):
    """
    Filters the restaurant dataframe based on location and budget.
    Args:
        df (pd.DataFrame): The restaurant dataset.
        location (str): User's preferred location.
        budget (float): User's budget per person.
    Returns:
        pd.DataFrame: Filtered list of restaurants.
    """
    # Case-insensitive location match
    filtered_df = df[df['location'].str.contains(location, case=False, na=False)]
    
    # Filter by budget
    # approx_cost(for two people) / 2 should be <= budget
    filtered_df = filtered_df[filtered_df['approx_cost(for two people)'] / 2 <= budget]
    
    # Sort by rating (rate) if available
    # rate is usually like '4.1/5'
    if 'rate' in filtered_df.columns:
        filtered_df['rating_val'] = filtered_df['rate'].astype(str).str.extract(r'(\d+\.\d+)').astype(float)
        filtered_df = filtered_df.sort_values(by='rating_val', ascending=False)
    
    return filtered_df

if __name__ == "__main__":
    import pandas as pd
    # Test data
    test_data = pd.DataFrame({
        'name': ['A', 'B', 'C'],
        'location': ['Bangalore', 'Bangalore', 'Delhi'],
        'approx_cost(for two people)': [800, 1200, 500],
        'rate': ['4.1/5', '4.5/5', '3.9/5']
    })
    
    results = filter_restaurants(test_data, 'Bangalore', 500)
    print("Filtered Results (Bangalore, 500):")
    print(results)
