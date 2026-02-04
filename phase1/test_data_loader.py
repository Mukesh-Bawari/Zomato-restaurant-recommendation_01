import unittest
import pandas as pd
from phase1.data_loader import load_zomato_dataset

class TestDataLoader(unittest.TestCase):
    def test_load_dataset(self):
        """
        Test if the dataset loads as a pandas DataFrame and has the required columns.
        """
        df = load_zomato_dataset()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty, "Dataset should not be empty")
        
        # Check for essential columns
        expected_columns = ['name', 'location', 'approx_cost(for two people)']
        for col in expected_columns:
            self.assertIn(col, df.columns, f"Column {col} missing from dataset")
            
        # Check if cost is numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(df['approx_cost(for two people)']), "Cost column should be numeric")

if __name__ == "__main__":
    unittest.main()
