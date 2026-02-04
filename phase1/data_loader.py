import pandas as pd
from datasets import load_dataset
from tqdm import tqdm
import os

def load_zomato_dataset():
    """
    Loads the Zomato restaurant recommendation dataset from Hugging Face.
    Returns:
        pd.DataFrame: Cleaned dataframe.
    """
    print("Fetching dataset from Hugging Face...")
    try:
        # Load the dataset
        # For MVP/Development, we use a sample or full load depending on environment
        # streaming=True allows us to start processing without downloading 574MB
        dataset = load_dataset("ManikaSaini/zomato-restaurant-recommendation", split='train', streaming=True)
        
        # Taking a substantial sample for development
        print("Loading whole dataset from streaming source...")
        data_list = []
        # Total records is roughly 51,000 for this dataset
        pbar = tqdm(desc="Ingesting data", unit=" records")
        for entry in dataset:
            data_list.append(entry)
            pbar.update(1)
        pbar.close()
        
        df = pd.DataFrame(data_list)
        
        print(f"Dataset loaded. Shape: {df.shape}")
        
        # Initial cleaning: Focus on columns needed for MVP
        # Required columns: 'name', 'location', 'approx_cost(for two people)', 'rate', 'cuisines'
        # Note: We need to verify actual column names from the dataset.
        
        # Standardizing column names for easier access if they differ
        # Expected columns based on typical Zomato datasets:
        # 'name', 'location', 'approx_cost(for two people)', 'rate', 'cuisines'
        
        # Basic cleaning
        df = df.dropna(subset=['location', 'approx_cost(for two people)'])
        
        # Convert cost to numeric
        df['approx_cost(for two people)'] = df['approx_cost(for two people)'].astype(str).str.replace(',', '')
        df['approx_cost(for two people)'] = pd.to_numeric(df['approx_cost(for two people)'], errors='coerce')
        
        # Drop rows where cost conversion failed
        df = df.dropna(subset=['approx_cost(for two people)'])
        
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

if __name__ == "__main__":
    df = load_zomato_dataset()
    if df is not None:
        print(df.head())
        print(df.columns)
